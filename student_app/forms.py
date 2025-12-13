from django import forms
from .models import Student, Subject


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['student_no', 'name', 'department', 'gender']


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'professor', 'textbook', 'class_time']