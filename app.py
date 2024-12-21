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

# Function to scrape YouTube shorts
def scrape_shorts(soup):
    shorts = []
    for short in soup.select("a#video-title"):
        title = short.text.strip()
        link = f"{BASE_URL}{short['href']}"
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
                    videos_response = requests.get(f"{channel_url}/videos", headers=HEADERS)
                    if videos_response.status_code == 200:
                        videos_soup = BeautifulSoup(videos_response.text, "html.parser")
                        results["videos"] = scrape_videos(videos_soup)
                        st.subheader("Videos Page HTML Preview")
                        st.text(videos_response.text[:500])  # Display first 500 characters of HTML
                    else:
                        st.error(f"Failed to fetch videos page. Status code: {videos_response.status_code}")

                # Scrape Shorts
                if scrape_shorts_section:
                    shorts_response = requests.get(f"{channel_url}/shorts", headers=HEADERS)
                    if shorts_response.status_code == 200:
                        shorts_soup = BeautifulSoup(shorts_response.text, "html.parser")
                        results["shorts"] = scrape_shorts(shorts_soup)
                        st.subheader("Shorts Page HTML Preview")
                        st.text(shorts_response.text[:500])  # Display first 500 characters of HTML
                    else:
                        st.error(f"Failed to fetch shorts page. Status code: {shorts_response.status_code}")

                # Scrape Community Posts
                if scrape_community_section:
                    community_response = requests.get(f"{channel_url}/community", headers=HEADERS)
                    if community_response.status_code == 200:
                        community_soup = BeautifulSoup(community_response.text, "html.parser")
                        results["community"] = scrape_community(community_soup)
                        st.subheader("Community Page HTML Preview")
                        st.text(community_response.text[:500])  # Display first 500 characters of HTML
                    else:
                        st.error(f"Failed to fetch community page. Status code: {community_response.status_code}")

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
