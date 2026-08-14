from django.db import models

# Create your models here.
class Student(models.Model):
    student_id = models.CharField( unique=True ,max_length=20 ) #student id must be unique
    name = models.CharField(max_length=50, null=False, blank=False)
    date_of_birth = models.DateField(auto_now=False, auto_now_add=False)
    contact_number = models.CharField( max_length=15)
    email = models.EmailField( max_length=254)
    course = models.CharField( max_length=50)
    start_year = models.IntegerField()
    end_year = models.IntegerField()
    address = models.TextField()

    def __str__(self):
        return self.name 