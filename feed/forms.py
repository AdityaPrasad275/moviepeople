# feed/forms.py
from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["content"]  # Only allow user to set the content
        widgets = {
            "content": forms.Textarea(
                attrs={"rows": 3, "placeholder": "What's on your mind?"}
            ),
        }

from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(
                attrs={"rows": 2, "placeholder": "Add a comment..."}
            ),
        }
        labels = {"content": ""}  # Hide the label for content
