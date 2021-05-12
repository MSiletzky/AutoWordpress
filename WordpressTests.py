# Import
import unittest
import random
import string
import time
from WordpressFunctions import *

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class WordPressProfileSmokeTest(unittest.TestCase):

    def setUp(self):
        #Set up computer specific file path
        DRIVER_PATH = "C:\Program Files (x86)\chromedriver.exe"

        self.driver = webdriver.Chrome(DRIVER_PATH)
        self.wait = WebDriverWait(self.driver, 10)

        loadWebPage(self.driver)

        # Check login
        login(self.driver)
        content_header = self.wait.until(
            EC.presence_of_element_located((By.TAG_NAME, "h1")))
        self.assertTrue(("My Profile") in content_header.text)

    def tearDown(self):
        self.driver.quit()

    # Test modifying and saving profile details - presumes successful login
    def test_save_changes(self):
        NOTICE_MESSAGE = "Settings saved successfully"
        save_button = self.wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "button.button.form-button.is-primary")))
        self.assertFalse(save_button.is_enabled())

        #Hold previous detail values
        time.sleep(1)
        first_name_text = self.wait.until(EC.visibility_of_element_located((By.ID, "first_name"))).get_attribute("defaultValue")
        last_name_text = self.driver.find_element_by_id(
            "last_name").get_attribute("defaultValue")
        display_name_text = self.driver.find_element_by_id(
            "display_name").get_attribute("defaultValue")
        description_text = self.driver.find_element_by_id(
            "description").get_attribute("defaultValue")

        #Add "test" to detail values, toggle hide profile and check save button
        change_and_save_profile_details(self.driver, first_name_text + "test",
                                        last_name_text + "test",
                                        display_name_text + "test",
                                        description_text + "test", True)
        notice = self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "notice__text")))
        self.assertIn(NOTICE_MESSAGE, notice.text)

        #Check for persistence after save
        self.driver.refresh()
        curr_first_name = self.wait.until(
            EC.element_to_be_clickable(
                (By.ID, "first_name"))).get_attribute("defaultValue")
        self.assertTrue(first_name_text + "test", curr_first_name)

        #Revert Changes
        change_and_save_profile_details(self.driver, first_name_text,
                                        last_name_text, display_name_text,
                                        description_text, True)
        self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "notice__text")))

    # Test changing profile picture
    def test_change_profile_picture(self):
        OLDPICPATH = "C:\Users\Max\Documents\OldPic.png"
        NEWPICPATH = "C:\Users\Max\Documents\NewPic.png"
        NOTICE_MESSAGE = "successfully uploaded a new profile photo"

        # Test uploading file
        change_profile_picture(self.driver, NEWPICPATH)
        notice = self.wait.until(
            EC.visibility_of_element_located((By.CLASS_NAME, "notice__text")))
        self.assertIn(NOTICE_MESSAGE, notice.text)
        self.driver.find_element_by_class_name("notice__dismiss").click()

        # Revert to previous image
        change_profile_picture(self.driver, OLDPICPATH)
        self.wait.until(
            EC.visibility_of_element_located((By.CLASS_NAME, "notice__text")))

    # Test adding and removing profile links
    def test_profile_links(self):
        URL = "Selenium.com"
        DESCRIPTION = "I'm a PRO"
        WEBPRESS_URL = "sunandstone136468616.wordpress.com"
        NOTICE_MESSAGE = "That link is already in your profile links"
        list_size = int(
            self.driver.find_element_by_class_name(
                "profile-links__list").get_attribute("childElementCount"))

        # Test adding url link
        add_url(self.driver, URL, DESCRIPTION)
        url_index = list_size + 1
        url_link = self.wait.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "li:nth-child(" + str(url_index) +
                 ") > a:nth-child(2) > span.profile-link__url")))
        self.assertIn(URL, url_link.text)

        # Test rejection of duplicate
        add_url(self.driver, URL, DESCRIPTION)
        notice = self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "notice__text")))
        self.assertIn(NOTICE_MESSAGE, notice.text)

        # Test adding wordpress link
        add_wordpress_site(self.driver)
        webpress_index = url_index + 1
        webpress_link = self.wait.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "li:nth-child(" + str(webpress_index) +
                 ") > a:nth-child(2) > span.profile-link__url")))
        self.assertIn(WEBPRESS_URL, webpress_link.text)

        # Test added link persistence
        self.driver.refresh()
        added_link = self.wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR,
                 "ul > li:nth-child(" + str(webpress_index) + ") > button ")))
        link_list = self.driver.find_element_by_class_name(
            "profile-links__list")
        self.assertEqual(webpress_index,
                         int(link_list.get_attribute("childElementCount")))

        # Test removal and persistence
        remove_link(self.driver, webpress_index)
        self.wait.until(EC.staleness_of(added_link))
        remove_link(self.driver, url_index)

        self.driver.refresh()
        link_list = self.wait.until(
            EC.visibility_of_element_located(
                (By.CLASS_NAME, "profile-links__list")))
        self.assertEqual(list_size,
                         int(link_list.get_attribute("childElementCount")))

unittest.main()