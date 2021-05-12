import pyautogui
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException

# Loads the webpage
def loadWebPage(driver):
	driver.get("https://wordpress.com/me")

# Presumes successful loading of webpage
def login(driver):
    # Contains username and associated password
    PASSPATH = "C:\Users\Max\Documents\Login.txt"
    wait = WebDriverWait(driver, 10)

    with open(PASSPATH, 'r') as file:
        USERNAME = file.readline().rstrip('\n')
        PASSWORD = file.readline()

    # Enter username
    username_box = wait.until(
        EC.element_to_be_clickable((By.ID, "usernameOrEmail")))
    username_box.clear()
    username_box.send_keys(USERNAME)
    WebDriverWait(driver, 1).until(
        EC.text_to_be_present_in_element_value((By.ID, "usernameOrEmail"),
                                               USERNAME))
    username_box.submit()

    # Enter password
    password_box = wait.until(
        EC.visibility_of(driver.find_element_by_id("password")))
    password_box.clear()
    password_box.send_keys(PASSWORD)
    wait.until(
        EC.text_to_be_present_in_element_value((By.ID, "password"), PASSWORD))
    password_box.submit()


# Presumes successful login
def change_and_save_profile_details(driver, first_name, last_name,
                                    display_name, description, toggle_hide):
    wait = WebDriverWait(driver, 10)

    # Get text boxes and replace the text if not None
    first_name_box = wait.until(
        EC.visibility_of_element_located((By.ID, "first_name")))
    last_name_box = driver.find_element_by_id("last_name")
    display_name_box = driver.find_element_by_id("display_name")
    description_box = driver.find_element_by_id("description")
    hide_profile = driver.find_element_by_id("inspector-toggle-control-0")

    if (first_name is not None):
        first_name_box.clear()
        first_name_box.send_keys(first_name)

    if (last_name is not None):
        last_name_box.clear()
        last_name_box.send_keys(last_name)

    if (display_name is not None):
        display_name_box.clear()
        display_name_box.send_keys(display_name)

    if (description is not None):
        description_box.clear()
        description_box.send_keys(description)

    if (toggle_hide):
        hide_profile.click()

    # Save the details
    save_button = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "button.button.form-button.is-primary")))
    save_button.click()

# Presumes successful login
def change_profile_picture(driver, pic_path):
    driver.find_element_by_class_name("edit-gravatar__image-container").click()

    # Wait for native filer explorer to open
    time.sleep(2)

    # Work in file explorer
    pyautogui.write(pic_path)
    pyautogui.press('enter')
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.CLASS_NAME,
             "button.image-editor__buttons-button.is-primary"))).click()

# Presumes successful login
def add_url(driver, url, description):
    wait = WebDriverWait(driver, 10)

    # Click through menu buttons 
    wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "div.section-header__actions > button")))
    driver.find_elements_by_class_name("button.is-compact")[1].click()
    wait.until(
        EC.element_to_be_clickable((By.CLASS_NAME, "popover__menu-item")))
    driver.find_elements_by_class_name("popover__menu-item")[1].click()

    # Enter url information
    wait.until(
        EC.presence_of_element_located(
            (By.CLASS_NAME,
             "form-text-input.profile-links-add-other__value"))).send_keys(url)
    driver.find_element_by_class_name(
        "form-text-input.profile-links-add-other__title").send_keys(
            description)
    wait.until(
        EC.element_to_be_clickable(
            (By.CLASS_NAME,
             "button.profile-links-add-other__add.form-button.is-primary"
             ))).click()


# Presumes login and available wordpress site
def add_wordpress_site(driver):
    wait = WebDriverWait(driver, 10)
    driver.find_elements_by_class_name("button.is-compact")[1].click()
    wait.until(
        EC.element_to_be_clickable(
            (By.CLASS_NAME, "popover__menu-item"))).click()
    wait.until(
        EC.element_to_be_clickable(
            (By.CLASS_NAME,
             "profile-links-add-wordpress__checkbox.form-checkbox"))).click()
    driver.find_elements_by_class_name(
        "button.form-button.is-primary")[1].click()

# Presumes successful login and valid url link index
def remove_link(driver, index):
    remove_link_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR,
             "ul > li:nth-child(" + str(index) + ") > button ")))

    # Site design requires java script execution for click
    driver.execute_script("arguments[0].click();", remove_link_button)