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
    posts_list_selector = config['posts_list_selector']
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

    # Find and iterate through the list of posts on the web page
    posts_list = driver.find_elements(By.CSS_SELECTOR, posts_list_selector)
    for post in posts_list:
        # Extract information about each post (title, link, description, date, etc.)
        post_title = post.find_element(By.CSS_SELECTOR, title_selector).text
        post_link = post.find_element(By.CSS_SELECTOR, link_selector).get_attribute('href')
        image_link = post.find_element(By.CSS_SELECTOR, image_selector).get_attribute('src')
        post_description = f'<p>{post.find_element(By.CSS_SELECTOR, description_selector).text}</p>'
        post_description += f'<img src="{image_link}" alt="{post_title}">'
        post_date = post.find_element(By.CSS_SELECTOR, date_selector).text
        post_date = datetime.strptime(post_date, date_format).replace(tzinfo=pytz.utc)

        # Create a new entry in the RSS feed for each post
        fe = fg.add_entry()
        fe.title(post_title)
        fe.link(href=post_link)
        fe.guid(post_link)
        fe.description(post_description)
        fe.pubDate(post_date)

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
    with open(os.path.join("config", args.config_file), 'r') as config_file:
        config = json.load(config_file)

    # Scrape website and generate the RSS feed
    rss_feed = scrape_and_generate_rss(config)

    # Save the generated RSS feed to a file
    if rss_feed:
        file_name = f'{"".join(x for x in config["website_title"] if x.isalnum())}.xml'
        with open(f'{os.path.join("feeds", file_name)}', 'wb') as rss_file:
            rss_file.write(rss_feed)
        print(f'RSS feed generated and saved as "{file_name}".')