import streamlit as st
import requests
from bs4 import BeautifulSoup

# Define headers with a User-Agent to mimic a browser
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

BASE_URL = "https://www.youtube.com"

# Function to scrape YouTube videos
def scrape_videos(soup):
    videos = []
    for video in soup.select("a#video-title"):
        title = video.text.strip()
        link = f"{BASE_URL}{video['href']}"
        videos.append({"title": title, "link": link})
    return videos

# Main Streamlit app
def main():
    st.title("YouTube Video Scraper")

    # Input YouTube channel URL
    channel_url = st.text_input("Enter the YouTube channel URL:", "https://www.youtube.com/@example")

    if st.button("Scrape Videos"):
        with st.spinner("Scraping videos..."):
            try:
                # Scrape Videos
                videos_response = requests.get(f"{channel_url}/videos", headers=HEADERS)
                if videos_response.status_code == 200:
                    videos_soup = BeautifulSoup(videos_response.text, "html.parser")
                    videos = scrape_videos(videos_soup)

                    # Display videos
                    if videos:
                        st.success("Videos scraped successfully!")
                        for video in videos:
                            st.write(f"- [{video['title']}]({video['link']})")
                    else:
                        st.warning("No videos found.")
                else:
                    st.error(f"Failed to fetch videos page. Status code: {videos_response.status_code}")

            except Exception as e:
                st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
