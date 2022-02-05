#!/usr/bin/env python
# -*- coding: utf-8 -*-
# bot.py

import os
import re
import socket
import json
from threading import Thread
import AutoHostList
import requests
from AutoHostConfig import *
from time import sleep


def message(msg):
    try:
        s.send("PRIVMSG " + Channel + " :" + msg + "\n")
        print Nickname + ": " + msg
        sleep(30 / 20)
    except IndexError:
        pass


def host_channel(channel, title, game):
    # comment this out if you want to disable hosts for testing
    # print "test host " + channel
    message("/host " + channel)
    content = "Now hosting the channel " + channel + " who is playing " + game + " with the title: " + title + ". Go check them out over at: https://twitch.tv/" + channel
    data = {
        'content': content,
        'username': "Riboture"
            }
    r = requests.post(Webhook_url, data=json.dumps(data), headers={'Content-Type': 'application/json'})


def streamLink():
    os.system('cmd /c "' + StreamLinkLocation + ' -p ' + VLCLocation + ' twitch.tv/' + currentHost + ' worst"')


def host():
    global minecraftStream
    global hostGame
    global currentHost
    global currentTitle
    global currentGame
    for i1 in range(len(AutoHostList.hostList)):
        try:
            url = "https://api.twitch.tv/helix/streams?user_login=" + AutoHostList.hostList[i1]
            params = {"Client-ID": "" + ClientID + "", "Authorization": "Bearer " + FollowerToken}
            response = requests.get(url, headers=params)
            streamData = response.json()
            if response.status_code == 400:
                print ("Bad request")
                break
            if response.status_code == 429:
                print ("Too many user requests")
                break
            elif not streamData['data']:
                pass
            elif streamData['data'][0]['game_name'] == 'Minecraft':
                game = streamData['data'][0]['game_name']
                channel = AutoHostList.hostList[i1]
                title = streamData['data'][0]['title'].encode('utf', 'ignore')
                c = 0
                for i5 in AutoHostList.blackListTitle:
                    if re.search(r"" + i5.lower(), title.lower()):
                        c = 1
                        break
                if c == 1:
                    pass
                else:
                    host_channel(channel, title, game)
                    print ("Tried to host the Minecraft stream: " + channel)
                    print ("They are playing: " + game)
                    print ("The title of the stream is: " + title)
                    minecraftStream = True
                    currentHost = channel
                    currentTitle = title
                    currentGame = game
                    Thread(target=streamLink).start()
                    break
            else:
                minecraftStream = False
        except Exception as e:
            print "Error in getting Minecraft streams"
            print (str(e))
            pass
    if not minecraftStream:
        print "No Minecraft streams found"
        for i3 in range(len(AutoHostList.hostGames)):
            for i2 in range(len(AutoHostList.hostList)):
                try:
                    url = "https://api.twitch.tv/helix/streams?user_login=" + AutoHostList.hostList[i2]
                    params = {"Client-ID": "" + ClientID + "", "Authorization": "Bearer " + FollowerToken}
                    response = requests.get(url, headers=params)
                    streamData = response.json()
                    if response.status_code == 400:
                        print ("Bad request")
                        break
                    if response.status_code == 429:
                        print ("Too many user requests")
                        break
                    elif not streamData['data']:
                        pass
                    elif streamData['data'][0]['game_name'] == AutoHostList.hostGames[i3]:
                        game = streamData['data'][0]['game_name']
                        channel = AutoHostList.hostList[i2]
                        title = streamData['data'][0]['title'].encode('utf', 'ignore')
                        c = 0
                        titleLowercase = title.lower()
                        for i5 in AutoHostList.blackListTitle:
                            if re.search(r"" + i5.lower(), titleLowercase):
                                c = 1
                                break
                        if c == 1:
                            pass
                        else:
                            host_channel(channel, title, game)
                            print ("Tried to host the non Minecraft stream: " + channel)
                            print ("They are playing: " + game)
                            print ("The title of the stream is: " + title)
                            hostGame = True
                            currentHost = channel
                            Thread(target=streamLink).start()
                            break
                    else:
                        hostGame = False
                except Exception as e:
                    print "Error in getting good game streams"
                    print (str(e))
                    pass
    if not hostGame and not minecraftStream:
        print "No good games are being streamed"
        for i4 in range(len(AutoHostList.hostList)):
            try:
                url = "https://api.twitch.tv/helix/streams?user_login=" + AutoHostList.hostList[i4]
                params = {"Client-ID": "" + ClientID + "", "Authorization": "Bearer " + FollowerToken}
                response = requests.get(url, headers=params)
                streamData = response.json()
                if response.status_code == 429:
                    print ("Too many user requests")
                    break
                if not streamData['data']:
                    pass
                else:
                    game = streamData['data'][0]['game_name']
                    channel = AutoHostList.hostList[i4]
                    title = streamData['data'][0]['title'].encode('utf', 'ignore')
                    c = 0
                    titleLowercase = title.lower()
                    for i5 in AutoHostList.blackListTitle:
                        if re.search(r"" + i5.lower(), titleLowercase):
                            c = 1
                            break
                    if c == 1:
                        pass
                    else:
                        host_channel(channel, title, game)
                        print ("Tried to host the other game stream: " + channel)
                        print ("They are playing: " + game)
                        print ("The title of the stream is: " + title)
                        currentHost = channel
                        Thread(target=streamLink).start()
                        break
            except Exception as e:
                print "Error in getting non good game streams"
                print (str(e))
                pass


s = socket.socket()
s.connect((Host, Port))
s.send("PASS {}\r\n".format("oauth:" + SubscriberToken).encode("utf-8"))
s.send("NICK {}\r\n".format(Nickname).encode("utf-8"))
s.send("JOIN {}\r\n".format(Channel).encode("utf-8"))
s.send("CAP REQ :twitch.tv/commands\r\n")
s.send("CAP REQ :twitch.tv/tags\r\n")

# Global variables
minecraftStream = False
hostGame = False
currentHost = ""
currentTitle = ""
currentGame = ""

# Host a stream when the bot starts
host()

while True:

    try:
        response = s.recv(1024).decode("utf-8")
        data = response.strip("\r\n")
        if response == "":
            print "Lost connection"
            exit()
        if response == "PING :tmi.twitch.tv\r\n":
            s.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
            try:
                url = "https://api.twitch.tv/helix/streams?user_login=" + currentHost
                params = {"Client-ID": "" + ClientID + "", "Authorization": "Bearer " + FollowerToken}
                response = requests.get(url, headers=params)
                streamData = response.json()
                if response.status_code == 400:
                    print ("Bad request")
                    break
                if response.status_code == 429:
                    print ("Too many user requests")
                    break
                if not streamData['data']:
                    print "Currently hosted stream is no longer live. New stream will be hosted"
                    host()
                if currentGame == streamData['data'][0]['game_name']:
                    pass
                else:
                    print "Game changed to: " + streamData['data'][0]['game_name']
                    currentGame = streamData['data'][0]['game_name']
                    if currentGame == 'Minecraft':
                        minecraftStream = True
                    else:
                        c = 0
                        for i in AutoHostList.hostGames:
                            print i
                            if i == currentGame:
                                c = 1
                                break
                        if c == 1:
                            pass
                        else:
                            print "Current stream is no longer streaming a good game. New stream will be hosted"
                            host()
                if currentTitle == streamData['data'][0]['title'].encode('utf', 'ignore'):
                    pass
                else:
                    print "Title changed to: " + streamData['data'][0]['game_name']
                    currentTitle = streamData['data'][0]['title'].encode('utf', 'ignore')
                    c = 0
                    currentTitleLowercase = currentTitle.lower()
                    for i5 in AutoHostList.blackListTitle:
                        if re.search(r"" + i5.lower(), currentTitleLowercase):
                            c = 1
                            break
                    if c == 1:
                        print "This title is no longer good and a new stream will be hosted"
                        host()
            except Exception as e:
                print "Error in getting non good game streams"
                print (str(e))
                pass
        elif "NOTICE" in data:
            print data
            text = re.search(r'(?<=NOTICE)\W+\w+\s\:(.*)', response).group(1)
            id = re.search(r'(?<=msg-id=)\w+', response).group(0)
            if id == "host_on":
                print("Target was successfully hosted")
            elif id == "host_off":
                print("Exited host mode")
                exit()
            elif id == "host_target_went_offline":
                print("target went offline")
                host()
            elif id == "hosts_remaining":
                print(text)
        else:
            print "Response: " + data
        sleep(0.1) #If bot is registered 0.1, Else put 2/3 if you do not want a global 30 minute timeout
    except IndexError:
        pass
    except Exception, e:
        print "An error just occurred"
        print str(e)
        s.shutdown(1)
        s.close()
        s = socket.socket()
        s.connect((Host, Port))
        s.send("PASS {}\r\n".format("oauth:" + SubscriberToken).encode("utf-8"))
        s.send("NICK {}\r\n".format(Nickname.lower()).encode("utf-8"))
        s.send("JOIN {}\r\n".format(Channel).encode("utf-8"))
        s.send("CAP REQ :twitch.tv/commands\r\n")
        s.send("CAP REQ :twitch.tv/tags\r\n")
        pass
