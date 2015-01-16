from django.shortcuts import render
#from db.models import DiscussionTopic
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import render_to_response
from db.models import *
#from cms.forms import LoginForm
from django.contrib import auth
from django.core.context_processors import csrf
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from db.forms import *
from django.contrib.auth import authenticate, login
from django.core.paginator import *
# user authentication views
		

@login_required
def articles(request):
    
    language = 'en-gb'
    session_language = 'en-gb'
    username=request.user.username
    if 'lang' in request.COOKIES:
        language = request.COOKIES['lang']

    if 'lang' in request.session:
        session_language = request.session['lang']

    if request.method ==  'POST':
        if 'upvote' in request.POST:
            article_id=request.POST['article_id']                               # for upvoting, checking if already voted or not, if not then vote is added
            article=Article.objects.get(id=article_id)
            try:

                vote.objects.get(article=article,user=request.user)
                return HttpResponseRedirect('/app/multiupvote/')
            except vote.DoesNotExist:

                vote.objects.create(article=article,user=request.user)

    args = {}
    args.update(csrf(request))
    articles_list = Article.objects.all()
    paginator = Paginator(articles_list,5)

    page = request.GET.get('page')
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)

    args['articles'] = articles
    args['language'] = language
    args['session_language'] = session_language                             # passing data and rendering  templates
    args['username'] = username
    return render_to_response('articles.html',args)

@login_required
def article(request, article_id=1):
   
    if request.method ==  'POST':
        if 'upvote' in request.POST:                                        # for upvoting, checking if already voted or not, if not then vote is added
            article_id=request.POST['article_id']
            article=Article.objects.get(id=article_id)
            try:

                vote.objects.get(article=article,user=request.user)
                return HttpResponseRedirect('/app/multiupvote/')
            except vote.DoesNotExist:

                vote.objects.create(article=article,user=request.user)

         

    comment = Comment.objects.filter(article__id=article_id)                    # passing data and rendering  templates

    return render(request,'article.html',{'article': Article.objects.get(id=article_id),'comments':comment,'username':request.user.username})

@login_required
def language(request, language='en-gb'):
    response = HttpResponse("setting language to %s" % language)

    response.set_cookie('lang', language)

    request.session['lang'] = language

    return response

@login_required
def create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST,request.FILES)              # using django forms to create a topic in forum
        if form.is_valid():                                         # if data entered is properly then a topic is created with the data and data is added to database
            title=form.cleaned_data['title']
            subject=form.cleaned_data['subject']
            thumbnail=form.cleaned_data['thumbnail']

            article=Article.objects.create(title=title,body=subject,thumbnail=thumbnail,article_creator=request.user)

            return HttpResponseRedirect('/app/all/')
    else:
        form = ArticleForm()

    args = {}
    args.update(csrf(request))

    args['form'] = form

    return render_to_response('create_article.html', args)          # rendering form

@login_required
def add_comment(request, article_id):
    a=Article.objects.get(id=article_id) 

    if request.method == "POST":                                # using django forms to create a comment in forum
        f = CommentForm(request.POST)                           # if data entered is properly then a comment is created with the data and data is added to database
        if f.is_valid():
            body=f.cleaned_data['body']
            comment=Comment.objects.create(body=body,article=a,comment_creator=request.user)

            return HttpResponseRedirect('/app/get/%s' % article_id)
    else:
        f = CommentForm()

    args = {}
    args.update(csrf(request))
    username = request.user.username

    args['article'] = a
    args['f'] = f 
    args['username'] = username

    return render(request,'add_comment.html', args)  # rendering form

@login_required
def search_titles(request):
    if request.method == "POST":
        search_text = request.POST['search_text']           # searching topics in discussion form
    if search_text == '':
        search_text = '$%^&*#$@*'

    articles = Article.objects.filter(title__icontains=search_text)    # filtering based upon typed text
    art = Article.objects.filter(article_creator__username=search_text)
    
    #for a in art:
     #   if a not in articles:
      #      articles.append(a)


    return render_to_response('ajax_search.html',{'articles' : articles | art})

@login_required
def my_articles(request):
    username=request.user.username
    articles_list=Article.objects.filter(article_creator__username=request.user.username)               # displaying topics created by user
    paginator = Paginator(articles_list,5)

    if request.method ==  'POST':                           # for upvoting, checking if already voted or not, if not then vote is added
        if 'upvote' in request.POST:
            article_id=request.POST['article_id']
            article=Article.objects.get(id=article_id)
            try:

                vote.objects.get(article=article,user=request.user)
                return HttpResponseRedirect('/app/multiupvote/')
            except vote.DoesNotExist:

                vote.objects.create(article=article,user=request.user)

    page = request.GET.get('page')
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles = paginator.page(1)       #        using django's paginator to view 5 topics in one page
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)
    args = {}
    args.update(csrf(request))

    args['articles'] = articles
    args['username'] = username

    return render(request,'mytopics.html',args)         # rendering html

@login_required
def user_articles(request,uname):
    username=request.user.username
    articles_list=Article.objects.filter(article_creator__username=uname)               # displaying topics created by user
    paginator = Paginator(articles_list,5)

    if request.method ==  'POST':                           # for upvoting, checking if already voted or not, if not then vote is added
        if 'upvote' in request.POST:
            article_id=request.POST['article_id']
            article=Article.objects.get(id=article_id)
            try:

                vote.objects.get(article=article,user=request.user)
                return HttpResponseRedirect('/app/multiupvote/')
            except vote.DoesNotExist:

                vote.objects.create(article=article,user=request.user)

    page = request.GET.get('page')
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles = paginator.page(1)       #        using django's paginator to view 5 topics in one page
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)
    args = {}
    args.update(csrf(request))

    args['articles'] = articles
    args['username'] = username

    return render(request,'usertopics.html',args)      

@login_required
def pop_articles(request):
    #articles=Article.objects.all()                     # displaying popular topics based on number of upvote + 2* number of comments

    articles_tuple=Article.objects.all()
    articles_list=list(articles_tuple)
    mergesort(articles_list)

    if request.method ==  'POST':                        # for upvoting, checking if already voted or not, if not then vote is added
        if 'upvote' in request.POST:
            article_id=request.POST['article_id']
            article=Article.objects.get(id=article_id)
            try:

                vote.objects.get(article=article,user=request.user)
                return HttpResponseRedirect('/app/multiupvote/')
            except vote.DoesNotExist:

                vote.objects.create(article=article,user=request.user)
    


    #articles_list=Article.objects.order_by('num_upvotes')

    paginator = Paginator(articles_list,5)

    page = request.GET.get('page')
    try:
        articles = paginator.page(page)                 #        using django's paginator to view 5 topics in one page
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)

    args = {}
    args.update(csrf(request))
    username = request.user.username
    args['articles'] = articles
    args['username'] = username

    return render(request,'poparticles.html', args)         # rendering html

@login_required
def del_article(request, article_id):
                                                    # to delete the topics created by user
    if request.POST.get('delete', ''):
        a=Article.objects.get(id=article_id)
        a.delete()
    return HttpResponseRedirect("/app/mytop/")

#sort
def mergesort( aList ):                             # used mergesort to sort topics for popular topics function
  _mergesort( aList, 0, len( aList ) - 1 )
 
 
def _mergesort( aList, first, last ):
  # break problem into smaller structurally identical pieces
  mid = ( first + last ) / 2
  if first < last:
    _mergesort( aList, first, mid )
    _mergesort( aList, mid + 1, last )
 
  # merge solved pieces to get solution to original problem
  a, f, l = 0, first, mid + 1
  tmp = [None] * ( last - first + 1 )
 
  while f <= mid and l <= last:
    if aList[f].sort() > aList[l].sort() :
      tmp[a] = aList[f]
      f += 1
    else:
      tmp[a] = aList[l]
      l += 1
    a += 1
 
  if f <= mid :
    tmp[a:] = aList[f:mid + 1]
 
  if l <= last:
    tmp[a:] = aList[l:last + 1]
 
  a = 0
  while first <= last:
    aList[first] = tmp[a]
    first += 1
    a += 1


#polls
@login_required
def cpoll(request):                     # to create a poll
    if request.method == 'POST':
        form = PollForm(request.POST)                   # using django's form for creating poll
        if form.is_valid():                         # if data entered is properly then a poll is created with the data and data is added to database
            question=form.cleaned_data['question']

            poll=Poll.objects.create(question=question,poll_creator=request.user)

            return HttpResponseRedirect('/app/polls/')
    else:
        form = PollForm()

    username = request.user.username

    args = {}
    args.update(csrf(request))
    args['username'] = username
                                                            # rendering html
    args['form'] = form

    return render_to_response('create_poll.html', args)

@login_required
def polls(request):
    
    

    if request.method ==  'POST':                       #  for poling yes, checking if already voted or not, if not then vote is added
        if 'yes' in request.POST:
            poll_id=request.POST['poll_id']
            poll=Poll.objects.get(id=poll_id)
            try:
                
                Yes.objects.get(poll=poll,user=request.user)

                return HttpResponseRedirect('/app/multivote/')
            except Yes.DoesNotExist:
                try:
                    No.objects.get(poll=poll,user=request.user)
                    return HttpResponseRedirect('/app/multivote/')
                except No.DoesNotExist:
                    try:
                        Cantsay.objects.get(poll=poll,user=request.user)
                        return HttpResponseRedirect('/app/multivote/')
                    except Cantsay.DoesNotExist:
                        Yes.objects.create(poll=poll,user=request.user)
                    

    if request.method ==  'POST':                           #  for poling no, checking if already voted or not, if not then vote is added
        if 'no' in request.POST:
            poll_id=request.POST['poll_id']
            poll=Poll.objects.get(id=poll_id)
            try:
                
                Yes.objects.get(poll=poll,user=request.user)
                return HttpResponseRedirect('/app/multivote/')
            except Yes.DoesNotExist:
                try:
                    No.objects.get(poll=poll,user=request.user)
                    return HttpResponseRedirect('/app/multivote/')
                except No.DoesNotExist:
                    try:
                        Cantsay.objects.get(poll=poll,user=request.user)
                        return HttpResponseRedirect('/app/multivote/')
                    except Cantsay.DoesNotExist:
                        No.objects.create(poll=poll,user=request.user)
                

    if request.method ==  'POST':                   #  for poling cantsay, checking if already voted or not, if not then vote is added
        if 'cantsay' in request.POST:
            poll_id=request.POST['poll_id']
            poll=Poll.objects.get(id=poll_id)
            try:
                
                Yes.objects.get(poll=poll,user=request.user)
                return HttpResponseRedirect('/app/multivote/')
            except Yes.DoesNotExist:
                try:
                    No.objects.get(poll=poll,user=request.user)
                    return HttpResponseRedirect('/app/multivote/')
                except No.DoesNotExist:
                    try:
                        Cantsay.objects.get(poll=poll,user=request.user)
                        return HttpResponseRedirect('/app/multivote/')
                    except Cantsay.DoesNotExist:
                        Cantsay.objects.create(poll=poll,user=request.user)
                    

    args = {}
    args.update(csrf(request))
    polls_list = Poll.objects.all()
    paginator = Paginator(polls_list,5)

    page = request.GET.get('page')
    try:
        polls = paginator.page(page)
    except PageNotAnInteger:
        polls = paginator.page(1)
    except EmptyPage:
        polls = paginator.page(paginator.num_pages)


    username= request.user.username

    args['polls'] = polls
    args['username'] = username
    
    return render_to_response('polls.html',args)


@login_required
def poll(request, poll_id=1): # to view result of a particular  poll

    return render(request,'poll.html',{'poll': Poll.objects.get(id=poll_id),'username':request.user.username})

@login_required
def search_polls(request):      # to search polls by question
    if request.method == "POST":
        search_text = request.POST['search_text']
    if search_text == '':
        search_text = '$%^&*#$@*'

    polls = Poll.objects.filter(question__icontains=search_text)
    art = Poll.objects.filter(poll_creator__username=search_text)
    

    return render_to_response('ajax_polls.html',{'polls' : polls | art})

@login_required
def my_polls(request):  # to view polls created by logged in user
    username=request.user.username
    polls_list=Poll.objects.filter(poll_creator__username=request.user.username)
    paginator = Paginator(polls_list,5)

    if request.method ==  'POST':           #  for poling yes, checking if already voted or not, if not then vote is added
        if 'yes' in request.POST:
            poll_id=request.POST['poll_id']
            poll=Poll.objects.get(id=poll_id)
            try:
                
                Yes.objects.get(poll=poll,user=request.user)

                return HttpResponseRedirect('/app/multivote/')
            except Yes.DoesNotExist:
                try:
                    No.objects.get(poll=poll,user=request.user)
                    return HttpResponseRedirect('/app/multivote/')
                except No.DoesNotExist:
                    try:
                        Cantsay.objects.get(poll=poll,user=request.user)
                        return HttpResponseRedirect('/app/multivote/')
                    except Cantsay.DoesNotExist:
                        Yes.objects.create(poll=poll,user=request.user)
                    

    if request.method ==  'POST':           #  for poling no, checking if already voted or not, if not then vote is added
        if 'no' in request.POST:
            poll_id=request.POST['poll_id']
            poll=Poll.objects.get(id=poll_id)
            try:
                
                Yes.objects.get(poll=poll,user=request.user)
                return HttpResponseRedirect('/app/multivote/')
            except Yes.DoesNotExist:
                try:
                    No.objects.get(poll=poll,user=request.user)
                    return HttpResponseRedirect('/app/multivote/')
                except No.DoesNotExist:
                    try:
                        Cantsay.objects.get(poll=poll,user=request.user)
                        return HttpResponseRedirect('/app/multivote/')
                    except Cantsay.DoesNotExist:
                        No.objects.create(poll=poll,user=request.user)
                

    if request.method ==  'POST':       #  for poling cantsay, checking if already voted or not, if not then vote is added
        if 'cantsay' in request.POST:
            poll_id=request.POST['poll_id']
            poll=Poll.objects.get(id=poll_id)
            try:
                
                Yes.objects.get(poll=poll,user=request.user)
                return HttpResponseRedirect('/app/multivote/')
            except Yes.DoesNotExist:
                try:
                    No.objects.get(poll=poll,user=request.user)
                    return HttpResponseRedirect('/app/multivote/')
                except No.DoesNotExist:
                    try:
                        Cantsay.objects.get(poll=poll,user=request.user)
                        return HttpResponseRedirect('/app/multivote/')
                    except Cantsay.DoesNotExist:
                        Cantsay.objects.create(poll=poll,user=request.user)


    

    page = request.GET.get('page')
    try:
        polls = paginator.page(page)
    except PageNotAnInteger:
        polls = paginator.page(1)
    except EmptyPage:
        polls = paginator.page(paginator.num_pages)
    args = {}
    args.update(csrf(request))

    args['polls'] = polls
    args['username'] = username
    return render(request,'mypolls.html',args)

@login_required
def user_polls(request,unam):  # to view polls created by logged in user
    username=request.user.username
    polls_list=Poll.objects.filter(poll_creator__username=unam)
    paginator = Paginator(polls_list,5)

    if request.method ==  'POST':           #  for poling yes, checking if already voted or not, if not then vote is added
        if 'yes' in request.POST:
            poll_id=request.POST['poll_id']
            poll=Poll.objects.get(id=poll_id)
            try:
                
                Yes.objects.get(poll=poll,user=request.user)

                return HttpResponseRedirect('/app/multivote/')
            except Yes.DoesNotExist:
                try:
                    No.objects.get(poll=poll,user=request.user)
                    return HttpResponseRedirect('/app/multivote/')
                except No.DoesNotExist:
                    try:
                        Cantsay.objects.get(poll=poll,user=request.user)
                        return HttpResponseRedirect('/app/multivote/')
                    except Cantsay.DoesNotExist:
                        Yes.objects.create(poll=poll,user=request.user)
                    

    if request.method ==  'POST':           #  for poling no, checking if already voted or not, if not then vote is added
        if 'no' in request.POST:
            poll_id=request.POST['poll_id']
            poll=Poll.objects.get(id=poll_id)
            try:
                
                Yes.objects.get(poll=poll,user=request.user)
                return HttpResponseRedirect('/app/multivote/')
            except Yes.DoesNotExist:
                try:
                    No.objects.get(poll=poll,user=request.user)
                    return HttpResponseRedirect('/app/multivote/')
                except No.DoesNotExist:
                    try:
                        Cantsay.objects.get(poll=poll,user=request.user)
                        return HttpResponseRedirect('/app/multivote/')
                    except Cantsay.DoesNotExist:
                        No.objects.create(poll=poll,user=request.user)
                

    if request.method ==  'POST':       #  for poling cantsay, checking if already voted or not, if not then vote is added
        if 'cantsay' in request.POST:
            poll_id=request.POST['poll_id']
            poll=Poll.objects.get(id=poll_id)
            try:
                
                Yes.objects.get(poll=poll,user=request.user)
                return HttpResponseRedirect('/app/multivote/')
            except Yes.DoesNotExist:
                try:
                    No.objects.get(poll=poll,user=request.user)
                    return HttpResponseRedirect('/app/multivote/')
                except No.DoesNotExist:
                    try:
                        Cantsay.objects.get(poll=poll,user=request.user)
                        return HttpResponseRedirect('/app/multivote/')
                    except Cantsay.DoesNotExist:
                        Cantsay.objects.create(poll=poll,user=request.user)


    

    page = request.GET.get('page')
    try:
        polls = paginator.page(page)
    except PageNotAnInteger:
        polls = paginator.page(1)
    except EmptyPage:
        polls = paginator.page(paginator.num_pages)
    args = {}
    args.update(csrf(request))

    args['polls'] = polls
    args['username'] = username
    return render(request,'userpolls.html',args)

@login_required
def pop_polls(request):         # to view popular polls
    #articles=Article.objects.all()
    username = request.user.username
    polls_tuple=Poll.objects.all()
    polls_list=list(polls_tuple)
    mergsort(polls_list)

    if request.method ==  'POST':           #  for poling yes, checking if already voted or not, if not then vote is added
        if 'yes' in request.POST:
            poll_id=request.POST['poll_id']
            poll=Poll.objects.get(id=poll_id)
            try:
                
                Yes.objects.get(poll=poll,user=request.user)

                return HttpResponseRedirect('/app/multivote/')
            except Yes.DoesNotExist:
                try:
                    No.objects.get(poll=poll,user=request.user)
                    return HttpResponseRedirect('/app/multivote/')
                except No.DoesNotExist:
                    try:
                        Cantsay.objects.get(poll=poll,user=request.user)
                        return HttpResponseRedirect('/app/multivote/')
                    except Cantsay.DoesNotExist:
                        Yes.objects.create(poll=poll,user=request.user)
                    

    if request.method ==  'POST':               #  for poling no, checking if already voted or not, if not then vote is added
        if 'no' in request.POST:
            poll_id=request.POST['poll_id']
            poll=Poll.objects.get(id=poll_id)
            try:
                
                Yes.objects.get(poll=poll,user=request.user)
                return HttpResponseRedirect('/app/multivote/')
            except Yes.DoesNotExist:
                try:
                    No.objects.get(poll=poll,user=request.user)
                    return HttpResponseRedirect('/app/multivote/')
                except No.DoesNotExist:
                    try:
                        Cantsay.objects.get(poll=poll,user=request.user)
                        return HttpResponseRedirect('/app/multivote/')
                    except Cantsay.DoesNotExist:
                        No.objects.create(poll=poll,user=request.user)
                

    if request.method ==  'POST':               #  for poling cantsay, checking if already voted or not, if not then vote is added
        if 'cantsay' in request.POST:
            poll_id=request.POST['poll_id']
            poll=Poll.objects.get(id=poll_id)
            try:
                
                Yes.objects.get(poll=poll,user=request.user)
                return HttpResponseRedirect('/app/multivote/')
            except Yes.DoesNotExist:
                try:
                    No.objects.get(poll=poll,user=request.user)
                    return HttpResponseRedirect('/app/multivote/')
                except No.DoesNotExist:
                    try:
                        Cantsay.objects.get(poll=poll,user=request.user)
                        return HttpResponseRedirect('/app/multivote/')
                    except Cantsay.DoesNotExist:
                        Cantsay.objects.create(poll=poll,user=request.user)

    

    #articles_list=Article.objects.order_by('num_upvotes')

    paginator = Paginator(polls_list,5)

    page = request.GET.get('page')
    try:
        polls = paginator.page(page)
    except PageNotAnInteger:
        polls = paginator.page(1)
    except EmptyPage:
        polls = paginator.page(paginator.num_pages)

    args = {}
    args.update(csrf(request))

    args['polls'] = polls
    args['username'] = username

    return render(request,'popolls.html', args)

def mergsort( aList ):
  _mergsort( aList, 0, len( aList ) - 1 )
 
 
def _mergsort( aList, first, last ):
  # break problem into smaller structurally identical pieces
  mid = ( first + last ) / 2
  if first < last:
    _mergsort( aList, first, mid )
    _mergsort( aList, mid + 1, last )
 
  # merge solved pieces to get solution to original problem
  a, f, l = 0, first, mid + 1
  tmp = [None] * ( last - first + 1 )
 
  while f <= mid and l <= last:
    if aList[f].most() > aList[l].most() :
      tmp[a] = aList[f]
      f += 1
    else:
      tmp[a] = aList[l]
      l += 1
    a += 1
 
  if f <= mid :
    tmp[a:] = aList[f:mid + 1]
 
  if l <= last:
    tmp[a:] = aList[l:last + 1]
 
  a = 0
  while first <= last:
    aList[first] = tmp[a]
    first += 1
    a += 1

@login_required
def del_poll(request, poll_id):  # to delete a poll
    
    if request.POST.get('delete', ''):
        a=Poll.objects.get(id=poll_id)
        a.delete()
    return HttpResponseRedirect("/app/mypolls/")

@login_required
def multivote(request): # if a user polled multiple times this will open
    return render(request, 'multivote.html', {'username':request.user.username})

@login_required
def multiupvote(request): # if a user upvoted multiple times this will open
    return render(request, 'multiupvote.html', {'username':request.user.username})