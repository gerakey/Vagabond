from flask import request, current_app, make_response

from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15


from base64 import b64decode, b64encode

import requests

from bs4 import BeautifulSoup

from vagabond.__main__ import app


#TODO: Standard error function for entire project
def error(message, code=400):
    app.logger.error(message)
    return make_response(message, code)

"""
returns: tuple (key_id, algorithm, headers, signature)
    key_id: string
    algorithm: string
    headers: list
    signature: string; base64 encoded signature
"""
def parse_keypairs(raw_signature):
    keypairs = raw_signature.split(',')
    for i in range (0, len(keypairs)): keypairs[i] = keypairs[i].strip()
    key_id = None
    algorithm = None
    headers = None
    signature = None
    header_digest = None

    for keypair in keypairs:
        keypair = keypair.strip()

        if keypair.find('keyId="') >= 0:
            key_id = keypair.replace('keyId="', '').rstrip('"')

        if keypair.find('algorithm="') >= 0:
            algorithm = keypair.replace('algorithm="', '').rstrip('"')

        elif keypair.find('headers="') >= 0:
            headers = keypair.replace('headers="', '').rstrip('"').split(' ')
            for i in range(0, len(headers)): headers[i] = headers[i].strip()

        elif keypair.find('signature="') >= 0:
            signature = keypair.replace('signature="', '').rstrip('"')
 
        else:
            continue

    return (key_id, algorithm, headers, signature)


"""
Takes a list of headers as present in the HTTP signature header and 
constructs a signing string 
"""
def construct_signing_string(headers):
    output = ''
    for i in range(0, len(headers)):
        header = headers[i]
        header = header.strip()
        if header == '(request-target)':
            output += f'(request-target): post {request.path}'
        else:
            output += (header + ': ')
            output += request.headers[header.title()]


        if i != (len(headers) - 1):
            output += '\n'
        
    return output



"""
Takes the "keyId" field of a request and does
whatever is necessary to resolve it into
a valid RSA public key object
"""
def get_public_key(key_id, iteration=0, original_key_id=None):

    app.logger.error(f'Attempting to get key with id {key_id}')

    # prevent stack overflow
    if iteration > 2: return None

    # Used for recursive calls
    if original_key_id == None: original_key_id = key_id

    response = requests.get(key_id)

    # If we get an HTML document, we need to
    # attempt to locate an alternate link. 
    if response.headers['Content-Type'].find('text/html') >= 0:
        soup = BeautifulSoup(response.text)
        links = soup.find_all('link')
        alt_key_url = None
        for link in links:

            if 'alternate' in link.get('rel') and link.get('type') == 'application/activity+json':
                alt_key_url = link.get('href')
                break

        if alt_key_url == None:
            app.logger.error('Alternate key could not be found. Returning  None')
            return None

        else:
            # This is for Mastodon compatability.
            # Mastodon isn't ActivityPub compliant! >:(
            with_json =  get_public_key(alt_key_url + '.json', iteration=iteration+1, original_key_id=original_key_id)


            # For some reason, comparing an RSA key to None throws an error.
            # This is the next best option. 
            if str(with_json) != 'None':
                return with_json
            else:
                without_json =  get_public_key(alt_key_url, iteration=iteration+1, original_key_id=original_key_id)
                return without_json

    # If we find the right content type on the first try,
    # great!
    elif response.headers['Content-Type'].find('application/activity+json') >= 0:
        json = response.json()
        if not json or not json.get('publicKey'): return error('An error occurred while attempting to fetch the public key of the inbound actor.', 400)
        public_key_wrapper = json.get('publicKey')
        if public_key_wrapper.get('id') != original_key_id: return error('Keys don\'t match', 400)
        public_key_string = public_key_wrapper.get('publicKeyPem')

        if not public_key_string: return error('Public key not found.')

        public_key =  RSA.importKey(bytes(public_key_string, 'utf-8'))

        return public_key


    #Something has gone horribly wrong
    else:
        app.error.log('Something has gone horribly wrong')
        return None



"""
Decoator that requires all post requests have a valid HTTP
signature according to the RFC standard
"""
def require_signature(f):
    def wrapper(*args, **kwargs):


        if request.method != 'POST': return f()
        
        if not request.get_json(): return error('No JSON provided.', 400)


        if 'Signature' not in request.headers or 'Digest' not in request.headers: return error('Authentication mechanism is missing or invalid', 400)
        raw_signature = request.headers['Signature']
        (key_id, algorithm, headers, signature) = parse_keypairs(raw_signature)
        signing_string = construct_signing_string(headers)

        digest = SHA256.new(bytes(signing_string, 'utf-8'))

        decoded_signature = b64decode(signature)

        public_key = get_public_key(key_id)

        if str(public_key) == 'None':
            return error(f'Could not get public key. Key id: {key_id}', 400)

        app.logger.error(f'Public key has been located...')

        try:
            pkcs1_15.new(public_key).verify(digest, decoded_signature)
            app.logger.error('2')
        except:
            return error(f"""
            
            Signing string: {signing_string}
            
            Signature: {signature}

            Decoded signature: {decoded_signature}
            
            """, 400)
            app.logger.error('3')

        app.logger.error('4')

        body_digest = b64encode(SHA256.new(request.get_data()).digest())

        app.logger.error('5')

        header_digest = bytes(request.headers.get('Digest').replace('SHA-256=', ''), 'utf-8')

        app.logger.error('6')

        if body_digest != header_digest:
            j = request.get_data()
            app.logger.error(f"""
            
                Header and body digests don't match. :(

                Header digest: {header_digest}

                Digest of message body: {body_digest}

                Message body: {j}

            """)
            return error('Body digest does not match header digest')

            app.logger.error('7')

        app.logger.error('8')

        app.logger.error(f'Header Digest: {header_digest}')
        app.logger.error(f'Body digest: {body_digest}')


        return f(*args, **kwargs)

    wrapper.__name__ = f.__name__
    return wrapper