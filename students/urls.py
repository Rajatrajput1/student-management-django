from django.urls import path
from . import views

urlpatterns = [
     path('', views.student_list, name= 'student_list'),
     path('add/',views.student_create, name = 'student_create'),
     path('edit/<str:student_id>', views.student_update, name= 'student_update'),
     path('delete/<str:student_id>', views.student_delete, name= 'student_delete'),

]