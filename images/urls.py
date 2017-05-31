from django.conf.urls import url
from views import CreateClass
from views import ShowClass

app_name = 'images'

urlpatterns = [
    url(r'^create/$', CreateClass.as_view(), name = 'create'),
    url(r'(?P<slug>[-\w]+)/$', ShowClass.as_view(), name = 'show')
]
