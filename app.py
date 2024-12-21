import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

# Configure Selenium WebDriver
CHROME_DRIVER_PATH = "/usr/bin/chromedriver"  # Ensure chromedriver is installed and accessible

def get_rendered_html(url):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    service = Service(CHROME_DRIVER_PATH)

    with webdriver.Chrome(service=service, options=options) as driver:
        driver.get(url)
        time.sleep(5)  # Allow time for JavaScript to load
        return driver.page_source

# Function to scrape YouTube videos
def scrape_videos(soup):
    videos = []
    for video in soup.select("a#video-title"):
        title = video.text.strip()
        link = f"https://www.youtube.com{video['href']}"
        videos.append({"title": title, "link": link})
    return videos

# Function to scrape YouTube shorts
def scrape_shorts(soup):
    shorts = []
    for short in soup.select("a#video-title"):
        title = short.text.strip()
        link = f"https://www.youtube.com{short['href']}"
        shorts.append({"title": title, "link": link})
    return shorts

# Function to scrape YouTube community posts
def scrape_community(soup):
    community_posts = []
    for post in soup.select("yt-formatted-string#content-text"):
        content = post.text.strip()
        community_posts.append(content)
    return community_posts

# Main Streamlit app
def main():
    st.title("YouTube Content Scraper")

    # Input YouTube channel URL
    channel_url = st.text_input("Enter the YouTube channel URL:", "https://www.youtube.com/@example")

    # Checkboxes for sections
    scrape_videos_section = st.checkbox("Scrape Videos", value=True)
    scrape_shorts_section = st.checkbox("Scrape Shorts", value=True)
    scrape_community_section = st.checkbox("Scrape Community Posts", value=True)

    if st.button("Start Scraping"):
        with st.spinner("Scraping selected sections..."):
            try:
                results = {}

                # Scrape Videos
                if scrape_videos_section:
                    videos_html = get_rendered_html(f"{channel_url}/videos")
                    videos_soup = BeautifulSoup(videos_html, "html.parser")
                    results["videos"] = scrape_videos(videos_soup)

                # Scrape Shorts
                if scrape_shorts_section:
                    shorts_html = get_rendered_html(f"{channel_url}/shorts")
                    shorts_soup = BeautifulSoup(shorts_html, "html.parser")
                    results["shorts"] = scrape_shorts(shorts_soup)

                # Scrape Community Posts
                if scrape_community_section:
                    community_html = get_rendered_html(f"{channel_url}/community")
                    community_soup = BeautifulSoup(community_html, "html.parser")
                    results["community"] = scrape_community(community_soup)

                # Display Results
                if results.get("videos"):
                    st.subheader("Videos")
                    for video in results["videos"]:
                        st.write(f"- [{video['title']}]({video['link']})")

                if results.get("shorts"):
                    st.subheader("Shorts")
                    for short in results["shorts"]:
                        st.write(f"- [{short['title']}]({short['link']})")

                if results.get("community"):
                    st.subheader("Community Posts")
                    for post in results["community"]:
                        st.write(f"- {post}")

                if not any(results.values()):
                    st.warning("No data was scraped. Please check the selected sections and try again.")

            except Exception as e:
                st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
