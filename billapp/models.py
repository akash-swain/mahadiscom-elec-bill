from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class ConDetail(models.Model):
    consumerno = models.CharField(max_length = 50)
    consumer = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return (self.consumerno)


    def get_absolute_url(self):
        return reverse("detail")
