from django.db import models

class InputData(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    github = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    contact = models.CharField(max_length=15)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    resume_text = models.TextField(blank=True, null=True)  # ✅ New field to store extracted resume text

    def __str__(self):
        return self.name
