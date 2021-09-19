from django.urls import path,include
from .views import *

from rest_framework import routers
router = routers.DefaultRouter()


# router.register(r'data', apiViewSet,'data'),
router.register(r'data', studentViewSet, 'home'),

urlpatterns = [
    # path('student/', student),
    # path('signup/', signup),
    path('login/', login),
    path('logout/', logout),
    path('adminsite/', adminsite,name="admin site"),
    path('addstudent/', studentRegister,name="studentRegister"),
    path('active/', activeStudent,name="activeStudent"),
    path('inactive/', inactiveStudent,name="inactiveStudent"),
    path('status/<int:id>', studentStatus,name="studentStatus"),
    path('studentDetails/', studentDetails,name="studentDetails"),
    path('updatedetails/', updateStudent,name="updateStudent"),

    # api
    # path('apiview/',apiView,name="apiView"),
    # path('apiview/<int:id>/',apiView,name="apiView"),
    
    # path('apidata/',apiViewSet.as_view(),name="apiViewSet"),
    path('studentdata/',sdatViewSet.as_view(),name="sdatViewSet"),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/', include(router.urls)),
    # path('std',student.as_view(),name='std'),
    path('students/',studentDtails,name="studentDtails"),
    path('students/<int:id>/',studentDtails,name="studentDtails"),
]