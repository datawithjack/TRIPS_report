# Connect to spotify API and download trips data
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd

# Authenticate with Spotify
# Set up your credentials (replace these with your actual Client ID and Client Secret)
client_id = ''
client_secret = ''
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Search for the "The Rest is Politics" podcast to get its ID
results = sp.search(q='The Rest is Politics', type='show', limit=10)

# Check if any shows were found
if not results['shows']['items']:
    raise Exception("Podcast not found.")

podcast = results['shows']['items'][0]
podcast_id = podcast.get('id')  # Use .get() to safely access the 'id'

if podcast_id:
    # Initialize a list to store episode data
    episodes_data = []

    # Fetch all episodes of the podcast
    offset = 0
    while True:
        episodes = sp.show_episodes(podcast_id, limit=50, offset=offset)
        for episode in episodes['items']:
            episodes_data.append({
                'Episode Name': episode['name'],
                'Release Date': episode['release_date'],
                'Duration (ms)': episode['duration_ms'],
                'Explicit': episode['explicit'],
                'Episode Description': episode['description'],
                'Episode URL': episode['external_urls']['spotify']
            })
        
        # Check if there are more episodes to fetch
        if episodes['next'] is not None:
            offset += 50
        else:
            break

    # Create a DataFrame from the episode data
    episodes_df = pd.DataFrame(episodes_data)

    # Display the DataFrame
    print(episodes_df)
else:
    print("Podcast not found.")
