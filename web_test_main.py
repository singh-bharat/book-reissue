from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

################################################################################
#to verify the internet connection
################################################################################
import socket
REMOTE_SERVER = "www.google.com"
def is_connected():
  try:
    host = socket.gethostbyname(REMOTE_SERVER)
    s = socket.create_connection((host, 80), 2)
    return True
  except:
     pass
  return False
################################################################################

if is_connected():
        
    #reaches the login page
    driver = webdriver.Chrome()
    driver.get("http://14.139.108.229/W27/w27SimpleSearch.aspx")
    try:
      assert "Simple Search" in driver.title
    except:
      print 'Something wrong with LIBRARY PAGE'
      driver.quit()
    
    #takes the username 
    while True:
        #check for correct username and password combination   
        while (driver.title != 'My Information'):
            driver.get('http://14.139.108.229/W27/login.aspx?ReturnUrl=%2fW27%2fMyInfo%2fw27MyInfo.aspx')
            username = raw_input("Enter your username : ")
            
            ####################################################################
            #verify the correctness of username (it should be an int)
            ####################################################################
            def is_int(username):
                try:
                    int(username)
                    return True
                except ValueError:
                    return False
            
            #to ensure a correct username
            while is_int(username) == False:
                username = raw_input('re-enter correct/valid username : ')
            ####################################################################
            
            #typecast username into an int
            username = int(username)
            
            #enter the username
            elem = driver.find_element_by_id("txtUserName")
            elem.clear()
            elem.send_keys(username)
            
            #enter the password
            elem = driver.find_element_by_id("Password1")
            elem.clear()
            elem.send_keys("MEMBER")
            
            #elem.send_keys(Keys.RETURN)
            elem = driver.find_element_by_xpath('//*[@id="Submit1"]')
            elem.click()
            
        #welcome note
        elem = driver.find_element_by_id('ctl00_lblUsername')
        elem = elem.text
        print '\nWelcome, ' + elem[8:] + '!\n'
        print '\n******************************************************\n'
        
        #reissue all the books (max 5)
        for i in range(2,6+1):
            try:
                elem = driver.find_element_by_id("ctl00_ContentPlaceHolder1_CtlMyLoans1_grdLoans_ctl0" + str(i) + "_Button1")
            except NoSuchElementException:
                break
            if elem.is_enabled():
                elem.click()

                #due date of every individual book
                book = driver.find_element_by_id("ctl00_ContentPlaceHolder1_CtlMyLoans1_grdLoans_ctl0" + str(i) + "_lnkTitle")
                due_on = driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_CtlMyLoans1_grdLoans"]/tbody/tr[2]/td[5]')
                print('"' + book.text + '" is due on "' + due_on.text.upper() + '"')

                #fine on every individual book
                elem = driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_CtlMyLoans1_lblMsg"]')
                fine_on_this_book = driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_CtlMyLoans1_grdLoans_ctl0' + str(i) + '_lblFine"]')
                print(elem.text)
                print 'Fine on this book is ' + fine_on_this_book.text + '.\n'

                print '******************************************************\n'

                
            
        #fine
        elem = driver.find_element_by_id("ctl00_ContentPlaceHolder1_CtlMyLoans1_lblTotFineAmt")
        print("Total fine till now is Rs. %s\n" %elem.text)
        print '******************************************************\n'
        
        #logout
        elem = driver.find_element_by_xpath('//*[@id="ctl00_Menu2n5"]/table/tbody/tr/td/a')
        elem.click()
        
        #finding my info
        elem = driver.find_element_by_xpath('//*[@id="ctl00_Menu1n2"]/table/tbody/tr/td/a')
        elem.click()
        
        assert "No results found." not in driver.page_source

else:
    print 'Please connect to internet and then try again!'
