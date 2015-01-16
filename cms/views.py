from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render,render_to_response
from django.utils.encoding import smart_str
from cmsdata.models import *
from django_bootstrap_calendar.models import *
#from cms.forms import LoginForm
from django.contrib import auth
from django.core.context_processors import csrf
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail


# user authentication views			

username=''

def loginpage_view(request):							# initial login page 			
    return render(request,'loginpage.html')

def documentation_view(request):							# documentation page 			
    return render(request,'documentation.html')
    
def onlinemanual_view(request):							# renders online manual
    return render(request,'onlinemanual.html')

def login_view(request):								# renders login details page
    c={}
    c.update(csrf(request))
    return render_to_response('logindetailspage.html', c)

def auth_view(request):
    context=RequestContext(request);
    if request.method == 'POST':
	username = request.POST.get('username','')
        password = request.POST.get('password','')
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
	    # Correct password, and the user is marked "active"
            auth.login(request, user)
            # Redirect to a success page
            return HttpResponseRedirect("/home/")
        else:
            # Show an error page
            return HttpResponseRedirect("/accounts/invalid/")
    else:
        return render(request,'logindetailspage.html', context)

@login_required	
def loggedin_view(request):
	username=request.user.username
	if request.user.profile.if_first_login == False:
		user_pro=UserProfile.objects.get(user=request.user)
		user_pro.if_first_login = True
		user_pro.save()
		if user_pro.Student_If_Fail == True:
			user_pro.batch = Group.objects.get(name="Students")
			user_pro.save()
			return render(request, 'invalid.html')
		else:
			return HttpResponseRedirect("/courseselection/")
	return render(request, 'index.html', {'username':request.user.username})

@login_required	
def courseselection_view(request):
	for group in request.user.groups.all():
		if group.name == 'Students':
			course_list = Course.objects.filter(Course_Students = request.user.profile.batch)
			return render(request, 'courseselection.html', {'course_list':course_list})
	return render(request, 'index.html', {'username':request.user.username})
	
@login_required	
def course_selected_submit_view(request):
	exists=0
	if request.method == 'POST':
		course_list = Course.objects.filter(Course_Students = request.user.profile.batch)
		for course in course_list:
			if request.POST.get(course.Course_Number,''):
				cn=request.POST.get(course.Course_Number,'')
				if cn=='1':
					
					for group in course.Course_Students.all():
						if group.name == (course.Course_Name+'_students'):
							exists=1
					if exists == 1:
						g=Group.objects.get(name=course.Course_Name+'_students')
						request.user.groups.add(g)
					else:
						g=Group(name=course.Course_Name+'_students')	
						g.save()
						request.user.groups.add(g)
					course.Course_Students.add(g)
					course.save()

				else:
					return render(request, 'courseselection.html', {'course_list':course_list, 'error':"Please select atleast one elective"} )
		return render(request, 'index.html', {'username':request.user.username, 'courses_added':True})
	# else:
		# return render(request, 'index.html', {'username':request.user.username})
	
def invalid_login_view(request):
	context=RequestContext(request);
        return render_to_response('invalidlogin.html', context)
	
def forgotpassword_view(request):
	return render(request, 'forgotpassword.html')
		
def logout_view(request):
    auth.logout(request)
    # Redirect to a success page.
    return HttpResponseRedirect("/loggedout/")
	
def loggedout_view(request):
    return render_to_response('loginpage.html')
	

# help views

def contact_us2_view(request):
    return render(request, 'help2.html')
	
@login_required
def contact_us1_view(request):
    return render(request, 'help.html', {'username':request.user.username})


# sendmail views

def sendmail_view(request):
	if request.method=='POST':
		email_id=request.POST.get('email_id','')
		send_mail(
                'PASSWORD CHANGE',
                'Your password is '+str(123)+
				'@127.0.0.1:1025',
                [email_id],
				fail_silently=False
            )
		return render(request, 'forgotpasswordsubmission.html')
	else:
		return render(request, 'forgotpassword.html')
	
	
# change password views

@login_required
def changepasswordpage_view(request):
    c={}
    c.update(csrf(request))
    return render_to_response('changepassword.html', c )
	
@login_required
def changepassword_view(request):
    context=RequestContext(request);
    if request.method == 'POST':
        old_password = request.POST.get('old_password','')
        new_password = request.POST.get('new_password','')
        new_password_retyped = request.POST.get('new_password_retyped','')
        if request.user.check_password(old_password):
	    	# Correct password
	    	if new_password:
	    		if (new_password==new_password_retyped):
					request.user.set_password(new_password)
					request.user.save()
					# Redirect to a success page
					return HttpResponseRedirect("/changepassword/successfull/")
	    		else:
					# Show an error page (new password not retyped correctly)
					return render_to_response('changepassword.html', {'username':request.user.username, 'error':'New password not retyped correctly', }, context )
    		else:
    			return render_to_response('changepassword.html', {'username':request.user.username, 'error':'Please enter some new password', }, context )
    	else:
            # Show an error page (incorrect password)
			return render_to_response('changepassword.html', {'username':request.user.username, 'error':'Incorrect password', }, context )
    else:
        return render_to_response('changepassword.html', {'username':request.user.username}, context)
		
@login_required
def changepassword_successfull_view(request):
	return render(request, 'changepasswordsubmission.html', {'username':request.user.username} )


# functional views

@login_required
def courses_view(request):
	loggedin_user=request.user
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
	# for course in course_list:
		# course_teachers_list=[]
		# for course_user in course.Course_Users.all():															
			# if course_user.groups.filter(name='Teachers').count():
				# course_teachers_list.append(course_user)
	return render(request, 'courses.html', {'username':loggedin_user.username, 'branch':'CSE', 'current_semester':'IV', 'course_list':course_list } )
	
@login_required
def coursematerial_view(request):
	if request.method == 'POST':
		selected_course_name=request.POST.get('selected_course','')
		selected_course=Course.objects.get(Course_Name__contains=selected_course_name)
		materials_list=Material.objects.filter(Material_Course=selected_course)
		return render(request, 'coursematerial.html', {'selected_course':selected_course, 'materials_list':materials_list})
	else:
		return render(request, 'coursematerial.html', RequestContext(request))
	
@login_required
def material_details_view(request):
	if request.method == 'POST':
		selected_course_name=request.POST.get('selected_course','')
		selected_course=Course.objects.get(Course_Name__contains=selected_course_name)
		return render(request, 'material_details.html', {'selected_course':selected_course })
	else:
		return render(request, 'material_details.html', RequestContext(request))
	
@login_required
def upload_material_view(request):
	if request.method == 'POST':
		no_url=False
		no_title=False
		selected_course_name=request.POST.get('selected_course','')
		title=request.POST.get('title','')
		if not title:
			no_title=True
		url=request.POST.get('url','')
		if not url:
			no_url=True
		thumbnail=request.FILES.get('thumbnail','')
		selected_course=Course.objects.get(Course_Name__contains=selected_course_name)
		if no_url or no_title:
			return render(request, 'material_details.html', {'selected_course':selected_course, 'no_title':no_title, 'no_url':no_url })
		else:
			material=Material(Material_Gist=title, Material_Link=url, Thumbnail=thumbnail, Material_Course=selected_course)
			material.save()
			return render(request, 'coursematerial.html', {'selected_course':selected_course, 'material_added':True})
	else:
		return render(request, 'coursematerial.html', RequestContext(request))

#def download_view(request):
    # file_name = request.GET.get('per_page')
    # path_to_file = "/media/{0}".format(file_name)
    # response = HttpResponse(mimetype='application/force-download')
    # response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(file_name)
    # response['X-Sendfile'] = smart_str(path_to_file)
    # return response
	return HttpResponseRedirect("media/uploaded_files/")

		
@login_required
def add_event_view(request):
	if request.method == 'POST':
		no_url=False
		no_title=False
		no_event_type=False
		no_start=False
		no_end=False
		no_single_word=False
		title=request.POST.get('title','')
		if not title:
			no_title=True
		if ' ' in title:
			no_single_word=True
		url=request.POST.get('url','')
		if not url:
			no_url=True
		event_type=request.POST.get('type','')
		if not event_type:
			no_event_type=True
		start=request.POST.get('start','')
		if not start:
			no_start=True
		end=request.POST.get('end','')
		if not end:
			no_end=True
		if no_url or no_title or no_event_type or no_start or no_end or no_single_word:
			return render(request, 'add_event.html', {'no_title':no_title, 'no_url':no_url, 'no_event_type':no_event_type, 'no_start':no_start, 'no_end':no_end,  'no_single_word':no_single_word })
		else:
			e = CalendarEvent(title=title, url=url, css_class=event_type, start=start, end=end)
			e.save()
			u = UserToCalender(Event_Creator=request.user, Event=e)
			u.save()
			return render(request, 'add_event.html', {'event_added':True} )
	else:
		return render(request, 'add_event.html', RequestContext(request))
		
@login_required
def edit_event_view(request):
	events = UserToCalender.objects.filter(Event_Creator=request.user)
	events_list=[]
	for event in events:
		events_list.append(event.Event)
	return render(request, 'edit_event.html', {'events_list':events_list} )
	
@login_required
def edit_event_details_view(request):
	if request.method=='POST':
		selected_event_id=request.POST.get('selected_event','')
		selected_event=CalendarEvent.objects.get(id=selected_event_id)
		return render(request, 'edit_event_details.html', {'selected_event':selected_event} )
	else:
		return render(request, 'edit_event_details.html', RequestContext(request))
		
@login_required
def edit_event_update_view(request):
	if request.method=='POST':
		no_url=False
		no_title=False
		no_event_type=False
		no_start=False
		no_end=False
		no_single_word=False
		title=request.POST.get('title','')
		if not title:
			no_title=True
		if ' ' in title:
			no_single_word=True
		url=request.POST.get('url','')
		if not url:
			no_url=True
		event_type=request.POST.get('type','')
		if not event_type:
			no_event_type=True
		start=request.POST.get('start','')
		if not start:
			no_start=True
		end=request.POST.get('end','')
		if not end:
			no_end=True
		selected_event_id=request.POST.get('selected_event','')
		selected_event=CalendarEvent.objects.get(id=selected_event_id)
		if no_url or no_title or no_event_type or no_start or no_end or no_single_word:
			return render(request, 'edit_event_details.html', {'selected_event':selected_event, 'no_title':no_title, 'no_url':no_url, 'no_event_type':no_event_type, 'no_start':no_start, 'no_end':no_end, 'no_single_word':no_single_word } )
		else:
			u = UserToCalender.objects.get(Event=selected_event)
			selected_event.title=title
			selected_event.url=url
			selected_event.css_class=event_type
			selected_event.start=start
			selected_event.end=end
			selected_event.save()
			u.Event=selected_event
			u.save()
			return render(request, 'edit_event_details.html', {'event_edited':True} )
	else:
		return render(request, 'edit_event_details.html', RequestContext(request))

@login_required
def remove_event_view(request):
	events = UserToCalender.objects.filter(Event_Creator=request.user)
	events_list=[]
	for event in events:
		events_list.append(event.Event)
	return render(request, 'remove_event.html', {'events_list':events_list} )

@login_required
def delete_event_view(request):
	if request.method=='POST':
		
		selected_event_id=request.POST.get('selected_event','')
		if selected_event_id:
			selected_event=CalendarEvent.objects.get(id=selected_event_id)
			u = UserToCalender.objects.get(Event = selected_event)
			selected_event.delete()
			u.delete()
		events = UserToCalender.objects.filter(Event_Creator=request.user)
		events_list=[]
		for event in events:
			events_list.append(event.Event)
		return render(request, 'remove_event.html', {'events_list':events_list, 'event_deleted':True} )
	else:
		return render(request, 'remove_event.html', {'events_list':events_list} )

def get_events_view(request):
	events_list=UserToCalender.objects.filter(Event_Creator=request.user)
	return render(request, 'eventlist.html', {'username':request.user.username, 'events_list':events_list} )
	
@login_required
def discussion_view(request):
	return HttpResponseRedirect("/app/all/")
	
@login_required
def polls_view(request):
	return HttpResponseRedirect("/app/polls/")
