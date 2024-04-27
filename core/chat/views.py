from django.shortcuts import render
from rest_framework.generics import ListAPIView
from .models import Group,Message
from .serializers import GroupMessageSerializer, MessageSerializer
# Create your views here.

class GroupMessageAPiView(ListAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupMessageSerializer
