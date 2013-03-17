import datetime

from django.http import HttpResponse
from django.shortcuts import render_to_response
from models import Task

def seed_task(request):
    task = Task()
    task.name = 'TGA'
    task.message = 'Testdriving Google Appengine'
    task.deadline = datetime.datetime.now()
    task.cache_and_put()

    return HttpResponse("Task seeded!")

def set_cookie(request):
    response = HttpResponse('Cookie set!')
    response.set_cookie(key='hola', value='hola12345')
    return response

def cookie(request):
    response_str = 'Cookies<br/><pre>{0}</pre>'.format(request.COOKIES);
    return HttpResponse(response_str)

def set_session(request):
    request.session.set('time', 'time is {0}'.format(str(datetime.datetime.now())))
    return render_to_response('halo.html');

def get_session(request):
    return HttpResponse('{0}'.format(request.session.get('time')));

def del_session(request):
    request.session.clear()
    return HttpResponse('{0}'.format('Session cleared!'))

def home(request):
    task = Task.get_by_name('TGA')
    return HttpResponse('<h1>HelloWorld! {0}</h1>'.format(task.message))