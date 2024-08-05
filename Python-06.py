#Function defination:in place of writing the same code repitedly we can use this (def):
def cal_sum(a, b):
    return a + b

sum  = cal_sum(1, 2)    #3
print(sum)

#
def print_hello():
    print("Hello")

print_hello()   
print_hello()
print_hello()

output = print_hello()
print(output)   #None

#Average of 3 numbers:

def calc_avg(a, b, c):
    sum = a + b + c
    avg = sum/3
    print(avg)

calc_avg(1, 2, 3) 

print(" ")

print("Apnacollege", end="  ")
print("shradhadidi")

#Functions in python:

#1 - Built-in Function:
#print( ),  len( ),  type( ),  range( )     -already in phython

#2 - User defined functions:                -which we made in python

def cal_prod(a, b=2):     #dusra case if b akela and a=2 then vo solve nhi hoga
    print(a * b)
    return a * b

cal_prod(1)              #python will multiply b by 1 

#WAP to print the length of a list( list is the parameter )

cities = ["delhi", "gurgoan", "noida", "mumbai", "chennai"]
heroes = ["thor", "ironman", "caption america", "black panther"]

def print_list(list):
    print(len(list))

print_list(cities)
print_list(heroes)

#WAP to print the elements of a list in a single line( list is the parameter )

cities = ["delhi", "gurgoan", "noida", "mumbai", "chennai"]
heroes = ["thor", "ironman", "caption america", "black panther"]

def print_list(list):
    for item in list:
        print(item, end=" ")

print_list(heroes)
print_list(cities)
print(" ")        

#WAP to find the factorial of n.( n is the parameter )

n = 6 
fact = 1
for i in range(1, n+1):
    fact *= i
print("Factorial :", fact)    

#but code it with the help of function:

def cal_fact(n):
    fact = 1 
    for i in range(1, n+1):
        fact *= i 
    print("Factorial :",fact)

cal_fact(6)

#WAP to convert USD to INR:

def converter(usd_val):
    inr_val = usd_val * 83
    print(usd_val, "USD =", inr_val, "INR")

converter(4)

#Recursive function:

def show(n):
    if(n == 0):
        return
    print(n)
    show(n-1)

show(6) 

#Recursion:
#returns n!

def fact(n):
    if(n == 1 or  n == 0):
        return 1
    return  fact(n-1) * n

print(fact(6))

#Write a recursive function to calculate the sum of first n natural numbers.

def cal_sum(n):
    if(n == 0):
        return 0
    return cal_sum(n - 1) + n

sum = cal_sum(6)
print("Sum :", sum)

#Write a recursive function to print all elements in a list:

def print_list(list, idx = 0):
    if(idx == len(list)):
        return
    print(list[idx])
    print_list(list, idx+1)

fruits = ["mango", "apple", "banana"]

print_list(fruits)