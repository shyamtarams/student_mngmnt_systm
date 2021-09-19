from rest_framework import serializers
from .models import *

class dataSerializers(serializers.ModelSerializer):
    class Meta:
        model = apiData
        fields = ('id','name','contact','email')
        
class studentSerializers(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ('id','name','contact', 'email', 'username', 'password','rule','status','login')
