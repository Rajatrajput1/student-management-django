from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter
from .views import StudentViewSet


router = DefaultRouter()

router.register(
    "api/students",
    StudentViewSet,
    basename="student"
)


urlpatterns = [
     path('', views.student_list, name= 'student_list'),
     path("login/", views.user_login, name="login"),
     path("logout/", views.user_logout, name="logout"),

     path('add/',views.student_create, name = 'student_create'),
     path('edit/<str:student_id>', views.student_update, name= 'student_update'),
     path('delete/<str:student_id>', views.student_delete, name= 'student_delete'),
] 

urlpatterns += router.urls 