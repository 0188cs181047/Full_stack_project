from django import forms
from .models import Post,CommentPost
from django.core.validators import FileExtensionValidator

class PostForm(forms.ModelForm):
    posti = forms.ImageField(required=True, validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif'])])
    video_file = forms.FileField(required=True)

    class Meta:
        model = Post
        fields = ("title", "video_file", "teacher", "posti", "description")
        labels = {
            'title': 'Title',
            'teacher': 'Teacher',
            'description': 'Description',
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = CommentPost
        fields = ("content",)



