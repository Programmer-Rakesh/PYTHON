#Reading a file:
f = open('demo.txt', 'r')

data = f.read()
print(data)
print(type(data))

f.close()

#WAP to print selective words from the txt file:
f = open("demo.txt", "r")

data = f.read(5)
print(data)

f.close()

#WAP to print the first line of txt file:
f = open("demo.txt", "r")

line1 = f.readline()
print(line1)

f.close

#WAP to add text in text file:
f = open("demo.txt", "a")

f.write("\nAnd my experience was very nice.")

f.close()

#WAP to replace the text in txt file:
f = open("demo.txt", "w")

f.write("I want to learn JavaScript tomorrow.")

f.close()

#WAP to create a new file using "a" or "w":
f = open("Sample.txt", "a")
f.close()

#WAP to overwrite in the txt file:
f = open("demo.txt", "r+")
f.write("abc")
print(f.read())
f.close

#WAP to erase verything from the txt file ( Truncate ):
f = open("demo.txt", "w+")
print(f.read())                    #txt file will get erased
f.write("OK")                      #txt file will get a new text: OK
f.close