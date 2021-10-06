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
    if e is not None:
        raise e

tries = 20

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

running = True
claimctr = 11
nextclicks = 2
claims = []
first = False

while running:
  browser.get("https://app.testgorilla.com/login")
  time.sleep(2)
  try:
    cookies = browser.find_element_by_class_name('cc-dismiss')
    cookies.click()
  except Exception as e:
    print(e)
  if first:
    time.sleep(30)
    first = False
  try:
    usernamefield = execute_with_retry(lambda: browser.find_element_by_id('mat-input-0'), tries)
    usernamefield.send_keys('YOURUSERNAMEHERE')
    browser.find_element_by_id('mat-input-1').send_keys('YOURPASSWORDHERE')
    browser.find_element_by_class_name('submit-button').click()

    pageloaded = execute_with_retry(lambda: browser.find_element_by_class_name('mat-row'), tries)
    action = action_chains.ActionChains(browser)

    browser.get("https://app.testgorilla.com/customer/assessments/YOURASSESSMENTIDHERE")
    pageloaded = execute_with_retry(lambda: browser.find_element_by_class_name('cdk-column-score'), tries)
    # browser.switch_to.window(browser.window_handles[0])
    next = execute_with_retry(lambda: browser.find_element_by_class_name('mat-paginator-navigation-next'), tries)
    browser.execute_script("arguments[0].scrollIntoView();", next)
    time.sleep(2)
    action.move_to_element(next)
    action.click()
    for x in range(nextclicks):
      print("clicking next")
      action.perform()
      time.sleep(3)
      print("done clicking")
  except Exception as e:
      print(e)
  clicked = True
  while clicked:
    try:
      claims.clear()
      print(claims)
      # browser.refresh()
      time.sleep(5)
      claims = browser.find_elements_by_class_name('cdk-row')
      c = claims[claimctr]
      browser.execute_script("arguments[0].scrollIntoView();", c)
      time.sleep(2)
      action.move_to_element_with_offset(c, 10, 10)
      time.sleep(2)
      action.click()
      print("click")
      action.perform()
      print("perform")
      print(claimctr)
      clicked = False
    except Exception as e:
      print(e)
  try:
    claims.clear()
    claimctr = claimctr + 1
    score = execute_with_retry(lambda: browser.find_element_by_link_text('(Report)'), tries)
    score.click()
    time.sleep(5)
    browser.switch_to.window(browser.window_handles[1])
    with open('assesmenturls.txt', 'a') as file:
      file.write(browser.current_url)
      file.write('\n')
    browser.close()
    if claimctr == 25:
      print("End of it")
      claimctr = 0
      nextclicks = nextclicks + 1

    browser.switch_to.window(browser.window_handles[0])

    logout = browser.find_element_by_class_name('username')
    logout.click()
    exit = execute_with_retry(lambda: browser.find_element_by_xpath("//*[contains(text(), 'Log out')]"), tries)
    exit.click()
  except Exception as e:
    print(e)
  time.sleep(3)

for i in range(1, 10):
  print('\a')
  time.sleep(1)
