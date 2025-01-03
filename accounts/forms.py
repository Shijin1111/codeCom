# from django import forms
# from .models import Note

# class NoteForm(forms.ModelForm):
#     class Meta:
#         model = Note
#         fields = ['heading', 'body']


from django import forms
from .models import Note, Subheading
from django.forms import inlineformset_factory

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title']

SubheadingFormSet = inlineformset_factory(Note, Subheading, fields=('heading', 'content'), extra=3,can_delete=False)

class PythonCodeForm(forms.Form):
    code = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 10, 'cols': 40, 'class': 'form-control', 'placeholder': 'Enter Python code...'})
    )


