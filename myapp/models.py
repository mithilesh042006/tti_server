# models.py

from django.db import models
import uuid

class GeneratedImage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    prompt = models.TextField()
    image = models.ImageField(upload_to='')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image generated for: {self.prompt[:50]}"
    



