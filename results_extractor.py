import time

from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common import action_chains

def execute_with_retry(method, max_attempts):
    e = None
    for i in range(0, max_attempts):
        try:
            return method()
        except Exception as e:
            print(e)
            time.sleep(1)

tries = 5

# fp = webdriver.FirefoxProfile()
# fp.set_preference('dom.popup_maximum', 2000)
# fp.set_preference('browser.link.open_newwindow', 3)
# fp.set_preference('browser.link.open_newwindow.restriction', 0)
# fp.set_preference('browser.link.open_newwindow.override.external', 3)
 
capabilities = DesiredCapabilities.FIREFOX
options = Options()
options.headless = False
capabilities["marionette"] = True
firefox_bin = "/usr/bin/firefox"
browser = execute_with_retry(lambda: webdriver.Firefox(
    firefox_binary=firefox_bin, capabilities=capabilities, options=options), tries)
browser.set_page_load_timeout(24)
# time.sleep(30)

# Use this loop to extract specific data from the student's report sheet.
with open('assesmenturls.txt') as file:
    for line in file:
        browser.get(line)
        try:
          source = execute_with_retry(lambda: browser.find_element_by_class_name('CodeMirror-code'), tries)
          children = source.find_elements_by_xpath(".//*")
          with open('numlines.txt', 'a') as filex:
            filex.write(str(len(children)))
            filex.write(', ')
            filex.write(line)
            filex.write('\n')
        except Exception as e:
          print(e)

