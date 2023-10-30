# ccm/forms.py
from django import forms
from .models import Facility, Child, Staff, Classroom, Ledger, Attendance, WeeklyCharge

class FacilityForm(forms.ModelForm):
    class Meta:
        model = Facility
        fields = '__all__'  # Include all fields from the Facility model

class FacilityEditForm(forms.ModelForm):
    class Meta:
        model = Facility
        fields = ['name', 'address', 'phone_number', 'license_number']


class ChildForm(forms.ModelForm):
    class Meta:
        model = Child
        fields = ['first_name', 'last_name', 'dob', 'allergies', 'parents', 'facility']


    # Add a classroom field for selecting the classroom
    classroom = forms.ModelChoiceField(
        queryset=Classroom.objects.all(),  # Provide a queryset of available classrooms
        empty_label="Select a Classroom",  # Optional: Display a default label
    )



    def __init__(self, *args, **kwargs):
        super(ChildForm, self).__init__(*args, **kwargs)

class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ['first_name', 'last_name', 'dob', 'address', 'phone_number', 'hourly_salary', 'facility']

    def __init__(self, *args, **kwargs):
        super(StaffForm, self).__init__(*args, **kwargs)
        # Populate the 'facility' field with facility names
        self.fields['facility'].queryset = Facility.objects.all()

class ClassroomForm(forms.ModelForm):
    class Meta:
        model = Classroom
        fields = '__all__'

class LedgerForm(forms.ModelForm):
    class Meta:
        model = Ledger
        fields = '__all__'

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = '__all__'

class LedgerEntryForm(forms.ModelForm):
    class Meta:
        model = Ledger
        fields = ['child', 'tuition_fee', 'weekly_charge', 'balance', 'last_payment_date']

class WeeklyChargeForm(forms.ModelForm):
    class Meta:
        model = WeeklyCharge
        fields = '__all__'


class WithdrawalRequestForm(forms.ModelForm):
    withdrawal_reason = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Reason for withdrawal'}),
        required=True
    )

    class Meta:
        model = Child
        fields = []  # Add any fields you need here



from django import forms

class ParentForm(forms.Form):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
