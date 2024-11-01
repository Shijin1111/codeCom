from django.contrib import admin
from accounts.models import Note,Subheading,CodeExecution,Problem
# Register your models here.
admin.site.register(Note)
admin.site.register(Subheading)


admin.site.register(CodeExecution)
admin.site.register(Problem)