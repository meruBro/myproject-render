from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Avg
from .models import Student, Subject, Score
from .forms import StudentForm, SubjectForm

# Create your views here.
def sidebar_students():
    return Student.objects.all().order_by('student_no')

def calc_grade(score):
    if score is None:
        return "-"
    if score >= 80:
        return "A"
    elif score >= 60:
        return "B"
    return "C"
    
def student_list(request):
    students = sidebar_students()
    return render(request, 'student_app/student_list.html', {'students': students})



def student_detail(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    students = sidebar_students()
    subjects = Subject.objects.all().order_by('name')

    # 1) "선택" 클릭 여부: ?show=1 이면 성적표 보이기
    show_scores = (request.GET.get('show') == '1')

    # 2) POST면 성적 저장 처리 (성적표 화면에서 수정)
    if request.method == 'POST':
        for subj in subjects:
            val = request.POST.get(f"score_{subj.id}")
            if val not in (None, ''):
                try:
                    Score.objects.update_or_create(
                        student=student,
                        subject=subj,
                        defaults={'score': int(val)}
                    )
                except ValueError:
                    pass
        # 저장 후 성적표가 보이도록 show=1로 리다이렉트
        return redirect(f"/students/{student.id}/?show=1")

    # 3) 이 학생의 점수 dict
    score_dict = {
        s.subject_id: s.score
        for s in Score.objects.filter(student=student)
    }

    # 4) (선택) 과목평균이 필요하면 유지
    subject_avg_map = {
        item['subject_id']: item['avg_score']
        for item in Score.objects.values('subject_id').annotate(avg_score=Avg('score'))
    }

    # 5) 성적표 행 데이터
    rows = []
    for subj in subjects:
        student_score = score_dict.get(subj.id)
        rows.append({
            'subject': subj,
            'student_score': student_score,
            'avg_score': subject_avg_map.get(subj.id),
            'grade': calc_grade(student_score),
        })

    return render(request, 'student_app/student_detail.html', {
        'students': students,
        'student': student,
        'show_scores': show_scores,
        'rows': rows,
    })

def student_create(request):
    students = sidebar_students()
    subjects = Subject.objects.all().order_by('name')

    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save()
            for subj in subjects:
                val = request.POST.get(f"score_{subj.id}")
                if val not in (None, ''):
                    try:
                        Score.objects.update_or_create(
                            student=student, subject=subj,
                            defaults={'score': int(val)}
                        )
                    except ValueError:
                        pass
            return redirect('student_app:student_detail', student_id=student.id)
    else:
        form = StudentForm()

    score_rows = [{'subject': subj, 'value': ''} for subj in subjects]

    return render(request, 'student_app/student_form.html', {
        'students': students,
        'form': form,
        'score_rows': score_rows,
    })


def student_update(request, student_id):
    students = sidebar_students()
    student = get_object_or_404(Student, id=student_id)
    subjects = Subject.objects.all().order_by('name')

    existing = {s.subject_id: s.score for s in Score.objects.filter(student=student)}

    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            student = form.save()
            for subj in subjects:
                val = request.POST.get(f"score_{subj.id}")
                if val not in (None, ''):
                    try:
                        Score.objects.update_or_create(
                            student=student, subject=subj,
                            defaults={'score': int(val)}
                        )
                    except ValueError:
                        pass
            return redirect('student_app:student_detail', student_id=student.id)
    else:
        form = StudentForm(instance=student)

    score_rows = [{'subject': subj, 'value': existing.get(subj.id, '')} for subj in subjects]

    return render(request, 'student_app/student_form.html', {
        'students': students,
        'form': form,
        'student': student,
        'score_rows': score_rows,
    })

def student_delete(request, student_id):
    students = sidebar_students()
    student = get_object_or_404(Student, id=student_id)

    if request.method == 'POST':
        student.delete()  # Score는 FK(CASCADE)라 함께 삭제됨
        return redirect('student_app:student_list')

    return render(request, 'student_app/student_confirm_delete.html', {
        'students': students,
        'student': student,
    })

def subject_list(request):
    students = sidebar_students()
    subjects = Subject.objects.all().order_by('name')

    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('student_app:subject_list')
    else:
        form = SubjectForm()

    return render(request, 'student_app/subject_list.html', {
        'students': students,
        'subjects': subjects,
        'form': form,
    })

def subject_detail(request, subject_id):
    students = sidebar_students()
    subject = get_object_or_404(Subject, id=subject_id)
    return render(request, 'student_app/subject_detail.html', {
        'students': students,
        'subject': subject,
    })

def subject_delete(request, subject_id):
    students = sidebar_students()
    subject = get_object_or_404(Subject, id=subject_id)

    if request.method == 'POST':
        subject.delete()
        return redirect('student_app:subject_list')

    return render(request, 'student_app/subject_confirm_delete.html', {
        'students': students,
        'subject': subject,
    })

def subject_update(request, subject_id):
    students = sidebar_students()
    subject = get_object_or_404(Subject, id=subject_id)

    if request.method == 'POST':
        form = SubjectForm(request.POST, instance=subject)
        if form.is_valid():
            form.save()
            return redirect('student_app:subject_detail', subject_id=subject.id)
    else:
        form = SubjectForm(instance=subject)

    return render(request, 'student_app/subject_form.html', {
        'students': students,
        'form': form,
        'subject': subject,
    })
