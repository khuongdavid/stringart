from django.db import models
from user.models import User 
# Create your models here.
class Categories(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True)
    def __str__(self):
        return self.name
    
class Art(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    image1 = models.FileField(max_length=255, null= True)
    image2 = models.FileField(max_length=255, null=True, blank=True)
    categories = models.ForeignKey(Categories, on_delete=models.CASCADE, default='')
    artists = models.ForeignKey( User, on_delete=models.CASCADE)
    is_published = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title}   -   {self.categories}"
