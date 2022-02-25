import discord
import os
import requests
from bs4 import BeautifulSoup
from pycoingecko import CoinGeckoAPI
import random
import csv


TOKEN = os.environ["TOKEN"]

client = discord.Client()


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    if message.content.startswith('$greet'):
        await message.channel.send('Hello ' + message.author.name)
    #print(dir(message))
    if message.content.startswith('$echo'):
        await message.channel.send(message.content[1:])

    if message.content == '$s&p':
      ticker = '%5EGSPC'
      url=requests.get("https://finance.yahoo.com/quote/"+ ticker)
      soup = BeautifulSoup(url.text, "html.parser")
      result = soup.find("fin-streamer", {"class":"Fw(b) Fz(36px) Mb(-4px) D(ib)"})
      await message.channel.send(result.text)

    if message.content.startswith('$stock'):
      stock = message.content.split(" ")[-1]
      url=requests.get("https://finance.yahoo.com/quote/"+ stock.upper())
      soup = BeautifulSoup(url.text, "html.parser")
      result = soup.find("fin-streamer", {"class":"Fw(b) Fz(36px) Mb(-4px) D(ib)"})
      #print(result)
      if not result:
         await message.channel.send("There is no such ticker: " + stock.upper())
      await message.channel.send("The price of " + stock.upper() + ": $" + result.text)

    if message.content.startswith('$weather'):
      url = requests.get('https://weather.com/weather/today/l/40d92ffe08acbc7c20fdcbbfe506ad8afc966707687735f6721261542f362d83?unit=m')
      soup = BeautifulSoup(url.text, "html.parser")
      
      result = soup.find("span", {"class":"CurrentConditions--tempValue--3a50n"})

      await message.channel.send("The weather is: " + result.text + "C")

    if message.content.startswith('$quote'):
      url = requests.get('https://zenquotes.io/api/random')

      quote = url.json()[0]['q']
      await message.channel.send(quote)

    if message.content.startswith('$bitcoin'):
      cg = CoinGeckoAPI()
      price = cg.get_price(ids='bitcoin', vs_currencies='usd')
      usd_price = str(price['bitcoin']['usd'])

      await message.channel.send("Master, the price of bitcoin as of now is $" + usd_price)

    if message.content.startswith('$crypto'):
      cg = CoinGeckoAPI()
      crypto = message.content.split(" ")[-1]
      price = cg.get_price(ids=crypto, vs_currencies='usd')
      usd_price = str(price[crypto]['usd'])
      
      await message.channel.send("Master, the price of " + crypto + " as of now is $" + usd_price)

  
    if message.content.startswith('$malaysia_news'):
      url = requests.get('https://newsapi.org/v2/top-headlines?country=my&apiKey=3953e6fe0f3042fe8b94ab707457d9ae')
      all_articles = url.json()['articles']
      random_article = random.choice(all_articles)
      await message.channel.send(random_article['url'])

    if message.content.startswith('$news'):
      topic=message.content[1:]
      url = requests.get('https://newsapi.org/v2/everything?q='+ topic+'&apiKey=3953e6fe0f3042fe8b94ab707457d9ae')
      all_articles = url.json()['articles']
      if all_articles != None:
        random_article = random.choice(all_articles)
      await message.channel.send(random_article['url'])

    if message.content.startswith('$write'):
      text = message.content.split(" ")
      text.pop(0)
      with open('report.csv', 'a') as f: #a for append new line, w for overwrite
        # create the csv writer
        writer = csv.writer(f)
        # write a row to the csv file
        writer.writerow(text)
      await message.channel.send("Written!")

    if message.content.startswith('$read'):
      with open('report.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=' ')
        for row in reader:
          await message.channel.send(', '.join(row))

    if message.content.startswith('$analyze'):
      with open('ratings.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        largest_rating=0
        for row in reader:
          # print(row)
          # print(int(row[1]))
          current_row_vote = int(row[1])
          if current_row_vote > largest_rating:
            largest_rating = current_row_vote
            top_voted = row[0]
          #convert vote counter from string to integer
      await message.channel.send('The top voted place was ' + top_voted + ' with '+ str(largest_rating) + ' votes')

    if message.content.startswith('$vote_list'):
      restaurant_list='You may choose: to vote for:\n'
      with open('vote.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
          restaurant_list=restaurant_list+row[0]+'\n'
      await message.channel.send(restaurant_list)

    if message.content.startswith('$vote '):
      restaurant_name = message.content[6:]
      vote=0
      r = csv.reader(open('vote.csv'))
      lines = list(r)
      for restaurants in lines:
        if restaurants[0] == restaurant_name:
          print(restaurants)
          restaurants[1]=int(restaurants[1])+1
      with open('vote.csv', 'w', newline ='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(lines)
      await message.channel.send('You have vote for ' + restaurant_name)
      
client.run(TOKEN)

# Taco Bell,0
# Kyochon,0
# Go Noodles,0
# Hana Dining,0
# Kim Gary,0


# message = '$stock tsla'
# message1=message.split(" ") #['$stock','tsla']
# print('last item? ', message1[-1].upper())
# https://finance.yahoo.com/quote/TSLA

# url = requests.get('https://weather.com/?Goto=Redirected')

# url_result = BeautifulSoup(url.text, "html.parser")
# result = url_result.find("span", {"class":"styles--temperature--3MBn3"})
# print(result)

