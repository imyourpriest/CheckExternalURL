import csv
import requests
from bs4 import BeautifulSoup
import time

# Set the base URL to crawl
base_url = '.com'

# Set the limit of requests per minute
request_limit = 10

# Set the time delay between requests
time_delay = 60 / request_limit

# Initialize an empty list to store the links
links = [base_url]

# Loop through each page of the website and extract the links
while True:
    print(f"Requesting {links[0]}...")

    # Set the start time of the request
    start_time = time.time()

    try:
        # Make the HTTP request and retrieve the page HTML
        response = requests.get(links[0])
        html_page = response.content

        # Parse the HTML using BeautifulSoup
        soup = BeautifulSoup(html_page, 'html.parser')

        # Extract the links from the HTML using BeautifulSoup
        for link in soup.findAll('a'):
            href = link.get('href')
            if href and href.startswith(base_url):
                links.append(href)

    except (requests.exceptions.RequestException) as error:
        # Handle errors that occur during the request process
        print(f"Error while requesting {links[0]}: {error}")

    # Wait for the remaining time until the request limit is reached
    end_time = time.time()
    time_elapsed = end_time - start_time
    if time_elapsed < time_delay:
        time.sleep(time_delay - time_elapsed)

    # Break out of the loop if all pages have been checked
    links.pop(0)
    if len(links) == 0:
        break
    
    print(f"Found {len(links)} links so far...")

# Save the checked links to a CSV file
print(f"Checking {len(links)} links...")
with open('URL_links.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Link', 'Status'])

    for link in links:
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

            # Write the link and status to the CSV file
            writer.writerow([link, status])

print("Done!")
