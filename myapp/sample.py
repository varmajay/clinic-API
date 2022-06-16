from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

import time  
from selenium.webdriver.common.keys import Keys  
print("sample test case started")  
driver = webdriver.Chrome(ChromeDriverManager().install())
#driver=webdriver.firefox()  
#driver=webdriver.ie()  
#maximize the window size  
driver.maximize_window()  
#navigate to the url  
driver.get("https://github.com/varmajay")  
#identify the Google search text box and enter the value  
time.sleep(5)  
#click on the Google search button  
driver.find_element_by_name("btnK").send_keys(Keys.ENTER)  
time.sleep(3)  
#close the browser  
driver.close()  
print("sample test case successfully completed")  