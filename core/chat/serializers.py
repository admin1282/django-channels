from rest_framework import serializers
from .models import Message, Group
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','first_name','email']
class MessageSerializer(serializers.ModelSerializer):
    first_name = serializers.SerializerMethodField()
    class Meta:
        model = Message
        fields = ('__all__')

    def get_first_name(self, obj):
        instance = User.objects.get(id=obj.sender.id)
        return instance.first_name

class GroupMessageSerializer(serializers.ModelSerializer):
    message = serializers.SerializerMethodField()
    class Meta:
        model = Group
        fields = ('__all__')

    def get_message(self, obj):
        instance = obj
        message = Message.objects.filter(group=obj)
        return MessageSerializer(message, many=True).data