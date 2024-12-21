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

# Logic to ensure videos are always selected
if not include_videos:
    st.warning("Videos must be selected. Please enable 'Videos' to proceed.")
    include_shorts = False
    include_community = False

# Function to scrape YouTube content
def scrape_youtube_data(channel_url, include_videos, include_shorts, include_community):
    # Base YouTube URLs for scraping
    base_urls = {
        "videos": f"{channel_url}/videos",
        "shorts": f"{channel_url}/shorts",
        "community": f"{channel_url}/community"
    }

    scraped_data = {
        "videos": [],
        "shorts": [],
        "community": []
    }

    # Scrape Videos
    if include_videos:
        st.info("Scraping videos...")
        video_data = scrape_section(base_urls["videos"], "videos")
        scraped_data["videos"] = video_data

    # Scrape Shorts
    if include_shorts:
        st.info("Scraping shorts...")
        shorts_data = scrape_section(base_urls["shorts"], "shorts")
        scraped_data["shorts"] = shorts_data

    # Scrape Community Posts
    if include_community:
        st.info("Scraping community posts...")
        community_data = scrape_community(base_urls["community"])
        scraped_data["community"] = community_data

    return scraped_data


def scrape_section(url, section_type):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Debug: Print raw HTML to Streamlit
        st.text(f"Raw HTML content for {section_type}:")
        st.text(soup.prettify()[:1000])  # Limit output for readability
        
        # Scrape Titles and Links
        data = []
        for item in soup.find_all("a", {"id": "video-title"}):  # Adjust selector if needed
            title = item.text.strip()
            link = f"https://www.youtube.com{item['href']}"
            data.append({"title": title, "link": link})
        
        return data
    except Exception as e:
        st.error(f"Failed to scrape {section_type}: {e}")
        return []

    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Scrape Titles and Links
        data = []
        for item in soup.find_all("a", {"id": "video-title"}):  # Adjust selector if needed
            title = item.text.strip()
            link = f"https://www.youtube.com{item['href']}"
            data.append({"title": title, "link": link})
        
        return data
    except Exception as e:
        st.error(f"Failed to scrape {section_type}: {e}")
        return []


def scrape_community(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Scrape Community Text Posts
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
