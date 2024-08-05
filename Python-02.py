str1 = "Hello this is me Hapsi.But my actuall name is also Hapsi."       #One line print.
print(str1)
print("")

str2 = "Hello this is me Hapsi.\nBut my actuall name is also Hapsi."     #Two line print ( using \n without space )
print(str2)
print("")

str3 ="Hello this is me Hapsi.\tBut my actuall name is also Hapsi."      #to keep some space between those two sentences( using \t )  didnt work??
print(str3)
print("")

#Concatenation and length:

str4 = "Hello"
str5 = "World"
final_str = str4 + " " + str5
print( final_str )
print(len(str4), len(str5))

#Indexing:

str6 = "Hello World"
ch = str6[0]      
ch1 = str6[1]     
ch2 = str6[2]     
print(ch)
print(ch1)
print(ch2)     #Space walle jagah ko koi fill nhi kr sakta.

#Slicing:

print(str6[0:4])   #Hell
print(str6[1:4])   #ell
print(str6[:4])    #means[0:4] i.e Hell
print(str6[5:11])          #eq - 1
print(str6[5:len(str6)])   #eq - 2
#Both eq1 & eq2 will have the same result.

#          A   P   P   L   E
#         -5  -4  -3  -2  -1
str7 = "APPLE"
print(str7[-5:-2])  #APP

#String Functions:
str8 = "i am studying python from apna college"

#1 - str.endswith("word")
print(str8.endswith("ege"))                         #True
print(str8.endswith("qrp"))                         #False

#2 - str.capitalize()
print(str8.capitalize())      #String me agr first letter small hua to ye code output me capital kar dega.

#3 - str.replace( "old" , "new" )
print(str8.replace( "o" , "a" ))     #'O' will be replaced by 'a', or we can replace a whole word also.

#4 - str.find( "word" )
print(str8.find("o"))        #'O' find karke uska location number batayega, or we can find for a whole word also.

#5 - str.count( "word" )
print(str8.count( "am" ))    #1 ( number of times 'am' is used in the string ).
print(" ")

#Conditional statements:
#( if-elif-else )

age = 21
if(age >= 18):
    print("You can vote & apply for license")
elif(age <= 18):
    print("You are not eligible.")

#Self    

#a = float(input("Enter your marks :"))
a = 88.9

if(a >= 90):
    print("You got A")
elif( 90 > a >= 80):
    print("You got B")
else:
    print("FAILED")
print(" ")    

#Nesting( KIND OFF BY PARTS):
age = 55
if(age >= 18):
    if(age >= 70):
        print("Cannot drive")
    else:
        print("Can drive")
print(" ")        

#WAP to check if the number is even or odd   

#num = int(input("Enter your number :"))
num = 98
if(num%2 ==0 ):
    print("It's an even number.")
else:
    print("It's an odd number.")
print(" ")    

#WAP to find the greatest integer:
a=9
b=6
c=8
if( a>=b and a>=c ):
    print("Greatest integer : 9")
elif( b>=a and b>=c ):
    print("Greatest integer : 6")
elif( c>=a and c>=b ):
    print("Greatest integer : 8")
print(" ")

#WAP to check if the number is divisible by 7:
num1 = 49
if(num1%7 == 0):
    print("Yes it is divisible by 7")
else:
    print("Written number is not divisible by 7")