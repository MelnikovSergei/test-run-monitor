import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

def setup_chrome_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run Chrome in headless mode
    chrome_options.add_argument("--no-sandbox")  # Bypass OS security model
    chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
    chrome_options.add_argument("--disable-gpu")  # Applicable for running in Linux
    chrome_options.add_argument("--window-size=1920x1080")  # Set window size if needed
    return webdriver.Chrome(options=chrome_options)

@pytest.fixture
def browser():
    driver = setup_chrome_driver()  # Or use webdriver.Firefox() for Firefox
    driver.get("http://127.0.0.1:5000")  # Replace with your app's URL
    yield driver
    driver.quit()

# Test loading of the main page
def test_load_main_page(browser):
    assert "Test Run Monitor" in browser.title

# Test adding a new project
def test_add_project(browser):
    project_input = browser.find_element(By.ID, "addProjectInput")
    project_input.send_keys("Test Project")
    project_input.send_keys(Keys.ENTER)

    time.sleep(1)  # Wait for the project to be added

    # Verify that the project appears in the sidebar
    projects = browser.find_elements(By.CSS_SELECTOR, ".menu-item a")
    assert any("Test Project" in p.text for p in projects)

# Test removing a project
def test_remove_project(browser):
    # Assuming we added "Test Project" in the previous test
    project_input = browser.find_element(By.ID, "addProjectInput")
    project_input.send_keys("Project to Remove")
    project_input.send_keys(Keys.ENTER)

    time.sleep(1)  # Wait for the project to be added

    # Select the project we just added
    project_links = browser.find_elements(By.CSS_SELECTOR, ".menu-item a")
    for project in project_links:
        if "Project to Remove" in project.text:
            project.click()
            break

    time.sleep(1)  # Wait for the project selection

    # Click the remove button
    remove_button = browser.find_element(By.ID, "removeProjectBtn")
    remove_button.click()

    # Wait for the project to be removed
    time.sleep(1)

    # Check that the project is no longer in the list
    projects = browser.find_elements(By.CSS_SELECTOR, ".menu-item a")
    assert all("Project to Remove" not in p.text for p in projects)

# Test adding a new test suite
def test_add_test_suite(browser):
    # Add a new project first
    project_input = browser.find_element(By.ID, "addProjectInput")
    project_input.send_keys("Test Project with Suites")
    project_input.send_keys(Keys.ENTER)

    time.sleep(1)

    # Select the project we just added
    project_links = browser.find_elements(By.CSS_SELECTOR, ".menu-item a")
    for project in project_links:
        if "Test Project with Suites" in project.text:
            project.click()
            break

    time.sleep(1)

    # Add a test suite to the project
    suite_input = browser.find_element(By.ID, "addTestSuiteInput")
    suite_input.send_keys("Test Suite 1")
    suite_input.send_keys(Keys.ENTER)

    time.sleep(1)

    # Verify the suite is added in the main area
    suites = browser.find_elements(By.CSS_SELECTOR, ".suite-item")
    assert any("Test Suite 1" in suite.text for suite in suites)

# Test changing the test suite status
def test_update_test_suite_status(browser):
    # Add a new project and test suite first
    project_input = browser.find_element(By.ID, "addProjectInput")
    project_input.send_keys("Project with Status Test")
    project_input.send_keys(Keys.ENTER)

    time.sleep(1)

    # Select the project we just added
    project_links = browser.find_elements(By.CSS_SELECTOR, ".menu-item a")
    for project in project_links:
        if "Project with Status Test" in project.text:
            project.click()
            break

    time.sleep(1)

    # Add a test suite to the project
    suite_input = browser.find_element(By.ID, "addTestSuiteInput")
    suite_input.send_keys("Status Test Suite")
    suite_input.send_keys(Keys.ENTER)

    time.sleep(1)

    # Open the test suite details
    suite_divs = browser.find_elements(By.CSS_SELECTOR, ".suite-item")
    for suite_div in suite_divs:
        if "Status Test Suite" in suite_div.text:
            suite_div.click()
            break

    time.sleep(1)

    # Change the status to 'in progress'
    in_progress_button = browser.find_element(By.ID, "inProgressBtn")
    in_progress_button.click()

    time.sleep(1)

    # Verify that the status is updated in the main area
    suite_divs = browser.find_elements(By.CSS_SELECTOR, ".suite-item")
    assert any("in_progress" in suite.text for suite in suite_divs)

# Test removing a test suite
def test_remove_test_suite(browser):
    # Add a new project and test suite first
    project_input = browser.find_element(By.ID, "addProjectInput")
    project_input.send_keys("Project with Suite Removal")
    project_input.send_keys(Keys.ENTER)

    time.sleep(1)

    # Select the project we just added
    project_links = browser.find_elements(By.CSS_SELECTOR, ".menu-item a")
    for project in project_links:
        if "Project with Suite Removal" in project.text:
            project.click()
            break

    time.sleep(1)

    # Add a test suite to the project
    suite_input = browser.find_element(By.ID, "addTestSuiteInput")
    suite_input.send_keys("Suite to Remove")
    suite_input.send_keys(Keys.ENTER)

    time.sleep(1)

    # Open the test suite details
    suite_divs = browser.find_elements(By.CSS_SELECTOR, ".suite-item")
    for suite_div in suite_divs:
        if "Suite to Remove" in suite_div.text:
            suite_div.click()
            break

    time.sleep(1)

    # Click the remove test suite button
    remove_suite_button = browser.find_element(By.ID, "removeSuiteBtn")
    remove_suite_button.click()

    time.sleep(1)

    # Verify that the suite has been removed from the main area
    suite_divs = browser.find_elements(By.CSS_SELECTOR, ".suite-item")
    assert all("Suite to Remove" not in suite.text for suite in suite_divs)
