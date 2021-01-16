from django.forms import ModelForm
from blog.models import Blog


# Create the form class.
class BlogForm(ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'content']
