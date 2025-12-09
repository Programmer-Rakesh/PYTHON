

# greatest and smallest among three numbers using if statement

# we have to input marks of 6 subject. Calculate percentage based on percentage above 90 % A+, between 80 to 90 A, between 70 to 80 B, 60 to 70 d, below 60 = fail.


a = int(input("Enter subject 1 :"))
b = int(input("Enter subject 2 :"))
c = int(input("Enter subject 3 :"))
d = int(input("Enter subject 4 :"))
e = int(input("Enter subject 5 :"))
f = int(input("Enter subject 6 :"))

total_marks = a+b+c+d+e+f
percentage = (total_marks / ( 6 * 100)) * 100

if percentage > 90:
        grade = "A+"
elif percentage >=80:
        qqqqgrade = "A"
elif percentage >=70:
        grade = "B"
elif percentage >= 60:
        grade = "D"
else:
        grade = "Fail"
        print("Total marks :", total_marks)
        print("Percentage :", percentage)
        print("Grade :", grade)