import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

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

# Configure Selenium WebDriver
def init_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode for Streamlit
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    service = Service("/usr/bin/chromedriver")  # Path to ChromeDriver (adjust if necessary)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

# Scrape videos and shorts
def scrape_section(url, section_type):
    driver = init_driver()
    driver.get(url)
    
    try:
        data = []
        video_elements = driver.find_elements(By.ID, "video-title")
        for video in video_elements:
            title = video.text.strip()
            link = video.get_attribute("href")
            if title and link:
                data.append({"title": title, "link": link})
        return data
    except Exception as e:
        st.error(f"Failed to scrape {section_type}: {e}")
        return []
    finally:
        driver.quit()

# Scrape community posts
def scrape_community(url):
    driver = init_driver()
    driver.get(url)
    
    try:
        data = []
        post_elements = driver.find_elements(By.CLASS_NAME, "style-scope ytd-backstage-post-renderer")
        for post in post_elements:
            text = post.text.strip()
            if text:
                data.append({"content": text})
        return data
    except Exception as e:
        st.error(f"Failed to scrape community posts: {e}")
        return []
    finally:
        driver.quit()

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
