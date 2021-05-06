from datetime import datetime
from random import randint

import tweepy
from PIL import Image, ImageDraw, ImageFont

from config import *
from lines import *

def run():
    print("Running quenau-bot.py at", str(datetime.now()))
    sonnet = generateSonnet()
    counter = updateTotalCounter()
    generateTwitterImage(sonnet)
    tweetSonnet(sonnet,counter)
    print("Finished.")

def generateSonnet():

    sonnet = []
    number = ""

    for line in lines:
        choice = randint(0,9)
        sonnet.append(line[choice])
        number += str(choice)           # each line controls one digit of number
                                        # reverse the number and add 1 so
    number = int(number[::-1]) + 1      # all first choices = 1, all last = 10^14
    sonnet.append("{:,}".format(number).replace(","," "))
    return sonnet

def updateTotalCounter():

    # if the counter file doesn't exist, create it; increment the counter
    try:
        with open("counter.txt", "r") as rf:
            counter = int(rf.read()) + 1
    except:
        open("counter.txt", "w")
        counter = 1

    # save the new counter and return the value
    with open("counter.txt", "w") as wf:
        wf.write(str(counter))
    return counter

def generateTwitterImage(sonnet):

    im = Image.new("RGB",(3600,2025),(255,255,255))         # make large and shrink
    draw = ImageDraw.Draw(im)                               # to smooth out text

    title_font = ImageFont.truetype("./fonts/Goudy Old Style Bold.ttf", 120, encoding="unic")
    text_font = ImageFont.truetype("./fonts/Goudy Old Style Regular.ttf", 91, encoding="unic")

    # add title
    draw.multiline_text((1000,50), sonnet[14], font=title_font, fill=(0, 0, 0))

    # add sonnet
    text = ""
    for line in range(0,14):
        text += sonnet[line] + "\n"
        if line in [3,7,10]:
            text += "\n"
    draw.multiline_text((1000,210), text, font=text_font, fill=(0, 0, 0,), spacing=20)

    im = im.resize((1200,675), Image.ANTIALIAS)
    im.save("sonnet.png")

def tweetSonnet(sonnet,counter):

    # authenticate and set up the Twitter bot
    try:
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        twitter = tweepy.API(auth)
    except Exception as e:
        print("Error authenticating with Twitter:",e)

    # upload the image
    try:
        sonnet_image = twitter.media_upload("sonnet.png")
    except Exception as e:
        print("Error uploading image:",e)

    # Calculate remaining sonnets to tweet
    # I assume that the bot will never repeat sonnets because at the rate of one per hour
    # it will not be finished for 11.4 billion years.
    remaining = "{:,}".format(100000000000000 - counter).replace(","," ")

    # post the tweet with text
    tweet_text = "Voici le sonnet " + sonnet[14] + " sur " + "100 000 000 000 000. Il en reste " + remaining + " à tweeter."
    try:
        twitter.update_status(status=tweet_text,media_ids=[sonnet_image.media_id])
        print("Tweet of sonnet",sonnet[14],"sent successfully!")
    except Exception as e:
        print("Error posting tweet:",e)

run()