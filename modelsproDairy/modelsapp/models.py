from django.db import models
import datetime

# Create your models here.


class AcademicYear(models.Model):
    academic_year = models.CharField(max_length=30)
    current = models.BooleanField(default=False)
    #current = models.BooleanField()
    class Meta:
        unique_together = (("academic_year"),)

class Address(models.Model):
    H_No = models.CharField(max_length=30)
    Line1 = models.CharField(max_length=30)
    street = models.CharField(max_length=30)
    colony = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    pin = models.IntegerField()

class JobTitle(models.Model):
    title = models.CharField(max_length=30)
    class Meta:
        unique_together = (("title"),)

class Department(models.Model):
    dep_name=models.CharField(max_length=30)
    class_teacher_id = models.IntegerField(default=0)
    ac_year = models.ManyToManyField(AcademicYear)
    """
    from_year = models.IntegerField(default=int(datetime.datetime.today().year))
    to_year = models.IntegerField(default=int(datetime.datetime.today().year)+1)
    """
    class Meta:
        #unique_together = (("dep_name","from_year","to_year"),)
        unique_together = (("dep_name"),)

class Subject(models.Model):
    sub_name=models.CharField(max_length=50)
    teacher_id = models.IntegerField(default=0)
    text_book=models.CharField(max_length=50)
    publisher=models.CharField(max_length=50)
    """
    from_year = models.IntegerField(default=int(datetime.datetime.today().year))
    to_year = models.IntegerField(default=int(datetime.datetime.today().year)+1)
    """
    ac_year = models.ManyToManyField(AcademicYear)
    department = models.ManyToManyField(Department)
    department_name=models.CharField(max_length=50, default="No deparment")
    class Meta:
        #unique_together = (("sub_name","text_book","publisher","from_year","to_year", "department_name"),)
        unique_together = (("sub_name","text_book","publisher", "department_name"),)


"""
class Department(models.Model):
    dep_name = models.CharField(max_length=30)
"""

class Supervisor(models.Model):
    sup_id = models.IntegerField()
    class Meta:
        unique_together = (("sup_id"),)

class Contact(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    sur_name = models.CharField(max_length=30)
    login_name = models.CharField(max_length=30,default="suser1")
    email = models.EmailField()
    emp_id = models.IntegerField()
    supervisor = models.ForeignKey(Supervisor)
    #department = models.ForeignKey(Department)
    department = models.ManyToManyField(Department)
    ac_year = models.ManyToManyField(AcademicYear)
    job_title = models.ForeignKey(JobTitle)
    phone = models.IntegerField()
#   picture = models.CharField(max_length=30)
    picture = models.FileField(upload_to='tmp/')
    address = models.OneToOneField(Address)
    class Meta:
        unique_together = (("first_name", "last_name", "sur_name"),)

class SkillTitle(models.Model):
    skill_title = models.CharField(max_length=30)
    class Meta:
        unique_together = (("skill_title"),)
    
class Skill(models.Model):
    skill_name = models.CharField(max_length=30)
    exp_years = models.IntegerField()
    exp_level = models.IntegerField()
    contact = models.ManyToManyField(Contact)

class Leave(models.Model):
    requester = models.ForeignKey(Contact)
    app_id = models.IntegerField(default=0)
    req_date = models.DateField(blank=False, default=datetime.datetime.now)
    app_date = models.DateField(blank=False, default=datetime.datetime.now)
    from_date = models.DateField(blank=False, default=datetime.datetime.now)
    to_date = models.DateField(blank=False, default=datetime.datetime.now)
    count = models.IntegerField(default=0)
    state = models.IntegerField(default=0)
    type = models.IntegerField(default=0)
    req_comment = models.CharField(max_length=250, default='-')
    app_comment = models.CharField(max_length=250, default='-')

class Holiday(models.Model):
    h_date = models.DateField()
    holiday_name = models.CharField(max_length=50)

class LeaveBalance(models.Model):
    contact = models.OneToOneField(Contact)
    sick_leave_balance = models.IntegerField(default=0)
    earned_leave_balance = models.IntegerField(default=0)

class Test(models.Model):
    test_name=models.CharField(max_length=50)
    marks = models.IntegerField(default=0)
    grade=models.CharField(max_length=50)
    comment=models.CharField(max_length=500)
    academic_year = models.ManyToManyField(AcademicYear)
    subject = models.ManyToManyField(Subject)
    contact = models.ManyToManyField(Contact)
