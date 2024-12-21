import streamlit as st
import requests
from bs4 import BeautifulSoup

# App title
st.title("YouTube Compendium Generator")

# Input field for YouTube user URL
youtube_url = st.text_input("Enter YouTube User URL:", "")

# Checkboxes for content types
st.subheader("Select Content Types to Include:")
include_videos = st.checkbox("Videos", value=True)
include_shorts = st.checkbox("Shorts", value=True)
include_community = st.checkbox("Community", value=True)

# Headers to mimic a browser request
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# Scrape YouTube content
def scrape_youtube_data(channel_url, include_videos, include_shorts, include_community):
    scraped_data = {"videos": [], "shorts": [], "community": []}

    # Scrape Videos
    if include_videos:
        st.info("Scraping videos...")
        video_data = scrape_section(f"{channel_url}/videos", "videos")
        scraped_data["videos"] = video_data

    # Scrape Shorts
    if include_shorts:
        st.info("Scraping shorts...")
        shorts_data = scrape_section(f"{channel_url}/shorts", "shorts")
        scraped_data["shorts"] = shorts_data

    # Scrape Community Posts
    if include_community:
        st.info("Scraping community posts...")
        community_data = scrape_community(f"{channel_url}/community")
        scraped_data["community"] = community_data

    return scraped_data


# Scrape a section (videos or shorts)
def scrape_section(url, section_type):
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract titles and links
        data = []
        for item in soup.find_all("a", {"id": "video-title"}):
            title = item.text.strip()
            link = f"https://www.youtube.com{item['href']}"
            data.append({"title": title, "link": link})

        return data
    except Exception as e:
        st.error(f"Failed to scrape {section_type}: {e}")
        return []


# Scrape community posts
def scrape_community(url):
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract text posts
        data = []
        for item in soup.find_all("yt-formatted-string", {"class": "style-scope ytd-backstage-post-renderer"}):
            text = item.text.strip()
            if text:
                data.append({"content": text})

        return data
    except Exception as e:
        st.error(f"Failed to scrape community posts: {e}")
        return []


# Button to start scraping
if st.button("Start Processing"):
    if youtube_url:
        st.info("Scraping content from YouTube...")
        scraped_data = scrape_youtube_data(youtube_url, include_videos, include_shorts, include_community)

        # Display scraped data for testing
        if scraped_data["videos"]:
            st.subheader("Videos")
            for video in scraped_data["videos"]:
                st.write(f"{video['title']} - [Watch]({video['link']})")

        if scraped_data["shorts"]:
            st.subheader("Shorts")
            for short in scraped_data["shorts"]:
                st.write(f"{short['title']} - [Watch]({short['link']})")

        if scraped_data["community"]:
            st.subheader("Community Posts")
            for post in scraped_data["community"]:
                st.write(post['content'])

        st.success("Scraping complete!")
    else:
        st.warning("Please enter a valid YouTube channel URL.")
