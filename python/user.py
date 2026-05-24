username=input("enter a name")
if len(username)>12:
    print("name cannot be more than 12 charcater")
elif not username.find(" ")==-1:
    print("your useer name v=cantt note conain space")
elif not  username.isalpha():
    print("you user name cannot cannot conatian digit")
    
else:
    print(f"welcome{username}")