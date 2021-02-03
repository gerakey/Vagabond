# Vagabond

[Vagabond](https://www.teamvagabond.com) is a federated social network built using the ActivityPub protocol that prioritizes user privacy, security, and autonomy. Vagabond is [free and open source software](https://www.gnu.org/licenses/gpl-3.0.en.html).  

## Features

* Anonymous registration without email
* Multiple profiles per account
* Ephemeral identities to mask post history
* Encrypted messaging suite
* The ability to request a copy of or erase all user data at any time, immediately, and with no questions asked
* Automatic stripping of image metadata prior to being stored server-side
* User defined blacklists to restrict outbound traffic
* Minimal bundle size and efficient AJAX requests to accommodate users of TOR and other anonymity networks

## Compatability

Vagabond is compatable with [Mastodon's](https://github.com/tootsuite/mastodon) authentication protocol. 

## Developer Instructions

Vagabond comes with a number of shell scripts to automate deployment and project setup. All scripts are written under two assumptions:

1. **The scripts are being executed from the same directory they are located in.** 
2. The host platform is Ubuntu version 20.04 or higher. 

*initialize.sh* should be run after cloning the repository. 

*update.sh* will download the latest dependencies for both the client and server. 

*build.sh* will produce a production ready version of the client and server. 

*deploy.sh* will build a production ready version of the client and server and deploy it to a local apache web server to the /var/www/$USER directory. 

*server_deploy.sh* will apply the latest server-side changes without recompiling the client. 
