from django.conf.urls import url
from django.urls import path
from . import views, main_course_api

app_name = 'main'

urlpatterns = [
    #main url:
    path('', views.home, name='home'),
    path('get/realtime/course/', main_course_api.RealTimeCourseShower.as_view(), name='get_realtime_course'),

    #user auth urls:
    path('get/register/page/', views.AuthRegisterView.as_view(), name='register'),
    path('get/login/page/', views.AuthLoginView.as_view(), name='login'),
    path('logout/user/', views.logout_user, name='logout'),

    #user validate ajax urls:
    path('validate/register/form/', views.validate_register_form, name='validate_register_form'),
    path('validate/login/form/', views.validate_login_form, name='validate_login_form'),

    path('send/stream/data/', main_course_api.send_stream_data, name='send_stream_data'),
    path('handle/parse/task/', main_course_api.handle_parse_task, name='handle_parse'),

]

