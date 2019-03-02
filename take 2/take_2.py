""" Tyler Sargent ~ Welcome to Hell, Enjoy Your Stay ! ~"""
'''Notes
~After installing asarm file, firmware ((v02.13.0712)), many of the CSS selectors change 

'''


import time
import ftplib
import os
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains 
from selenium.webdriver.common.alert import Alert 
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from ftplib import FTP

#Drivers------------------------------------------
driver = webdriver.Firefox()
#driver = webdriver.Chrome("C:/Users/tas24/source/repos/take 2/take 2/Drivers/chromedriver") #sets browser to the driver for Chrome specifying driver location DOES NOT WORK    
#Variables----------------------------------------
debug_mode      = False
device_ip       = "192.168.40.50" #Device IP
start_key       = "admin"
extension       = "http://admin:" #allows bypass of alert feilds asking for username and password
device_id       = "Device Error"  #This is the 4 didgit unique device ID
device_password = "Password Error"  #formatted password with unique device ID
asarm_path      = "C:\\Users\\tas24\\Desktop\\CPower\\Firmware\\v02-13-0712\\asarm.cramfs" #set path to asarm file
ramdisk_path    = "C:\\Users\\tas24\\Desktop\\CPower\\Firmware\\v02-13-0712\\ramdisk.gz"  #set path to ramdisk file
usrarm_path     = "C:\\Users\\tas24\\Desktop\\CPower\\Firmware\\v02-13-0712\\usrarm.cramfs" #set path to usrarm file
zimage_path     = "C:\\Users\\tas24\\Desktop\\CPower\\Firmware\\v02-13-0712\\zImage" #set path to zimage file
manifest_path   = "C:\\Users\\tas24\\Desktop\\CPower\\Firmware\\v02-13-0712\\Manifest.txt"   #set path to manifest file
rootcerts_path  = "C:\\Users\\tas24\\Desktop\\CPower\\Firmware\\Modules\\SSLUpload_v0.14.0410_12\\AcquiSuite_RootCerts.asmodule.cramfs" #set path to AcquiSuite_RootCerts file
sslupload_path  = "C:\\Users\\tas24\\Desktop\\CPower\\Firmware\\Modules\\SSLUpload_v0.14.0410_12\\Obvius_SSLUpload.asmodule.cramfs" #set path to Obvius_SSLUpload.asmodule file
sslmanifest_path = "C:\\Users\\tas24\\Desktop\\CPower\\Firmware\\Modules\\SSLUpload_v0.14.0410_12\\Manifest_File_SSL.txt"  #set path to Manifest_File_SSL file
os_path         = "C:\\Users\\tas24\\Desktop\\CPower\\A7810 Configuration Files"                    #path to directory where files are stored 
log_path        = "C:\\Users\\tas24\\Desktop\\CPower\\A7810 Configuration Files\loggerconfig.ini"   #path to logger_config.ini
mb250_path      = "C:\\Users\\tas24\\Desktop\\CPower\\A7810 Configuration Files\mb-250.ini"         #path to mb-250.ini file

modbus_path = '#toc > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(3) > td:nth-child(1) > a:nth-child(1) > img:nth-child(1)'  #pathway to Modbus drop down with v02.13.0712

firmware_xmem_213    = ''    #LEFT BLANK css pathway to firmware version before xmem deleted v2.13
firmware_xmem_218    = '#as_toc > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(10) > td:nth-child(1) > a:nth-child(1) > img:nth-child(1)' #path to firmware version before xmem deleted v02.18.1117
                     
firmware_213 = '' #LEFT BLANK pathway to firmware after xmem is deleted for v2.13
firmware_218 = '#as_toc > table > tbody > tr:nth-child(9) > td:nth-child(1) > a > img' #css path to firmware version after xmem is deleted v02.18.1117
firmware_asarm = '#toc > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(11) > td:nth-child(1) > a:nth-child(1) > img:nth-child(1)'  #css path to firmware version after xmem is deleted v02.13.0712

dont_213 = '' #LEFT BLANK css path to "Apply" button for dont_check() after xmem is deleted on v02.13
dont_218 = '#asmoduleform > div:nth-child(10) > div:nth-child(1) > input:nth-child(1)' #css path to "Apply" button for dont_check() after xmem is deleted on v02.18.1117

xmem_accept_213 = '' #LEFT BLANK pathway to firmware with xmem installed for v2.13
xmem_accept_218 = '#asmoduleform > div:nth-child(10) > div:nth-child(1) > input[type="submit"]:nth-child(1)' #css for accept on firware version with xmem installed v02.18.1117
             
network_menu = '#toc > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(6) > td:nth-child(1) > a:nth-child(1) > img:nth-child(1)' #css selector for drop down on networking tab.       
network_menu_mod = '#toc > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(10) > td:nth-child(1) > a:nth-child(1) > img:nth-child(1)'    #css selector for drop down on networking tab.
setup_link = '#toc > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(8) > td:nth-child(3) > font:nth-child(1) > a:nth-child(1)'  #css selector for Setup under Networking when modbus menu is closed.
setup_link_mod = '#toc > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(12) > td:nth-child(3) > font:nth-child(1) > a:nth-child(1)' #css selector for Setup under Networking when Modbus menu is open.

old_fig = 'logger_config.ini'   #file name of old logger_config file
new_fig = 'loggerconfig.ini'     #DO NOT CHANGE! file name for loggerconfig.ini
old_mb  = 'mb-250.ini'  #file name of old mb-250 file
new_mb  = 'mb-250.ini'  #DO NOT CHANGE! file name for mb-250.ini

rec_indicator  = 'The AcquiLite name, location, description, and contact should be configured.'
edit_indicator = 'edit'
#Define Functions-----------------------------------------------
def get_device(device_id):   #Prompts users for the Device ID

    device_id = input("Enter the last four digits of the device to create a unique password: ")  #Sets input of prompt to device ID.

    print("Device ID set to " + device_id)  #Prints device ID.

    check_id = input("Are these the correct numbers? (Y/N): ") #Promps for confirmation of correct ID.
        
    if check_id.lower() == 'y': #Checks that user specified ID is the correct ID, otherwise it askes again.
        print("Device ID confirmed...")
        
    else:
        print("Try again.")
        get_device(device_id)

    return(device_id)

def set_password(device_id): #Takes global devic_id and returns a formatted password to be used.

    device_password = ("Drm!" + device_id)

    #print("This is the password for this device: " + device_password)
    return(device_password)

def go_to_firmware():   #naviagtes from home to firmware version page
    
    return_frame('TableOfContents')

    time.sleep(1)

    #driver.switch_to.parent_frame() #reset to parent frame
    #driver.switch_to_frame(driver.find_element_by_name('TableOfContents')) #choose frame Table of Contents
    
    found_path = False  #Boolean for finding correct version of pathway to System drop down
   
    if found_path == False :
        try:
            #try to find element based off version 2.13
            system_drop = driver.find_element_by_css_selector(firmware_213) 
            attribute_check = system_drop.get_attribute("src")
            if debug_mode == True :
                print('Using firmware version path for v2.13...')
            found_path = True
        except:
            if debug_mode == True :
                print('Path Not Found: go_to_firmware v2.13. Now trying path for v02.18.1117 ...')

    if found_path == False :
        try:
            #try to find element based off version v02.18.1117
            system_drop = driver.find_element_by_css_selector(firmware_218) #select element system_drop
            attribute_check = system_drop.get_attribute("src")
            if debug_mode == True :
                print('Using firmware version path for v02.18.1117 ...')
            found_path = True
        except:
            if debug_mode == True :
                print('Path Not Found: go_to_firmware v02.18.1117. Now trying path for v02.13.0712 ...')

    if found_path == False :
        try:
            #try to find element after v02.13.0712 installed
            system_drop = driver.find_element_by_css_selector(firmware_asarm) #select element system_drop
            attribute_check = system_drop.get_attribute("src")
            if debug_mode == True :
                print('Using firmware version path for v02.13.0712 ...')
            found_path = True
        except:
            if debug_mode == True :
                print('CRITICAL ERROR: Path Not Found: potential unknwon pathway for go_to_frimware()')

    if found_path == False :
        try:
            #try to find element based off version 2.13 with xmem
            system_drop = driver.find_element_by_css_selector(firmware_xmem_213) 
            attribute_check = system_drop.get_attribute("src")
            if debug_mode == True :
                print('Using firmware version path for v2.13 with xmem...')
            found_path = True
        except:
            if debug_mode == True :
                print('Path Not Found: go_to_firmware_xmem v2.13')

    if found_path == False :
        try:
            #try to find element based off version v02.18.1117 with xmem
            system_drop = driver.find_element_by_css_selector(firmware_xmem_218) #select element system_drop
            attribute_check = system_drop.get_attribute("src")
            if debug_mode == True :
                print('Using firmware version path for v02.18.1117 with xmem...')
            found_path = True
        except:
            if debug_mode == True :
                print('Path Not Found: go_to_firmware_xmem v02.18.1117')  


    time.sleep(1)

    if(attribute_check == "http://admin:" + start_key + "@" + device_ip + "/images/ti_plus.png"):   #if system tab unexpanded, expand
        if debug_mode == True :
            print('true 1')
        select_and_click(driver, system_drop)

    if(attribute_check == "http://admin:" + start_key + "@" + device_ip + "/setup/images/ti_plus_end.png"):   #if system tab unexpanded, expand before ASARM and after xmem notice ti_plus_end.png
        if debug_mode == True :
            print('true 2')
        select_and_click(driver, system_drop)
        
    if(attribute_check == "http://admin:" + start_key + "@" + device_ip + "/setup/images/ti_plus.png"):   #if system tab unexpanded, expand AFTER ASARM notice /setup/
        if debug_mode == True :
            print('true 3')
        select_and_click(driver, system_drop)


    time.sleep(2)

    element = driver.find_element_by_link_text('Firmware Version')  #select element Firmware Version
    select_and_click(driver, element)

def go_to_network() :

    return_frame('TableOfContents')

    time.sleep(1)

    found_path = False
    if found_path == False :
        try:
            #try to find element based off version v02.13.0712 modbus menu closed
            network_drop = driver.find_element_by_css_selector(network_menu) 
            attribute_check = network_drop.get_attribute("src")
            print('Using networking>setup path for v02.13.0712...')
            found_path = True
        except:
            print('Path Not Found: go_to_network v02.13.0712.')

    if found_path == False :
        try:
            #try to find element based off version v02.13.0712 with modbus menu opened
            network_drop = driver.find_element_by_css_selector(network_menu_mod) 
            attribute_check = network_drop.get_attribute("src")
            if debug_mode == True :
                print('Using networking>setup path for v02.13.0712 with modbus tab open...')
            found_path = True
        except:
            if debug_mode == True :
                print('Path Not Found: go_to_network v02.13.0712 modbus open. Potential unknown path')

    if(attribute_check == "http://admin:" + start_key + "@" + device_ip + "/setup/images/ti_plus.png"):   #if system tab unexpanded, expand AFTER ASARM notice /setup/
        print('true 3')
        select_and_click(driver, network_drop)


        time.sleep(1)

    try:  
        network_setup = driver.find_element_by_css_selector(setup_link)
        select_and_click(driver, network_setup)
    except:
        if debug_mode == True :
            print('Path Not Found: tried to select element "Setup" when modbus closed...')

    try:
        network_setup = driver.find_element_by_css_selector(setup_link_mod)
        select_and_click(driver, network_setup)
    except:
        if debug_mode == True :
            print('Path Not Found: tried to select element "Setup" when modbus open... Unknown Path!')


    print('Networking tab opened...')

def go_to_modbus():

    return_frame('TableOfContents')
    time.sleep(1)

    found_path = False  #Boolean for finding correct version of pathway to Modbus drop down
   
    if found_path == False :
        try:
            #try to find element based off version v02.13.0712
            modbus_drop = driver.find_element_by_css_selector('#toc > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(3) > td:nth-child(1) > a:nth-child(1) > img:nth-child(1)') 
            attribute_check = modbus_drop.get_attribute("src")
            if debug_mode == True :
                print('Using Modbus path for v02.13.0712...')
            found_path = True
        except:
            print('Path Not Found: go_to_modbus v02.13.0712.')

    if(attribute_check == "http://admin:" + start_key + "@" + device_ip + "images/ti_plus.png"):   #if system tab unexpanded, expand
        if debug_mode == True :
            print('true 1')
        select_and_click(driver, system_drop)

    time.sleep(1)
    element = driver.find_element_by_link_text('Setup')
    select_and_click(driver, element)

    print('Modbus tab opened...')

def delete_xmem(): #uses go_to_firmware_xmem to delete and uninstall xmem if found.

    
    go_to_firmware()

    return_frame('Body')
   
    time.sleep(1)

    xmem_found = False
    try:
        select = Select(driver.find_element_by_name('ASMODULE03')) #select drop down for xmem 
        select.select_by_visible_text("Uninstall & Delete*")    #choose "Uninstall & Delete*" from drop down list
        button = driver.find_element_by_css_selector(xmem_accept_218)    #find and click apply 
        time.sleep(1)
        button.click()
    except:
        print('xmem not found')
        xmem_found = True
    
    if xmem_found == False :
        #Waits for Please Reboot link or times out after 5 seconds. NOT the same as in submit_reboot()
        try:     
            element = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.LINK_TEXT, 'Reboot.')), 'Looking for Reboot...')
                                                                          
        except TimeoutException:
            print('timeout on finding reboot for xmem')


        return_frame('Body')

        reboot = driver.find_element_by_link_text('Reboot')
        select_and_click(driver, reboot)
    

        #Waits for 3 seconds then attempts to find alert to reboot 
        try:
            WebDriverWait(driver, 1).until(EC.alert_is_present(),
                                   'Waiting for alert...')
    
            alert = driver.switch_to_alert()
            alert.accept()
            print("Rebooting...")

        except TimeoutException:
            print('No alert for xmem reboot')

        wait_reboot()

        print(" xmem deleted and reboot done.")
    

    time.sleep(1)   

    driver.get(extension + start_key + "@" + device_ip + '/setup/')

    wait_reboot(rec_indicator)
   
def upload_file(primary_file, manifest_file): #inputs are file to be uploaded and the manifest file. Fills these files in to be uploaded inside firmware version

    return_frame('Body')
        
    time.sleep(1)

    #select have disk BEFORE v02.13.0712 installed
    found_path = False
    if found_path == False :
        try:                                            
            button = driver.find_element_by_css_selector('#asmoduleform > div:nth-child(10) > div:nth-child(2) > form:nth-child(1) > input:nth-child(1)')  #select have disk
            button.click()
            found_path = True
        except:
            print('Searching for "Have Disk"...')

    #select have disk AFTER v02.13.0712 installed
    if found_path == False :
        try:
            button = driver.find_element_by_css_selector('#asmoduleform > div:nth-child(11) > div:nth-child(2) > form:nth-child(1) > input:nth-child(1)')  
            button.click()
            found_path = True
        except:
            print('"Have Disk" not found using v02.13.0712 pathway')

    time.sleep(1)

    fileinput = driver.find_element_by_name("CMD_OS_FILE") #choose file for OS
    fileinput.send_keys(primary_file)

    fileinput = driver.find_element_by_name("CMD_MANIFEST_FILE")    #choose file for Manifest
    fileinput.send_keys(manifest_file)

    time.sleep(1)

    print('Files selected...')
                                                                           
def submit_reboot(primary_file):    #submits the files selected by upload_file() and then reboots after upload to apply changes.

    time.sleep(1)

    button = driver.find_element_by_css_selector('#submitspace > input:nth-child(1)')   #selects and clicks submit on file select page
    button.click()

    #Waits for Please Reboot link while uploading files or times out after 60 seconds 
    try:     
        element = WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.LINK_TEXT, 'Please Reboot.')), 'Upload in progress...')
                                                                            
    except TimeoutException:
        print('timeout on upload of ' + primary_file)

    return_frame('Body')

    reboot = driver.find_element_by_link_text('Please Reboot.')
    select_and_click(driver, reboot)

    #Waits for 3 seconds then attempts to find alert to reboot 
    try:
        WebDriverWait(driver, 3).until(EC.alert_is_present(), 'Waiting for alert...')
        pop_up = driver.switch_to_alert()
        pop_up.accept()
        print("Rebooting...")

    except TimeoutException:
        print('alert failed on ' + primary_file)

    wait_reboot(rec_indicator) 
    
    print(primary_file + ' Finished.')
              
def wait_reboot(indicator):  #Waits for reboot to "Welcome" page by looking for link text of 'The default administrator password should be changed.'

    counter = 0
    while counter <= 20 :

        try:
            try:
                return_frame('Body')
            except:
                print('')
                
            element = WebDriverWait(driver, 11).until(           
            EC.visibility_of_element_located((By.LINK_TEXT, indicator)), 'Looking for indicator element to verify reload')
            break
        
        except TimeoutException:
            print("Waiting for page refresh...")

            try:
                driver.get(extension + start_key + "@" + device_ip + '/setup/')
            except:
                print('Tried, No Connection...')

            counter = counter + 1 
            if counter >= 12 :
                print('CRITICAL ERROR: Device cannot be reached.')


    time.sleep(1)

def dont_check():   #Finds and selects the Don't Check option from menu and then applies change  ******implement later

    return_frame('Body')
   
    time.sleep(1)

    select = Select(driver.find_element_by_name('UPDATEMGRPERIOD')) #select drop down for checking and installing firmware updates. 
    select.select_by_visible_text("Don't check")    #choose "Don't check" from list

    found_path = False
    if found_path == False :
        try:
            button = driver.find_element_by_css_selector(dont_213)    #find and click apply path for v2.13
            button.click()   
            found_path = True
        except:
            if debug_mode == True :
                print('Path Not Found: v2.13 to "Apply" in dont_check(). Now trying path for v02.18.1117.')

    if found_path == False :
        try: 
            button = driver.find_element_by_css_selector(dont_218)    #find and click apply path for v02.18.1117
            button.click()   
            found_path = True
        except:
            if debug_mode == True :
                print('Path Not Found: v02.18.1117 to "Apply" in dont_check(). Potential uknown pathway.')

    print("Applied 'Don't Check'")

def accept_alert(success, error):
    try:
        WebDriverWait(driver, 3).until(EC.alert_is_present(), 'Waiting for alert...')
        pop_up = driver.switch_to_alert()
        pop_up.accept()
        print(success)

    except TimeoutException:
        print(error)
    print('')

def select_and_click(driver, element):  #Used for selecting hyperlinks. Input is always driver and generic button name for specific case
    click_element_chain = ActionChains(driver)
    click_element_chain.click(element)
    click_element_chain.perform()

def return_frame(frame):    #Input string with 'String' returns to parent frame then selects either 'Body' or 'TableOfContents' 
    
    driver.switch_to.parent_frame() 
    driver.switch_to.frame(driver.find_element_by_name(frame)) 

def config_pass(start_key): #use gobal variable start_key. Asks user if device has had password other than default configured to it. returns configured password

    check_input = input("Does this device have a configured password? (Y/N): ") #Promps for confirmation of configured password
        
    if check_input.lower() == 'y' : #Checks that user specified ID is the correct ID, otherwise it askes again.

        start_key = device_password
        print("Password set as device id...")
        return(start_key)
        
    if check_input.lower() == 'n' : 
        
        print("Password set as default...")
        return(start_key)
       
    else:
        print("Try again.")
        config_pass(start_key)

def change_password(start_key):

  
    if start_key != device_password : 
        
        driver = webdriver.Chrome("C:/Users/tas24/source/repos/take 2/take 2/Drivers/chromedriver") #sets browser to the driver for Chrome specifying driver location DOES NOT WORK     
        driver.get(extension + start_key + "@" + device_ip + '/setup/')   #Firefox to open         
        driver.refresh()
        
        return_frame('Body')
        time.sleep(1)

        element = driver.find_element_by_link_text('The default administrator password should be changed.')
        select_and_click(driver, element)


        return_frame('Body')
        time.sleep(1)
        button = driver.find_element_by_css_selector('body > div:nth-child(2) > form:nth-child(1) > p:nth-child(3) > input:nth-child(4)')
        button.click()

        WebDriverWait(driver, 3).until(EC.alert_is_present(), 'Typing in password')
        alert = driver.switch_to_alert()
        alert.send_keys(device_password)
        alert.accept()

        alert = driver.switch_to_alert()
        alert.accept()

        start_key = device_password
        print('Password has been changed to: ' + device_password )
        driver.quit()
        return(start_key)
       
        



        '''
        try:
            return_frame('Body')
            time.sleep(1)
            element = driver.find_element_by_css_selector('body > div:nth-child(2) > div:nth-child(1) > table:nth-child(14) > tbody > tr:nth-child(1) > td:nth-child(2) > a')
            select_and_click(driver, element)
            try:
                return_frame('Body')
                time.sleep(1)
                button = driver.find_element_by_css_selector('body > div:nth-child(2) > form:nth-child(1) > p:nth-child(3) > input:nth-child(4)')
                button.click()
                try:
                    WebDriverWait(driver, 3).until(EC.alert_is_present(), 'Typing in password')
                    alert = driver.switch_to_alert()
                    alert.send_keys(device_password)
                    alert.accept()
                    try:
                        time.sleep(1)                       
                        alert.send_keys(Keys.SPACE)
                        try:
                            #WebDriverWait(driver, 3).until(EC.alert_is_present(), 'failed to dismiss login feilds')
                            #alert = driver.switch_to_alert()
                            #alert.dismiss()

                            start_key = device_password
                            print('Password has been changed to: ' + device_password )
                            driver.close()
                            return(start_key)

                        except TimeoutException:
                            print('failed to dismss alert')
                    except:
                        print('Could not click ok on re-authenticate alert')
                except TimeoutException:
                    print('alert failed on change pasword') 
            except:
                print('Could not click "Change Password" button')
        except:
            print('Could not find "The default administrator password should be changed." ')
            alert.next
         '''  
    if start_key == device_password :
        print('Password has already been reset...')
        return(start_key)

    print('Should not have reached this point... change_password()')

def allow_ftp():

    return_frame('Body')
    time.sleep(1)

    select = Select(driver.find_element_by_name('FTPLOGINENABLED')) #select drop down for allowing FTP logins
    select.select_by_visible_text("Temporarily, for 1 hour")    #choose "Don't check" from list

    button = driver.find_element_by_css_selector('body > div:nth-child(2) > div:nth-child(1) > form:nth-child(3) > table:nth-child(3) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > input:nth-child(1)')    #find and click apply path for v2.13
    button.click()                             

    return_frame('Body')
    time.sleep(1)

    element = driver.find_element_by_link_text('Please Reboot.')
    select_and_click(driver, element)

    try:
        WebDriverWait(driver, 3).until(EC.alert_is_present(), 'Waiting for alert...')
        alert = driver.switch_to_alert()
        alert.accept()
        print("Rebooting...")

    except TimeoutException:
        print('No alert on FTP reboot')

    wait_reboot(rec_indicator)

    print('FTP Enabled.')

def replace_files_ftp():  #input string of filename to replaced

    ftp = FTP(device_ip)
    os.chdir(os_path)

    print(ftp.login('root', start_key))
    print(ftp.cwd('/'))


    #replace logger config file
    print(ftp.cwd('/mnt/main/sysconfig'))
    print(ftp.pwd())
    try:
        print(ftp.delete(old_fig))
    except:
        print('Could not find ' + old_fig + ' to delete.')
    try:
        print(ftp.storbinary('STOR ' + new_fig, open(new_fig, 'rb')))
        print('Replaced ' + old_fig + ' with ' + new_fig)
    except:
        print('Failed to upload ' + new_fig)
    print(ftp.nlst())

    #replace mb-250 file
    print(ftp.cwd('/mnt/main/sysconfig/modbus'))
    print(ftp.pwd())
    try:
        print(ftp.delete(old_mb))
    except:
        print('Could not find ' + old_mb + ' to delete.')
    try:
        print(ftp.storbinary('STOR ' + new_mb, open(new_mb, 'rb')))
        print('Replaced ' + old_mb + ' with ' + new_mb)
    except:
        print('Failed to upload ' + new_mb)
    print(ftp.nlst())
    

    print(ftp.quit())

    driver.get(extension + start_key + "@" + device_ip + '/setup/')   #Firefox to open

    #dismiss alert resulting from FTP
    accept_alert('Alert after FTP accepted.', 'Could not accept alert after FTP.')
   
    go_to_network()
    
    #dismiss alert resulting from ftp
    accept_alert('Alert after FTP accepted.', 'Could not accept alert after FTP.')

    return_frame('Body')
    time.sleep(1)

    #click check box to not use DHCP automatically
    element = driver.find_element_by_css_selector('body > div:nth-child(2) > div:nth-child(1) > form:nth-child(3) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(9) > td:nth-child(2) > input:nth-child(3)')
    element.click()

    return_frame('Body')
    time.sleep(1)
    
    #click the apply button
    button = driver.find_element_by_css_selector('body > div:nth-child(2) > div:nth-child(1) > form:nth-child(3) > table:nth-child(3) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > input:nth-child(1)')
    button.click()

    return_frame('Body')
    time.sleep(1)

    element = driver.find_element_by_link_text('Please Reboot.')
    select_and_click(driver, element)

    accept_alert('Rebooting...', 'Could not reboot after disabling DHCP')
    
    print('FTP successful')

def upload_all_files():

    upload_file(asarm_path, manifest_path)

    submit_reboot(asarm_path)

    go_to_firmware()

    upload_file(ramdisk_path, manifest_path)

    submit_reboot(ramdisk_path)

    go_to_firmware()

    upload_file(usrarm_path, manifest_path)

    submit_reboot(usrarm_path)

    go_to_firmware()

    upload_file(zimage_path, manifest_path)

    submit_reboot(zimage_path)

    go_to_firmware()

    upload_file(rootcerts_path, sslmanifest_path)

    submit_reboot(rootcerts_path)

    go_to_firmware()

    upload_file(sslupload_path, sslmanifest_path)

    submit_reboot(sslupload_path)

def tcp_dhcp():

    return_frame('Body')
    time.sleep(1)

    #select from subnet only under Modus TCP Access
    select = Select(driver.find_element_by_name('MODBUSTCPACCESS')) 
    select.select_by_visible_text("Allow ModbusTCP access from local subnet only")    

    return_frame('Body')
    time.sleep(1)

    #click apply to chnage allow DHCP automatically
    button = driver.find_element_by_css_selector('body > div:nth-child(2) > div:nth-child(1) > form:nth-child(3) > input:nth-child(3)')
    button.click()

    go_to_network()

    return_frame('Body')
    time.sleep(1)

    #click check box to use DHCP automatically          
    element = driver.find_element_by_css_selector('body > div:nth-child(2) > div:nth-child(1) > form:nth-child(3) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(9) > td:nth-child(2) > input:nth-child(3)')
    element.click()

    return_frame('Body')
    time.sleep(1)
    
    #click the apply button
    button = driver.find_element_by_css_selector('body > div:nth-child(2) > div:nth-child(1) > form:nth-child(3) > table:nth-child(3) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > input:nth-child(1)')
    button.click()

    return_frame('Body')
    time.sleep(1)

    #click reboot
    element = driver.find_element_by_link_text('Please Reboot.')
    select_and_click(driver, element)

    accept_alert('Rebooting...', 'Could not reboot after enabling DHCP')

#MainScript--------------------------------------

device_id = get_device(device_id)   

device_password = set_password(device_id)

start_key = config_pass(start_key)

driver.get(extension + start_key + "@" + device_ip + '/setup/')   #Firefox to open 

delete_xmem()

#start_key = change_password(start_key)

go_to_firmware()

dont_check()

#upload_all_files()

go_to_network()

allow_ftp()

replace_files_ftp()

time.sleep(45) #dumb need a better restart monitor

driver.get(extension + start_key + "@" + device_ip + '/setup/')   #Firefox to open 

go_to_modbus()

tcp_dhcp()

print('Device Successfully Configured')



