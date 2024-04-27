from django.urls import  path
from .views import GroupMessageAPiView
urlpatterns = [
    path('group/message', GroupMessageAPiView.as_view())
]

