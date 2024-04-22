import os
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class LinkedinBot:
    def __init__(self, position="Software Engineer", location="Germany"):
        self.position = position
        self.location = location
        self.page_number = 1
        self.setup_driver()

    def setup_driver(self):
        local_bin_directory = os.path.expanduser("~/bin")
        chrome_options = Options()
        chrome_options.add_argument("--user-data-dir=" + os.path.join(local_bin_directory, "chrome-data"))
        chrome_options.add_experimental_option("useAutomationExtension", False)
        self.driver = webdriver.Chrome(options=chrome_options)

        self.driver.get("https://linkedin.com/jobs")
    def sign_in(self):
        # Wait for the login form to be present
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "session_key"))
        )

        # Enter the user's email and password
        email_field = self.driver.find_element(By.ID, "session_key")
        password_field = self.driver.find_element(By.ID, "session_password")
        email_field.send_keys("YOUR_EMAIL")
        password_field.send_keys("YP_PASSWORD")

        # Submit the login form
        password_field.submit()

    def do_search(self):
        WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, "jobs-search-box__text-input"))
        )
        inputs = self.driver.find_elements(By.CLASS_NAME, "jobs-search-box__text-input")
        inputs[0].send_keys(self.position + '\n')
        time.sleep(5)
        self.enable_easy_apply()

    def enable_easy_apply(self):
        try:
            easy_apply_filter = self.driver.find_element(
                By.CLASS_NAME, 'search-reusables__filter-binary-toggle'
            )
            easy_apply_filter.find_element(By.TAG_NAME, 'button').click()
        except Exception as e:
            print("Easy Apply filter not found:", e)

    def click_easy_jobs(self):
        while True:
            job_list = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "jobs-search-results__list-item"))
            )
            for job in job_list:
                job.find_element(By.CLASS_NAME, 'job-card-list__title').click()
                if not self.apply_to_job():
                    break  # Exit if apply_to_job signals to stop
                WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, "artdeco-pagination__button--next"))
                ).click()
   
    def apply_to_job(self):
            try:
                WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, "jobs-apply-button"))
                ).click()
                # Handle application form by filling out and submitting the form
                # This part may require additional code specific to the application form
                return True
            except Exception as e:
                print("Issue applying to job:", e)
                return False
    def close(self):
        self.driver.quit()
    



if __name__ == "__main__":
    position = sys.argv[1] if len(sys.argv) > 1 else "Software Engineer"
    location = sys.argv[2] if len(sys.argv) > 2 else "France"
    bot = LinkedinBot(position, location)
    try:
        bot.do_search()
        bot.click_easy_jobs()
    finally:
        bot.close()