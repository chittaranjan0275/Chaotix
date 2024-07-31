# tasks.py

import base64
import os

from celery import shared_task
import requests
from django.core.files.base import ContentFile
from dotenv import load_dotenv

from .models import GeneratedImage

# Load environment variables from the .env file
load_dotenv()


@shared_task
def generate_image(prompt):
    """
    Generate an image based on the given prompt using the Stability AI API.

    Args:
        prompt (str): The text prompt to generate the image from.

    Returns:
        int: The ID of the generated image record in the database.

    Raises:
        Exception: If the image generation request fails.
    """
    api_url = 'https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image'
    api_key = os.getenv('STABILITY_AI_API_KEY')

    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    # The headers include the API key for authorization and specify the content type.

    payload = {
        "text_prompts": [{"text": prompt}],
        "cfg_scale": 7,
        "height": 1024,
        "width": 1024,
        "samples": 1,
        "steps": 30,
    }
    # The payload contains the parameters for the image generation request.

    response = requests.post(api_url, headers=headers, json=payload)
    # Send a POST request to the API with the headers and payload.

    if response.status_code == 200:
        result = response.json()
        image_data = result['artifacts'][0]['base64']
        # If the request is successful, decode the JSON response and extract the base64 image data.

        generated_image = GeneratedImage(prompt=prompt)
        # Create a new GeneratedImage instance with the given prompt.

        image_name = f"{prompt.replace(' ', '_')}.png"
        # Generate a name for the image file by replacing spaces with underscores in the prompt.

        image_content = ContentFile(base64.b64decode(image_data), name=image_name)
        # Decode the base64 image data and create a ContentFile object with the decoded data.

        generated_image.image.save(image_name, image_content, save=True)
        # Save the image file to the GeneratedImage instance and save the instance to the database.

        return generated_image.id
        # Return the ID of the generated image record in the database.
    else:
        raise Exception(f'Failed to generate image: {response.text}')
        # If the request fails, raise an exception with the error message from the response.
