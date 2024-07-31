# views.py

from django.shortcuts import render, redirect, get_object_or_404
from celery.result import AsyncResult
from celery import group
from .tasks import generate_image
from .models import GeneratedImage


def generate_images(request):
    """
    Handle the form submission to generate a single image from a prompt.

    If the request method is POST, extract the prompt from the form,
    create a Celery task to generate the image, and redirect to the
    image output page. If the prompt is missing, display an error message.

    If the request method is GET, render the image generation form.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The response object.
    """
    if request.method == 'POST':
        prompt = request.POST.get('prompt')
        if prompt:
            task = generate_image.delay(prompt)
            return redirect('image_output', task_id=task.id)
        else:
            return render(request, 'generate_images.html', {'error': 'Please provide a prompt.'})
    else:
        return render(request, 'generate_images.html')


def generate_images_in_parallel(request):
    """
    Handle the form submission to generate multiple images in parallel from a list of prompts.

    If the request method is POST, extract prompts from the form, create a group of
    Celery tasks to generate the images, and redirect to the image output page with task IDs.
    If the prompts are missing, display an error message.

    If the request method is GET, render the image generation form.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The response object.
    """
    if request.method == 'POST':
        prompts = request.POST.get('prompts').strip().split('\n')
        prompts = [prompt.strip() for prompt in prompts if prompt.strip()]

        if prompts:
            tasks = [generate_image.s(prompt) for prompt in prompts]
            result = group(tasks).apply_async()

            task_ids = [task.id for task in result.results]
            task_ids_str = ','.join(task_ids)

            return redirect('image_output', task_ids=task_ids_str)
        else:
            return render(request, 'generate_images.html', {'error': 'Please provide prompts.'})
    else:
        return render(request, 'generate_images.html')


def image_output(request, task_ids):
    """
    Display the status and results of image generation tasks.

    Extract task IDs from the URL, check the status of each task, and
    collect the generated images or error messages. Render the results
    in the image output page.

    Args:
        request (HttpRequest): The HTTP request object.
        task_ids (str): A comma-separated string of task IDs.

    Returns:
        HttpResponse: The response object.
    """
    task_ids = task_ids.split(',')
    tasks = [AsyncResult(task_id) for task_id in task_ids]
    context = {'tasks': []}

    for task in tasks:
        if task.ready():
            if task.successful():
                image_id = task.result
                try:
                    generated_image = GeneratedImage.objects.get(id=image_id)
                    context['tasks'].append({'status': 'success', 'image': generated_image})
                except GeneratedImage.DoesNotExist:
                    context['tasks'].append({'status': 'error', 'message': 'Image not found in database.'})
            else:
                context['tasks'].append(
                    {'status': 'pending', 'message': 'Image is still being generated. Please wait.'})
        else:
            context['tasks'].append({'status': 'pending', 'message': 'Image is still being generated. Please wait.'})

    return render(request, 'image_output.html', context)


def image_list(request):
    """
    Display a list of all generated images, ordered by creation date.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The response object.
    """
    images = GeneratedImage.objects.all().order_by('-created_at')
    return render(request, 'image_list.html', {'images': images})


def image_detail(request, image_id):
    """
    Display the details of a specific generated image.

    Args:
        request (HttpRequest): The HTTP request object.
        image_id (int): The ID of the generated image.

    Returns:
        HttpResponse: The response object.
    """
    image = get_object_or_404(GeneratedImage, id=image_id)
    return render(request, 'image_detail.html', {'image': image})
