from django.shortcuts import render
from bs4 import BeautifulSoup
import requests

# Create your views here.
def players_list(request):
    # Make a request to the Basketball-Reference website to fetch player data
    players_url = "https://www.basketball-reference.com/players/"
    response = requests.get(players_url)
    
    if response.status_code == 200:
        # Parse the HTML content using Beautiful Soup
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find all player links
        player_links = soup.find_all('a', class_='poptip')
        
        # Extract player names and URLs
        player_data = []
        for link in player_links:
            player_name = link.text
            player_url = link['href']
            player_data.append({'name': player_name, 'url': player_url})
        
        # Pass player data to the template
        context = {'player_data': player_data}
        return render(request, 'players_list.html', context)
    else:
        # Handle request error
        return render(request, 'error.html', {'error_message': 'Failed to fetch player data'})
    
def player_profile(request, player_id):
    # Construct the URL for the player's profile page on Basketball-Reference
    player_url = f"https://www.basketball-reference.com/players/{player_id[0]}/{player_id}.html"
    
    # Make a request to fetch the player's profile page
    response = requests.get(player_url)
    
    if response.status_code == 200:
        # Parse the HTML content using Beautiful Soup
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract player information from the parsed HTML
        player_name = soup.find('h1', itemprop='name').text
        player_image = soup.find('img', itemprop='image')['src']
        # Extract other player data as needed
        
        # Pass player data to the template
        context = {
            'player_name': player_name,
            'player_image': player_image,
            # Add other player data to the context dictionary
        }
        
        # Render the player profile template with the player data
        return render(request, 'player_profile.html', context)
    else:
        # Handle request error
        return render(request, 'error.html', {'error_message': 'Failed to fetch player profile'})