from django.contrib import admin
from .models import Student, Subject, Score

# Register your models here.
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_no', 'name', 'department', 'gender')
    search_fields = ('student_no', 'name', 'department')


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'professor', 'class_time')
    search_fields = ('name', 'professor')


@admin.register(Score)
class ScoreAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'score')
    list_filter = ('subject',)