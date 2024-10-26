# from django.db import models

# class Note(models.Model):
#     heading = models.CharField(max_length=200)
#     body = models.TextField()

#     def __str__(self):
#         return self.heading


from django.db import models

class Note(models.Model):
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Subheading(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name='subheadings')
    heading = models.CharField(max_length=200)
    content = models.TextField()

    def __str__(self):
        return f"{self.note.title} - {self.heading}"
