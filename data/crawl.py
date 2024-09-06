import requests
from bs4 import BeautifulSoup

# The URL of the page you want to scrape
url = "https://machinelearningcoban.com/2016/12/28/linearregression/"

# Send a request to fetch the content of the page
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the page content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the div with itemprop="articleBody"
    main_content = soup.find('div', {'itemprop': 'articleBody'})
    
    if main_content:
        # Get all the text content from the article body
        page_text = main_content.get_text()

        # Clean up the text: remove extra line breaks and whitespace
        clean_text = "\n".join([line.strip() for line in page_text.splitlines() if line.strip()])

        # Save the cleaned text into a single file
        with open("linearregression.txt", "w", encoding='utf-8') as file:
            file.write(clean_text)
        print("Content saved to 'article_content.txt'.")
    else:
        print("Could not find the article body.")
else:
    print(f"Failed to retrieve content. Status code: {response.status_code}")
