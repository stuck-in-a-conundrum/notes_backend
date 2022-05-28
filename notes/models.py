from django.db import models
from django.contrib.auth.models import User
class Note(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255, blank=True, default="")
    desc = models.TextField(blank=True, default="")
    color = models.CharField(max_length=255)
    owner = models.ForeignKey(User, related_name='notes', on_delete=models.CASCADE)

    class Meta:
        ordering = ['created']

    def __str__(self):
        return self.title
    
# Create your models here.
