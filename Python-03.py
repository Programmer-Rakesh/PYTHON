marks = [88.9, 77.8, 56.4, 73.5, 76.8]
print(marks)                                  #list
print(type(marks))                            #list
print(len(marks))                             #5
print(marks[0])                               #88.9
print(marks[3])                               #73.5
print(" ")

student = ["Rakesh", 89.7, 19, "Delhi"]
print(student)
student[0] = "Hapsi"                          #Replacing
print(student)                                #New list

#List slicing:
marks = [88.9, 77.8, 56.4, 73.5, 76.8]
print(marks[1:4])                             #poistive index starts from 0 (from left)
print(marks[-4:-2])                           #negative index starts from -1 (from right)

#List methods:
list = [3,5,8,4]

#1:-
list.append(9)                               #For adding an element at the end.
print(list)
print(" ")

#2:-
list.sort()                                  #Ascending order.
print(list)
print(" ")

#3:-
list.sort( reverse=True)                     #Descending order.
print(list)
print(" ")

#4:-
list.reverse()                               #Reverse.
print(list)
print(" ")

#5:-
list.insert( 5, 1 )                          #Inserting element at index.
print(list)
print(" ")

#6:-
list1 = [2, 3, 1, 5, 1]                      #To remove the first occurance of selected number.
list1.remove(1)
print(list1)
print(" ")

#7:-
list1.pop(3)                                 #To remove element from index.
print(list1)
print(" ")

#Tuples in python
tup = (68, 87, 68, 56, 45)                        #it can be filled wiht words also ( with strings )
print(tup)
print(type(tup))                              #tuples
print(tup[2])                                 #68

#tuples method:

#1:-
print(tup.index(68))                          #to find the first occurance of the mentioned number.

#2:-
print(tup.count(68))                          #to count how many times it exist in the tuples.
print(" ")

#WAP

movies = []
mov1 = input("Enter your first movie : ")
mov2 = input("Enter your second movie : ")
mov3 = input("Enter your third movie : ")

movies.append(mov1)
movies.append(mov2)
movies.append(mov3)

print(movies)

#or

movies = []
mov1 = input("Enter your first movie : ")
movies.append(mov1)
mov2 = input("Enter your second movie : ")
movies.append(mov2)
mov3 = input("Enter your third movie : ")
movies.append(mov3)

print(movies)
print(" ")

#WAP to check if the list contains a palindrom of element.
#if the default list is same as of the list after copying and reversed then that list can be said as palindrom.

list1 = [1, 2, 1]
list2 = [1, 2, 3]

list1_copy = list1.copy()
list1_copy.reverse()

if(list1_copy == list1):
    print("Plindrom")

else:
    print("Not a palindrom")
print(" ")    

#WAP to count number of times "A" from the list:

grade  = ["A", "B", "C", "A", "E", "A"]
print(grade.count("A"))
print(" ")

#WAP to store the above values in a list and sort then from "A" to "B"
grade.sort()
print(grade)