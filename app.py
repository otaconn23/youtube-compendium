import streamlit as st
from bs4 import BeautifulSoup
import requests

# Function to scrape video data from the uploaded or fetched videos page
def scrape_videos_page(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    videos = []

    # Find all video elements by their HTML structure (adjust selectors if needed)
    for video_tag in soup.find_all('a', {'id': 'video-title'}):
        title = video_tag.text.strip()
        link = f"https://www.youtube.com{video_tag['href']}"
        videos.append({'title': title, 'link': link})

    return videos

# Streamlit UI
st.title("YouTube Channel Scraper")

# Input for URL
url = st.text_input("Enter YouTube Channel URL:")
uploaded_file = st.file_uploader("Or upload the videos HTML file:", type="html")

if st.button("Scrape Videos"):
    if uploaded_file:
        # Use uploaded HTML file
        html_content = uploaded_file.read()
        st.info("Scraping uploaded file...")
        videos = scrape_videos_page(html_content)
    elif url:
        try:
            st.info("Fetching page from URL...")
            response = requests.get(url)
            response.raise_for_status()
            html_content = response.text
            videos = scrape_videos_page(html_content)
        except Exception as e:
            st.error(f"Failed to fetch the page: {e}")
            videos = []
    else:
        st.error("Please provide a URL or upload a file.")
        videos = []

    # Display results
    if videos:
        st.success(f"Found {len(videos)} videos!")
        for video in videos:
            st.write(f"[{video['title']}]({video['link']})")
    else:
        st.warning("No videos found. Ensure the page structure is correct.")
