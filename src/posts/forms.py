from django import forms
from tinymce import TinyMCE
from .models import Post, Comment
from tinymce.widgets import TinyMCE

class TinyMCEWidget(TinyMCE):
    def use_required_attribute(self, *args):
        return False


class PostForm(forms.ModelForm):
    content = forms.CharField(
        widget=TinyMCE(
            attrs={'required': False, 'cols': 20, 'rows': 10}
        )
    )

    class Meta:
        model = Post
        fields = ('title', 'overview', 'content', 'thumbnail', 
        'categories', 'featured', 'previous_post', 'next_post')


class CommentForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Type your comment',
        'id': 'usercomment',
        'rows': '4'
    }), label='')
    class Meta:
        model = Comment
        fields = ('content', )