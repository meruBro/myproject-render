from django.urls import path
from . import views

app_name = 'student_app'

urlpatterns = [
    # 메인 화면: 학생 목록 (UI-1)
    path('', views.student_list, name='student_list'),

    # 학생 상세 + 성적 (UI-2)
    path('students/<int:student_id>/', views.student_detail, name='student_detail'),

    # 학생정보 관리
    path('students/create/', views.student_create, name='student_create'),
    path('students/<int:student_id>/edit/', views.student_update, name='student_update'),
    path('students/<int:student_id>/delete/', views.student_delete, name='student_delete'),

    # 수강과목 관리 (UI-3)
    path('subjects/', views.subject_list, name='subject_list'),
    path('subjects/<int:subject_id>/', views.subject_detail, name='subject_detail'),
    path('subjects/<int:subject_id>/edit/', views.subject_update, name='subject_update'),
    path('subjects/<int:subject_id>/delete/', views.subject_delete, name='subject_delete'),
]