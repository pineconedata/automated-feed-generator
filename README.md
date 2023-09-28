# Web Scraper and RSS Generator

This Python script allows you to scrape content from a website and generate an RSS feed. It's a flexible tool that can be configured to work with different websites and data sources. You can easily set up your web scraping and RSS feed generation by defining parameters in a JSON configuration file.

## Features

- **Website Scraping**: Scrape content from a specified website using Selenium.

- **RSS Feed Generation**: Create an RSS feed of the scraped content using the `feedgen` library.

- **Command-Line Interface**: Configure and run the script with command-line arguments and a configuration file.

## Prerequisites

Before using this tool, you need to have the following installed on your system:

- [Python](https://www.python.org/downloads/) (version 3.6 or higher)

- [Selenium](https://pypi.org/project/selenium/) (Python library for web scraping)

- [Firefox WebDriver](https://github.com/mozilla/geckodriver) (for headless web scraping)

- [feedgen](https://pypi.org/project/feedgen/) (Python library for RSS feed generation)

Additional details about dependencies and version numbers can be found in the `requirements.txt` file. 

## Usage

1. Clone this repository to your local machine:

```shell
git clone https://github.com/pineconedata/automated-feed-generator.git
cd automated-feed-generator
```

2. Create a configuration file (e.g., config.json) in the `config` directory of the repository. You can use the provided JSON configuration as a template and adjust the values to match your target website and scraping requirements. 

3. Run the script with the configuration file as a command-line argument:

```shell
python3 automated_feed_generator.py --config_file 'config.json'
```
- `--config_file`: Path to the configuration file you created in step 2.

4. The script will scrape the website, generate an RSS feed, and save it as an XML file in the `feeds` directory. The filename is derived from the website title, and any non-alphanumeric characters are removed.

## Configuration File 

The configuration file (e.g., `config.json`) should contain the following parameters:

- `website_url`: URL of the website to scrape.
- `website_title`: Title for the RSS feed.
- `website_description`: Description for the RSS feed.
- `posts_list_selector`: CSS selector for the list of posts to include in the RSS feed. This selector goes inside of a `document.querySelectorAll(elements_selector)` call. 
- `title_selector`: CSS selector for the title of each element. This selector goes inside of a `.querySelector()` call that is run on each post element.
- `link_selector`: CSS selector for the link of each element. This selector goes inside of a `.querySelector()` call that is run on each post element.
- `image_selector`: CSS selector for the image of each element. This selector goes inside of a `.querySelector()` call that is run on each post element.
- `description_selector`: CSS selector for the description of each element. This selector goes inside of a `.querySelector()` call that is run on each post element.
- `date_selector`: CSS selector for the date of each element. This selector goes inside of a `.querySelector()` call that is run on each post element.
- `date_format`: Date format of the date on the web page. This is used in conjunction with the `date_selector` to convert the date string to a datetime object using the [strptime](https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior) method. 

Adjust the arguments within this configuration file to match the website you want to scrape and the selectors you want to use.

### Example Configuration

An example configuration file for scraping the webpage of [NASA's Space Station Blog](https://blogs.nasa.gov/spacestation/) is provided in this repository as the `NASASpaceStationBlog.json` file in the `config` directory.

Here's an example of an empty configuration file for easy copy-pasting. 

```json
{
  "website_url": "",
  "website_title": "",
  "website_description": "",
  "posts_list_selector": "",
  "title_selector": "",
  "link_selector": "",
  "image_selector": "",
  "description_selector": "",
  "date_selector": "",
  "date_format": ""
}
```

## Cron Job Scheduling

To keep your feed up-to-date, we recommend scheduling this Python script as a cron job. You can use any cron job manager you like, but the example provided below works with [crontab](https://man7.org/linux/man-pages/man5/crontab.5.html).

1. Open your crontab configuration by running `crontab -e` as usual. 

2. Add a cron job entry to schedule the script at your desired frequency. For example, to run the script every day at 2:00 AM, you can add the following line:

```bash
0 2 * * * python3 /path/to/your/script/directory/automated-feed-generator.py --config_file '/path/to/your/script/directory/config/NASASpaceStationBlog.json'
```

* Make sure to replace `/path/to/your/script/directory/` with the actual directory where your Python script (`automated_feed_generator.py`) is located. 

- Add a separate line to your crontab file for each job that you want to schedule (typically one per configuration file).

## License

This project is licensed under the GNU General Public License v3.0 - see the LICENSE file for details.

## Contributing 

If you'd like to contribute to this project or report issues, please open a pull request or create an issue in the repository. Feel free to add a feed that you have generated to the `feeds` folder via pull request as well. 
