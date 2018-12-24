from django.conf.urls import url
from mysite import views
from django.urls import path
from django.views.generic import TemplateView

# SET THE NAMESPACE!
app_name = 'mysite'

urlpatterns=[
    url('', TemplateView.as_view(template_name='mysite/homepage.html')),
]
