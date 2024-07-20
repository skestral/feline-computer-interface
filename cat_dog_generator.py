####################################################################################################
# Custom API Grabbing Module - The Cat-Dog Generator
# Used to call the API for Cat As A Service or Dog As A Service
####################################################################################################
import requests

###################
# Fetch Images
# this function will use the correct API call using APIs sourced from auth.py
###################
def fetch_image_url(animal_type, api_key):
    # docs for calling the API are here: https://developers.thecatapi.com/view-account/ylX4blBYT9FaoVd6OhvR?report=bOoHBz-8t
    # there are lots of options for filtering, at this point we're just grabbing random images
    # but in the future this could be expanded to offer the user enhanced search / filter options, etc
    if animal_type == "cat":
        api_url = "https://api.thecatapi.com/v1/images/search" # cat as a service rawr meow
        key = api_key["cat"]
    else:
        api_url = "https://api.thedogapi.com/v1/images/search" # dog as a service lolol woof
        key = api_key["dog"]

    headers = {"x-api-key": key}
    response = requests.get(api_url)
    data = response.json()
    if data:
        return data[0]['url']
    return None
