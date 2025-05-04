# MyText2Speech
Simple text to speech app

================================================================================================
------------------------------------------------------------------------------------------------
Created : 2025/04/25
------------------------------------------------------------------------------------------------
================================================================================================

================================================================================================
Tested Environment/Setup :
------------------------------------------------------------------------------------------------
How to setup :
python -m venv .venv
pip install -r requirements.txt
------------------------------------------------------------------------------------------------
Basic Environment :

Windows 11 Pro 23H2
Python 3.13.3 (3.13.3 (tags/v3.13.3:6280bb5, Apr  8 2025, 14:47:33) [MSC v.1943 64 bit (AMD64)])
------------------------------------------------------------------------------------------------
3rd Modules :

pip install pyttsx3
pip install ttkbootstrap
pip freeze > requirements.txt

Package      Version
------------ -------
comtypes     1.4.10
pillow       10.4.0
pip          25.0.1
pypiwin32    223
pyttsx3      2.98
pywin32      310
ttkbootstrap 1.12.2
------------------------------------------------------------------------------------------------
NOTE :
1)
pyttsx3
1-1) Linux installation requirements :
If you are on a linux system and if the voice output is not working , then :

Install espeak , ffmpeg and libespeak1 as shown below:

sudo apt update && sudo apt install espeak ffmpeg libespeak1

1-1) Mac installation requirements :
If you face error related to "pyobjc" when running the `init()` method :
Install 9.0.1 version of pyobjc : "pip install pyobjc>=9.0.1"

------------------------------------------------------------------------------------------------
================================================================================================
