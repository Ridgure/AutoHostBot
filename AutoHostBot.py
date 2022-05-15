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
    global currentHost
    global currentTitle
    global currentGame
    content = "Now hosting the channel " + channel + " who is playing " + game + " with the title: " + title + ". Go check them out over at: https://twitch.tv/" + channel
    print "Tried to host the " + game + " stream: " + channel
    print "The title of the stream is: " + title.encode("utf-8", "ignore")
    if testing:
        try:
            print Nickname + ": " + "/host " + channel
            currentHost = channel
            currentTitle = title.encode("ascii", "ignore")
            currentGame = game
            Thread(target=streamLink(currentHost, currentGame, currentTitle)).start()
        except Exception as e:
            print "Error in testing of hosting of the Minecraft stream " + channel + " with the title: " + title
            print str(e)
            pass
    else:
        try:
            message("/host " + channel)
            currentHost = channel
            currentTitle = title.encode("ascii", "ignore")
            currentGame = game
            Thread(target=streamLink(currentHost, currentGame, currentTitle)).start()
            data = {
                'content': content,
                'username': "Riboture"
                    }
            r = requests.post(Webhook_url, data=json.dumps(data), headers={'Content-Type': 'application/json'})
        except Exception as e:
            print "Error in hosting the Minecraft stream " + channel + " with the title: " + title
            print str(e)
            pass

def streamLink(currentHost, currentGame, currentTitle):
    try:
            if testing:
                streamLinkStart = 'cmd /c "' + StreamLinkLocationBackup + ' -p ' + VLCLocationBackup + ' twitch.tv/' + currentHost
            else:
                streamLinkStart = 'cmd /c "' + StreamLinkLocation + ' -p ' + VLCLocation + ' twitch.tv/' + currentHost
            if "^" in currentTitle:
                currentTitle = re.sub(r"\^", "\^", currentTitle)
            if "|" in currentTitle:
                currentTitle = re.sub(r"\|", "^|", currentTitle)
            if "&" in currentTitle:
                currentTitle = re.sub(r"&", "and", currentTitle)
            if "\\" in currentTitle:
                currentTitle = re.sub(r"\\", "^\\", currentTitle)
            if "<" in currentTitle:
                currentTitle = re.sub(r"<", "\<", currentTitle)
            if ">" in currentTitle:
                currentTitle = re.sub(r">", "\>", currentTitle)
            streamLinkArguments = ' worst -l none --title "' + currentHost + " - " + currentGame + " - " + currentTitle + '"'
            os.system(streamLinkStart + streamLinkArguments)
    except IndexError:
        pass
    except Exception, e:
        print "An error occurred in Streamlink thread"
        print str(e)
        if str(e)[0:9] == "[Errno 10053]":
            print "An established connection was aborted by the sooftware in your host machine"
            try:
                url = "https://api.twitch.tv/helix/streams?user_login=" + currentHost
                params = {"Client-ID": "" + ClientID + "", "Authorization": "Bearer " + BotToken}
                response = requests.get(url, headers=params)
                streamData = response.json()
                if response.status_code == 400:
                    print "Bad request"
                if response.status_code == 429:
                    print "Too many user requests"
                if not streamData['data']:
                    print "Currently hosted stream is no longer live. New stream will be hosted"
                    host()
            except IndexError:
                pass
            except Exception, e:
                print "An error just occurred after the stream is no longer outputting data"
                print str(e)
        elif str(e)[0:9] == "[Errno 10054]":
            try:
                print "An existing connection was forcibly closed by the remote host"
            except IndexError:
                pass
            except Exception, e:
                print "An error just occurred after the stream is no longer outputting data"
                print str(e)
        pass

def notice():
    text = re.search(r'(?<=NOTICE)\W+\w+\s\:(.*)', response).group(1)
    msgId = re.search(r'(?<=msg-id=)\w+', response).group(0)
    if msgId == "host_on":
        print "Target was successfully hosted"
    elif msgId == "host_off":
        print "Exited host mode"
        exit()
    elif msgId == "host_target_went_offline":
        print "target went offline"
        host()
    elif msgId == "hosts_remaining":
        print(text)
    elif msgId == "bad_host_rate_exceeded":
        print(text)
    elif msgId == "bad_host_hosting":
        print(text)


def host():
    global minecraftStream
    global hostGameStream
    global currentHost
    global currentTitle
    global currentGame
    print "Searching for Minecraft streams"
    for i1 in range(len(AutoHostList.hostList)):
        try:
            url = "https://api.twitch.tv/helix/streams?user_login=" + AutoHostList.hostList[i1]
            params = {"Client-ID": "" + ClientID + "", "Authorization": "Bearer " + BotToken}
            response = requests.get(url, headers=params)
            streamData = response.json()
            if response.status_code == 400:
                print "Bad request"
                break
            elif response.status_code == 429:
                print "Too many user requests"
                break
            elif not streamData['data']:
                pass
            elif streamData['data'][0]['game_name'] == 'Minecraft':
                game = streamData['data'][0]['game_name']
                channel = AutoHostList.hostList[i1]
                title = streamData['data'][0]['title']
                c = 0
                for i5 in AutoHostList.blackListTitle:
                    if re.search(r"" + i5.lower(), title.lower().encode("utf-8", "ignore")):
                        c = 1
                        break
                if c == 1:
                    pass
                else:
                    host_channel(channel, title, game)
                    minecraftStream = True
                    break
            else:
                minecraftStream = False
        except Exception as e:
            print "Error in getting the Minecraft stream " + channel + " with the title: " + title
            print str(e)
            pass
    if not minecraftStream:
        print "No Minecraft streams found"
        for i3 in range(len(AutoHostList.hostGames)):
            print "Searching for " + AutoHostList.hostGames[i3] + " streams"
            for i2 in range(len(AutoHostList.hostList)):
                try:
                    url = "https://api.twitch.tv/helix/streams?user_login=" + AutoHostList.hostList[i2]
                    params = {"Client-ID": "" + ClientID + "", "Authorization": "Bearer " + BotToken}
                    response = requests.get(url, headers=params)
                    streamData = response.json()
                    if response.status_code == 400:
                        print ("Bad request")
                        break
                    elif response.status_code == 429:
                        print ("Too many user requests")
                        break
                    elif not streamData['data']:
                        pass
                    elif streamData['data'][0]['game_name'] == AutoHostList.hostGames[i3]:
                        game = streamData['data'][0]['game_name']
                        channel = AutoHostList.hostList[i2]
                        title = streamData['data'][0]['title']
                        c = 0
                        for i6 in AutoHostList.blackListTitle:
                            if re.search(r"" + i6.lower(), title.lower().encode("utf-8", "ignore")):
                                c = 1
                                break
                        if c == 1:
                            pass
                        else:
                            host_channel(channel, title, game)
                            hostGameStream = True
                            break
                    else:
                        hostGameStream = False
                except Exception as e:
                    print "Error in getting the good game stream " + channel + " with the title: " + title
                    print str(e)
                    pass
            if hostGameStream:
                break
            else:
                print "No " + AutoHostList.hostGames[i3] + " streams found"
    elif not minecraftStream and not hostGameStream:
        print "No good games are being streamed"
        for i4 in range(len(AutoHostList.hostList)):
            try:
                url = "https://api.twitch.tv/helix/streams?user_login=" + AutoHostList.hostList[i4]
                params = {"Client-ID": "" + ClientID + "", "Authorization": "Bearer " + BotToken}
                response = requests.get(url, headers=params)
                streamData = response.json()
                if response.status_code == 429:
                    print "Too many user requests"
                    break
                if not streamData['data']:
                    pass
                else:
                    game = streamData['data'][0]['game_name']
                    channel = AutoHostList.hostList[i4]
                    title = streamData['data'][0]['title']
                    c = 0
                    print "Searching for any stream with good title"
                    for i5 in AutoHostList.blackListTitle:
                        if re.search(r"" + i5.lower(), title.lower().encode("utf-8", "ignore")):
                            c = 1
                            break
                    if c == 1:
                        pass
                    else:
                        host_channel(channel, title, game)
                        break
            except Exception as e:
                print "Error in getting the non good game stream " + channel + " with the title: " + title
                print (str(e))
                pass


s = socket.socket()
s.connect((Host, Port))
s.send("PASS {}\r\n".format("oauth:" + UserToken).encode("utf-8"))
s.send("NICK {}\r\n".format(Nickname).encode("utf-8"))
s.send("JOIN {}\r\n".format(Channel).encode("utf-8"))
s.send("CAP REQ :twitch.tv/commands\r\n")
s.send("CAP REQ :twitch.tv/tags\r\n")

# Global variables
minecraftStream = False
hostGameStream = False
currentHost = ""
currentTitle = ""
currentGame = ""
testing = True

while True:

    try:
        response = s.recv(1024).decode("utf-8")
        data = response.strip("\r\n")
        if response == "":
            print "Lost connection"
            exit()
        elif "PING" in data:
            s.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
            try:
                url = "https://api.twitch.tv/helix/streams?user_login=" + currentHost
                params = {"Client-ID": "" + ClientID + "", "Authorization": "Bearer " + BotToken}
                response = requests.get(url, headers=params)
                streamData = response.json()
                if response.status_code == 400:
                    print "Bad request"
                    break
                if response.status_code == 429:
                    print "Too many user requests"
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
                            if i == currentGame:
                                c = 1
                                break
                        if c == 1:
                            pass
                        else:
                            print "Current stream is no longer streaming a good game. New stream will be hosted"
                            host()
                if currentTitle == streamData['data'][0]['title']:
                    pass
                else:
                    print "Title changed to: " + streamData['data'][0]['title'].encode("utf-8", "ignore")
                    currentTitle = streamData['data'][0]['title']
                    c = 0
                    for i5 in AutoHostList.blackListTitle:
                        if re.search(r"" + i5.lower(), currentTitle.lower().encode("utf-8", "ignore")):
                            c = 1
                            break
                    if c == 1:
                        print "This title is no longer good and a new stream will be hosted"
                        host()
            except Exception as e:
                print "Error in getting non good game streams"
                print str(e)
                pass
        elif "JOIN" in data:
            username = re.search(r':(\w+)', response).group(1)
            if username == Nickname:
                print data
                print "Successfully joined " + Channel
                if "End of /NAMES list" in data:
                    host()
            pass
        elif "PART" in data:
            print data
            username = re.search(r':(\w+)', response).group(1)
            if username == Nickname:
                print Nickname + " has left the channel " + Channel
            pass
        elif "NOTICE" and "HOSTTARGET" in data:
            print data
            notice()
        elif "NOTICE" in data:
            print data
            notice()
        elif "HOSTTARGET" in data:
            try:
                print data
                currentHost = re.search(r'(?<=HOSTTARGET)\W+\w+\s\:(\w*)', response).group(1)
                streamEnd = re.search(r'(?<=HOSTTARGET)\W+\w+\s\:(\w*)(\W)', response).group(2)
                url = "https://api.twitch.tv/helix/streams?user_login=" + currentHost
                params = {"Client-ID": "" + ClientID + "", "Authorization": "Bearer " + BotToken}
                response = requests.get(url, headers=params)
                streamData = response.json()
                if response.status_code == 400:
                    print "Bad request"
                    break
                elif response.status_code == 429:
                    print "Too many user requests"
                    break
                elif not streamData['data']:
                    print "Host target is not live"
                elif streamEnd == "-":
                    print "Hosted stream went offline"
                    currentGame = streamData['data'][0]['game_name']
                    currentTitle = streamData['data'][0]['title']
                    content = "Now hosting the channel " + currentHost + " who is playing " + currentGame + " with the title: " + currentTitle.encode("utf-8", "ignore") + ". Go check them out over at: https://twitch.tv/" + currentHost
                    print "Manually hosted the " + currentGame + " stream: " + currentHost
                    print "The title of the stream is: " + currentTitle.encode("utf-8", "ignore")
                    if not testing:
                        Thread(target=streamLink(currentHost, currentGame, currentTitle)).start()
                        data = {
                            'content': content,
                            'username': "Riboture"
                        }
                        r = requests.post(Webhook_url, data=json.dumps(data), headers={'Content-Type': 'application/json'})
            except Exception as e:
                print "Error manually hosting stream"
                print str(e)
                pass
        else:
            pass
        sleep(0.1)  # If bot is registered 0.1, Else put 2/3 if you do not want a global 30 minute timeout
    except IndexError:
        pass
    except Exception, e:
        if str(e)[0:9] == "[Errno 10053]":
            print "An established connection was aborted by the sooftware in your host machine"
            try:
                url = "https://api.twitch.tv/helix/streams?user_login=" + currentHost
                params = {"Client-ID": "" + ClientID + "", "Authorization": "Bearer " + BotToken}
                response = requests.get(url, headers=params)
                streamData = response.json()
                if response.status_code == 400:
                    print "Bad request"
                if response.status_code == 429:
                    print "Too many user requests"
                if not streamData['data']:
                    print "Currently hosted stream is no longer live. New stream will be hosted"
                    host()
            except IndexError:
                pass
            except Exception, e:
                print "An error just occurred after the stream is no longer outputting data"
                print str(e)
        elif e[0:9] == "[Errno 10054]":
            try:
                print "An existing connection was forcibly closed by the remote host"
            except IndexError:
                pass
            except Exception, e:
                print "An error just occurred after the stream is no longer outputting data"
                print str(e)
        s.shutdown(1)
        s.close()
        s = socket.socket()
        s.connect((Host, Port))
        s.send("PASS {}\r\n".format("oauth:" + UserToken).encode("utf-8"))
        s.send("NICK {}\r\n".format(Nickname.lower()).encode("utf-8"))
        s.send("JOIN {}\r\n".format(Channel).encode("utf-8"))
        s.send("CAP REQ :twitch.tv/commands\r\n")
        s.send("CAP REQ :twitch.tv/tags\r\n")
        pass
