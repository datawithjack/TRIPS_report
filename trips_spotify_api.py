
import requests
from requests.auth import HTTPBasicAuth
import pandas as pd

##### GET DATA VIA SPOTIFY API #####

# Your Spotify Client ID and Client Secret
client_id = ''
client_secret = ''


# Spotify URL for obtaining an access token
token_url = 'https://accounts.spotify.com/api/token'

# Request headers
headers = {'Content-Type': 'application/x-www-form-urlencoded'}

# Request body parameters for the Client Credentials flow
body_params = {'grant_type': 'client_credentials'}

# Making the POST request to obtain an access token
token_response = requests.post(token_url, data=body_params, headers=headers, auth=HTTPBasicAuth(client_id, client_secret))

if token_response.status_code == 200:
    # Extract the access token from the response
    access_token = token_response.json().get('access_token')
else:
    raise Exception(f'Failed to obtain access token: {token_response.status_code}')

# The Spotify Web API endpoint for fetching show episodes, replace 'your_show_id_here' with your actual show ID
show_id = '1Ysx8g1Iw42gESAtegrFaH'
url = f'https://api.spotify.com/v1/shows/{show_id}/episodes'

# Authorization headers with the obtained access token
auth_headers = {
    'Authorization': f'Bearer {access_token}',
}

# Initialize an empty list to store episodes data
episodes_data = []

# Loop through all pages of episodes
while url:
    response = requests.get(url, headers=auth_headers, params={'limit': 50})  # API allows max 50 items per request
    if response.status_code != 200:
        print(f'Failed to fetch episodes data: {response.status_code}')
        break

    data = response.json()
    episodes = data['items']

    for episode in episodes:
        # Append each episode's details to the list
        episodes_data.append({
            'id': episode['id'],
            'name': episode['name'],
            'description': episode['description'],
            'audio_preview_url': episode['audio_preview_url'],
            'release_date': episode['release_date'],
            'duration_ms': episode['duration_ms'],
            'external_urls': episode['external_urls']['spotify'],
        })

    # Get the next page of episodes, if available
    url = data.get('next')

# Convert the list of episodes data into a pandas DataFrame
episodes_df = pd.DataFrame(episodes_data)

# Display the DataFrame
print(episodes_df.head())  # Show the first few rows of the DataFrame

##### CLEAN THE DATA #####

# extract episode numbers
# Use regular expression to extract episode number and title
episodes_df_clean = episodes_df.copy()


episodes_df_clean[['ep_no', 'ep_title']] = episodes_df_clean['name'].str.extract(r'^(\d+)[.:]\s*(.*)')

# Convert ep_no to numeric type if necessary
episodes_df_clean['ep_no'] = pd.to_numeric(episodes_df_clean['ep_no'])

# filter out non episodes i.e episode number nan
episodes_df_clean = episodes_df_clean.dropna(subset=['ep_no'])

# quick check of data quality

# Display data types and non-null counts
print("DataFrame Information:")
episodes_df_clean.info()

# Display summary statistics for numerical columns
print("\nSummary Statistics for Numerical Columns:")
print(episodes_df_clean.describe())

# Display summary statistics for categorical/object columns
print("\nSummary Statistics for Categorical Columns:")
print(episodes_df_clean.describe(include='object'))

# Checking for missing values in each column
print("\nMissing Values in Each Column:")
print(episodes_df_clean.isnull().sum())

# Unique values in each column
print("\nUnique Values in Each Column:")
print(episodes_df_clean.nunique())


# data looks good
# export to csv
episodes_df_clean.to_csv('trips_data_via_python_clean.csv')




