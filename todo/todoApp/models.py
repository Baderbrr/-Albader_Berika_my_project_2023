from django.db import models
from django.contrib.auth.models import AbstractUser

class Note(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE) 
    title = models.CharField(max_length=100)
    content = models.TextField(max_length=1000)
    created_date = models.DateTimeField(auto_now_add=True) 
    due_date = models.DateTimeField()
    expired = models.BooleanField(default=False)

    def __str__(self): # returns title of note for representing Note object in string data format
        return self.title
    
class User(AbstractUser): # inherit AbstractUser that contains all the authettication methods  
    my_notes = models.ForeignKey(Note, on_delete=models.CASCADE, null=True, blank=True, default=None, related_name='notes') # expend the User model with Foreig Key to Note 
