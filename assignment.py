import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
# Set fonts to prevent Chinese garbled characters
plt.rcParams['font.sans-serif'] = ['SimHei']  # Set Chinese font to SimHei
plt.rcParams['axes.unicode_minus'] = False  # Fix issue with negative sign not showing up
# Target webpage URL (Hong Kong Observatory tide data)
base_url = 'https://www.hko.gov.hk'
url = base_url + '/en/tide/ttext.htm'

# Send an HTTP GET request
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Use BeautifulSoup to parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the link for the tide data (2024 data)
    table = soup.find('table')  # Find the table
    link_tag = table.find('a', href=True, text='2024')  # Find the first link with year 2024
    
    if link_tag:
        # Get the tide data link
        tide_url = base_url + link_tag['href']
        print(f"Fetched tide data link: {tide_url}")
        
        # Request the tide data page
        tide_response = requests.get(tide_url)
        if tide_response.status_code == 200:
            tide_soup = BeautifulSoup(tide_response.content, 'html.parser')

            # Assuming tide data is inside <pre> tag, fetch all text data
            pre_tag = tide_soup.find('table')
            if pre_tag:
                data_lines = pre_tag.text.splitlines()

                # Print a preview of the first few lines of data
                print("Tide data preview:")
                for line in data_lines[:10]:  # Show first 10 lines
                    print(line)

                # Assuming each line of data is in the format: Date, Time, Tide Height
                dates, heights = [], []
                for line in data_lines[3:]:  # Skip the first few descriptive lines
                    parts = line.split()
                    if len(parts) >= 3:
                        date = parts[0]
                        height = round(float(parts[1]),2)  # Tide height
                        dates.append(date)
                        heights.append(height)

                # Visualize the tide height changes
                plt.figure(figsize=(10, 6))
                plt.plot(dates, heights, marker='o', linestyle='-', color='b')
                plt.xticks(rotation=90)
                plt.title('Tide Height Changes')
                plt.xlabel('Date')
                plt.ylabel('Tide Height (m)')
                plt.grid(True)
                plt.tight_layout()
                plt.show()
            else:
                print("Could not find <table> tag containing tide data.")
        else:
            print(f"Failed to request tide data page, status code: {tide_response.status_code}")
    else:
        print("Could not find the link for the 2024 tide data.")

else:
    print(f"Failed to request the main page, status code: {response.status_code}")
