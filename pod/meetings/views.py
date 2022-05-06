from django.http import (HttpResponse, HttpResponseRedirect)
from django.shortcuts import redirect, render, get_object_or_404
from django.template import RequestContext, loader
from django.urls import reverse
from django.contrib import messages
#from pod.meetings.filters import MeetingsFilter
from pod.meetings.forms import JoinForm, MeetingsForm
from pod.meetings.models import Meetings

def index(request):

  return render(request, 'meeting.html', {'dataMeetings':Meetings.objects.all()})

def add(request):
  print("add")
  if request.method == "POST":
    print('POST')
    form = MeetingsForm(request.POST)
    if form.is_valid():
      meeting = form.save()
      print(meeting, meeting.id)
      
      return redirect('/meeting')
  else:
    form = MeetingsForm()

  return render(request, 'meeting_add.html', {'form': form})

def begin_meeting(request):

    if request.method == "POST":
        begin_url = "http://bigbluebutton.org"
        return HttpResponseRedirect(begin_url)

    return render(request, 'meeting_begin.html')

def delete_meeting(request, meeting_id, password):
    if request.method == "POST":
        Meetings.end_meeting(meeting_id, password)

        msg = 'Successfully ended meeting %s' % meeting_id
        messages.success(request, msg)
        return redirect('/meeting')
    else:
        msg = 'Unable to end meeting %s' % meeting_id
        messages.error(request, msg)
        return redirect('/meeting')