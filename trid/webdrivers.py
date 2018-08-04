from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

def download_complete(driver):
  last_url = driver.current_url
  if not driver.current_url.startswith("chrome://downloads"):
    driver.get("chrome://downloads/")
    js_commands = [
      r"var items = downloads.Manager.get().items_",
      r"if (items.every(e => e.state === 'COMPLETE')) {return items.map(e => e.file_url)}"
    ]
    script = ';'.join(js_commands)
    paths = driver.execute_script(script)
  driver.get(last_url)
  return paths

class ChromeDriver:

  CHROME_DRIVER = webdriver.Chrome
  CHROME_DRIVER_EXECUTABLE = r"C:\Program Files (x86)\Chromedriver\chromedriver.exe"
  CHROME_OPTIONS = Options
  WAITS = {'download_complete': download_complete}

  def __init__(self, headless=False, prompt_for_download = False, download_directory = None):
    self.headless = headless
    self.prompt_for_download = prompt_for_download
    self.download_directory = download_directory
    self.is_active = False

    # initialize chrome options
    self.options = self.CHROME_OPTIONS()
    self.set_preferences()

  def execute(self, commands):
    if not self.is_active:
      raise Exception("Chrome dirver not started.")
    return self.driver.execute_script(commands)

  def open(self, URL):
    if not self.is_active:
      raise Exception("Chrome dirver not started.")
    self.driver.get(URL)

  def set_headless(self, headless):
    self.headless = headless
    self.options.set_headless(headless = headless)

  def set_preferences(self,prefs=None):
    if not prefs:
      prefs = {
      "download.default_directory": self.download_directory,
      "download.prompt_for_download": self.prompt_for_download,
      "download.directory_upgrade": True,
      "safebrowsing.enabled": True,
      'profile.default_content_setting_values.automatic_downloads': 1
      }
    self.options.add_experimental_option("prefs",prefs)

  def start(self):
    self.driver = self.CHROME_DRIVER(
      options = self.options,
      executable_path = self.CHROME_DRIVER_EXECUTABLE
    )
    self.is_active = True
    
  def stop(self):
    self.driver.quit()
    self.driver = self.CHROME_DRIVER
    self.is_active = False

  @property
  def title(self):
    return self.driver.title

  def wait_for(self, wait_option, time_out=30, poll=0.5):
    wait = self.WAITS[wait_option]
    WebDriverWait(self.driver, time_out, poll).until(wait)

  def __enter__(self):
    self.driver = self.CHROME_DRIVER(
      options = self.options,
      executable_path = self.CHROME_DRIVER_EXECUTABLE
    )
    self.is_active = True
    return self

  def __exit__(self, exc_type=None, exc_val=None, exc_tb=None):
    self.driver.quit()
    self.is_active = False
    self.driver = self.CHROME_DRIVER

