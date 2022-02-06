import shelve

import requests
from bs4 import BeautifulSoup
from django import dispatch
from django.contrib.auth.decorators import login_required

from django.dispatch import receiver
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

from django.conf import *
from .models import Course, CustomUser
from .views import logger

URL = 'https://www.finanz.ru/valyuty/v-realnom-vremeni'
HTML_CLASS = 'push-data'
TAG = 'span'
db = shelve.open(filename='list_course_db')

class RealTimeCourseShower(View):
    """Method implements real-time course start point.... renders page......"""
    context = {'banner': 'Main Page', 'title': 'Main Page'}
    template_name = 'main/index.html'

    def get(self, request):
        self.context['courses'] = [course.course_name for course in Course.objects.all()]
        return render(request, template_name=self.template_name, context=self.context)

def handle_parse_task(request):
    """
    :param request: Http Request
    :return: None
    """
    append_to_list(request.GET.get('list_of_courses'))
    print('Test message....')

    from django.http import HttpResponse
    return HttpResponse(status=200)

def get_parsed_data(request, data):
    """
    :param request
    :param data: Http GET Request
    :return: JsonResponse
    """
    list_of_courses = [elem for elem in data.strip("[']").split()]
    context = {}

    if len(list_of_courses) < 2:
        specific_course = get_specific_course(course_name=list_of_courses[0])
        context[list_of_courses[0]] = specific_course
    else:
        all_courses = get_all_courses()
        valid_names = check_course_name_valid(list(all_courses.keys()))

        for course in valid_names:
            context[course] = all_courses[course]

    return context

def append_to_list(request_data):
    if request_data is not None:
        db['courses'] = request_data

def send_data_to_stream(request, stop_event_loop=False):
    from django_eventstream import send_event
    while True:
        if stop_event_loop:
            break

        parsed_data = get_parsed_data(request, data=db['courses'])
        send_event(channel='course', event_type='message',
        data=parsed_data)
        time.sleep(10)

def send_stream_data(request):
    """Signal, waiting for http request, when client connects to event urls....."""
    from django.http import HttpResponse
    stop = request.GET.get('stop')
    send_data_to_stream(request, stop_event_loop=stop)

    return HttpResponse(status=200)

def check_course_name_valid(courses: list) -> list:
    """This method checks for valid name of course"""
    result_list = []
    import re
    for course in courses: # in regex checking for first 3 letters and for 3 last letters should be like that
        # WUI/XUQ, OOP/GUI ....... (means that the string is valid)...
        if re.match('.{3}/.{3}', string=course):
            result_list.append(course)

    return result_list

def get_specific_course(course_name):

    get_valid_list = check_course_name_valid([course_name])
    valid_course_name = get_valid_list[0]

    if valid_course_name is not None:
        logger.debug('valid course name %s' % course_name)
        all_courses = get_all_courses()

        if valid_course_name in all_courses.keys():
            return all_courses[valid_course_name]

def get_all_courses() -> dict:
    """This method parse data from website...."""
    website_url = URL
    result = {}
    headers = {'Cache-Control': 'no-cache'}

    response = requests.get(url=website_url, timeout=10, headers=headers)
    if not str(response.status_code).startswith('4'):
        soup = BeautifulSoup(response.text, 'html.parser')

        courses = [course.attrs['data-jsvalue'] for course in soup.find_all(TAG, class_=HTML_CLASS,
        attrs={'data-jsvalue': True})]

        names = [name.text[:-1].replace('\xa0 (100:1', '') for name in soup.find_all(
        'div', attrs={'style': 'float:left;'})]

        for name, course in zip(names, courses):
            result[str(name)] = course

    return result
