# Warframe Price Finder Discord Bot
Old project from 2 years ago that took a few weeks to write and test. I made a new repository because it had token files and other sensitive information.
Deployable on heroku. 

# What it does

The bot scrapes the internet for prices of an item (in platinum, currency bought by money), and displays the top 3 deals as well as the top 3 expensive prices so one has a guideline of prices when they make deals. Also lists online users selling or buying the item with their desired price so you can quickly contact them. For set items, it can show sub item prices in the set, as well as whole set item prices.

Also implements a cache so repeated queries dont cause more overhead.

# How to use
1. Setup discord authentications for bots.
2. Get the dependencies.
3. Deploy the bot on your computer or a webservice that can run 24/7 such as heroku.
