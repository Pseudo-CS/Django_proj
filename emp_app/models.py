from django.db import models

# Create your models here.
# A Django model is the built-in feature that Django uses to create tables, their fields, and various constraints

class Department(models.Model):
    name = models.CharField(max_length=100, null=False)
    location = models.CharField(max_length=100)

    def __str__(self):      # this is the conventional way of defining the output when trying to print a class(print(mydept), where mydept is a object of class department)
        return self.name    # in the django context, defining this function helps us see the object's name in the db


class Role(models.Model):
    name = models.CharField(max_length=100, null=False)

    def __str__(self):
        return self.name


class Employee(models.Model):
    first_name = models.CharField(max_length=100, null=False)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(default='')
    dept = models.ForeignKey(Department, on_delete=models.CASCADE) # when we want to connect a field to the database we use foreign key
    salary = models.IntegerField(default=0)
    bonus = models.IntegerField(default=0)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    phone = models.IntegerField(default=0)
    hire_date = models.DateField()
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return '%s %s %s' %(self.first_name, self.last_name, self.phone)