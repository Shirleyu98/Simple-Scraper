
This is a simple web crawler project combining `Selenium` and `BeautifulSoup` to fetch and parse HTML content.

**Features:**

1. Automatically opens and logs into a website.
2. Scrapes specified text and saves it to a text file.
3. Scrapes images, fetches URLs, and downloads them into `src/`.

**Setup Instructions:**

1. Run `pip install -r requirements.txt` to install dependencies.
2. Navigate to the `src` folder: `cd src`.
3. Update `config.json` with your `username`, `password`, `target_urls`, and Chrome profile directory.
4. Uncomment the functions you need.
5. Adjust the selectors, class names, or tag names for targeted scraping.
6. Run the crawler with `python web_crawler.py`.

**Note:**  
If you want the program to load specific Chrome profile data automatically, set your profile path in `config.json` (usually ending in `\\User Data`):

```
{

"user_data_dir":"your profile location"

}

```