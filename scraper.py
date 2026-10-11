#-------------------------------------------------------------------------
# AUTHOR: Andrew Mazmanian
# FILENAME: scraper.py
# SPECIFICATION: A simple web crawler to scrape links from a seed URL
# FOR: CS 4250 - Assignment #2
# TIME SPENT: 10 hours
#-------------------------------------------------------------------------

# Importing Python libraries
import requests
from bs4 import BeautifulSoup

# Defining the seed URL
seed = "https://testingurl.dev/scraping/links/circular"
baseURL = "https://testingurl.dev"

# Creating the frontier and seen collections
frontier = [seed] # for URLs to be crawled (FIFO)
seen = [seed] # every URL added to the frontier is also added to seen


# Crawling until the frontier is empty
while frontier:

    # Removing the first URL from the frontier
    url = frontier.pop(0)


    # Retrieving and parsing the Web page
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error retrieving {url}: {e}")
        continue

    soup = BeautifulSoup(response.text, 'html.parser')


    # Printing the text contained in the <h1> element
    h1 = soup.find('h1')
    if h1 is not None:
        print(h1.get_text())
    else:
        print("No <h1> element found at", url)
    


    # Extracting and processing hyperlinks
    links = []
    for a in soup.find_all("a"):
        #Skipping <a> tags that do not have an href attribute
        href = a.get("href")
        if href is None:
            continue
        #Removing any #fragment from the URL so that the same page is not crawled multiple times
        href = href.split('#')[0]
        if href == "":
            continue
        #Converting relative to absolute URLs
        if href[:7] == "http://" or href[:8] == "https://":
            link = href
        elif href[0] == "/":
            link = baseURL + href
        else:
            link = url.rsplit('/', 1)[0] + '/' + href
        #Following only hyperlinks that belong to the Circular Links section
        if link[:len(seed)] == seed:
            links.append(link)

    links.sort()
    for link in links:
        if link not in seen:
            seen.append(link)
            frontier.append(link)

        

# Printing all URLs in seen
print("\nURLs in seen:")
for url in seen:
    print(url)