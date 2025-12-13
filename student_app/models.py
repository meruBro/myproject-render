from django.db import models

# Create your models here.
class Subject(models.Model):
    """수강 과목 정보"""
    name = models.CharField("과목명", max_length=50, unique=True)
    professor = models.CharField("담당 교수", max_length=50, blank=True)
    textbook = models.CharField("교재명", max_length=100, blank=True)
    class_time = models.CharField("수업 시간", max_length=50, blank=True)

    def __str__(self):
        return self.name


class Student(models.Model):
    """학생 기본 정보"""
    student_no = models.CharField("학번", max_length=20, unique=True)
    name = models.CharField("이름", max_length=20)
    department = models.CharField("학과", max_length=50)
    gender = models.CharField("성별", max_length=10)

    def __str__(self):
        return f"{self.student_no} {self.name}"


class Score(models.Model):
    """학생별 과목 성적"""
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="scores")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="scores")
    score = models.IntegerField("점수")

    class Meta:
        unique_together = ('student', 'subject')  # 한 학생-과목 조합당 1행

    def __str__(self):
        return f"{self.student} - {self.subject}: {self.score}"
