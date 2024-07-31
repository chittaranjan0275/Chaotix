# forms.py

from django import forms

class PromptForm(forms.Form):
    """
    A form for submitting prompts.
    """
    prompt = forms.CharField(max_length=255, required=True, help_text="Enter your prompt here.")
    # The prompt field is a CharField with a maximum length of 255 characters.
    # It is a required field, meaning the form cannot be submitted without it.
    # The help_text provides additional information to the user.
