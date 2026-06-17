from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    # 🌟 Cambiados los ":" por "="
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_completed = models.DateTimeField(null=True, blank=True) 
    completed = models.BooleanField(default=False)
    important = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title+" - "+str(self.created_by)+" - "+str(self.date_created)[:10] # 🌟 Cambiado el_created)
    