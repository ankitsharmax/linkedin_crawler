import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

def manual_login(driver):
    driver.get("https://www.linkedin.com/login")
    print("🔐 Please log in manually within 90 seconds...")
    time.sleep(90)  # Wait for manual login (adjust if needed)

def linkedin_search(driver, search_query):
    search_box = driver.find_element(By.CSS_SELECTOR, "input.search-global-typeahead__input")
    search_box.clear()
    search_box.send_keys(search_query)
    search_box.send_keys(Keys.RETURN)
    time.sleep(5)

def scrape_search_results(driver):
    profiles = []
    results = driver.find_elements(By.CSS_SELECTOR, "div.entity-result__content")

    for result in results:
        try:
            name_elem = result.find_element(By.CSS_SELECTOR, "span.entity-result__title-text a span[aria-hidden='true']")
            headline_elem = result.find_element(By.CSS_SELECTOR, "div.entity-result__primary-subtitle")
            name = name_elem.text.strip()
            headline = headline_elem.text.strip()
            profiles.append({"name": name, "headline": headline})
        except Exception:
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
    SEARCH_QUERY = "ankit sharma meesho"

    options = uc.ChromeOptions()
    options.add_argument("--start-maximized")

    driver = uc.Chrome(options=options)

    try:
        manual_login(driver)  # Wait for you to log in manually
        linkedin_search(driver, SEARCH_QUERY)

        all_profiles = []
        for _ in range(3):  # Adjust number of pages if needed
            profiles = scrape_search_results(driver)
            all_profiles.extend(profiles)
            if not go_to_next_page(driver):
                break

        print(f"✅ Found {len(all_profiles)} profiles:")
        for profile in all_profiles:
            print(f"Name: {profile['name']}")
            print(f"Headline: {profile['headline']}")
            print("-" * 40)

    finally:
        driver.quit()

if __name__ == "__main__":
    main()
