from django.db import models


class Update(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    date = models.DateField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class images(models.Model):
    imagen = models.ImageField(upload_to='Pheflux/media')