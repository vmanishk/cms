from django.db import models
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from time import time
from django.conf import settings
from cms import settings

def get_upload_file_name(instance, filename):
    return settings.UPLOAD_FILE_PATTERN % (str(time()).replace('.','_'), filename)
# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=1000)
    body = models.TextField()
    pub_date = models.DateTimeField('date published',auto_now_add=True,blank=True)
    article_creator = models.ForeignKey(User)
    thumbnail = models.FileField(upload_to=get_upload_file_name,default=None,blank=True,null=True)
    class Meta:
        ordering=['-pub_date']
    
    def __unicode__(self):
        return self.title
    def sort(self):
        return self.num_upvotes()+2*self.num_comments()
    def num_upvotes(self):
        return self.vote_set.count()
    def num_comments(self):
    	return self.comment_set.count()

class vote(models.Model):
    article = models.ForeignKey(Article)
    user = models.ForeignKey(User)
    upvoted = models.BooleanField(default=True)

class Comment(models.Model):
    body = models.TextField()
    pub_date = models.DateTimeField('date published',auto_now_add=True,blank=True)
    article = models.ForeignKey(Article)
    comment_creator = models.ForeignKey(User)
    class Meta:
        ordering=['-pub_date']


class Poll(models.Model):
    question = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published',auto_now_add=True,blank=True)
    poll_creator = models.ForeignKey(User)
    class Meta:
        ordering=['-pub_date']

    def __unicode__(self):
        return self.question
    def most(self):
        return self.num_yes()+self.num_no()+self.num_cantsay()
    def num_yes(self):
        return self.yes_set.all().count()
    def num_no(self):
        return self.no_set.all().count()
    def num_cantsay(self):
        return self.cantsay_set.all().count()

class Yes(models.Model):
    poll = models.ForeignKey(Poll)
    user = models.ForeignKey(User)
    yes = models.BooleanField(default=True)
    class Meta:
        ordering=['-yes']

class No(models.Model):
    poll = models.ForeignKey(Poll)
    user = models.ForeignKey(User)
    no = models.BooleanField(default=True)
    class Meta:
        ordering=['-no']

class Cantsay(models.Model):
    poll = models.ForeignKey(Poll)
    user = models.ForeignKey(User)
    cantsay = models.BooleanField(default=True)
    class Meta:
        ordering=['-cantsay']




