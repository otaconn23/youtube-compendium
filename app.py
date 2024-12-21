import streamlit as st
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

def scrape_page(url):
    """Scrape fully rendered HTML using Playwright."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        html_content = page.content()
        browser.close()
    return html_content

def scrape_videos(soup):
    videos = []
    for video in soup.select("a#video-title"):
        title = video.text.strip()
        link = f"https://www.youtube.com{video['href']}"
        videos.append({"title": title, "link": link})
    return videos

def scrape_shorts(soup):
    shorts = []
    for short in soup.select("a#video-title"):
        title = short.text.strip()
        link = f"https://www.youtube.com{short['href']}"
        shorts.append({"title": title, "link": link})
    return shorts

def scrape_community(soup):
    community_posts = []
    for post in soup.select("yt-formatted-string#content-text"):
        content = post.text.strip()
        community_posts.append(content)
    return community_posts

def main():
    st.title("YouTube Content Scraper")

    channel_url = st.text_input("Enter the YouTube channel URL:", "https://www.youtube.com/@example")
    scrape_videos_section = st.checkbox("Scrape Videos", value=True)
    scrape_shorts_section = st.checkbox("Scrape Shorts", value=True)
    scrape_community_section = st.checkbox("Scrape Community Posts", value=True)

    if st.button("Start Scraping"):
        with st.spinner("Scraping selected sections..."):
            try:
                results = {}

                if scrape_videos_section:
                    videos_html = scrape_page(f"{channel_url}/videos")
                    videos_soup = BeautifulSoup(videos_html, "html.parser")
                    results["videos"] = scrape_videos(videos_soup)

                if scrape_shorts_section:
                    shorts_html = scrape_page(f"{channel_url}/shorts")
                    shorts_soup = BeautifulSoup(shorts_html, "html.parser")
                    results["shorts"] = scrape_shorts(shorts_soup)

                if scrape_community_section:
                    community_html = scrape_page(f"{channel_url}/community")
                    community_soup = BeautifulSoup(community_html, "html.parser")
                    results["community"] = scrape_community(community_soup)

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
