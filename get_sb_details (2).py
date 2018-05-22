# -*- coding: utf-8 -*-
"""
Created on Thu Mar 22 11:29:04 2018

@author: Ponraj

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
import time, csv, os

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
#    print('Rotation: {:.2f} degrees'.format(90 - rotation))   
    img = cv2.imread(infile,0)
    rows,cols = img.shape
    M = cv2.getRotationMatrix2D((cols/2,rows/2),90.0-rotation,1)
    dst = cv2.warpAffine(img,M,(cols,rows))
    img = cv2.resize(dst,None,fx=2, fy=2, interpolation = cv2.INTER_CUBIC)
    ret1,th1 = cv2.threshold(img,30,255,cv2.THRESH_BINARY)
    cv2.imwrite("rotate.png", th1)

def main():
    start_time=time.time()
    xl = pd.ExcelFile("C:/Users/thamir/Desktop/Test/Tesser/test_data1.xlsx")
    df = xl.parse("Sheet1")
    data_li = []
    bill_no = df['Bill No']
    date = df['Date']
    port = df['Indian Port']
    for i in range(0,bill_no.size,1):
        print i
        driver = webdriver.PhantomJS(executable_path="C://Users//thamir//phantomjs//bin//phantomjs.exe",)
        while True:
            exception = None
            try:
                driver.get('https://enquiry.icegate.gov.in/enquiryatices/sbTrack')
                driver.save_screenshot("Screenshot1.png")
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
                captcha.clear()
                captcha.send_keys(txt)
                driver.find_element_by_id("SubB").click()
            except NoSuchElementException as exception:
                print "Element not found"
            if exception is None:
                try:
                    wait = WebDriverWait(driver, 20)
                    ele = wait.until(EC.element_to_be_clickable((By.LINK_TEXT,'SB Details')))
                    driver.execute_script("arguments[0].click();", ele)
                except TimeoutException as exception:
                    print "Captcha not found"
            if exception is None:
                try:
                    table = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'thText')))
                    driver.save_screenshot("Screenshot2.png")
                    table_val =driver.find_element_by_class_name('tdText')
                    title_val = table.text
                    print table.text
                    print table_val.text.split("  ")
                    data_li.append(table_val.text.split("  "))
                except NoSuchElementException or TimeoutException :
                    data_li.append([" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "])
                    print "No Record Found"
                    driver.save_screenshot(str(bill_no[i])+"_scr.png")              
                driver.quit()
                break
    with open('test_file.csv','wb') as fn:
        w = csv.writer(fn)
        w.writerow(["IEC", "CHA No.", "Job No.", "Job Date", "Port of Discharge",
                    "Total Package", "Gross Weight", "FOB(INR)", "Total cess", "Drawback",
                    "STR", "Total (DBK+STR)", "Reward Flag"])
        w.writerows(data_li)
    fn.close()
    et = time.time()-start_time
    print (et/(60*60))
    df1 = pd.read_csv('test_file.csv')
    final_data = pd.concat([df, df1], axis=1)
    final_data.to_csv('Final_results.csv')
    os.remove('test_file.csv')
    os.remove('Screenshot2.png')
    os.remove('captcha.png')
    os.remove('rotate.png')
    os.remove('Screenshot1.png')
    

#    df_tb = pd.DataFrame(data_li)
    #df_tb.columns = ["Current Que", "LEO Date", "EP Copy Print Status", "DBK Scroll No", "Scroll Date", "Integration Status"]
#    df_tb.to_csv('Oct17_sb_details.csv')
    

if __name__ == "__main__":
    main()
