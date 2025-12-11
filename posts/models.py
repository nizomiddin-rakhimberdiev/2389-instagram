from django.db import models
from users.models import CustomUser
# Create your models here.

class Post(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    video = models.FileField(upload_to='videos/', blank=True, null=True)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    title = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
Vazifa = """
aiogramda state nima?
u qanday amalga oshiriladi?
FSMContext nima? nima vazifa bajaradi?
state qanday to'xtatiladi?
"""