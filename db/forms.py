from django import forms
from db.models import *

class ArticleForm(forms.Form):    # for creating a topic in discussion forum
	title=forms.CharField()
	subject=forms.CharField(widget=forms.Textarea())
	thumbnail=forms.ImageField(required=False)

class CommentForm(forms.Form):     # for adding a comment in a topic in discussion forum
	body=forms.CharField(widget=forms.Textarea())

class PollForm(forms.Form):      # for creating a poll 
	question=forms.CharField()
	