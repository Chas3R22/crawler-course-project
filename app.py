from flask import Flask, request, render_template
import requests
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.sentiment import SentimentIntensityAnalyzer
from urllib.robotparser import RobotFileParser
from urllib.parse import urlparse

# Download required NLTK resources
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('vader_lexicon')

app = Flask(__name__)


# Function to check robots.txt
def is_allowed_by_robots(url):
    try:
        parsed_url = urlparse(url)
        robots_url = f"{parsed_url.scheme}://{parsed_url.netloc}/robots.txt"

        rp = RobotFileParser()
        rp.set_url(robots_url)
        rp.read()

        return rp.can_fetch('*', url)
    except Exception as e:
        print(f"Error checking robots.txt: {e}")
        return False  # Default to disallow on failure


# Function to crawl, process text, extract metadata/images, and perform analysis
def crawl_and_process(url):
    try:
        # Check robots.txt
        if not is_allowed_by_robots(url):
            return {"error": "Crawling this website is disallowed by its robots.txt file."}

        # Fetch the web page content
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract Metadata
        title = soup.title.string if soup.title else "No title found"
        meta_description = soup.find('meta', attrs={'name': 'description'})
        meta_description_content = meta_description['content'] if meta_description else "No description found"
        meta_keywords = soup.find('meta', attrs={'name': 'keywords'})
        meta_keywords_content = meta_keywords['content'] if meta_keywords else "No keywords found"

        # Extract Images
        images = []
        for img in soup.find_all('img'):
            img_src = img.get('src')
            img_alt = img.get('alt', 'No alt text')
            if img_src:
                images.append({"src": img_src, "alt": img_alt})

        # Extract and analyze text
        paragraphs = soup.find_all('p')
        text = " ".join([para.get_text() for para in paragraphs])
        tokens = word_tokenize(text)
        tokens = [word.lower() for word in tokens if word.isalnum()]  # Remove punctuation
        stop_words = set(stopwords.words('english'))
        filtered_tokens = [word for word in tokens if word not in stop_words]

        # Get most common words
        freq_dist = nltk.FreqDist(filtered_tokens)
        common_words = freq_dist.most_common(10)  # Top 10 common words

        # Sentiment Analysis
        sia = SentimentIntensityAnalyzer()
        sentiment_scores = sia.polarity_scores(text)

        return {
            "title": title,
            "description": meta_description_content,
            "keywords": meta_keywords_content,
            "images": images[:10],  # Limit to 10 images for display
            "text": text[:1000],  # Limit to 1000 characters for display
            "common_words": common_words,
            "sentiment_scores": sentiment_scores,
        }
    except Exception as e:
        return {"error": str(e)}


# Routes
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/result', methods=['POST'])
def result():
    url = request.form.get('url')  # Get the URL from the form
    if not url:
        return render_template('result.html', error="Please provide a valid URL.")

    result = crawl_and_process(url)  # Crawl and process the website
    if "error" in result:
        return render_template('result.html', error=result["error"])

    return render_template(
        'result.html',
        title=result["title"],
        description=result["description"],
        keywords=result["keywords"],
        images=result["images"],
        text=result["text"],
        common_words=result["common_words"],
        sentiment_scores=result["sentiment_scores"],
        url=url
    )


if __name__ == '__main__':
    app.run(debug=True)
