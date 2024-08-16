import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi as yta
import re

def find_word_in_video(video_url, search_word):
    # Extract video ID from the URL
    video_id = video_url.split("v=")[1]

    # Get the video transcript
    transcript = yta.get_transcript(video_id, languages=("en",))  # Specify the language (e.g., English)

    # Clean the transcript data
    data = [re.sub(r"[^a-zA-Z0-9 ]", "", t["text"]) for t in transcript]

    # Search for the word and collect timestamps
    timestamps = []
    for idx, line in enumerate(data):
        if search_word.lower() in line.lower():
            timestamps.append(transcript[idx]["start"])

    return timestamps

def main():
    st.title("YouTube Word Timestamp Finder")

    # Input YouTube URL
    video_url = st.text_input("Enter the YouTube URL:")

    # Input search word
    search_word = st.text_input("Enter the word to search for:")

    if st.button("Find Timestamps"):
        if video_url and search_word:
            timestamps = find_word_in_video(video_url, search_word)
            if timestamps:
                st.success(f"'{search_word}' was mentioned at the following timestamps:")
                for ts in timestamps:
                    print_time(ts)
            else:
                st.warning(f"'{search_word}' was not found in the video transcript.")
        else:
            st.warning("Please enter both a YouTube URL and a search word.")

def print_time(time):
    hours = int(time // 3600)
    minutes = int((time // 60) % 60)
    seconds = int(time % 60)
    st.write(f"{hours:02d}:{minutes:02d}:{seconds:02d}")

if __name__ == "__main__":
    main()
