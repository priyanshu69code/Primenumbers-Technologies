# Required Libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv
# Function to scrape project details


def scrape_registered_projects(url):
    # Set up Selenium
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # To run Chrome in headless mode

    driver = webdriver.Chrome(options=options)
    results = []

    # Open the website
    driver.get(url)
    # Allowing time for dynamic content to load (adjust as needed)
    time.sleep(60)

    # Click on the "Registered Projects" tab
    for i in range(1, 7):
        registered_tab = driver.find_element(
            By.XPATH, f'//*[@id="reg-Projects"]/div/div/div[{i}]/div/div/a')
        registered_tab.click()
        time.sleep(15)  # Wait for the content to load

        try:
            gstin = driver.find_element(
                By.XPATH, "//td[contains(text(), 'GSTIN No.')]/following-sibling::td/span").text
            if gstin == "":
                gstin = "-NA-"
        except:
            gstin = "-NA-"

        name = driver.find_element(
            By.XPATH, "//td[contains(text(), 'Name')]/following-sibling::td").text
        pan = driver.find_element(
            By.XPATH, "//td[contains(text(), 'PAN No.')]/following-sibling::td/span").text
        p_address = driver.find_element(
            By.XPATH, "//td[contains(text(), 'Permanent Address')]/following-sibling::td/span").text

        results.append({
            "Name": name,
            "GSTIN": gstin,
            "PAN": pan,
            "Permanent Address": p_address
        })

        close = driver.find_element(
            By.XPATH, '//*[@id="modal-data-display-tab_project_main"]/div/div/div[3]/button')
        close.click()
        time.sleep(5)

    # Close the Selenium WebDriver
    driver.quit()

    return results

# Main function to run the scraper


def main():
    url = 'https://hprera.nic.in/PublicDashboard'
    project_data = scrape_registered_projects(url)

    # Save the results to a CSV file
    csv_filename = "project_data.csv"
    csv_headers = ["Name", "GSTIN", "PAN", "Permanent Address"]

    with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=csv_headers)
        writer.writeheader()
        for data in project_data:
            writer.writerow(data)

    print(f"Data has been saved to {csv_filename}")


# Run the main function
if __name__ == "__main__":
    main()
