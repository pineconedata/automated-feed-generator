import os
import pytz
import time
import json
import argparse
from datetime import datetime
from selenium import webdriver
from selenium.webdriver import FirefoxOptions
from selenium.webdriver.common.by import By
from feedgen.feed import FeedGenerator


def scrape_and_generate_rss(config):
    # Parse all of the settings from the configuration dictionary
    website_url = config['website_url']
    website_title = config['website_title']
    website_description = config['website_description']
    elements_selector = config['elements_selector']
    title_selector = config['title_selector']
    link_selector = config['link_selector']
    image_selector = config['image_selector']
    description_selector = config['description_selector']
    date_selector = config['date_selector']
    date_format = config['date_format']

    # Initialize a headless Firefox WebDriver for Selenium
    opts = FirefoxOptions()
    opts.add_argument("--headless")
    driver = webdriver.Firefox(options=opts)

    # Navigate to the specified website URL and wait for any dynamic content to load
    driver.get(website_url)
    time.sleep(2)

    # Create an RSS feed using FeedGenerator
    fg = FeedGenerator()
    fg.title(website_title)
    fg.link(href=website_url, rel='alternate')
    fg.description(website_description)

    # Find and iterate through the elements on the web page
    elements = driver.find_elements(By.CSS_SELECTOR, elements_selector)
    for element in elements:
        # Extract information about each item (title, link, description, date, etc.)
        item_title = element.find_element(By.CSS_SELECTOR, title_selector).text
        item_link = element.find_element(By.CSS_SELECTOR, link_selector).get_attribute('href')
        image_link = element.find_element(By.CSS_SELECTOR, image_selector).get_attribute('src')
        item_description = f'<p>{element.find_element(By.CSS_SELECTOR, description_selector).text}</p>'
        item_description += f'<img src="{image_link}" alt="{item_title}">'
        item_date = element.find_element(By.CSS_SELECTOR, date_selector).text
        item_date = datetime.strptime(item_date, date_format).replace(tzinfo=pytz.utc)

        # Create a new entry for the item in the RSS feed
        fe = fg.add_entry()
        fe.title(item_title)
        fe.link(href=item_link)
        fe.guid(item_link)
        fe.description(item_description)
        fe.pubDate(item_date)

    # Generate the RSS feed and return it as a string
    rss_feed = fg.rss_str(pretty=True)

    # Close the WebDriver
    driver.quit()

    return rss_feed


if __name__ == "__main__":
    # Create an argument parser for command-line options
    parser = argparse.ArgumentParser(description="Scrape a website and generate an RSS feed.")

    # Add and parse a  command-line argument for specifying the path to the configuration file 
    parser.add_argument('--config_file', required=True, help="Path to the configuration file")
    args = parser.parse_args()

    # Open and read the specified configuration file that contains the website and scraping parameters
    with open(args.config_file, 'r') as config_file:
        config = json.load(config_file)

    # Scrape website and generate the RSS feed
    rss_feed = scrape_and_generate_rss(config)

    # Save the generated RSS feed to a file
    if rss_feed:
        file_name = f'{"".join(x for x in config["website_title"] if x.isalnum())}.xml'
        with open(f'{os.path.join("feeds", file_name)}', 'wb') as rss_file:
            rss_file.write(rss_feed)
        print(f'RSS feed generated and saved as "{file_name}".')