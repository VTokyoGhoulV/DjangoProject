from django import forms

from blog.models import Blog


class PostForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = [
            "title",
            "content",
            "image",
            "published",
        ]

        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "content": forms.Textarea(
                attrs={"class": "form-control", "rows": 5}
            ),
            "image": forms.FileInput(attrs={"class": "form-control"}),
            "published": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
