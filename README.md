# crawler-course-project
 A web scraper that crawls through a website to round up its metadata, most used words, a sentiment analysis and a roundup of images.

How to run:
1. Install dependancies

Open a terminal window in your IDE of choice. Make sure you have pip already installed, then run the following commands:

```
pip install Flask
```

```
pip install nltk
```

```
pip install requests
```

```
pip install BeautifulSoup
```

2. Run the project

Type the following command in your terminal to run the program:

```
python app.py
```

To access the website, make sure you read the console to check where the project just ran on. It should be something like "http://127.0.0.1:5000".

3. Using the project

Once you arrive at the landing page, supply the text box with a url of a website and press the submit button.
It will take you to the results page, where it will display the output. If the website has robots.txt present, the site may not be crawled at all.

