# Author: Dominik Pathuis
# Grade Calculator is provided student status and grades for
# homework, midterm exam, and final exam. A course letter grade
# is calculated and output
# January 30, 2024

student_status = input()
print(f'Enter status: {student_status}')
homework_points = float(input())
midterm_exam_score = float(input())
final_exam_score = float(input())

print(f'Enter HW: {int(homework_points)}')
print(f'Enter midterm: {int(midterm_exam_score)}')
print(f'Enter final exam: {int(final_exam_score)}\n')

hw_avg = (homework_points / 800) * 100
midterm_avg = (midterm_exam_score / 150) * 100
final_avg = (final_exam_score / 200) * 100


if hw_avg >= 100:
    hw_avg = 100
elif midterm_avg >= 100:
    midterm_avg = 100
elif final_avg >= 100:
    final_avg = 100

hm_wt = 0.35
mt_wt = 0.30
fi_wt = 0.35
if student_status == "G":
    hm_wt = 0.10
    mt_wt = 0.45
    fi_wt = 0.45
elif student_status == "OL":
    hm_wt = 0.25
    mt_wt = 0.25
    fi_wt = 0.50


avg = (hw_avg * hm_wt) + (midterm_avg * mt_wt) + (final_avg * fi_wt)

print(f'{student_status} average: {avg:.1f}%')


if avg >= 90:
    course_grade = 'A'
elif avg >= 80 and avg < 90:
    course_grade = 'B'
elif avg >= 70 and avg < 80:
    course_grade = 'C'
elif avg >= 60 and avg < 70:
    course_grade = 'D'
else:
    course_grade = 'F'

print(f'Course grade: {course_grade}')


