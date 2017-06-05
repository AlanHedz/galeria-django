from django.conf.urls import url
from views import LoginClass
from views import RegisterClass
from views import MyImages
from views import logout

app_name = 'user'

urlpatterns = [
    url(r'^login/$', LoginClass.as_view(), name = 'login'),
    url(r'^register/$', RegisterClass.as_view(), name = 'register'),
    url(r'^logout/$', logout, name = 'logout'),
    url(r'^my_images/$', MyImages.as_view(), name = 'my_images'),
]
