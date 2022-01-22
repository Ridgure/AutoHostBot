<a href="http://www.twitch.tv/ridgure"><img src="https://pbs.twimg.com/profile_banners/4144666635/1497981943/1500x500" title="FVCproductions" alt="FVCproductions"></a>

<h1 align="center">
  <br>
  <a href="http://www.twitch.tv/ridgure"><img src="https://pbs.twimg.com/profile_images/965416492924891136/N-EvLzcd_400x400.jpg" alt="Markdownify" width="200"></a>
  <br>
  Auto Host Bot
  <br>
</h1>

<h4 align="center">An IRC bot written in python and made for my Twitch channel <a href="https://twitch.tv/ridgure" target="_blank">Twitch.tv/Ridgure</a>.</h4>

<p align="center">
  <a href="#key-features">Key Features</a> •
  <a href="#getting-started">Getting started</a> •
  <a href="#acknowledgements">Acknowledgements</a> •
  <a href="#connect">Connect</a>
</p>

## Features:

**Auto hosting:**

###### Commands for everyone:

| General:      | 
| ------------- |
| Host function that will host the the person on top of your host list    |

**Automated functions:**

| Done by the bot automatically:| 
| ------------- |
|Filter stream titles with regular expressions|
|Filter games so only games that you like are hosted|
|Hosts a new stream as soon as the current stream switches to a game you don't like|

| Socials:      |Links to socials:|                  
| ------------- |:-------------:|
| !social       | Shows all Ridgure's social media accounts| 
| !instagram    | [link to Instagram](https://www.instagram.com/rigidstructure/?hl=en)|
| !facebook     | [link to Facebook](https://www.facebook.com/ridgidstructure)|    
| !twitter      | [link to Twitter](https://twitter.com/ridgure)|  
| !discord      | [link to Discord](https://discord.com/invite/yddBmCE)|  
| !ctt          | Generates a custom Click to Tweet link when sent in the twitch chat|


## Getting started

**Clone**

Clone this repository to your local machine using 
```git clone https://github.com/Ridgure/TwitchBot.git```

**Setup**

In order to be able to run the bot add a file `config.py` in the same folder as the bot and go through the steps below:
`config.py` should look something like this:

```python
Host = "irc.twitch.tv"         # The Twitch IRC server
Port = 6667                    # Always use port 6667!
Nickname = "<Name>"            # Your Twitch username, lowercase
Token = "<Token>"    # Self generated token that has to have the editor scope
Channel = "#<Channel>"         # The channel you want to join
ClientID = "<ClientID>"        # Your client ID
```

- Create a Twitch account with the name of your bot
- Register your application on the [Twitch developer site](https://glass.twitch.tv/login)
  - Set the Name to the name of the account you just created
  - Set the redirect uri to `http://localhost`
  - Set the application directory to Chat Bot
  - Agree to the terms and conditions
  - Get a `Client_ID` and a `Client_Secret`
- Generate your token for accessing follower data and chat
  - Go to  [Get token here](twitchapps.com/tmi) and click connect with twitch
  - Click Authorize
  - Your token should look something like this: `oauth:a1b2c3d4e5f6g7h8i9j1k2l3m5n6o7`
- Generate your token for accessing subscriber data
  - Go to the link underneath 
  - Remember to swap out `<clientID>` with your `client id!`
  - Click Authenticate
  - It will look like you got a blank page but your url should look like the second url
  - Your access token is the gibberish where it says Token in the url 

```
https://id.twitch.tv/oauth2/authorize?client_id=<clientID>&redirect_uri=http://localhost&response_type=token&scope=channel_subscriptions+user_read+channel_check_subscription+chat_login
http://localhost/#access_token=<Token>&scope=channel_subscriptions+user_read+channel_check_subscription+chat_login&token_type=bearer
```

**Prerequisites**

You will need to install these things to run the bot

- [Python 2.7.x](https://www.python.org/downloads/)
- Libraries:
  - [Requests](https://github.com/psf/requests)
  - [Regular Expressions](https://pypi.org/project/regex/)
  
**Running the bot**

Run [bot.py](docs/bot.py) by going to its location and running this command:

```python
python bot.py
```

## Acknowledgements:

This whole project started off with this [Instructables article](https://www.instructables.com/id/Twitchtv-Moderator-Bot/)

**Other interesting projects to check out:**

[PythonBot](https://github.com/ZERG3R/PythonBot) by ZERG3R on Twitch as [ZERG3R](https//:twitch.tv/ZERG3R)

Ponderier by DillonEA on Twitch as [DillonEA](https//:twitch.tv/DillonEA)

[Xekeism](https://www.xekeland.com/) by XekeDeath on Twitch as [XekeDeath](https//:twitch.tv/DillonEA)

## Connect:

**Twitch**

See the bot in action when I am live on [Twitch](https://twitch.tv/ridgure) over at [Twitch.tv/Ridgure](https://twitch.tv/ridgure)

**Social media**

Please follow me on:
[Facebook](https://www.Facebook.com/ridgure), 
[Twitter](https://www.Twitter.com/ridgure) and
[Instagram](https://www.Instagram.com/rigidstructure)