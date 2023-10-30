from django.db import models
from django.contrib import admin



#from django.db import models
from django.contrib.auth.models import User

class Facility(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    phone_number = models.CharField(max_length=15)
    admin_info = models.ForeignKey(User, on_delete=models.CASCADE)
    license_number = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Parent(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    # password = models.CharField(widget=forms.PasswordInput)

    def __str__(self):
        return self.first_name


class Classroom(models.Model):
    TYPES = [
        ('Infant', 'Infant'),
        ('Toddler', 'Toddler'),
        ('Twaddler', 'Twaddler'),
        ('3 Years Old', '3 Years Old'),
        ('4 Years Old', '4 Years Old'),
    ]
    type = models.CharField(max_length=20, choices=TYPES)
    capacity = models.PositiveIntegerField()
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE)
    # children = models.ManyToManyField(Child)
    def __str__(self):
        return self.type


class Child(models.Model):

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    dob = models.DateField()
    allergies = models.TextField()
    parents = models.ManyToManyField(Parent)
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE)
    classroom = models.ForeignKey(Classroom, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"



class Staff(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    dob = models.DateField()
    address = models.TextField()
    phone_number = models.CharField(max_length=15)
    hourly_salary = models.DecimalField(max_digits=8, decimal_places=2)
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE)



class Ledger(models.Model):
    child = models.ForeignKey(Child, on_delete=models.CASCADE)
    tuition_fee = models.DecimalField(max_digits=8, decimal_places=2)
    weekly_charge = models.DecimalField(max_digits=8, decimal_places=2)
    balance = models.DecimalField(max_digits=8, decimal_places=2)
    last_payment_date = models.DateField()

    def __str__(self):
        return f'{self.child.first_name} {self.child.last_name} Ledger'



class WeeklyCharge(models.Model):
    child = models.ForeignKey(Child, on_delete=models.CASCADE)
    week_start_date = models.DateField()

    def get_tuition_fee(self):
        classroom = self.child.classroom
        tuition_fee = ClassroomTuition.objects.get(classroom=classroom).tuition_fee
        return tuition_fee

    def save(self, *args, **kwargs):
        self.tuition_fee = self.get_tuition_fee()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.child.first_name} {self.child.last_name} Weekly Charge'



    def get_tuition_fee(self):
        classroom = self.child.classroom
        tuition_fee = ClassroomTuition.objects.get(classroom=classroom).tuition_fee
        return tuition_fee

    def save(self, *args, **kwargs):
        self.tuition_fee = self.get_tuition_fee()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.child.first_name} {self.child.last_name} Weekly Charge'


class Attendance(models.Model):
    child = models.ForeignKey(Child, on_delete=models.CASCADE)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    date = models.DateField()
    signed_in = models.TimeField()
    signed_out = models.TimeField()

    def __str__(self):
        return f'{self.child.first_name} {self.child.last_name} Attendance'

    class Meta:
        unique_together = ['child', 'date']  # Ensure one attendance record per child per day


class Attendance(models.Model):
    child = models.ForeignKey(Child, on_delete=models.CASCADE)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    date = models.DateField()
    signed_in = models.TimeField()
    signed_out = models.TimeField()

class ClassroomAssignment(models.Model):
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Staff, on_delete=models.CASCADE)
    assigned_children = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.classroom.type} Classroom Assignment for {self.teacher.first_name}'

    class Meta:
        unique_together = ['classroom', 'teacher']

from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from .models import Child, Classroom

@receiver(post_save, sender=Child)
@receiver(pre_delete, sender=Child)
def update_teacher_assignments(sender, instance, **kwargs):
    if kwargs.get('raw', False):
        # Skip this signal for raw database operations
        return
    from .views import assign_teachers
    assign_teachers()

@receiver(post_save, sender=Classroom)
@receiver(pre_delete, sender=Classroom)
def update_teacher_assignments_classroom(sender, instance, **kwargs):
    if kwargs.get('raw', False):
        # Skip this signal for raw database operations
        return
    assign_teachers()



class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(unique=True)
    # Add other fields as needed, e.g., salary, working hours, etc.



