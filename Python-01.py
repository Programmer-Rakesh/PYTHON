name = "hapsi"
age = 19
male = True

print("My name is", name)
print("My age is", age)

#Type:

print(type(name))
print(type(age))
print(type(male))

a = 43
b = 2
sum = a + b
print(sum)
 
#for remaider:
print( a % b)

#( for = we code == and for not equal to we code !=)
#Relation/Comparison operators:

print(a <= b) #False
print(a >= b) #True
print(a == b) #False
print(a != b) #True
print(a > b) #True
print(a < b) #False

#Assignment operators:

#1 - Addition
num = 5
num = num + 10     #eq 1
print(num)
#OR
num = 5
num += 10
print(num)         #eq 2

#Ans will be same for both( if we are using eq 1 & 2 )

#2 - Substraction
num2 = 5
num2 -= 2
print(num2)

#3 -  Multipication
num3 = 10
num3 *= 5
print(num3)

#4 - Division
num4 = 50
num4 /= 10
print(num4)

#5 - Remainder
num5 = 23
num5 %= 2
print(num5)

#6 - Power
num6 = 10
num6 **= 5
print(num6)

#Logical operators:
print(not False)
print(not True)
#example
a = 50 
b = 30
print(not (b > a))  #True
print(not (a > b))  #False

#And, Or operator:

val1 = True
val2 = True
print("and operator :", val1 and val2)  #True
print("or operator :", val1 or val2)

val1 = True
val2 = False
print("and operator :", val1 and val2)  #False
print("or operator :", val1 or val2)    #Priority( True > False )

#Example:
a = 50 
b = 30
print("or operator :", (a == b) or (a >= b))  #True

#Type conversion:
#methode - 1
a = 5
b = 8.5

print( a + b )

#methode - 2
a = int("5")   #( type casting kiya hai )
b = 8.5
print(type(a))
print( a + b )   #so conclusion - both are giving same reslts but can be written in two diff methods.

#int to str
a = 8.99
a = str(a)
print(type(a))

#Input:

name = input("enter your name :")
print("Welcome", name )
print(type(name) , name)

#Converting a string into int or float:
#1 - To int
int("5")
val1 = int(input("Enter your age :"))       #Format
print(type(val1), val1)

#2 - To float
float("5.5")
val2 = float(input("Enter your chest size :"))
print(type(val2), val2)

#Area( Rectangle ):
val1 = 4
val2 = 8
print("area :" , val1 * val2)

#Average:
a = float(input("Enter your first number :"))
b = float(input("Enter your second number :"))

print("Average :" , ( a + b )/2 )