from django.db import models


class Appuser(models.Model):
    email = models.EmailField()
    password = models.TextField()

    def __str__(self):
        return self.email


class Blog(models.Model):
    key = models.IntegerField()
    email = models.EmailField()
    title = models.TextField()
    content = models.TextField()
    from datetime import datetime
    date = models.DateField(default=datetime.now)


    def __str__(self):
        return self.email