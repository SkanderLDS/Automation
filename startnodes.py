from selenium import webdriver
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import IEDriverManager
from selenium.webdriver.common.by import By
import time

# Configure the WebDriver
service = Service(IEDriverManager().install())
driver = webdriver.Edge(service=service)

try:
    # Open EVE-NG login page
    driver.get("http://192.168.192.200/#!/login")

    # Perform login
    driver.find_element(By.NAME, "username").send_keys("admin")
    driver.find_element(By.NAME, "password").send_keys("eve")
    driver.find_element(By.XPATH, "//button[contains(text(), 'Login')]").click()

    # Wait for login to complete
    time.sleep(10)

    # Navigate to the lab
    driver.get("http://192.168.192.200/legacy/LAB-AUTO.unl/topology")

    # Wait for the lab page to load
    time.sleep(10)

    # Start all nodes (this assumes there is a "Start All Nodes" button or equivalent)
    try:
        start_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Start All Nodes')]")
        start_button.click()
        print("Started all nodes successfully!")
    except Exception as e:
        print("Failed to start nodes:", e)

    # Wait for the nodes to start
    time.sleep(30)

finally:
    # Close the WebDriver
    driver.quit()
