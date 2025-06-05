from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

def linkedin_login(driver, username_str, password_str):
    driver.get("https://www.linkedin.com/login")
    time.sleep(3)
    
    username = driver.find_element(By.ID, "username")
    password = driver.find_element(By.ID, "password")
    
    username.send_keys(username_str)
    password.send_keys(password_str)
    password.send_keys(Keys.RETURN)
    
    time.sleep(5)  # wait for login to complete

def linkedin_search(driver, search_query):
    search_box = driver.find_element(By.CSS_SELECTOR, "input.search-global-typeahead__input")
    search_box.clear()
    search_box.send_keys(search_query)
    search_box.send_keys(Keys.RETURN)
    time.sleep(5)

def scrape_search_results(driver):
    profiles = []
    # Find all search result containers
    results = driver.find_elements(By.CSS_SELECTOR, "div.entity-result__content")
    
    for result in results:
        try:
            name_elem = result.find_element(By.CSS_SELECTOR, "span.entity-result__title-text a span[aria-hidden='true']")
            headline_elem = result.find_element(By.CSS_SELECTOR, "div.entity-result__primary-subtitle")
            
            name = name_elem.text.strip()
            headline = headline_elem.text.strip()
            profiles.append({"name": name, "headline": headline})
        except Exception as e:
            # Skip results where info isn't found
            continue
    
    return profiles

def go_to_next_page(driver):
    try:
        next_button = driver.find_element(By.CSS_SELECTOR, "button.artdeco-pagination__button--next")
        if next_button.is_enabled():
            next_button.click()
            time.sleep(5)
            return True
        else:
            return False
    except:
        return False

def main():
    # Your LinkedIn credentials here
    USERNAME = "your_email@example.com"
    PASSWORD = "your_password"
    SEARCH_QUERY = "John Doe"
    
    # Setup Chrome driver
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)
    
    try:
        linkedin_login(driver, USERNAME, PASSWORD)
        linkedin_search(driver, SEARCH_QUERY)
        
        all_profiles = []
        
        for _ in range(3):  # scrape 3 pages max, adjust as needed
            profiles = scrape_search_results(driver)
            all_profiles.extend(profiles)
            if not go_to_next_page(driver):
                break
        
        print(f"Found {len(all_profiles)} profiles:")
        for profile in all_profiles:
            print(f"Name: {profile['name']}")
            print(f"Headline: {profile['headline']}")
            print("-" * 40)
    
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
