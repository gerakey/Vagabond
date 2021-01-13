# Vagabond

[Vagabond](https://www.teamvagabond.com) is a federated social network built using the ActivityPub protocol that prioritizes user privacy, security, and autonomy. Vagabond is free and open source software.  

## Developer Instructions

Two shell scripts are included with this repository to run via git bash on Windows or the native terminal on MacOS/Linux. These scripts **must be run in the root directory of the repository**. 

*update.sh* will download the latest dependencies for both the client and server. This should be run every time you use git pull. 

*build.sh* will produce a production ready version of the client and server. 

*deploy.sh* will build a production ready version of the client and server and deploy it to a local apache web server. Only use this script on the VPS. 

## About

Vagabond is a federated social network built using the [ActivityPub](https://www.w3.org/TR/2018/REC-activitypub-20180123/) protocol. It protects user privacy by offering:

* User defined blacklists to restrict outbound traffic
* Support for sending and receiving encrypted messages using public key cryptography
* Ephemeral identities to mask post history
* Minimal bundle size and efficient AJAX requests to accommodate users of TOR and other anonymity networks
* Automatic stripping of image metadata prior to being stored server-side
* The ability to erase all user data at any time, immediately, and with no questions asked
* The ability to request a complete copy of all user data free of charge

## Compatability

Vagabond is compatible with the [Mastodon](https://mastodon.social/about) network when the authentication method is set to MASTODON in the configuration file. 
