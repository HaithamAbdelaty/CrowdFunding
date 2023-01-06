import re
import datetime
from datetime import datetime
import calendar
from typing import Tuple, Union
import uuid


#----------------------------------------------------------
#needed functions to validate the project inputs 
#validate Email
#email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

def checkst(msg):
    val=input(msg)
    if val.isdigit() or val.isspace() or not val:
        print("enter a valid string")
        return checkst(msg)
    else:
        return val

def checkint(msg):
    val=input(msg)
    if val.isdigit():
        return int(val)
    else:
        print("enter a valid number ")
        return checkint(msg)

from curses.ascii import isdigit, isspace
import mailbox
import re
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
def checkmail(msg):
    val=input(msg)
    if(re.fullmatch(regex, val)):
        return val
 
    else:
        print("enter valid email ")
        return checkmail(msg)

def checvkpass(msg):
    val=input(msg)
    if val.isspace() or not val  :
        print("enter valid password ")
        return checkpass
    else:
        return val

def checkpass(msg,password):
    confirm=input(msg)
    if confirm.isspace() or not confirm :
        print("please enter valid password ")
        return checkpass(msg)
        
    else:
        if confirm != password :
            print("password does not match ")
            return checkpass(msg)
        else :
            return confirm
    
def checkmobile(msg):
    val=input(msg)
    sp=val[0:3]
    ll=['011','010','012','015']
    if val.isdigit():
        if (len(val) != 11) or (sp not in ll ):
            print("please enter valid phone number ")
            return checkmobile(msg)
        else:
            return val
    else:
        print("please enter valid digits")
        return checkmobile(msg)

def checkdetails(msg):
    val=input(msg)
    if not val :
        print("enter valid detail ")
        return checkdetails(msg)
    else:
        return val

import datetime


def checkdate(msg):
    inputDate = input(msg)
    if inputDate.isspace() or not inputDate:
        print("please enter valid string ")
        return checkdate(msg)
    else:    
        day, month, year = inputDate.split('/')
        isValidDate = True
        try:
            datetime.datetime(int(year), int(month), int(day))
        except ValueError:
            isValidDate = False

        if(isValidDate):
            return inputDate
        else:
            return checkdate(msg)


#--------------------------------------------- project functions-------------------------

def create_project(id):
    f=open("projects.txt","a")
    title=checkst(" enter title of your project ")
    details=input(" enter project details ")
    total=input(" enter your total target ")
    start_date=checkdate("enter start date in format 'dd/mm/yy' : ")
    end_date=checkdate("enter end date in format 'dd/mm/yy' : ")
    user_id=id
    projects_data=f"{user_id}:{title}:{details}:{total}:{start_date}:{end_date}"
    print(" project created successfully ")
    f.write( projects_data)
    f.close()
    


def project_file(id):
    try:
        fileobject=open("projects.txt","a")
    except Exception as e :
        print(e)
        return False
    else:
        p=create_project(id)
        fileobject.write(p+"\n")
        return True

def listAll_projects():
    try:
        fileobject=open("projects.txt", "r")
    except Exception as e:
        print(e)
        return False
    else:
        projects= fileobject.readlines()
        return(projects)




def search_project_byID(id):
    allprojects=listAll_projects()
    for project in allprojects:
        project_details=project.split(":")
        if project_details[0]==id:
            project_index=allprojects.index(project)
            return project_index
    else:
        return False

def delete_project(id):
    project_index=search_project_byID(id)
    allprojects=listAll_projects()
    del allprojects[project_index]
    deleted=write_projects_on_file(allprojects)
    if deleted:
        print("project deleted successfully")
    print(allprojects)

def write_projects_on_file(projects):
    try:
        fileobject=open("projects.txt", "w")
    except Exception as e:
        print(e)
        return False
    else:
        fileobject.writelines(projects)
        return True


def edit_project(id):
    project_index=search_project_byID(id)
    allprojects=listAll_projects()
    if project_index and project_index == 0:
        project_data=create_project(id)
        print(project_data)
        updated_data=f"{id}:{project_data[0]}:{project_data[1]}:{project_data[2]}:{project_data[3]}:{project_data[4]}"
        allprojects[project_index]=updated_data
        update=write_projects_on_file(allprojects)
        return update
#-----------------------------------------------------------------------------------
#----------------------login functions--------------------
def log_in():
    email=checkmail("enter your email: ") 
    password=checvkpass("Ente your password ")
    userID=f"{email}:{password}" 
    fileobject=open("users.txt","r")
    allusers=fileobject.readlines()
    for user in allusers:
        user_detail = user.split(":")
        if (user_detail[4] == email) and (user_detail[3] ==password) :
            print("login successfully")
            return user_detail[0]
        project_menu(userID)
    else:
        print("Invalid credentials !")       
        
#------------------------regestration functions ----------------
def create_user(user):
    try:
        fileobject=open("users.txt","a")
    except Exception as e :
        print(e)
        return False
    else:
        fileobject.write(user+"\n")
        return True

def registeration():
    print("============== welcome to register page =================\n")
    fname=checkst("please enter your first name ")
    lname=checkst("please enter your last name ")
    email=checkmail("please enter your email ")
    password=checvkpass("please enter your password ")
    confirm_pass=checkpass("please retype password ",password)
    mobile=checkmobile("please enter your mobile phone ")
    userID=str(uuid.uuid4())

    return f"{userID}:{fname}:{lname}:{password}:{email}:{mobile}"

def user_details():
    user_data=registeration()
    if create_user(user_data):
        print("user created ")
        return True
    else:
        print("Error, Something went wrong !")
        return False



#----------------------------project menu------------------------

def project_menu(userID):
    while True:
        choice=input("""
        1) create project
        2) list projects
        3) edit project
        4) delete project 
        
        """)
        if choice in ['1','2','3','4']:
            if choice == '1':
                create_project(userID)
            elif choice == '2':
                print(listAll_projects())
            elif choice == '3':
                edit_project(userID)
            elif choice =='4':
                delete_project(userID)
        else: 
            print("Invalid choice, please try again")
    done

#---------------------------------main menu -------------------------------------
def Core_menu():
    choice=input("""
    1) login 
    2) register,if you don't have account 
    """)

    if choice in ['1','2']:
        if choice == '1':
            log_in()
        else:            
            if user_details():
                log_in()
    else:
        print("Error, please Enter valid choice !")
        return Core_menu()

Core_menu()

