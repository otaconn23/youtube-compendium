import streamlit as st

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

# Display placeholder messages for selected options
if st.button("Start Processing"):
    st.write("Processing the following selections:")
    st.write(f"YouTube URL: {youtube_url}")
    st.write(f"Include Videos: {include_videos}")
    st.write(f"Include Shorts: {include_shorts}")
    st.write(f"Include Community: {include_community}")
    st.write("This is a placeholder. Full functionality will be added later.")
