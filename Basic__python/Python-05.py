#Loops
count = 1                       #shuru 1 se ho rha hai.
while count <= 5 :              #khtm smaller than equal to 5 me ho rha hai.
    print(count)
    count += 1            
print("Loop ended")

#for reverse:
count = 5                        #shuru 5 se ho rha hai.
while count >= 1:                #khtm greater than equal to 1 me ho rha hai.
    print(count)
    count -= 1
print("Loop ended")

#WAP to print numbers from 1 to 100:
i = 1
while i <= 100:
    print(i)
    i += 1    
print("Loop ended")

#WAP to print numbers from 100 to 1:
a = 100
while a >= 1:
    print(a)
    a -= 1
print("Loop ended")   

#WAP to print multiplication table of 2:
b = 1
while b <= 10:
    print(2*b)
    b += 1
print("Table ended")  

#WAP to print elements of following list using a loop:
nums = [1, 3, 5, 33, 44, 55, 66, 77, 88, 99,]
index = 0
while index < len(nums):
    print(nums[index])
    index += 1
print("Program ended")    

#WAP to search for a number X in this tuple using loop:
num = (1, 3, 5, 6, 7, 8, 9)
X = 6
i = 0
while i < len(num):
    if(num[i] == X):
       print("Found at indx :", i )
    else:
        print("Finding...")
    i += 1
print(" ")    

#break & continue:

#1 - break:
num2 = (1, 3, 5, 6, 7, 8, 9, 10, 11)
X = 8
i = 0
while i < len(num2):
    if(num[i] == X):
       print("Found at indx :", i )
       break
    else:
        print("Finding...")
    i += 1
print("End of Loop.") 

#2 - continue:
p = 0
while p <= 5:
    if(p == 2):
        p += 1
        continue          #'2' skip ho jayega.
    print(p)
    p += 1

print(" ")    

#another example:
i = 1000

while i <= 2000:
    if(i%2 != 0):      #even numbers.
        i += 1
        continue
    print(i)
    i += 1

print(" ")

#Loops in python:
#1 - For loops:
nums = [1, 2, 3, 4, 5, 6]

for val in nums:
    print(val)

#2 - for loops with else:
str = ("Apna college")

for chr in str:
    print(chr)
else:
    print("End")

#WAP to print following elements in a loop:

nums = [1, 2, 3, 4, 5, 6]

for el in nums:
    print(el)

#WAP  to search for a number x in this tuple:
num1 = (1, 2, 3, 4, 5, 3, 6, 7)
x = 3

idx = 0
for el in num1:
    if(el == x ):
        print("Number found at index", idx)
    idx += 1

#now using break in the same question:
num3 = (1, 2, 3, 4, 5, 3, 6, 7)
x = 3

idx = 0
for el in num3:
    if ( el == x):
        print("Number found at index", idx)
        break
    idx += 1

print(" ")    

#Range:

print(range(5))

#or print the range in index:

seq = range(5)
print(seq[0])
print(seq[1])
print(seq[2])
print(seq[3])
print(seq[4])

print(" ")
#Or:

seq = range(5)

for i in seq:
    print(i)

print(" ")
#Or:

for i in range(5):           #( start )
    print(i)

print(" ")
#( start, stop, step)

for i in range(2, 10):       #( start, stop )
    print(i)

print(" ")

for i in range(2, 10, 2):    #( start, stop, step )
    print(i)

print(" ")    

#WAP to print a table:

n = int(input("Enter your number : "))

for i in range(1, 11):
    print(n * i)

print(" ")    

#Pass statement:

for i in range(5):
    pass                     #for pending works.

print(" ")

#WAP to find the sum of numbers ranging( 1, 5 ):

n = 5

sum = 0
for i in range(1, n+1):
    sum += i

print(" sum :", sum)

#WAP to finf factorail of first n numbers:

n = 5
fact = 1
i = 1
while i <= n:
    fact *= i
    i += 1

print("Factorial =", fact) 
#or:

n = 5
fact1 = 1

for i in range(1, n+1):
    fact1 *= i

print("Factorial =", fact1)    