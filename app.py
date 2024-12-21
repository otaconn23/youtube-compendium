import streamlit as st
from playwright.sync_api import sync_playwright
import os

# Install Playwright browsers if not already installed
os.system("playwright install")

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

# Function to scrape YouTube content using Playwright
def scrape_youtube_data(channel_url, include_videos, include_shorts, include_community):
    scraped_data = {
        "videos": [],
        "shorts": [],
        "community": []
    }

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Scrape Videos
        if include_videos:
            st.info("Scraping videos...")
            page.goto(f"{channel_url}/videos")
            video_elements = page.query_selector_all('a#video-title')
            scraped_data["videos"] = [
                {"title": video.inner_text(), "link": f"https://www.youtube.com{video.get_attribute('href')}"}
                for video in video_elements
            ]

        # Scrape Shorts
        if include_shorts:
            st.info("Scraping shorts...")
            page.goto(f"{channel_url}/shorts")
            shorts_elements = page.query_selector_all('a#video-title')
            scraped_data["shorts"] = [
                {"title": short.inner_text(), "link": f"https://www.youtube.com{short.get_attribute('href')}"}
                for short in shorts_elements
            ]

        # Scrape Community Posts
        if include_community:
            st.info("Scraping community posts...")
            page.goto(f"{channel_url}/community")
            community_elements = page.query_selector_all(
                'yt-formatted-string[class*="style-scope ytd-backstage-post-renderer"]'
            )
            scraped_data["community"] = [
                {"content": post.inner_text()}
                for post in community_elements
            ]

        browser.close()

    return scraped_data

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
