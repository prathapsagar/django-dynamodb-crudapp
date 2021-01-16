from django.db import models

# Create your models here.


class Blog(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    objects = None

    def __str__(self):
        return self.title

    # objects = models.Blog()
