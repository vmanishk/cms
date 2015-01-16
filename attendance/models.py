from django.db import models
from django.contrib.auth.models import User, Group
from cmsdata.models import *

# Create your models here.
class Attendance_main(models.Model):
	course=models.ForeignKey(Course)
	Todays_Date = models.DateField(max_length=11)
	def get_attendance_list(self):
		return self.attendance_set.all()
	def __unicode__(self):
		return self.course.Course_Name+"--"+unicode(self.Todays_Date)

	class Meta:
		ordering = ['Todays_Date']



class Attendance(models.Model):
	attendance=models.ForeignKey(Attendance_main)
	Status = models.BooleanField()
	Attendance_Students=models.ForeignKey(User)

	#left blank for some bright idea
	def __unicode__(self):
		return unicode(self.Attendance_Students.username)
		