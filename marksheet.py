print('MARKSHEET:')
name=input('NAME:')
father_name=input('FATHER NAME:')
Class=input('class:')
courses=input('NUMBER OF COURSES:')
courses=int(courses)
obtained_marks=0
for a in range(1,courses+1):
    a=str(a)
    marks=input('MARKS OF ' +a+ ' courses:')
    marks=int(marks)
    obtained_marks+=marks
percentage=(obtained_marks/(courses*100))*100
print('NAME:',name)
print('FATHER NAME:',father_name)
print('CLASS:',Class)
print('OBTAINED MARKS:',obtained_marks)
print('TOTAL MARKS:',courses*30)
print('PERCENTAGE:',percentage,'%')
if percentage>=80:
    grade='A+'
elif percentage>=70:
    grade='A'
elif percentage>=60:
    grade='B'
elif percentage>=50:
    grade='C'
else:
    grade='FAIL'
print('GRADE:',grade)
if percentage>=80:
    remarks='MARVILLOUS:'
elif percentage>=70:
    remarks='EXCELLENT:'
elif percentage>=60:
    remarks='GOOD:'
elif percentage>=50:
    remarks='FAIR:'
else: 
    remarks='KEEP IT UP:'
print('REMARKS:',remarks)
if percentage>=40:
    result='PASS:'
else:
    result='FAIL:'
print('RESULT:',result)