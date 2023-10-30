from django.urls import path
from . import views

app_name = 'ccm'

urlpatterns = [
    # URLs for System Administrator
    path('', views.home, name='home'),
    path('administration/', views.admin_dashboard, name='admin_dashboard'),
    path('administration/create-facility/', views.create_facility, name='create_facility'),
    path('administration/facilities/', views.view_facilities, name='view_facilities'),
    path('administration/facility/<int:facility_id>/', views.facility_details, name='facility_details'),
    path('administration/facility/edit/<int:facility_id>/', views.edit_facility, name='edit_facility'),
    path('administration/facility/delete/<int:facility_id>/', views.delete_facility, name='delete_facility'),
    path('administration/reports/', views.admin_reports, name='admin_reports'),

    # URLs for Facility Administrator
    
    path('facility-admin/', views.facility_admin_dashboard, name='facility_admin_dashboard'),
    path('facility-admin/enroll-child/', views.enroll_child, name='enroll_child' ),
    path('facility-admin/enrolled_children/', views.enrolled_children_list, name='enrolled_children_list'),
    path('facility-admin/enrolled_children/<int:child_id>/edit/', views.edit_child, name='edit_child'),
    path('facility-admin/enrolled_children/<int:child_id>/delete/', views.delete_child, name='delete_child'),
    path('facility-admin/enrolled_children/<int:child_id>/confirm-delete/', views.confirm_delete_child, name='confirm_delete_child'),
    path('facility-admin/add-parent/', views.add_parent, name='add_parent'),
    path('facility-admin/parent-list/', views.parent_list, name='parent_list'),
    path('facility-admin/delete-parent/<int:parent_id>/', views.delete_parent, name='delete_parent'),
    path('facility-admin/edit-parent/<int:parent_id>/', views.edit_parent, name='edit_parent'),

    
    path('facility-admin/staff-management/', views.staff_management, name='staff_management'),
    path('facility-admin/add-staff/', views.add_staff, name='add_staff'),
    path('facility-admin/edit-staff/<int:staff_id>/', views.edit_staff, name='edit_staff'),
    path('facility-admin/delete-staff/<int:staff_id>/', views.delete_staff, name='delete_staff'),
    path('facility-admin/view-staff/', views.view_staff, name='view_staff'),
    path('facility-admin/classroom-management/', views.classroom_management, name='classroom_management'),
    path('facility-admin/classroom/add/', views.add_classroom, name='add_classroom'),
    path('facility-admin/view-classrooms/', views.view_classrooms, name='view_classrooms'),
    path('facility-admin/edit-classroom/<int:classroom_id>/', views.edit_classroom, name='edit_classroom'),
    path('facility-admin/delete-classroom/<int:classroom_id>/', views.delete_classroom, name='delete_classroom'),
    path('facility-admin/attendance/add/', views.attendance_form, name='attendance_form'),
    path('facility-admin/attendance/', views.attendance_list, name='attendance_list'),
    path('facility-admin/daily-attendance/', views.daily_attendance, name='daily_attendance'),
    path('facility-admin/edit/<int:attendance_id>/', views.edit_attendance, name='edit_attendance'),
    path('facility-admin/delete/<int:attendance_id>/', views.delete_attendance, name='delete_attendance'),
    path('facility-admin/ledger/', views.ledger, name='ledger'),
    path('facility_admin/ledger/list/', views.list_ledger_entries, name='list_ledger_entries'),
    path('facility_admin/ledger/add/', views.add_ledger_entry, name='ledger_add'),
    path('facility_admin/ledger/edit/<int:entry_id>/', views.edit_ledger_entry, name='ledger_edit'),
    path('facility_admin/ledger/delete/<int:entry_id>/', views.delete_ledger_entry, name='ledger_delete'),
    path('facility_admin/weekly-charges/', views.list_weekly_tuition_charges, name='list_weekly_tuition_charges'),
    path('facility_admin/weekly-charges/add/', views.add_weekly_tuition_charge, name='add_weekly_tuition_charge'),
    path('facility_admin/weekly-charges/edit/<int:charge_id>/', views.edit_weekly_tuition_charge, name='edit_weekly_tuition_charge'),


    path('facility_admin/weekly-charges/delete/<int:charge_id>/', views.delete_weekly_tuition_charge, name='delete_weekly_tuition_charge'),
    path('teacher/teacher_assignments/', views.list_teacher_assignments, name='list_teacher_assignments'),
    path('teacher/view-child-ledger/', views.view_child_ledger, name='view_child_ledger'),
    path('parent/<int:child_id>/request_withdrawal/', views.parent_request_withdrawal, name='parent_request_withdrawal'),

    # Add more URLs for Facility Administrator functionality

    # Other URLs
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
]

