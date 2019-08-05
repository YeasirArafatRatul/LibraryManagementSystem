from django.db import models

# Create your models here.


class SlideShow(models.Model):
    image1 = models.ImageField(
        upload_to='slideImages')
    image2 = models.ImageField(
        upload_to='slideImages', blank=True, null=True)
    image3 = models.ImageField(
        upload_to='slideImages', blank=True, null=True)
    title = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=100)

    def __str__(self):
        return self.title
