# models.py

from django.db import models

class GeneratedImage(models.Model):
    """
    Model representing a generated image based on a prompt.
    """
    prompt = models.CharField(max_length=255)
    # The prompt field is a CharField with a maximum length of 255 characters.
    # This field stores the text prompt based on which the image is generated.

    image = models.ImageField(upload_to='generated_images/')
    # The image field is an ImageField that stores the generated image file.
    # The uploaded image files will be stored in the 'generated_images/' directory.

    created_at = models.DateTimeField(auto_now_add=True)
    # The created_at field is a DateTimeField that stores the timestamp of when the object is created.
    # auto_now_add=True means the timestamp is set automatically when the object is created.

    def __str__(self):
        """
        Return a string representation of the GeneratedImage instance.
        """
        return f"{self.prompt} - {self.created_at}"
        # The __str__ method returns a string that includes the prompt and the creation timestamp.
        # This is useful for displaying readable representations of the object in the Django admin interface and other contexts.
