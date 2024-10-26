from django.db import models

class Note(models.Model):
    heading = models.CharField(max_length=200)
    body = models.TextField()

    def __str__(self):
        return self.heading
