import csv
import requests
from bs4 import BeautifulSoup
import time

# Set the base URL to crawl
base_url = 'https://.com'

# Set the limit of requests per minute
request_limit = 10

# Set the time delay between requests
time_delay = 60 / request_limit

# Initialize an empty list to store the links and their corresponding pages
links = [(base_url, base_url)]

# Initialize a set to store visited links
visited_links = set()

# Loop through each page of the website and extract the links
while links:
    # Get the next link to check
    link, page = links.pop(0)

    # Check if the link has already been visited
    if link in visited_links:
        continue

    print(f"Requesting {link}...")

    # Set the start time of the request
    start_time = time.time()

    try:
        # Make the HTTP request and retrieve the page HTML
        response = requests.get(link)
        html_page = response.content

        # Parse the HTML using BeautifulSoup
        soup = BeautifulSoup(html_page, 'html.parser')

        # Extract the links from the HTML using BeautifulSoup
        for link_tag in soup.findAll('a'):
            href = link_tag.get('href')
            if href and href.startswith(base_url):
                links.append((href, link))

        # Add the current link to the set of visited links
        visited_links.add(link)

    except (requests.exceptions.RequestException) as error:
        # Handle errors that occur during the request process
        print(f"Error while requesting {link}: {error}")

    # Wait for the remaining time until the request limit is reached
    end_time = time.time()
    time_elapsed = end_time - start_time
    if time_elapsed < time_delay:
        time.sleep(time_delay - time_elapsed)

    print(f"Visited {len(visited_links)} links so far...")

# Save the checked links to a CSV file
print(f"Checking {len(visited_links)} links...")
with open('URL_links.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Link', 'Page Found On', 'Status'])

    for link in visited_links:
        if ".com" not in link:
            print(f"Checking {link}...")
            try:
                # Make the HTTP request and check the response code
                response = requests.head(link)
                status = response.status_code

            except (requests.exceptions.RequestException) as error:
                # Handle errors that occur during the request process
                status = str(error)
                print(f"Error while checking {link}: {error}")

            # Write the link, page found on, and status to the CSV file
            writer.writerow([link, '', status])

print("Done!")
