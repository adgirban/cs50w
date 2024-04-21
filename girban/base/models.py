from django.db import models

# Create your models here.
class Tag (models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Work (models.Model):
    headline = models.CharField(max_length=200)
    sub_headline = models.CharField(max_length=200)
    thumbnail = models.ImageField(null=True, blank=True, upload_to='static/base/images', default="static/base/images/default.jpg")
    created = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.headline