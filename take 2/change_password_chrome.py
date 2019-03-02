import time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains 
from selenium.webdriver.common.alert import Alert 
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


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
ssl_manifest_path = "C:\\Users\\tas24\\Desktop\\CPower\\Firmware\\Modules\\SSLUpload_v0.14.0410_12\\Manifest_File_SSL.txt"  #set path to Manifest_File_SSL file

firmware_xmem_213    = ''    #LEFT BLANK css pathway to firmware version before xmem deleted v2.13
firmware_xmem_218    = '#as_toc > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(10) > td:nth-child(1) > a:nth-child(1) > img:nth-child(1)' #path to firmware version before xmem deleted v02.18.1117
                        
firmware_213 = '' #left blank: pathway to firmware after xmem is deleted for v2.13
firmware_218 = '#as_toc > table > tbody > tr:nth-child(9) > td:nth-child(1) > a > img' #css path to firmware version after xmem is deleted v02.18.1117
firmware_asarm = '#toc > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(11) > td:nth-child(1) > a:nth-child(1) > img:nth-child(1)'  #css path to firmware version after xmem is deleted v02.13.0712

dont_213 = '' #LEFT BLANK css path to "Apply" button for dont_check() after xmem is deleted on v02.13
dont_218 = '#asmoduleform > div:nth-child(10) > div:nth-child(1) > input:nth-child(1)' #css path to "Apply" button for dont_check() after xmem is deleted on v02.18.1117

xmem_accept_213 = '' #css for accept on firware version with xmem installed v02.18.1117
xmem_accept_218 = '#asmoduleform > div:nth-child(10) > div:nth-child(1) > input[type="submit"]:nth-child(1)' #css for accept on firware version with xmem installed v02.18.1117
             
network_menu = '#toc > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(6) > td:nth-child(1) > a:nth-child(1) > img:nth-child(1)' #css selector for drop down on networking tab.       
network_menu_mod = '#toc > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(10) > td:nth-child(1) > a:nth-child(1) > img:nth-child(1)'    #css selector for drop down on networking tab.
setup_link = '#toc > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(8) > td:nth-child(3) > font:nth-child(1) > a:nth-child(1)'  #css selector for Setup under Networking when modbus menu is closed.
setup_link_mod = '#toc > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(12) > td:nth-child(3) > font:nth-child(1) > a:nth-child(1)' #css selector for Setup under Networking when Modbus menu is open.
   
def return_frame(frame):    #Input string with 'String' returns to parent frame then selects either 'Body' or 'TableOfContents' 
    
    driver.switch_to.parent_frame() 
    driver.switch_to.frame(driver.find_element_by_name(frame)) 

def select_and_click(driver, element):  #Used for selecting hyperlinks. Input is always driver and generic button name for specific case
    click_element_chain = ActionChains(driver)
    click_element_chain.click(element)
    click_element_chain.perform()



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
driver.close()
