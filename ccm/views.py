from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Facility, Child, Staff, Classroom, Ledger, Attendance, Parent
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from django.utils import timezone
from django.contrib.auth.models import User
from .forms import FacilityForm, ChildForm, StaffForm, ClassroomForm, LedgerForm, AttendanceForm, FacilityEditForm, LedgerEntryForm, WeeklyChargeForm, ParentForm

# Views for the System Administrator

def home(request):
    return render(request, 'students/home.html')

# @login_required
def admin_dashboard(request):
    facilities = Facility.objects.all()
    return render(request, 'admin/dashboard.html', {'facilities': facilities})

# views.py

# ccm/views.py

def create_facility(request):
    if request.method == 'POST':
        form = FacilityForm(request.POST)
        if form.is_valid():
            form.save()
            # Add a success message
            messages.success(request, 'Facility created successfully.')
            return redirect('ccm:facility_admin_dashboard')
    else:
        form = FacilityForm()

    return render(request, 'admin/create_facility.html', {'form': form})

def view_facilities(request):
    # Retrieve all facilities from the database
    facilities = Facility.objects.all()

    return render(request, 'admin/view_facilities.html', {'facilities': facilities})

# @login_required
def facility_details(request, facility_id):
    facility = get_object_or_404(Facility, pk=facility_id)
    return render(request, 'admin/facility_details.html', {'facility': facility})

def edit_facility(request, facility_id):
    facility = get_object_or_404(Facility, pk=facility_id)

    if request.method == 'POST':
        form = FacilityEditForm(request.POST, instance=facility)
        if form.is_valid():
            form.save()
            # Add a success message
            return redirect('ccm:view_facilities')

    else:
        form = FacilityEditForm(instance=facility)

    return render(request, 'admin/edit_facility.html', {'form': form})

def delete_facility(request, facility_id):
    facility = get_object_or_404(Facility, pk=facility_id)

    if request.method == 'POST':
        facility.delete()
        # Add a success message
        return redirect('ccm:view_facilities')

    return render(request, 'admin/delete_facility.html', {'facility': facility})


# @login_required
def admin_reports(request):
    week_start = timezone.now() - timezone.timedelta(days=timezone.now().weekday())
    week_end = week_start + timezone.timedelta(days=4)
    total_earnings = Ledger.objects.filter(last_payment_date__gte=week_start, last_payment_date__lte=week_end).aggregate(Sum('weekly_charge'))['weekly_charge__sum']
    total_billing = Ledger.objects.filter(last_payment_date__gte=week_start, last_payment_date__lte=week_end).aggregate(Sum('tuition_fee'))['tuition_fee__sum']
    return render(request, 'admin/reports.html', {'total_earnings': total_earnings, 'total_billing': total_billing})

# Views for Facility Admin

# @login_required
def facility_admin_dashboard(request):
    return render(request, 'facility_admin/facility_dashboard.html')

# @login_required
def enroll_child(request):
    if request.method == 'POST':
        form = ChildForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Child enrolled successfully.')
            return redirect('ccm:enrolled_children_list')
    else:
        form = ChildForm()

    return render(request, 'facility_admin/enroll_child.html', {'form': form})

def enrolled_children_list(request):
    children = Child.objects.all()  # Query the database to get all enrolled children
    return render(request, 'facility_admin/enrolled_children_list.html', {'children': children})

def edit_child(request, child_id):
    child = get_object_or_404(Child, pk=child_id)
    if request.method == 'POST':
        form = ChildForm(request.POST, instance=child)
        if form.is_valid():
            form.save()
            return redirect('ccm:enrolled_children_list')
    else:
        form = ChildForm(instance=child)

    return render(request, 'facility_admin/edit_child.html', {'form': form, 'child': child})



def confirm_delete_child(request, child_id):
    child = get_object_or_404(Child, pk=child_id)

    if request.method == 'POST':
        child.delete()
        return redirect('ccm:enrolled_children_list')

    return render(request, 'facility_admin/confirm_delete_child.html', {'child': child})


def delete_child(request, child_id):
    child = get_object_or_404(Child, pk=child_id)

    if request.method == 'POST':
        # Redirect to the confirmation view
        return redirect('ccm:confirm_delete_child', child_id=child_id)

    return render(request, 'facility_admin/delete_child.html', {'child': child})



# @login_required
def staff_management(request):
    if request.method == 'POST':
        form = StaffForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Staff record updated successfully.')
            return redirect('ccm:facility_admin_dashboard')
    else:
        form = StaffForm()

    return render(request, 'facility_admin/staff_management.html', {'form': form})

def add_staff(request):
    if request.method == 'POST':
        form = StaffForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ccm:staff_management')
    else:
        form = StaffForm()

    return render(request, 'facility_admin/add_staff.html', {'form': form})

# Edit Staff
def edit_staff(request, staff_id):
    staff = get_object_or_404(Staff, pk=staff_id)
    if request.method == 'POST':
        form = StaffForm(request.POST, instance=staff)
        if form.is_valid():
            form.save()
            return redirect('ccm:staff_management')
    else:
        form = StaffForm(instance=staff)

    return render(request, 'facility_admin/edit_staff.html', {'form': form, 'staff': staff})

# Delete Staff
def delete_staff(request, staff_id):
    staff = get_object_or_404(Staff, pk=staff_id)
    staff.delete()
    return redirect('ccm:staff_management')


def view_staff(request):
    staff_list = Staff.objects.all()
    return render(request, 'facility_admin/view_staff.html', {'staff_list': staff_list})


# @login_required
def classroom_management(request):
    if request.method == 'POST':
        form = ClassroomForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Classroom capacity updated successfully.')
            return redirect('ccm:facility_admin_dashboard')
    else:
        form = ClassroomForm()

    return render(request, 'facility_admin/classroom_management.html', {'form': form})


# Add classroom view
def add_classroom(request):
    if request.method == 'POST':
        form = ClassroomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ccm:facility_admin_dashboard')
    else:
        form = ClassroomForm()

    return render(request, 'facility_admin/add_classroom.html', {'form': form})


# @login_required
def daily_attendance(request):
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():  # Corrected 'is valid' to 'is_valid'
            form.save()
            messages.success(request, 'Attendance recorded successfully.')
            return redirect('ccm:facility_admin_dashboard')
    else:
        form = AttendanceForm()

    return render(request, 'facility_admin/daily_attendance.html', {'form': form})

def view_classrooms(request):
    classrooms = Classroom.objects.all()
    return render(request, 'facility_admin/view_classrooms.html', {'classrooms': classrooms})

def edit_classroom(request, classroom_id):
    classroom = get_object_or_404(Classroom, pk=classroom_id)
    if request.method == 'POST':
        form = ClassroomForm(request.POST, instance=classroom)
        if form.is_valid():
            form.save()
            messages.success(request, 'Classroom updated successfully.')
            return redirect('ccm:view_classrooms')
    else:
        form = ClassroomForm(instance=classroom)

    return render(request, 'facility_admin/edit_classroom.html', {'form': form})

def delete_classroom(request, classroom_id):
    classroom = get_object_or_404(Classroom, pk=classroom_id)
    classroom.delete()
    messages.success(request, 'Classroom deleted successfully.')
    return redirect('ccm:view_classrooms')

# @login_required
def ledger(request):
    if request.method == 'POST':
        form = LedgerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Payment collected successfully.')
            return redirect('ccm:facility_admin_dashboard')
    else:
        form = LedgerForm()

    return render(request, 'facility_admin/ledger.html', {'form': form})

def daily_attendance(request):
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ccm:attendance_list')
    else:
        form = AttendanceForm()

    return render(request, 'acility_admin/attendance_form.html', {'form': form})

def attendance_form(request):
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            form.save()
            # You can add a success message here if needed
            return redirect('ccm:attendance_list')  # Redirect to the list of attendance records
    else:
        form = AttendanceForm()

    return render(request, 'facility_admin/attendance_form.html', {'form': form})

def attendance_list(request):
    attendance_records = Attendance.objects.all()
    return render(request, 'facility_admin/attendance_list.html', {'attendance_records': attendance_records})

def edit_attendance(request, attendance_id):
    # Retrieve the attendance record to be edited
    attendance_record = get_object_or_404(Attendance, pk=attendance_id)

    if request.method == 'POST':
        form = AttendanceForm(request.POST, instance=attendance_record)
        if form.is_valid():
            form.save()
            return redirect('attendance_list')
    else:
        form = AttendanceForm(instance=attendance_record)

    return render(request, 'attendance_edit.html', {'form': form, 'attendance_record': attendance_record})

def delete_attendance(request, attendance_id):
    # Retrieve the attendance record to be deleted
    attendance_record = get_object_or_404(Attendance, pk=attendance_id)

    if request.method == 'POST':
        attendance_record.delete()
        return redirect('attendance_list')

    return render(request, 'attendance_delete.html', {'attendance_record': attendance_record})




def list_ledger_entries(request):
    ledger_entries = Ledger.objects.all()  # Retrieve all ledger entries
    # Implement any filtering or searching logic if needed
    return render(request, 'facility_admin/ledger_list.html', {'ledger_entries': ledger_entries})



def add_ledger_entry(request):
    if request.method == 'POST':
        form = LedgerEntryForm(request.POST)
        if form.is_valid():
            form.save()  # Save the new ledger entry
            return redirect('list_ledger_entries')
    else:
        form = LedgerEntryForm()

    return render(request, 'facility_admin/ledger_form.html', {'form': form})



def edit_ledger_entry(request, entry_id):
    ledger_entry = get_object_or_404(Ledger, pk=entry_id)
    if request.method == 'POST':
        form = LedgerEntryForm(request.POST, instance=ledger_entry)
        if form.is_valid():
            form.save()  # Save the edited ledger entry
            return redirect('list_ledger_entries')
    else:
        form = LedgerEntryForm(instance=ledger_entry)

    return render(request, 'facility_admin/ledger_form.html', {'form': form})


def delete_ledger_entry(request, entry_id):
    ledger_entry = get_object_or_404(Ledger, pk=entry_id)
    if request.method == 'POST':
        ledger_entry.delete()  # Delete the ledger entry
        return redirect('list_ledger_entries')

    return render(request, 'facility_admin/ledger_confirm_delete.html', {'ledger_entry': ledger_entry})





def loginPage(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                messages.info(request, 'Incorrect Username or Password')
        context = {}
        return render(request, 'students/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')

def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account created for ' + user)
                return redirect('login')
        context = {'form': form}
        return render(request, 'students/register.html', context)


def list_weekly_tuition_charges(request):
    weekly_charges = WeeklyCharge.objects.all()
    # Implement any filtering or searching logic if needed
    return render(request, 'facility_admin/weekly_charge_list.html', {'weekly_charges': weekly_charges})


def add_weekly_tuition_charge(request):
    if request.method == 'POST':
        form = WeeklyChargeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_weekly_tuition_charges')
    else:
        form = WeeklyChargeForm()

    return render(request, 'facility_admin/weekly_charge_form.html', {'form': form})


def edit_weekly_tuition_charge(request, charge_id):
    weekly_charge = get_object_or_404(WeeklyCharge, pk=charge_id)
    if request.method == 'POST':
        form = WeeklyChargeForm(request.POST, instance=weekly_charge)
        if form.is_valid():
            form.save()
            return redirect('list_weekly_tuition_charges')
    else:
        form = WeeklyChargeForm(instance=weekly_charge)

    return render(request, 'facility_admin/weekly_charge_form.html', {'form': form})


def delete_weekly_tuition_charge(request, charge_id):
    weekly_charge = get_object_or_404(WeeklyCharge, pk=charge_id)
    if request.method == 'POST':
        weekly_charge.delete()
        return redirect('list_weekly_tuition_charges')

    return render(request, 'facility_admin/weekly_charge_confirm_delete.html', {'weekly_charge': weekly_charge})


from .models import Classroom, Staff, ClassroomAssignment

def assign_teachers():
    classrooms = Classroom.objects.all()


    for classroom in classrooms:
        teacher_capacity = {
            'Infant': (4, 8),
            'Toddler': 6,
            'Twaddler': 8,
            '3 Years Old': 9,
            '4 Years Old': 10,
        }

        # Get the number of enrolled children for the classroom
        enrolled_children = classroom.child_set.count()

        # Get the assigned teachers for the classroom
        classroom_assignments = ClassroomAssignment.objects.filter(classroom=classroom)

        if classroom.type in teacher_capacity:
            capacity = teacher_capacity[classroom.type]

            # Calculate the number of teachers needed based on enrollment
            if isinstance(capacity, tuple):
                min_teachers, max_teachers = capacity
                if enrolled_children <= min_teachers:
                    needed_teachers = 1
                else:
                    needed_teachers = 2
            else:
                needed_teachers = (enrolled_children + capacity - 1) // capacity

            # Check if there are enough assigned teachers
            assigned_teachers = classroom_assignments.count()
            if assigned_teachers < needed_teachers:
                # Assign additional teachers if needed
                unassigned_teachers = Staff.objects.exclude(id__in=classroom_assignments.values('teacher__id'))
                additional_teachers = unassigned_teachers[:needed_teachers - assigned_teachers]
                for teacher in additional_teachers:
                    ClassroomAssignment.objects.create(classroom=classroom, teacher=teacher)
            elif assigned_teachers > needed_teachers:
                # Remove excess teachers
                excess_teachers = classroom_assignments[:assigned_teachers - needed_teachers]
                for assignment in excess_teachers:
                    assignment.delete()

def list_teacher_assignments(request):
    teacher_assignments = ClassroomAssignment.objects.all()
    return render(request, 'facility_admin/teacher_assignments_list.html', {'teacher_assignments': teacher_assignments})




def register_teacher(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Associate the user with the Teacher model
            Teacher.objects.create(user=user, email=user.email)
            # Perform authentication and redirect
            # Customize this part as needed
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/teacher_register.html', {'form': form})


def view_weekly_attendance(request):
    # Get the logged-in teacher
    teacher = Teacher.objects.get(user=request.user)
    # Calculate the start and end dates for the current week
    today = datetime.now()
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)
    # Retrieve attendance records for the current week
    attendance_records = Attendance.objects.filter(
        teacher=teacher,
        date__gte=start_of_week,
        date__lte=end_of_week
    )
    return render(request, 'teacher/weekly_attendance.html', {'attendance_records': attendance_records})



def view_salary_and_hours_worked(request):
    # Get the logged-in teacher
    teacher = Teacher.objects.get(user=request.user)
    # Calculate the start and end dates for the current week
    today = datetime.now()
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)
    # Retrieve attendance records for the current week
    attendance_records = Attendance.objects.filter(
        teacher=teacher,
        date__gte=start_of_week,
        date__lte=end_of_week
    )
    # Calculate hours worked and salary based on your logic
    hours_worked = 0
    weekly_salary = 0  # Calculate salary based on rate and hours worked
    return render(request, 'teacher/salary_and_hours.html', {'hours_worked': hours_worked, 'weekly_salary': weekly_salary})


@login_required
def view_child_ledger(request):
    # Get the logged-in parent
    parent = Parent.objects.get(user=request.user)

    # Retrieve the children associated with the parent
    children = parent.child_set.all()

    # Initialize a dictionary to store ledger and related information
    child_ledger_data = {}

    # Fetch ledger and related information for each child
    for child in children:
        # Query ledger entries related to the child
        ledger_entries = Ledger.objects.filter(child=child)

        # You can add more data fetching logic here

        # Store the data for the child
        child_ledger_data[child] = {
            'ledger_entries': ledger_entries,
            # Add more data as needed
        }

    return render(request, 'parent/view_child_ledger.html', {'child_ledger_data': child_ledger_data})




# @login_required
def parent_view_child_attendance(request, child_id):
    child = get_object_or_404(Child, pk=child_id)
    # Retrieve child's attendance records
    attendance_records = Attendance.objects.filter(child=child)
    return render(request, 'parent/child_attendance.html', {'child': child, 'attendance_records': attendance_records})



# @login_required
def parent_view_child_ledger(request, child_id):
    child = get_object_or_404(Child, pk=child_id)
    # Retrieve child's ledger entries
    ledger_entries = Ledger.objects.filter(child=child)
    return render(request, 'parent/child_ledger.html', {'child': child, 'ledger_entries': ledger_entries})



def parent_request_withdrawal(request, child_id):
    child = get_object_or_404(Child, pk=child_id)

    if request.method == 'POST':
        form = WithdrawalRequestForm(request.POST, instance=child)
        if form.is_valid():
            withdrawal_reason = form.cleaned_data['withdrawal_reason']

            # Update the child's status to "Withdrawn" (you may have a status field in your Child model)
            child.status = 'Withdrawn'
            child.save()

            # Store the withdrawal reason
            child.withdrawal_reason = withdrawal_reason
            child.save()

            # Redirect to a success page or another appropriate URL
            return redirect('success_url_name')
    else:
        form = WithdrawalRequestForm()

    return render(request, 'parent/withdrawal_request.html', {'child': child, 'form': form})


from django import forms
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from .models import Parent

# Your ParentForm definition
class ParentForm(forms.Form):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

def add_parent(request):
    if request.method == 'POST':
        form = ParentForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']

            # Check if a user with the provided email already exists
            if User.objects.filter(username=email).exists():
                # An account with this email already exists; show an error message
                error_message = "An account with this email already exists."
                return render(request, 'facility_admin/add_parent.html', {'form': form, 'error_message': error_message})

            # Create a new user and parent instance
            user = User.objects.create_user(
                username=email,
                email=email,
                password=form.cleaned_data['password']
            )

            # Create a Parent instance associated with the User
            parent = Parent(
                user=user,
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                email=email
            )
            parent.save()

            return redirect('ccm:parent_list')
    else:
        form = ParentForm()
    return render(request, 'facility_admin/add_parent.html', {'form': form})



def parent_list(request):
    parents = Parent.objects.all()
    return render(request, 'facility_admin/parent_list.html', {'parents': parents})

def edit_parent(request, parent_id):
    parent = Parent.objects.get(pk=parent_id)
    
    if request.method == 'POST':
        form = ParentForm(request.POST)
        if form.is_valid():
            # Update the parent's information
            parent.first_name = form.cleaned_data['first_name']
            parent.last_name = form.cleaned_data['last_name']
            parent.email = form.cleaned_data['email']
            parent.save()
            return redirect('ccm:parent_list')
    else:
        # Populate the form with the existing parent information
        form = ParentForm(initial={
            'first_name': parent.first_name,
            'last_name': parent.last_name,
            'email': parent.email,
        })
    
    return render(request, 'facility_admin/edit_parent.html', {'form': form, 'parent': parent})


def delete_parent(request, parent_id):
    parent = Parent.objects.get(pk=parent_id)
    user = parent.user
    parent.delete()
    user.delete()
    return redirect('ccm:parent_list')


