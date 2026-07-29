import streamlit as st
import pandas as pd

# Load the music dataset
df = pd.read_csv("songs_datasets.csv")

# Page settings
st.set_page_config(
    page_title="Music Recommendation Chatbot",
    page_icon="🎵"
)

# Title
st.title("🎵 Music Recommendation Chatbot")

st.write("Enter a song name and get song details and recommendations.")

# Show some songs available in the dataset
st.subheader("🎵 Songs Available in the Dataset")

available_songs = df["track_name"].dropna().head(20).tolist()

for i, song_name in enumerate(available_songs, 1):
    st.write(f"{i}. {song_name}")

# Song input
song = st.text_input("Enter Song Name")

# Recommend button
if st.button("Recommend"):

    if song.strip() == "":
        st.warning("Please enter a song name.")

    else:
        # Search for the song
        result = df[
            df["track_name"].astype(str).str.lower().str.strip()
            == song.lower().strip()
        ]

        # Check if song exists
        if result.empty:
            st.error("Song not found in the dataset.")

        else:
            # Get the first matching song
            row = result.iloc[0]

            st.success("Song Found!")

            # Display song details
            st.subheader("🎵 Song Details")

            st.write("Song:", row["track_name"])
            st.write("Artist:", row["artist(s)_name"])
            st.write("Released Year:", row["released_year"])
            st.write("Streams:", row["streams"])

            # Find other songs by the same artist
            artist = row["artist(s)_name"]

            recommendations = df[
                (df["artist(s)_name"].astype(str).str.lower() == str(artist).lower())
                & (df["track_name"].astype(str).str.lower() != song.lower().strip())
            ]

            # Display recommendations
            st.subheader("🎧 Recommended Songs")

            if recommendations.empty:
                st.info("No other songs by this artist were found.")

            else:
                st.dataframe(
                    recommendations[
                        ["track_name", "artist(s)_name", "released_year"]
                    ].head(5)
                )