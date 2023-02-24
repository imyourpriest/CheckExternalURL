def is_external_link(link):
    return link.startswith("http") and ".com" not in link

def crawl(url):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.content, "html.parser")
        for link in soup.find_all("a"):
            href = link.get("href")
            if href and is_external_link(href):
                external_links.add(href)
        print(f"Found {len(external_links)} external links on {url}")
    except Exception as e:
        print(f"Failed to crawl {url}: {e}")

def save_to_csv(links):
    with open("external_links.csv", mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        if file.tell() == 0:
            writer.writerow(["Page URL", "External URL"])
        for url, external_url in links:
            writer.writerow([url, external_url])
    print(f"Saved {len(links)} external links to external_links.csv")

def main():
    pages_to_crawl = set([base_url])
    crawled_pages = set()

    while pages_to_crawl:
        page_url = pages_to_crawl.pop()
        crawled_pages.add(page_url)
        print(f"Crawling {page_url}...")
        crawl(page_url)
        external_links_to_save = [(page_url, external_link) for external_link in external_links]
        save_to_csv(external_links_to_save)
        external_links.clear()

        for link in BeautifulSoup(requests.get(page_url).content, "html.parser").find_all("a"):
            href = link.get("href")
            if href and href.startswith(base_url) and href not in crawled_pages:
                pages_to_crawl.add(href)

        time.sleep(5) # Wait for 5 seconds before crawling next page

if __name__ == "__main__":
    main()
