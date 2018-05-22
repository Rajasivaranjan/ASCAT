# -*- coding: utf-8 -*-
"""
Created on Thu Mar 22 11:29:04 2018

@author: Rajasivaranjan
Email: rajasivaranjan92@gmail.com

"""

from PIL import Image
import urllib
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
import cv2
import pytesseract
from skimage.transform import radon
from PIL import Image
from numpy import asarray, mean, array, blackman
import numpy as np
import numpy
from numpy.fft import rfft
import matplotlib.pyplot as plt
from matplotlib.mlab import rms_flat
import pandas as pd
import datetime
import time

pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files (x86)/Tesseract-OCR/tesseract'


try:
    from parabolic import parabolic

    def argmax(x):
        return parabolic(x, np.argmax(x))[0]
except ImportError:
    from numpy import argmax


def get_captcha(driver, element):
    location = element.location
    size = element.size
    image = Image.open('Screenshot1.png')
    left = location['x']
    top = location['y'] 
    right = location['x'] + size['width']
    bottom = location['y'] + size['height'] 
    image = image.crop((left, top, right, bottom))  # defines crop points
    image.save('captcha.png')
    
    

def rotate(infile):
    I = asarray(Image.open(infile).convert('L'))
    I = I - mean(I)
    sinogram = radon(I)
    r = array([rms_flat(line) for line in sinogram.transpose()])
    rotation = argmax(r)
    print('Rotation: {:.2f} degrees'.format(90 - rotation))   
    img = cv2.imread(infile,0)
    rows,cols = img.shape
    M = cv2.getRotationMatrix2D((cols/2,rows/2),90.0-rotation,1)
    dst = cv2.warpAffine(img,M,(cols,rows))
    img = cv2.resize(dst,None,fx=2, fy=2, interpolation = cv2.INTER_CUBIC)
    ret1,th1 = cv2.threshold(img,30,255,cv2.THRESH_BINARY)
    cv2.imwrite("rotate.png", th1)

def main():
    start_time=time.time()
    xl = pd.ExcelFile("C:/Users/thamir/Desktop/Test/Tesser/Sep17.xlsx")
    df = xl.parse("Sheet1")
    data_li = []
    bill_no = df['Bill No']
    date = df['Date']
    port = df['Indian Port']
    for i in range(0,bill_no.size,1):
        print i
        driver = webdriver.PhantomJS(executable_path="C://Users//thamir//phantomjs//bin//phantomjs.exe")
        while True:
            exception = None
            driver.get('https://enquiry.icegate.gov.in/enquiryatices/sbTrack')
            driver.save_screenshot("Screenshot1.png")
    #        wait = WebDriverWait(driver, 10)
    #        element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'p img')))
            element = driver.find_element_by_css_selector('p img')
            get_captcha(driver,element)     
            op = driver.find_element_by_name('sbTrack_location')
            select = Select(driver.find_element_by_name('sbTrack_location'))
            select.select_by_value(str(port[i]))
            sb_no = driver.find_element_by_name("SB_NO")
            sb_no.clear()
            sb_no.send_keys(str(bill_no[i]))
            driver.execute_script('document.getElementsByName("SB_DT")[0].removeAttribute("readonly")')
            sb_dt = driver.find_element_by_name("SB_DT")
            dt_str = str(datetime.datetime.strftime(date[i], '%Y/%m/%d'))
            sb_dt.clear()
            sb_dt.send_keys(dt_str)
            captcha = driver.find_element_by_name("captchaResp")
            rotate('captcha.png')
            txt = pytesseract.image_to_string(Image.open("rotate.png"))
            print txt
            captcha.clear()
            captcha.send_keys(txt)
            driver.find_element_by_id("SubB").click()
            try:
                driver.find_element_by_link_text('SB Details').click()
            except NoSuchElementException as exception:
                print "Element not founnd"
            if exception is None:
                try:
                    wait = WebDriverWait(driver, 20)
                    table = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'thText')))
                    driver.save_screenshot("Screenshot2.png")
                    table_val =driver.find_element_by_class_name('tdText')
                    title_val = table.text
                    print table.text
                    print table_val.text.split("  ")
                    data_li.append(table_val.text.split("  "))
                except TimeoutException:
                    data_li.append([])
                    print "No Record Found"
                    driver.save_screenshot(str(bill_no[i])+"_scr.png")              
                driver.quit()
                break
    et = time.time()-start_time
    df_tb = pd.DataFrame(data_li)
    #df_tb.columns = ["Current Que", "LEO Date", "EP Copy Print Status", "DBK Scroll No", "Scroll Date", "Integration Status"]
    df_tb.to_csv('sep17_sb_details.csv')
    print (et/(60*60))

if __name__ == "__main__":
    main()