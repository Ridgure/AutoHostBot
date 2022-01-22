#!/usr/bin/env python
# -*- coding: utf-8 -*-
# bot.py

import re
import socket
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


def host_channel(channel):
    #comment this out if you want to disable hosts for testing
    message("/host " + channel)


def host():
    global minecraftStream
    global hostGame
    global currentHost
    for i1 in range(len(AutoHostList.hostList)):
        try:
            url = "https://api.twitch.tv/helix/streams?user_login=" + AutoHostList.hostList[i1]
            params = {"Client-ID": "" + ClientID + "", "Authorization": "Bearer " + FollowerToken}
            response = requests.get(url, headers=params)
            streamData = response.json()
            if response.status_code == 429:
                print ("Too many user requests")
                break
            elif not streamData['data']:
                pass
            elif streamData['data'][0]['game_name'] == 'Minecraft':
                c = 0
                title = streamData['data'][0]['title'].encode('utf', 'ignore').lower()
                for i5 in AutoHostList.blackListTitle:
                    if re.match(i5.lower(), title):
                        c = 1
                        break
                if c == 1:
                    pass
                else:
                    host_channel(AutoHostList.hostList[i1])
                    print ("Tried to host the Minecraft stream: " + AutoHostList.hostList[i1])
                    print ("The title of the stream is: " + streamData['data'][0]['title'])
                    minecraftStream = True
                    currentHost = AutoHostList.hostList[i1]
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
                    if response.status_code == 429:
                        print ("Too many user requests")
                        break
                    elif not streamData['data']:
                        pass
                    elif streamData['data'][0]['game_name'] == AutoHostList.hostGames[i3]:
                        c = 0
                        title = streamData['data'][0]['title'].encode('utf', 'ignore').lower()
                        for i5 in AutoHostList.blackListTitle:
                            if re.match(i5.lower(), title):
                                c = 1
                                break
                        if c == 1:
                            pass
                        else:
                            host_channel(AutoHostList.hostList[i2])
                            print ("Tried to host the Minecraft stream: " + AutoHostList.hostList[i2])
                            print ("The title of the stream is: " + streamData['data'][0]['title'])
                            hostGame = True
                            currentHost = AutoHostList.hostList[i2]
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
                    c = 0
                    title = streamData['data'][0]['title'].encode('utf', 'ignore').lower()
                    for i5 in AutoHostList.blackListTitle:
                        if re.match(i5.lower(), title):
                            c = 1
                            break
                    if c == 1:
                        pass
                    else:
                        host_channel(AutoHostList.hostList[i4])
                        print ("Tried to host" + AutoHostList.hostList[i4])
                        print ("The title of the stream is: " + streamData['data'][0]['title'])
                        currentHost = AutoHostList.hostList[i4]
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
            print "Reply: PONG :tmi.twitch.tv"
            try:
                url = "https://api.twitch.tv/helix/streams?user_login=" + currentHost
                params = {"Client-ID": "" + ClientID + "", "Authorization": "Bearer " + FollowerToken}
                response = requests.get(url, headers=params)
                streamData = response.json()
                if response.status_code == 429:
                    print ("Too many user requests")
                    break
                if not streamData['data']:
                    print "Currently hosted stream is no longer live. New stream will be hosted"
                    host()
                currentGame = streamData['data'][0]['game_name']
                currentTitle = streamData['data'][0]['title']
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
