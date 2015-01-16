from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render,render_to_response
from models import *
#from cms.forms import LoginForm
from django.contrib import auth
from django.core.context_processors import csrf
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
import re


#for attendence
@login_required
def attendence_view(request):
    course_list=[]
    for group in request.user.groups.all():
		if group.name=='Students':
			for course in Course.objects.filter(Course_Students = request.user.profile.batch):
				if course.Elective:
					for group in request.user.groups.all():
						if group.name==course.Course_Name+'_students':
							course_list.append(course)
				else:
					course_list.append(course)
		if group.name=='Teachers':
			for course in Course.objects.filter(Course_Teachers = request.user):
				course_list.append(course)
    user = request.user
    check_value = 0
    for group in user.groups.all():
        if group.name == 'Students':
            check_value = 1

    return render(request, 'attendance.html', {'username':request.user.username, 'course_list':course_list, 'branch':"cse", 'currentSemester':"     4th sem", 'check_value':check_value } )      
    
def sorter(ar):
    l = len(ar)
    for i in range(l):
        for j in range(i+1,l):
            if ar[i].profile.uid > ar[j].profile.uid:
                x = ar[i]
                ar[i] = ar[j]
                ar[j] = x 
				
				
@login_required				
def takenewattendance_view(request):

    #for showing the new attendance 
    if request.POST.get('attend_new', ''):
        c_nm = request.POST['cn']
        selected_course = Course.objects.get(Course_Name__contains=c_nm)
        attend_main=Attendance_main.objects.filter(course=selected_course)
        new_date_objects=[]
        
        if selected_course.Elective:
			group_list=Group.objects.filter(name=selected_course.Course_Name+'_students')
        else:
			group_list=selected_course.Course_Students.all()
        for group in group_list:
			for user in User.objects.filter(groups__name=group.name):
				new_date_objects.append(user)
        sorter(new_date_objects)
		
        return render(request, 'takenewattendance.html' , {'my_username':request.user.username,'new_date_objects': new_date_objects,'attend_main':attend_main ,'selected_course': selected_course} )


     # FOR STORING A NEW ATTENDANCE IN THE DATABASE    
    
    if request.POST.get('new_attend_update'):
        c_nm = request.POST['selected_newcourse']
        selected_course = Course.objects.get(Course_Name__contains=c_nm)
        attend_main=Attendance_main.objects.filter(course=selected_course)
        new_date_objects=[]
		
        if selected_course.Elective:
				group_list=Group.objects.filter(name=selected_course.Course_Name+'_students')
        else:
				group_list=selected_course.Course_Students.all()
        for group in group_list:
			for user in User.objects.filter(groups__name=group.name):
				new_date_objects.append(user)
        sorter(new_date_objects)		
		
        same_date=0
        new_object=Attendance_main()
        date_entered=request.POST.get('todays_date', '')
        check_format=str(request.POST.get('todays_date', ''))

        searchObj = re.search('([0-9]{4}\-[0-9]{2}\-[0-9]{2})', check_format , re.M|re.I)
        if searchObj:
            same_date=0
        else:
            same_date=3


        if not date_entered:
            same_date=2
        for item in Attendance_main.objects.all():
            if str(item.Todays_Date)==str(request.POST.get('todays_date', '')):
                same_date=1
        if same_date!=0:
            return render(request, 'takenewattendance.html' , {'my_username':request.user.username,'new_date_objects': new_date_objects,'attend_main':attend_main ,'selected_course': selected_course,'same_date':same_date} )
        else:
            new_object.Todays_Date=request.POST.get('todays_date', '')    
            new_object.course=selected_course
            new_object.save()
            i=1
            if selected_course.Elective:
				group_list=Group.objects.filter(name=selected_course.Course_Name+'_students')
            else:
				group_list=selected_course.Course_Students.all()
            for group in group_list:
				for user in User.objects.filter(groups__name=group.name):
					attendance_object=Attendance()
					attendance_object.attendance=new_object
					attendance_object.Status=int(request.POST.get("status"+str(i)))
					attendance_object.Attendance_Students=user
					attendance_object.save()
					i=i+1
            course_list=[]
            for group in request.user.groups.all():
                if group.name=='Students':
                    for course in Course.objects.filter(Course_Students = request.user.profile.batch):
                        if course.Elective:
                            for group in request.user.groups.all():
                                if group.name==course.Course_Name+'_students':
                                    course_list.append(course)
                        else:
                            course_list.append(course)
                if group.name=='Teachers':
                    for course in Course.objects.filter(Course_Teachers = request.user):
                        course_list.append(course)
            user = request.user
            check_value = 0
            for group in user.groups.all():
                if group.name == 'Students':
                    check_value = 1
            ADD_STATUS = 1                



		
            


            return render(request, 'attendance.html', {'username':request.user.username, 'course_list':course_list, 'branch':"cse", 'currentSemester':"     4th sem", 'check_value':check_value, 'ADD_STATUS':ADD_STATUS } )


        
        


        
    

@login_required
def takeattendance_view(request):

    #for showing the already stored attendance
    if request.POST.get('attend_stored', ''):
            c_nm = request.POST['cn']
            attend_main=Attendance_main.objects.get(id__exact=c_nm)
            date_objects=attend_main.get_attendance_list()
            total_students=0
            present_students=0
            absent_students=0
            total_per=100
            present_per=0
            absent_per=0


            for item in date_objects:
                total_students=total_students+1
                if item.Status==1:
                    present_students=present_students+1
                else:
                    absent_students=absent_students+1    
            if total_students:
                present_per = int((present_students*100))/total_students
                absent_per = int((absent_students*100))/total_students

            
            return render(request, 'takeattendance.html' , {'my_username':request.user.username,'date_objects': date_objects,'attend_main':attend_main, 'total_students':total_students, 'present_students':present_students, 'absent_students':absent_students , 'present_per':present_per, 'total_per':total_per, 'absent_per':absent_per } )
        
    
    if request.POST.get('new_attendance' , ''):        
        return HttpResponse(request.method)
    else:
            return HttpResponse("else")
    
@login_required
def subjectselected_view(request):

    # FOR PRINTING THE DETAILS OF ATTENDANCE FOR A STUDENT
    if request.POST.get('attend_student'):
        student_course_nm = request.POST['student_cn']
        selected_course = Course.objects.get(Course_Name__contains=student_course_nm)
        class_in_sem=selected_course.Course_expected_classes
        total_classes=0
        present_classes=0
        absent_classes=0
        attendance_stats = []
        selected_day=[]
        date_object = Attendance()
        date_object.Status = 0
        attendance_stats=(Attendance_main.objects.filter( course = selected_course))
        for item in attendance_stats:
            total_classes = total_classes + 1
            selected_day = Attendance.objects.filter(attendance = item )

            for day in selected_day:
                if day.Attendance_Students == request.user:
                    date_object = day
                    

            if date_object.Status == 1:
                present_classes = present_classes + 1
            else:
                absent_classes = absent_classes + 1
        if total_classes != 0:        
            percentage_attendance = int((present_classes*100))/total_classes
        else:
            percentage_attendance = 0 
        absent_attendance = 100 - percentage_attendance       
        projected_attendance = int((percentage_attendance * class_in_sem))/100
        if (class_in_sem - total_classes + present_classes)>0:
            max_attendance = ((class_in_sem - total_classes + present_classes)*100)/class_in_sem
        else:
            max_attendance = percentage_attendance    
        
        return render(request, 'subjectselected.html' , {'username':request.user.username ,'total_classes':total_classes, 'present_classes':present_classes, 'absent_classes':absent_classes, 'percentage_attendance':percentage_attendance, 'max_attendance':max_attendance , 'projected_attendance':projected_attendance ,'subject_selected_name':selected_course, 'absent_attendance':absent_attendance} )    


@login_required
def attendancelist_view(request):

    # FOR PRINTING THE TOTAL PERCENTAGE OF ATTENDANCES FOR A COURSE FOR A TEACHER
    if request.POST.get('attend_list'):
        course_nm = request.POST['coursename_list']
        selected_course = Course.objects.get(Course_Name__contains=course_nm)

        student_class_list=[]
        percentage_list=[]
        
        if selected_course.Elective:
			group_list=Group.objects.filter(name=selected_course.Course_Name+'_students')
        else:
			group_list=selected_course.Course_Students.all()
        for group in group_list:
			for user in User.objects.filter(groups__name=group.name):
				student_class_list.append(user)
        sorter(student_class_list)                               



        for student in student_class_list:                                                     #FOR EACH STUDENT
            total_classes=0
            present_classes=0
            absent_classes=0
            attendance_stats = []
            selected_day=[]
            date_object = Attendance()
            date_object.Status = 0
            attendance_stats=(Attendance_main.objects.filter(course = selected_course))    #FOR ALL THE ATTENDANCES OF THAT COURSE
            for item in attendance_stats:
                total_classes = total_classes + 1
                selected_day = Attendance.objects.filter(attendance = item)                #FOR ONE DAY ATTENDANCE

                for day in selected_day:                                            
                    if day.Attendance_Students == student:                                  #FOR SELECTING THAT PARTICULAR STUDENT ATTENDANCE
                        date_object = day
                    

                if date_object.Status == 1:
                    present_classes = present_classes + 1
                else:
                    absent_classes = absent_classes + 1

            if total_classes!=0:
				percentage_attendance = float((present_classes*100))/total_classes
            else:
				percentage_attendance = 0
            percentage_list.append(percentage_attendance)    
        return render(request, 'attendancelist.html' , {'student_class_list':student_class_list, 'percentage_list':percentage_list ,'my_username':request.user.username} )    
    

    

@login_required
def attendanceteacher_view(request):



    #for editing the stored attendance
    if  request.POST.get('attend_update'):
        main_id=request.POST.get('idd')
        attend_main=(Attendance_main.objects.get(id=int(main_id)))
        c_num=attend_main.course.Course_Name

        attend_list=Attendance.objects.filter(attendance = attend_main)
        i=1
        for attend in attend_list:
            attend.Status = int(request.POST.get("status"+str(i)))
            attend.save()
            i=i+1
        return HttpResponseRedirect("/attendance/")   
        
    #for displaying the list of dates on which attendance has been taken
        
    if request.POST.get('attend'):
        c_nm = request.POST['cn']
        selected_course = Course.objects.get(Course_Name__contains=c_nm)
        date_list = []
        date_list=(Attendance_main.objects.filter(course=selected_course))
        return render(request, 'attendanceteacher.html' , {'my_username':request.user.username, 'date_list':date_list, 'my_currentSemester':" 4th sem ", 'selected_course':selected_course} )

    else:
        c_nm = request.POST['coursepassed']
        selected_course = Course.objects.get(Course_Name__contains=c_nm)
        date_list = []
        date_list=(Attendance_main.objects.filter(course=selected_course))
        return render(request, 'attendanceteacher.html' , {'my_username':request.user.username, 'date_list':date_list, 'my_currentSemester':" 4th sem ", 'selected_course':selected_course} )


        
@login_required
def succesful_view(request):
    return render(request, 'index.html')
    