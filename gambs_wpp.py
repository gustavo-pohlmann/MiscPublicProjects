# -*- coding: utf-8 -*-
"""
Created on Fri Apr 30 11:02:25 2021

@author: gustavo.gonzaga

Bot que abre links do Whatsapp API e, através do Whatsapp Desktop, envia
mensagens pré-escritas.

Deve funcionar em qualquer diretório propriamente organizado.
"""

import os
import sys
import inspect
import time

# Loads the webdriver modules
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pyautogui as gui
# Loading calculation and email sending functions
import pandas as pd

# Setting global variables and constants
LOGIN = os.getlogin()
CHROME = "C:/Users/" + LOGIN + "/Downloads/chromedriver.exe"
FOLDER_PATH = "C:/Users/"+LOGIN+"/Documents/MiscProjects"
WHATSAPP = "C:/Users/"+LOGIN+"/AppData/Local/WhatsApp/WhatsApp.exe"
FILE = inspect.getfile(inspect.currentframe()) # gets system file name
C_DIR = os.path.dirname(os.path.abspath(FILE)) # gets current stored directory
os.chdir(C_DIR) # set current directory as working directory

# check if files exists
if 'infos.csv' not in os.listdir() and 'auto_msg.txt' not in os.listdir():
    sys.exit('Arquivos de informação infos.csv e auto_msg.txt não encontrados')

# Open files with names and message
info = pd.read_csv('infos.csv')
msg = open('auto_msg.txt', encoding='UTF-8').read()

t0 = time.time()
# Open Whatsapp Web Desktop and the links in ChromeDriver
try:
    # Whatsapp
    os.startfile(r'C:\\Users\\'+LOGIN+r'\AppData\Local\WhatsApp\WhatsApp.exe')
    # Chrome
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    
    driver = webdriver.Chrome(executable_path=CHROME, options=options)

    # Set Loop    
    
    for i, r in info.iterrows(): # loops and creates message to be added
        # Edit message and link
        message = msg.format(**r.to_dict())
    
        text = 'https://api.whatsapp.com/send?phone=' + str(r.tel) + '&text='+\
                message
        
        # Open edited link and do key presses to send messages
        driver.get(text)
        wait = WebDriverWait(driver, 120)
        box = wait.until(EC.presence_of_element_located(
            (By.ID, 'action-button')))
        driver.find_element(By.ID, 'action-button').click()
        time.sleep(3)
        gui.press(['left','enter'])
        time.sleep(15)
        gui.press('enter')
        gui.keyDown('alt')
        gui.press('tab')
        gui.keyUp('alt')
    driver.quit()
except:
    print('deu ruim')
    sys.exit('deu bem ruim')
    driver.quit()

print(f'Total time elapsed: {(time.time() - t0)/60} min')
