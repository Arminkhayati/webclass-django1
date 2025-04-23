from django import forms

from .models import Comment


class EmailPostForm(forms.Form):

    # name : length 25
    # email : from email address
    # to : to email address
    # comments : any message that user can send with the post. It is a Textarea widget and required=False.
    pass


class CommentForm(forms.ModelForm):
    # Define a form using "Comment Model" and "Meta" Class
    # for fields ['name', 'email', 'body']
    class Meta:
        pass
