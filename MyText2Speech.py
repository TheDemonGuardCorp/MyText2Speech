# ================================================================================================
# ------------------------------------------------------------------------------------------------
# Created : 2025/04/25
# ------------------------------------------------------------------------------------------------
# ================================================================================================
#
# ================================================================================================
# Tested Environment/Setup :
# ------------------------------------------------------------------------------------------------
# How to setup :
# python -m venv .venv
# pip install -r requirements.txt
# ------------------------------------------------------------------------------------------------
# Basic Environment :
#
# Windows 11 Pro 23H2
# Python 3.13.3 (3.13.3 (tags/v3.13.3:6280bb5, Apr  8 2025, 14:47:33) [MSC v.1943 64 bit (AMD64)])
# ------------------------------------------------------------------------------------------------
# 3rd Modules :
#
# pip install pyttsx3
# pip install ttkbootstrap
# pip freeze > requirements.txt
#
# Package      Version
# ------------ -------
# comtypes     1.4.10
# pillow       10.4.0
# pip          25.0.1
# pypiwin32    223
# pyttsx3      2.98
# pywin32      310
# ttkbootstrap 1.12.2
# ------------------------------------------------------------------------------------------------
# NOTE :
# 1)
# pyttsx3
# 1-1) Linux installation requirements :
# If you are on a linux system and if the voice output is not working , then :
#
# Install espeak , ffmpeg and libespeak1 as shown below:
#
# sudo apt update && sudo apt install espeak ffmpeg libespeak1
#
# 1-1) Mac installation requirements :
# If you face error related to "pyobjc" when running the `init()` method :
# Install 9.0.1 version of pyobjc : "pip install pyobjc>=9.0.1"
#
# ------------------------------------------------------------------------------------------------
# ================================================================================================

import tkinter as tk
from tkinter import filedialog as fd
from tkinter import messagebox as mb

from tkinter import ttk
import ttkbootstrap as ttkb          # pip install ttkbootstrap
from ttkbootstrap.constants import * # pip install ttkbootstrap

import os
import sys

from datetime import datetime
import time

import pathlib
from pathlib import Path

import traceback

import pyttsx3 # pip install pyttsx3
# Linux installation requirements :
# If you are on a linux system and if the voice output is not working , then :
#
# Install espeak , ffmpeg and libespeak1 as shown below:
#
# sudo apt update && sudo apt install espeak ffmpeg libespeak1

class MyText2Speech(ttkb.Window):
    def __init__(self):
        super().__init__()
        self.title("Text2Speech")
        self.resizable(False, False)
        # self.columnconfigure(0, weight=1)
        # # self.columnconfigure(1, weight=1)
        # self.rowconfigure(0, weight=1)
        # self.rowconfigure(1, weight=1)
        # self.rowconfigure(2, weight=1)

        self.VERSION_MAJOR           = "1"
        self.VERSION_MINOR           = "0"
        self.VERSION_PATCH           = "0"
        self.VERSION                 = f'{self.VERSION_MAJOR}.{self.VERSION_MINOR}.{self.VERSION_PATCH}'
        self.INIT_TEXT_VOICE:str     = "Enter your voice HERE"
        self.MIN_RATE:int            = 60
        self.MAX_RATE:int            = 300
        self.MIN_VOLUME:float        = 0.0
        self.MAX_VOLUME:float        = 1.0
        self.INIT_FILE_SAVE_PATH:str = os.getcwd()
        self.PYTHON_VERSION:str      = f'{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro} ({sys.version_info.releaselevel})'# sys.version
        self.TKINTER_VERSION:str     = tk.TkVersion
        # print(sys.version_info)
        # sys.version_info(major=3, minor=11, micro=3, releaselevel='final', serial=0)

        self.ENGINE:pyttsx3.Engine = pyttsx3.init() # Object creation
        self.INIT_RATE:int         = self.ENGINE.getProperty('rate')
        self.INIT_VOICE:str        = self.ENGINE.getProperty('voice')
        self.INIT_VOLUME:float     = self.ENGINE.getProperty('volume')
        self.INIT_VOICES:list      = self.ENGINE.getProperty('voices')
        self.INIT_VOICE_NAME:str   = None

        _, self.INIT_VOICE_NAME = self.getVoiceNameFromVoiceID(self.INIT_VOICE, self.INIT_VOICES)
        _, self.INIT_VOICE_NAMES = self.getVoiceNames(self.INIT_VOICES)

        self.textVoice:str    = tk.StringVar(value=self.INIT_TEXT_VOICE)
        self.rate:int         = tk.IntVar(value=self.INIT_RATE)
        self.voice:str        = tk.StringVar(value=self.INIT_VOICE)
        self.voiceID:str      = tk.StringVar(value=self.INIT_VOICE)
        self.volume:float     = tk.DoubleVar(value=self.INIT_VOLUME)
        self.voiceName:str    = tk.StringVar(value=self.INIT_VOICE_NAME)
        self.fileSavePath:str = tk.StringVar(value=self.INIT_FILE_SAVE_PATH)

        print(f'Initial speaking rate       : {self.INIT_RATE}')
        print(f'Initial speaking voice      : {self.INIT_VOICE}')
        print(f'Initial speaking volume     : {self.INIT_VOLUME}')
        print(f'Initial speaking voice name : {self.INIT_VOICE_NAME}')
        print(f'Initial speaking text voice : {self.INIT_TEXT_VOICE}')

        print(f'MIN_RATE            : {self.MIN_RATE}')
        print(f'MAX_RATE            : {self.MAX_RATE}')
        print(f'MIN_VOLUME          : {self.MIN_VOLUME}')
        print(f'MAX_VOLUME          : {self.MAX_VOLUME}')
        print(f'INIT_FILE_SAVE_PATH : {self.INIT_FILE_SAVE_PATH}')
        print(f'PYTHON_VERSION      : {self.PYTHON_VERSION}')
        print(f'TKINTER_VERSION     : {self.TKINTER_VERSION}')

        # self.update()
        self.menuBar()
        self.basicControlForm()
        # self.advancedControlInfoForm()
        self.advancedControlForm()
        # self.statusBar()

        self.update()
        self.resetAllValues()

    def menuBar(self) -> bool:
        status:bool = False

        try:
            # Menubar
            self.menubar = tk.Menu(master=self)
            self.configure(menu=self.menubar)

            # File Menu
            self.fileMenu = tk.Menu(master=self.menubar, tearoff=False)

            self.savetMenu  = tk.Menu(master=self.fileMenu, tearoff=False)
            self.savetMenu.add_command(label="Save2MP3File", command=self.s2f, accelerator="Ctrl+S")
            self.bind("<Control-s>", self.s2f)
            self.savetMenu.add_command(label="Save2MP3File As ...", command=self.save2MP3FileSaveAs, accelerator="Ctrl+Shift+S")
            self.bind("<Control-Shift-S>", self.save2MP3FileSaveAs)
            self.savetMenu.add_command(label="Set Save Directory ...", command=self.updateFileSavePath, accelerator="Ctrl+D")
            self.bind("<Control-d>", self.updateFileSavePath)
            # self.eachResetMenu.add_command(label="Reset Voice", command=self.resetVoiceName)
            self.fileMenu.add_cascade(label="Save ...", menu=self.savetMenu)

            # self.fileMenu.add_command(label="Save2MP3File", command=self.s2f)
            self.fileMenu.add_separator()

            self.fileMenu.add_command(label="Exit", command=self.quitApp, accelerator="Ctrl+Q")
            self.bind("<Control-q>", self.quitApp)

            self.menubar.add_cascade(label="File", menu=self.fileMenu)

            # Reset Menu
            self.resetMenu = tk.Menu(master=self.menubar, tearoff=False)
            self.resetMenu.add_command(label="Reset All", command=self.resetAllValues, accelerator="Ctrl+R")
            self.bind("<Control-r>", self.resetAllValues)
            self.resetMenu.add_separator()

            # self.resetMenu.add_command(label="Reset ...", command=self.quit)
            self.eachResetMenu  = tk.Menu(master=self.resetMenu, tearoff=False)
            self.eachResetMenu.add_command(label="Reset Text", command=self.resetTextVoice)
            self.eachResetMenu.add_command(label="Reset Rate", command=self.resetRate)
            self.eachResetMenu.add_command(label="Reset Voice", command=self.resetVoice)
            self.eachResetMenu.add_command(label="Reset Volume", command=self.resetVolume)
            self.eachResetMenu.add_command(label="Reset Save Directory", command=self.resetDirectory)
            # self.eachResetMenu.add_command(label="Reset Voice", command=self.resetVoiceName)
            self.resetMenu.add_cascade(label="Reset ...", menu=self.eachResetMenu)

            self.menubar.add_cascade(label="Reset", menu=self.resetMenu)

            # Help Menu
            self.helpMenu = tk.Menu(master=self.menubar, tearoff=False)
            self.helpMenu.add_command(label="About", command=self.showAboutDialog)
            self.menubar.add_cascade(label="Help", menu=self.helpMenu)

        except Exception as e:
            status = False
            traceback.print_exc()
            tracebackStr:str = traceback.format_exc()
            print(tracebackStr)
        else:
            status = True

        return status

    def basicControlForm(self) -> bool:
        status:bool = False

        try:
            self.basicControlFormFrame = ttkb.Frame(master=self)
            self.basicControlFormFrame.grid(row=0, column=0, sticky="nsew")

            self.textBox = ttkb.Entry(master=self.basicControlFormFrame, textvariable=self.textVoice) # , text="Enter your voice HERE"
            self.textBox.grid(row=0, column=0, sticky="nsew", rowspan=2)
            self.textBox.bind("<Return>", self.t2s)

            self.speakButton = ttkb.Button(master=self.basicControlFormFrame, text="Speak", command=self.t2s)
            self.speakButton.grid(row=0, column=1, sticky="ew")

            self.save2MP3File = ttkb.Button(master=self.basicControlFormFrame, text="Save2MP3File", command=self.s2f)
            self.save2MP3File.grid(row=1, column=1, sticky="ew")

        except Exception as e:
            status = False
            traceback.print_exc()
            tracebackStr:str = traceback.format_exc()
            print(tracebackStr)
        else:
            status = True

        return status

    def advancedControlForm(self) -> bool:
        status:bool = False

        try:
            self.advancedControlFormFrame = ttkb.Frame(master=self, borderwidth=5, relief=tk.RAISED)
            self.advancedControlFormFrame.grid(row=2, column=0, sticky="nsew")

            self.advancedControlRateFormFrame = ttkb.Frame(master=self.advancedControlFormFrame, borderwidth=5, relief=tk.RAISED)
            self.advancedControlRateFormFrame.grid(row=0, column=0, sticky="nsew")
            self.labelRate   = ttkb.Label(master=self.advancedControlRateFormFrame, text="Rate (WPM:Words Per Minute)   : ")
            self.labelRate.grid(row=0, column=0, sticky="nsew")
            # self.sliderRate = ttkb.Scale(self.advancedControlRateFormFrame, from_=self.MIN_RATE, to=self.MAX_RATE, variable=self.rate)
            self.sliderRate = ttk.LabeledScale(self.advancedControlRateFormFrame, from_=self.MIN_RATE, to=self.MAX_RATE, variable=self.rate)
            self.sliderRate.grid(row=0, column=1, sticky="nsew")
            # self.sliderRate.label.update()
            self.progressbarRate = ttkb.Progressbar(master=self.advancedControlRateFormFrame, variable=self.rate, maximum=self.MAX_RATE, value=self.rate.get())
            self.progressbarRate.grid(row=1, column=0, columnspan=2, sticky="nsew")

            self.advancedControlVoiceFormFrame = ttkb.Frame(master=self.advancedControlFormFrame, borderwidth=5, relief=tk.RAISED)
            self.advancedControlVoiceFormFrame.grid(row=1, column=0, sticky="nsew")
            self.labelVoice  = ttkb.Label(master=self.advancedControlVoiceFormFrame, text="Voice  : ")
            self.labelVoice.grid(row=0, column=0, sticky="nsew")
            self.comboVoice = ttkb.Combobox(master=self.advancedControlVoiceFormFrame, values=self.INIT_VOICE_NAMES, textvariable=self.voiceName, state="readonly")
            self.comboVoice.grid(row=0, column=1, sticky="nsew")
            # self.comboVoice.bind("<<ComboboxSelected>>", self.updateVoiceName)

            self.advancedControlVolumeFormFrame = ttkb.Frame(master=self.advancedControlFormFrame, borderwidth=5, relief=tk.RAISED)
            self.advancedControlVolumeFormFrame.grid(row=2, column=0, sticky="nsew")
            self.labelVolume = ttkb.Label(master=self.advancedControlVolumeFormFrame, text="Volume : ")
            self.labelVolume.grid(row=0, column=0, sticky="nsew")
            # self.sliderVolume = ttkb.Scale(self.advancedControlVolumeFormFrame, from_=self.MIN_VOLUME, to=self.MAX_VOLUME, variable=self.volume)
            self.sliderVolume = ttk.LabeledScale(self.advancedControlVolumeFormFrame, from_=self.MIN_VOLUME, to=self.MAX_VOLUME, variable=self.volume)
            self.sliderVolume.grid(row=0, column=1, sticky="nsew")
            self.progressbarVolume = ttkb.Progressbar(master=self.advancedControlVolumeFormFrame, variable=self.volume, maximum=self.MAX_VOLUME, value=self.volume.get())
            self.progressbarVolume.grid(row=1, column=0, columnspan=2, sticky="nsew")

            # self.labelRate
            # self.speakButton = ttkb.Button(master=self.controlFormFrame, text="Speak", command=self.t2s)
            # self.speakButton.grid(row=0, column=0, sticky="ew")

        except Exception as e:
            status = False
            traceback.print_exc()
            tracebackStr:str = traceback.format_exc()
            print(tracebackStr)
        else:
            status = True

        return status

    def statusBar(self) -> bool:
        status:bool = False

        try:
            self.statusBarFrame = ttkb.Frame(master=self, borderwidth=5, relief=tk.RAISED)
            self.statusBarFrame.grid(row=2, column=0, sticky="nsew")

            self.status_label = tk.Label(master=self.statusBarFrame, text="Ready", bd=1, relief=tk.SUNKEN, anchor=tk.W)
            self.status_label.grid(side=tk.BOTTOM, fill=tk.X)

        except Exception as e:
            status = False
            traceback.print_exc()
            tracebackStr:str = traceback.format_exc()
            print(tracebackStr)
        else:
            status = True

        return status

    def quitApp(self, event:tk.Event=None) -> bool:
        status:bool = False

        try:
            print("Exit")
            self.destroy()
            self.quit()

        except Exception as e:
            status = False
            traceback.print_exc()
            tracebackStr:str = traceback.format_exc()
            print(tracebackStr)
        else:
            status = True

        return status        

    def resetTextVoice(self, event:tk.Event=None) -> bool:
        status:bool = False

        try:
            # self.textVoice.set(self.INIT_TEXT_VOICE)
            self.after_idle(self.textVoice.set, self.INIT_TEXT_VOICE)
            # time.sleep(1)

        except Exception as e:
            status = False
            traceback.print_exc()
            tracebackStr:str = traceback.format_exc()
            print(tracebackStr)
        else:
            status = True

        return status

    def resetRate(self, event:tk.Event=None) -> bool:
        status:bool = False

        try:
            # self.rate.set(self.INIT_RATE)
            self.after_idle(self.rate.set, self.INIT_RATE)
            # time.sleep(1)

        except Exception as e:
            status = False
            traceback.print_exc()
            tracebackStr:str = traceback.format_exc()
            print(tracebackStr)
        else:
            status = True

        return status

    def resetVoice(self, event:tk.Event=None) -> bool:
        status:bool = False

        try:
            # self.voice.set(self.INIT_VOICE)
            self.after_idle(self.voice.set, self.INIT_VOICE)
            _, voiceName = self.getVoiceNameFromVoiceID(self.INIT_VOICE, self.INIT_VOICES)
            # self.voiceName.set(voiceName)
            self.after_idle(self.voiceName.set, voiceName)
            # time.sleep(1)

        except Exception as e:
            status = False
            traceback.print_exc()
            tracebackStr:str = traceback.format_exc()
            print(tracebackStr)
        else:
            status = True

        return status

    def resetVolume(self, event:tk.Event=None) -> bool:
        status:bool = False

        try:
            # self.volume.set(self.INIT_VOLUME)
            self.after_idle(self.volume.set, self.INIT_VOLUME)
            # time.sleep(1)

        except Exception as e:
            status = False
            traceback.print_exc()
            tracebackStr:str = traceback.format_exc()
            print(tracebackStr)
        else:
            status = True

        return status

    def resetDirectory(self, event:tk.Event=None) -> bool:
        status:bool = False

        try:
            # self.fileSavePath.set(self.INIT_FILE_SAVE_PATH)
            self.after_idle(self.fileSavePath.set, self.INIT_FILE_SAVE_PATH)
            # time.sleep(1)

        except Exception as e:
            status = False
            traceback.print_exc()
            tracebackStr:str = traceback.format_exc()
            print(tracebackStr)
        else:
            status = True

        return status

    def resetAllValues(self, event:tk.Event=None) -> bool:
        status:bool = False

        try:
            self.resetTextVoice()
            self.resetRate()
            self.resetVoice()
            self.resetVolume()
            self.resetDirectory()
            # self.resetVoiceName()

        except Exception as e:
            status = False
            traceback.print_exc()
            tracebackStr:str = traceback.format_exc()
            print(tracebackStr)
        else:
            status = True

        return status

    def getVoiceNameFromVoiceID(self, voiceID:str, voices:list) -> tuple[bool, str]:
        status:bool = False
        voiceName:str = None

        try:
            for voice in voices:
                if voiceID == voice.id:
                    voiceName  = voice.name
                    break

        except Exception as e:
            status = False
            traceback.print_exc()
            tracebackStr:str = traceback.format_exc()
            print(tracebackStr)
        else:
            status = True

        return status, voiceName

    def getVoiceIDFromVoiceName(self, voiceName:str, voices:list) -> tuple[bool, str]:
        status:bool = False
        voiceID:str = None

        try:
            for voice in voices:
                if voiceName == voice.name:
                    voiceID  = voice.id
                    break

        except Exception as e:
            status = False
            traceback.print_exc()
            tracebackStr:str = traceback.format_exc()
            print(tracebackStr)
        else:
            status = True

        return status, voiceID

    def getVoiceNames(self, voices:list) -> tuple[bool, list]:
        status:bool = False
        voiceNames:list = []

        try:
            for voice in voices:
                voiceNames.append(voice.name)

        except Exception as e:
            status = False
            traceback.print_exc()
            tracebackStr:str = traceback.format_exc()
            print(tracebackStr)
        else:
            status = True

        return status, voiceNames

    def updatePyttsx3Properties(self) -> bool:
        status:bool = False

        try:
            _, tmpVoiceID = self.getVoiceIDFromVoiceName(self.voiceName.get(), self.INIT_VOICES)
            print(tmpVoiceID)
            print(self.voiceName.get())
            self.voice.set(tmpVoiceID)
            self.voiceID.set(tmpVoiceID)

            self.ENGINE.setProperty('rate', self.rate.get())
            self.ENGINE.setProperty('voice', self.voice.get())
            self.ENGINE.setProperty('volume', self.volume.get())
            print(f'Update speaking rate   : {self.rate.get()}')
            print(f'Update speaking voice  : {self.voice.get()}')
            print(f'Update speaking volume : {self.volume.get()}')

            tmprate   = self.ENGINE.getProperty('rate')
            tmpvoice  = self.ENGINE.getProperty('voice')
            tmpvolume = self.ENGINE.getProperty('volume')
            print(f'Check speaking rate   : {tmprate}')
            print(f'Check speaking voice  : {tmpvoice}')
            print(f'Check speaking volume : {tmpvolume}')

        except Exception as e:
            status = False
            traceback.print_exc()
            tracebackStr:str = traceback.format_exc()
            print(tracebackStr)
        else:
            status = True

        return status

    # def updateFileSavePath(self, originalFileSavePath:str) -> tuple[bool, str]:
    def updateFileSavePath(self, event:tk.Event=None) -> bool:
        status:bool = False
        fileSavePath:str = self.fileSavePath.get()

        try:
            my_filetypes = [('all files', '.*'), ('mp3 files', '.mp3')]
            tmpPath:str = fd.askdirectory(parent=self, initialdir=fileSavePath, title="Please select a directory:", mustexist=True)

            if len(tmpPath) > 0:
                self.fileSavePath.set(tmpPath)
            # name= fd.askopenfilename()
            print(f'tmpPath : {tmpPath} ({len(tmpPath)})')
            print(f'fileSavePath : {fileSavePath} ({len(fileSavePath)})')
        except Exception as e:
            status = False
            traceback.print_exc()
            tracebackStr:str = traceback.format_exc()
            print(tracebackStr)
        else:
            status = True

        return status

    def save2MP3FileSaveAs(self, event:tk.Event=None) -> bool:
        status:bool = False
        fileSavePath:str = self.fileSavePath.get()

        try:
            _, defaultFileName = self.generateFileName()
            my_filetypes = [('MP3', '.mp3'), ('All Files', '*.*')]
            tmpPath:str = fd.asksaveasfilename(parent=self, filetypes=my_filetypes, initialdir=fileSavePath, title="Please select a directory:", defaultextension=".mp3", initialfile=defaultFileName)

            if len(tmpPath) > 0:
                self.speech2file(tmpPath)
            #     self.fileSavePath.set(tmpPath)
            # name= fd.askopenfilename()
            print(f'save2MP3FileSaveAs tmpPath : {tmpPath} ({len(tmpPath)})')
            # print(f'fileSavePath : {fileSavePath} ({len(fileSavePath)})')
        except Exception as e:
            status = False
            traceback.print_exc()
            tracebackStr:str = traceback.format_exc()
            print(tracebackStr)
        else:
            status = True

        return status

    def speech2file(self, fileName:str) -> bool:
        status:bool = False

        try:
            self.updatePyttsx3Properties()
            tmp_textVoice = self.textVoice.get()
            print(f'Current speaking text: {tmp_textVoice}')

            # Save to a file
            # Saving speech to an audio file
            self.ENGINE.save_to_file(f'{tmp_textVoice}', f'{fileName}')
            self.ENGINE.runAndWait()

            # Stop the engine
            self.ENGINE.stop()

        except Exception as e:
            status = False
            traceback.print_exc()
            tracebackStr:str = traceback.format_exc()
            print(tracebackStr)
        else:
            status = True

        return status

    def fill2Left(self, msg:str, filler:str) -> tuple[bool, str]:
        status:bool = False
        fillerMsg:str = None

        try:
            # Pad string to the left using a variable
            fillerMsg = f"{msg:{filler}>2}"
            print(fillerMsg)
        except Exception as e:
            status = False
            traceback.print_exc()
            tracebackStr:str = traceback.format_exc()
            print(tracebackStr)
        else:
            status = True

        return status, fillerMsg

    def generateFileName(self) -> tuple[bool, str]:
            status:bool = False
            fileName:str = None

            try:
                now:str = str(datetime.now())
                tmpDateTime:datetime = datetime.fromisoformat(now)
                _, month  = self.fill2Left(tmpDateTime.month, '0')
                _, day    = self.fill2Left(tmpDateTime.day, '0')
                _, hour   = self.fill2Left(tmpDateTime.hour, '0')
                _, minute = self.fill2Left(tmpDateTime.minute, '0')
                _, second = self.fill2Left(tmpDateTime.second, '0')
                fileName:str = f'{tmpDateTime.year}{month}{day}_{hour}{minute}{second}.mp3'
                # tmpFileName:str = f'{tmpDateTime.year}{tmpDateTime.month}{tmpDateTime.day}_{tmpDateTime.hour}{tmpDateTime.minute}{tmpDateTime.second}.mp3'
                print(tmpDateTime.year)
                print(tmpDateTime.month)
                print(tmpDateTime.day)
                print(tmpDateTime.hour)
                print(tmpDateTime.minute)
                print(tmpDateTime.second)
                print(fileName)
                print(now)
            except Exception as e:
                status = False
                traceback.print_exc()
                tracebackStr:str = traceback.format_exc()
                print(tracebackStr)
            else:
                status = True

            return status, fileName

    def t2s(self, event:tk.Event=None) -> bool:
        status:bool = False

        try:
            self.updatePyttsx3Properties()
            tmp_textVoice = self.textVoice.get()
            print(f'Current speaking text: {tmp_textVoice}')

            # Make the engine speak
            # Adding text to be spoken
            self.ENGINE.say(f'{tmp_textVoice}')
            self.ENGINE.runAndWait()

            # Stop the engine
            self.ENGINE.stop()
            # time.sleep(5)

        except Exception as e:
            status = False
            traceback.print_exc()
            tracebackStr:str = traceback.format_exc()
            print(tracebackStr)
        else:
            status = True

        return status

    def s2f(self, event:tk.Event=None) -> bool:
        status:bool = False

        try:
            self.updatePyttsx3Properties()
            tmp_textVoice = self.textVoice.get()
            print(f'Current speaking text: {tmp_textVoice}')

            _, tmpFileName = self.generateFileName()
            fileSavePathFileName:str = pathlib.Path(f'{self.fileSavePath.get()}/{tmpFileName}')
            print(fileSavePathFileName)
            self.speech2file(fileSavePathFileName)

        except Exception as e:
            status = False
            traceback.print_exc()
            tracebackStr:str = traceback.format_exc()
            print(tracebackStr)
        else:
            status = True

        return status

    def showAboutDialog(self, event:tk.Event=None):
        mb.showinfo("About", f"Created : 2025/04/25\nVersion : {self.VERSION}\nPython Version : {self.PYTHON_VERSION}\nTKinter Version : {self.TKINTER_VERSION}")

def main():
    print("Hello World!!")
    app = MyText2Speech()
    app.mainloop()

if __name__ == "__main__":
    main()
