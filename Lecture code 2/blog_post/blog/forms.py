from django import forms

from blog.models import BlogPost


class BlogPostForm(forms.Form):
    title = forms.CharField(
        label="Title",
        max_length=100,
    )
    text = forms.CharField(
        label="Text",
        help_text="Enter a valid email address.",
        widget = forms.TextInput(attrs={'class': 'form-control'})
    )
    created_at = forms.DateTimeField(
        label='Created at',
        widget=forms.DateTimeInput(
            attrs={
                'type': 'datetime-local',
                'class': 'form-control'
            }
        )
    )
    is_active = forms.BooleanField(label="Is active")


class CreateBlogPostModelForm(forms.ModelForm):
    cover = forms.ImageField(label="Cover", required=False)

    class Meta:
        model = BlogPost
        fields = ['title', 'text', 'document', 'is_active', 'category', 'authors', 'cover']


class UpdateBlogPostModelForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'text', 'document', 'is_active', 'category']
