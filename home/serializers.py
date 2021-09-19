from rest_framework import serializers
from .models import *
from accounts.models import myUser as User

class dataSerializers(serializers.ModelSerializer):
    class Meta:
        model = apiData
        fields = ('id','name','contact','email')

class userSerializers(serializers.HyperlinkedModelSerializer):
     class Meta:
        model = User
        fields = ['username', 'email', 'rule']


        
class studentSerializers(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ('id','name','contact', 'email', 'username', 'password','rule','status','login')

class studentDetailsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ('id','name','contact', 'email', 'username', 'password' )