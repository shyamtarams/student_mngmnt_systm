from django.shortcuts import render, redirect
from .models import *
from home.forms import studentRegisterForm

from accounts.models import myUser
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required

#searializers example
# from .serializers import dataSerializers
from .serializers import *
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from .models import apiData



from rest_framework import viewsets
from rest_framework.views import APIView
import json


@csrf_exempt
def apiView(request,id=0):
    if request.method == 'POST':
        print(request)
        udata = JSONParser().parse(request)
        print(udata)
        u_serializers = dataSerializers(data = udata)
        if u_serializers.is_valid():
            u_serializers.save()
            return JsonResponse('data in', safe=False)
        return JsonResponse("failed ",safe=False)
    elif request.method == 'GET':
        user= apiData.objects.all()
        u_serializers = dataSerializers(user, many='True' )
        return JsonResponse(u_serializers.data, safe=False)
    elif request.method == "PUT":
        udata = JSONParser().parse(request)
        print(udata['id'])
        user = apiData.objects.get(id=udata['id'])
        u_serializers = dataSerializers(user, udata)
        if u_serializers.is_valid():
            u_serializers.save()
            return JsonResponse('data updated', safe=False)
        return JsonResponse("failed ",safe=False)
    elif request.method == "DELETE":
        user = apiData.objects.get(id=id)
        user.delete()
        return JsonResponse("deleted data",safe=False)

#student function based
@csrf_exempt
def studentDtails(request, id=0):
    if request.method == 'GET':
        student=Student.objects.all()
        s_serializers = studentSerializers(student, many='True' )
        return JsonResponse(s_serializers.data, safe=False)
    
    elif request.method == 'POST':
        student = JSONParser().parse(request)
        print(student['username'])
        login=Login(username=student['username'],password=student['password'])
        login.save()
        std=Login.objects.get(username=login.username)
        print(login.username)
        student.update({"login":std.id})
        print(student)
        s_serializers = studentSerializers(data = student)
        print(s_serializers)
        if s_serializers.is_valid():
            s_serializers.save()
            return JsonResponse('data in', safe=False)
        return JsonResponse("failed ",safe=False)
    
    elif request.method == "PUT":
        student = JSONParser().parse(request)
        user = Student.objects.get(id=student['id'])
        s_serializers = studentSerializers(user, student)
        if s_serializers.is_valid():
            s_serializers.save()
            return JsonResponse('data updated', safe=False)
        return JsonResponse("failed ",safe=False)
    
    elif request.method == "DELETE":
        student = Student.objects.get(id=id)
        student.delete()
        return JsonResponse("deleted data",safe=False)



        

# class searializers        
class sdatViewSet(APIView):
    serializer_class = studentSerializers
    def get(self,request,*args, **kwargs):
        user= Student.objects.all()
        u_serializers = studentSerializers(user, many='True' )
        return JsonResponse(u_serializers.data, safe=False)
    
    def post(self,request,*args, **kwargs):
        udata = JSONParser().parse(request)
        print(udata)
        # nm=json.loads(request.data['username'])
        print(nm)
        # print(udata['username'])
        # print(username)
        # login=Login(username=udata['username'],password=udata['password'])
        # login.save()
        # print(udata)
        # udata.push({"login":"login"})
        print(udata)
        u_serializers = studentSerializers(data = udata)
        # print(u_serializers)
        if u_serializers.is_valid():
            u_serializers.save()
            print(u_serializers)
            return JsonResponse('data in', safe=False)
        return JsonResponse("failed ",safe=False)



class studentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all().order_by('name')
    serializer_class = studentSerializers
    # def get(self,request):
    #     print("re")
    #     serializer_class = studentSerializers
   
        








# Create your views here.


# def signup(request):
#     if request.method == 'POST':
#         form = studentRegisterForm(request.POST)
#         print(form)
#         if form.is_valid():
#             rule = form.cleaned_data.get('rule')
#             status = form.cleaned_data.get('status')
#             print(rule)
#             print(status)

#             form.save()

#             username = form.cleaned_data.get('username')
#             raw_password = form.cleaned_data.get('password')
#             user = authenticate(username=username, password=raw_password)
#             print(user)
#             login(request, user)
#             return redirect('/home/adminsite')
#     else:
#         form = studentRegisterForm()
#     return render(request, 'home/addstudent.html', {'form': form})

def login(request):
    if request.method=='POST':
        try:
            un=request.POST['username']
            pw=request.POST['password']
            # if Login.objects.get(username=un,password=pw):
                
            user=Login.objects.get(username=un,password=pw)
            request.session['log_id']=user.id 
            return redirect('/home/studentDetails/')
        except Exception as err:
            return redirect("/home/login")
    else:
        return render(request,"home/home.html")


 
def student(request):
    return render(request,"home/home.html")

@login_required(login_url='/accounts/login/')
def adminsite(request):
    data={}
    if Student.objects.filter(rule="student"):
        student_dtl=Student.objects.filter(rule="student")
        student_cnt=Student.objects.filter(rule="student").count()
        student_cnt_a=Student.objects.filter(status="active").count()
        student_cnt_a=Student.objects.filter(status="active").count()
        student_cnt_i=student_cnt - student_cnt_a

        data={
            'student_dtl':student_dtl,
            'student_cnt':student_cnt,
            'student_cnt_a':student_cnt_a,
            'student_cnt_i':student_cnt_i, 
        }
    return render(request,"home/adminsite.html",data)

# register student
@login_required(login_url='/accounts/login/')
def studentRegister(request):
    if request.method == "POST":
        name=request.POST["name"]
        contact=request.POST["contact"]
        email=request.POST["email"]
        username=request.POST["username"]
        password=request.POST["password"]
        rule="student"
        status="active"

        login=Login(username=username,password=password)
        login.save()

        newStudent=Student(name=name,contact=contact,email=email,username=username,password=password,rule=rule,status=status,login=login)
        print(newStudent)
        newStudent.save()

        

        return redirect("/home/adminsite")
    else:
        return render(request,"home/addstudent.html")

# active student
@login_required(login_url='/accounts/login/')
def activeStudent(request):
    student_dtl=Student.objects.filter(status="active")
    data={
            'student_dtl':student_dtl,
    }
    

    return render(request,"home/activestudent.html",data)

# inactive student
@login_required(login_url='/accounts/login/')
def inactiveStudent(request):
    student_dtl=Student.objects.filter(status="inactive")
    data={
            'student_dtl':student_dtl,
     }
    return render(request,"home/inactivestudent.html",data)

#change student status
@login_required(login_url='/accounts/login/')
def studentStatus(request,id):
    student_dtl=Student.objects.get(id=id)
    if student_dtl.status == "active":
        student_dtl.status="inactive"
        student_dtl.save()
    else:
        student_dtl.status="active"
        student_dtl.save()
    return redirect("/home/adminsite")

#get loged student details
def studentDetails(request):
    try:
        id= request.session['log_id']
        user=Login.objects.get(id=id)
        student_dtl=Student.objects.filter(id=1)

        data={
                'user':user,
                'student_dtl':student_dtl,
        }
        return render(request,"student/studentsite.html",data)
    except:
        return redirect("/home/login/")
    

def logout(request):
    try:
        del request.session['log_id']
        return redirect("/home/login/")
    except:
        return redirect("/home/login/")
    
#update student details
def updateStudent(request):
    try:
        id= request.session['log_id']
        user=Login.objects.get(id=id)
        if Student.objects.get(login=user.id,status="active"):
            student_dtl=Student.objects.get(login=user.id,status="active")
            if request.method=="POST":
                name=request.POST["name"]
                contact=request.POST["contact"]
                email=request.POST["email"]
                username=request.POST["username"]
                password=request.POST["password"]
                rule="student"
                status="active"

                update_data=Student.objects.get(login=user.id)
                update_data.name=name
                update_data.contact=contact
                update_data.email=email
                update_data.username=username
                update_data.password=password
                update_data.rule=rule
                update_data.status=status
                update_data.save()
                
                return redirect("/home/updatedetails/")
            else:
                data={
                    'user':user,
                    'student_dtl':student_dtl,
                }
                return render(request,"student/studentupdate.html",data)
        elif Student.objects.get(login=user.id,status="inactive"):
            return redirect("/home/studentDetails/")
    except:
        return redirect("/home/studentDetails/")

   



