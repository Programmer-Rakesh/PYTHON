info = {
    "Name" : "Rakesh Roy",
    "Subject" : ["Python", "C", "Java"],
    "Topic" : ("dict", "set"),
    "Age" : 19,
    "Is_adult" : True,
    12.99 : 94.4
}
print(info)    

#or if we want to change the name:
info["Name"] = "Hapsi"
print(info)

#we can print a null dictionary also:
null_dict = {}
print(null_dict)

#Nested dictionary:
Student = {
    "Name" : "Rakesh",
    "Subjects" :{
        "Physics" : 88,
        "Maths" : 98,
        "Chemistry" : 87,
    }
}
print(Student)      #or we can particularly print my subject:
print(Student["Subjects"])      #or we can particularly print one of my subject:
print(Student["Subjects"]["Maths"])
print(" ")

#Dictionary methods:

#dict_keys:
print(Student.keys())     #or we can print it in  form of list:
print(list(Student.keys()))

#dict_values:
print(list(Student.values()))

#dict_items:
print(list(Student.items()))

#dict_get(" "):
print(Student.get("Name"))

#dict_update
new_dict = {"City" : "Noida"}
Student.update(new_dict)
print(Student)
print(" ")

#Sets in python:
collection = {1, 2, 4, 2, 7}
print(collection)
print(type(collection))
print(len(collection))

collection1 = set()    #empty set
print(collection1)
print(type(collection1))
print(" ")

#Sets methods:
#1 - set.add( el ):
collection1.add( 1 )
collection1.add( 2 )
collection1.add( 3 )
collection1.add( 4 )
print(collection1)

#2 - set.remove( el ):
collection1.remove( 2 )
print(collection1)

#3 - set.pop():
collection1.pop()
print(collection1)

#4 - set.clear()
collection1.clear()
print(collection1)

print(" ")

set1 = {1, 2, 3}
set2 = {2, 3, 4}
#5 - set.union( set ):
print(set1.union(set2))               #new set = set1 + set2

#6 - set.intersection( set ):
print(set1.intersection(set2))        #new set with common elements.
print(" ")

#WAP to print yr question's ans in a set:
marks = {}

x = int(input("maths : "))
marks.update({"maths" : x })

Y = int(input("physics : "))
marks.update({"physics" : Y})

Z = int(input("chemistry : "))
marks.update({"chemistry" : Z })

print(marks)
print(" ")

#WAP to store both 9 & 9.0 as separate values in a set:
value = {9, "9.0"}
print(value)

#WAP tp store both 9 & 9.0 as separate values in a dic or tuples:
values = {
    ("int", 9),
    ("float", 9.0),
}
print(values)