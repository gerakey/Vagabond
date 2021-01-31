import requests

from bs4 import BeautifulSoup

def resolve_actor(url, iteration=0, original_url = None):
    # prevent stack overflow
    if iteration > 2: return None

    # Used for recursive calls
    if original_url == None: original_url = url

    response = requests.get(url)

    # If we get an HTML document, we need to
    # attempt to locate an alternate link. 
    if response.headers['Content-Type'].find('text/html') >= 0:
        soup = BeautifulSoup(response.text)
        links = soup.find_all('link')
        alt_url = None
        for link in links:

            if 'alternate' in link.get('rel') and link.get('type') == 'application/activity+json':
                alt_url = link.get('href')
                break

        if alt_url == None:
            return None

        else:
            # This is for Mastodon compatability.
            # Mastodon isn't ActivityPub compliant! >:(
            with_json =  resolve_actor(alt_url + '.json', iteration=iteration+1, original_url=original_url)


            # For some reason, comparing an RSA key to None throws an error.
            # This is the next best option. 
            if str(with_json) != 'None':
                return with_json
            else:
                without_json =  resolve_actor(alt_url, iteration=iteration+1, original_url=original_url)
                return without_json

    # If we find the right content type on the first try,
    # great!
    elif response.headers['Content-Type'].find('application/activity+json') >= 0:
        return response.json()

    #Something has gone horribly wrong
    else:
        return None