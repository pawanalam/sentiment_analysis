from django.contrib import admin
from .models import InputData  # Import the model

@admin.register(InputData)
class InputDataAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "github", "linkedin", "contact", "resume_text")  # Added resume_text
    search_fields = ("name", "email", "github", "linkedin", "resume_text")  # Enable search for resume text
    list_filter = ("linkedin", "github")  # Add filter options
