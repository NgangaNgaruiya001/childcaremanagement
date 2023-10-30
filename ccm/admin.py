from django.contrib import admin
from .models import Facility, Child, Staff, Classroom, Ledger, Attendance, Parent
@admin.register(Facility)
class FacilityAdmin(admin.ModelAdmin):
    list_display = ['name', 'address', 'phone_number', 'license_number']

# @admin.register(Child,)
# class ChildAdmin(admin.ModelAdmin):
#     list_display = ['first_name', 'last_name', 'dob', 'allergies', 'parent', 'facility']
#     list_filter = ['facility']
#     search_fields = ['first_name', 'last_name']

@admin.register(Child)
class ChildAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'dob', 'allergies', 'facility', 'parent_info']

    # Define a method to display parent information
    def parent_info(self, obj):
        # Access the related parent information
        parents = obj.parents.all()  # Use "parents" to get all related parents

        if parents:
            return ', '.join([f"{parent.first_name} {parent.last_name}" for parent in parents])
        else:
            return "No Parent"

    parent_info.short_description = 'Parent Information'  # Set the column header name

    list_filter = ['facility']
    search_fields = ['first_name', 'last_name']



@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
    list_display = ['user', 'child_count']  # You can customize this list display as needed
    search_fields = ['user__username', 'user__email']  # Add other fields you want to search by
    actions = ['delete_selected_parents']  # This adds an action to delete selected parents
    
    def child_count(self, obj):
        return obj.child_set.count()  # Display the number of children associated with each parent
    
    child_count.short_description = 'Number of Children'  # Set a user-friendly name for the child_count column

    # Define a custom action to delete selected parents
    def delete_selected_parents(self, request, queryset):
        for parent in queryset:
            parent.user.delete()  # This deletes the parent's User instance
        self.message_user(request, "Selected parents and their associated children have been deleted.")

# Register other models as needed



@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'dob', 'address', 'phone_number', 'hourly_salary', 'facility']
    list_filter = ['facility']
    search_fields = ['first_name', 'last_name']

@admin.register(Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    list_display = ['type', 'capacity', 'facility']
    list_filter = ['facility']
    search_fields = ['type']

@admin.register(Ledger)
class LedgerAdmin(admin.ModelAdmin):
    list_display = ['child', 'tuition_fee', 'weekly_charge', 'balance', 'last_payment_date']
    list_filter = ['child']
    search_fields = ['child__first_name', 'child__last_name']

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['child', 'classroom', 'date', 'signed_in', 'signed_out']
    list_filter = ['classroom', 'child']
    search_fields = ['child__first_name', 'child__last_name']

# You can customize the admin panel for other models as needed.