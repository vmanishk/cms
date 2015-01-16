from django.db import models
from django.contrib.auth.models import User, Group
from django_bootstrap_calendar.models import *
from django.db.models.signals import post_save
from time import time

def get_upload_file_name(instance, filename):
	return "uploaded_files/%s_%s" % (str(time()).replace('.','_'), filename)

# Create your models here.

# class Student(models.Model):
    # Student_name = models.CharField(max_length=30)
    # Student_id = models.CharField(max_length=8)
    # Student_username = models.CharField(max_length=20) 
    # Student_password = models.CharField(max_length=16)
    # Student_email = models.EmailField()
	# # linking
    # # myCourses_Student = models.ManyToManyField(Course)
    # # myVotingTopics_Student = models.ManyToManyField(VotingTopic)
    # # myAttendance_Student = models.ManyToManyField(Attendance)
    # # myDiscussionTopics_Student = models.ManyToManyField(DiscussionTopic)
    # # myCalender_Student = models.ManyToManyField(Calender)
    # #left blank for some bright idea
    # def __unicode__(self):
        # return self.Student_name    

# class Teacher(models.Model):
    # Teacher_name = models.CharField(max_length=30)
    # Teacher_id = models.CharField(max_length=20)
    # Teacher_username = models.CharField(max_length=20)
    # Teacher_password = models.CharField(max_length=16)
    # Teacher_email= models.EmailField()
	# # linking
    # Teacher = models.ManyToManyField(User)
    # # myVotingTopics_Teacher = models.ManyToManyField(VotingTopic)
	# # #myAttendance_Teacher = models.ManyToManyField(Attendance)
    # # myDiscussionTopics_Teacher = models.ManyToManyField(DiscussionTopic)
    # # myCalender_Teacher = models.ManyToManyField(Calender)
    # # yourStudyMaterial_Teacher = models.ManyToManyField(Material)
	# #left blank for some bright idea
    # def __unicode__(self):
        # return self.Teacher_name    
		
class Course(models.Model):
    Course_Name = models.CharField(max_length=30)
    Course_Number = models.CharField(max_length=6)
    Course_expected_classes = models.IntegerField(max_length=10, default=40)
    Elective = models.BooleanField(default = False)
	#linking
    Course_Prerequisites = models.ManyToManyField('self',null=True)
    #teachers = User.objects.filter(groups__name='Teachers')
    Course_Teachers = models.ManyToManyField(User)
    Course_Students = models.ManyToManyField(Group,null=True, blank = True)
    #Course_Students = models.ManyToManyField(Student)
    #Course_Attendance = models.ForeignKey(Attendance)
    #Course_Material = models.ManyToManyField(Material)
	#left blank for some bright idea
    def __unicode__(self):
        return self.Course_Name

class Material(models.Model):
	Material_Gist = models.CharField(max_length=100)
	Material_Link = models.URLField()
	Thumbnail = models.FileField(upload_to = get_upload_file_name, null=True)
	#linking
	Material_Course = models.ForeignKey(Course)
	def __unicode__(self):
		return self.Material_Gist

#class VotingTopic(models.Model):
#	Topic_Name = models.CharField(max_length=300)
#	Topic_Start_Date = models.DateField(max_length=11)
#	Topic_End_Date = models.DateField(max_length=11)
#	Topic_Count_Yes = models.CharField(max_length=20)
#	Topic_Count_No = models.CharField(max_length=20)
	#linking
#	Topic_Creator= models.ForeignKey(User)
#	def __unicode__(self):
#		return self.Topic_Name

class UserToCalender(models.Model):															#this will just include events which are public and same to all students and teachers
	#linking
	Event_Creator = models.ForeignKey(User)
	Event = models.ForeignKey(CalendarEvent)	 
		
class UserProfile(models.Model):
    # This field is required.
    user = models.OneToOneField(User)

    # Other fields here
    user_url = models.URLField(blank = True)
    uid = models.CharField(max_length = 20)
    if_first_login = models.BooleanField(default = False)
    Student_If_Fail = models.BooleanField(default=False)
    batch = models.ForeignKey(Group, null=True)
	# pass= True, fail = False
    def __unicode__(self):
        return self.user.username
    
User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])
	
# def create_user_profile(sender, instance, created, **kwargs):
    # if created:
        # UserProfile.objects.create(user=instance)

# post_save.connect(create_user_profile, sender=User)
		