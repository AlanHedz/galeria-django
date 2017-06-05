from django.conf.urls import url
from views import show_image
from views import delete_image
from views import create_image
from views import edit_image
from views import create_comment
from views import like_image

app_name = 'images'

urlpatterns = [
	url(r'^create/$', create_image, name = 'create'),
	url(r'^delete/(?P<pk>\d+)/$', delete_image, name = 'delete'),
	url(r'^edit/(?P<pk>\d+)/$', edit_image, name = 'edit'),
	url(r'(?P<slug>[-\w]+)/$', show_image, name = 'show'),
	url(r'like/(?P<slug>[-\w]+)/$', like_image, name = 'like'),
	url(r'^comment/$', create_comment, name = 'create_comment')
]
