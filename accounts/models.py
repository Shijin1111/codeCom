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



class CodeExecution(models.Model):
    code = models.TextField()
    input_data = models.TextField(blank=True)
    output = models.TextField()
    execution_time = models.DateTimeField(auto_now_add=True)
    



class Problem(models.Model):
    title = models.CharField(max_length=200)  
    description = models.TextField()           
    img = models.ImageField(upload_to='problems/', blank=True, null=True)  
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True)   