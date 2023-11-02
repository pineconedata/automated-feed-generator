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

- `website_url`: *Required*, URL of the website to scrape.
- `website_title`: *Required*, Title for the RSS feed.
- `website_description`: *Required*, Description for the RSS feed.
- `posts_list_selector`: *Required*, CSS selector for the list of posts to include in the RSS feed. 
- `title_selector`: *Required*, CSS selector for the title of each element.
- `link_selector`: *Required*, CSS selector for the link of each element.
- `image_selector`: *Optional*, CSS selector for the image of each element.
- `description_selector`: *Optional*, CSS selector for the description of each element.
- `description_type`: *Optional*, Determines if the description should pull from the `text` or `innerHTML` attribute of the element located via the `description_selector`. Certain RSS readers can have issues with HTML description content, so the default is `text`. 
- `date_selector`: *Optional - if specified, `date_format` is required*, CSS selector for the date of each element.
- `date_format`: *Optional - if specified, `date_selector` is required*, Date format of the date on the web page. This is used in conjunction with the `date_selector` to convert the date string to a datetime object using the [strptime](https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior) method.
- `file_name`: *Optional*, Name of the output feed file. If not specified, the alphanumeric characters of `website_title` will be used instead.

Adjust the arguments within this configuration file to match the website you want to scrape and the selectors you want to use.

### Selector Logic

At a high level, the script will first identify the list of posts to include in the RSS feed by using `posts_list_selector` (where `document.querySelectorAll(posts_list_selector)` should return the same number of HTML elements as the number of posts that should be included in your output RSS feed's content). Using the `document.querySelectorAll()` method is one of the quickets ways to identify your desired `posts_list_selector` valkue. MDN has additional details on the [`document.querySelectorAll()` method](https://developer.mozilla.org/en-US/docs/Web/API/Document/querySelectorAll) if you are not familiar with it.

Then, the script will scrape the details of each post using the other selectors (`title_selector`, `link_selector`, `image_selector`, `description_selector`, and `date_selector`. The selectors for the post details (`title_selector`, `link_selector`, etc.) are sub-selectors of the `posts_list_selector`. For example, this sub-selector logic for the `title_selector` would be implemented in JavaScript as `document.querySelectorAll(posts_list_selector)...querySelector(title_selector)` (this script uses Python and Selenium, but the JS logic can be helpful for identifying the proper value of `title_selector`, etc. more quickly). MDN has additional details on the [`document.querySelector()` method](https://developer.mozilla.org/en-US/docs/Web/API/Document/querySelector) as well if you are not familiar with it.

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
  "description_type": "",
  "date_selector": "",
  "date_format": "",
  "file_name": ""
}
```

## Scheduling

To keep your feed up-to-date, we recommend scheduling this Python script to run regularly. There are a variety of ways to do this, but the simplest example is setting it up as a cron job. You can use any cron job manager you like, but the example provided below works with [crontab](https://man7.org/linux/man-pages/man5/crontab.5.html).

1. Open your crontab configuration by running `crontab -e` as usual. 

2. Add a cron job entry to schedule the script at your [desired frequency](https://crontab.guru]. For example, to run the script every day at 2:00 AM, you can add the following line:

```bash
0 2 * * * python3 /path/to/your/script/directory/automated-feed-generator.py --config_file '/path/to/your/script/directory/config/NASASpaceStationBlog.json'
```

* Make sure to replace `/path/to/your/script/directory/` with the actual directory where your Python script (`automated_feed_generator.py`) is located. 

- Add a separate line to your crontab file for each job that you want to schedule (typically one per configuration file).

Alternatively, you might want to run this Python script for all of the configuration files in the `config` directory at once and add only one line to your crontab configuration. In that case, you can move the Python script into a Shell script, like this: 
```bash
#!/bin/bash
cd ~/path/to/dir/automated-feed-generator

# Directory containing configuration files
configs_dir="config"

# Iterate over each file in the configs directory
for config_file in "$configs_dir"/*.json; do
    if [ -e "$config_file" ]; then
        # Extract the file name without the directory path
        config_file_name=$(basename "$config_file")

        echo "Processing $config_file_name..."
        python3 automated_feed_generator.py --config_file "$config_file_name"
    fi
done
```

Then, you can add this script as a single cron job that will update all of the feeds at once. Here's an example of scheduling this script to run daily: 

```bash
@daily ~/path/to/dir/automated_feed_generator.sh
```

Now each `config_file.json` in the `config` directory will be passed to the `automated_feed_gneerator.py` script and will output a resulting file in the `feeds` directory. The only thing left is to host your `feeds` directory somewhere that a RSS feed reader can pull from (including GitHub, see the [Contributing](#Contributing) section below if you would like to subscribe to feeds generated in this repo).  

## Limitations

- **iFrames**: This script does not out-of-the-box support selectors that are within [iframes](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/iframe).
    - However, there could be ways around this limitation, depending on the site structure and iframe details. A first step might be to fork this repo and modify the `posts_list = driver.find_elements(By.CSS_SELECTOR, posts_list_selector)` logic to something like `posts_list = driver.find_element(By.CSS_SELECTOR, iframe_selector).find_elements(By.CSS_SELECTOR, posts_list_selector)`. Note that this example logic is untested and might not work in all scenarios. 
- **Shadow DOMs**: This script does not out-of-the-box support selectors that are within [shadow DOMs](https://developer.mozilla.org/en-US/docs/Web/API/Web_components/Using_shadow_DOM).
    - Similar to iframes, there could be ways around this limitation. One possible solution might involve selecting the shadow DOM element and then selecting the posts_list (in JavaScript, this would look something like `document.querySelector(shadow_dom_selector).shadowRoot.querySelectorAll(posts_list_selector)`). 
- **Blocking**: This script is meant to be run at a low-volume (once per day) from a personal machine that has access to the website that you are scraping. This is not intended to be used for any malicious purposes, and, as such, no steps have been taken to ensure that the website owner does not block or tarpit your traffic.
    - Your traffic typically will not get blocked from running this script once per day. However, website owners have different policies and some might be more aggressive about blocking traffic (such as blocking all Linux+Firefox traffic). If you are concerned about getting blocked, then there is plenty of additional logic that could be added to this script to mitigate those risks.

## License

This project is licensed under the GNU General Public License v3.0 - see the LICENSE file for details.

## Contributing 

If you'd like to contribute to this project or report issues, please open a pull request or create an issue in the repository. Feel free to add a feed that you have generated to the `feeds` folder via pull request as well. Once your pull request is approved, you can subscribe to the URL in your RSS reader directly from this GitHub repo. To get the URL, simply navigate to the appropriate output file in the `feeds` folder in this GitHub repository, click on `Raw` in the top right corner of the file, and then copy/paste the resulting URL into your RSS feed reader (the URL should begin with something like `https://raw.githubusercontent.com/pineconedata/automated-feed-generator/`). 
