import discord
from Query import Query

file_name = "token"
# Gets token and prefix from a file
with open(file_name, 'r') as f:
    TOKEN = f.readline().strip()
f.close()

client = discord.Client()

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('quote'):
        query = message.content.replace('quote ', '', 1)
        q1 = Query(query)
        q1.quote()

        if Query._ERROR:
            await message.channel.send('```diff\n' + '- Cant find ' + '\n```')
        else:
            msgs = []
            if Query._isMod:
                high = str(Query.quotes[0]) + '|' + str(Query.quotes[3])
                med = str(Query.quotes[1]) + '|' + str(Query.quotes[4])
                low = str(Query.quotes[2]) + '|' + str(Query.quotes[5])
                mhigh = str(Query.quotes[6]) + '|' + str(Query.quotes[9])
                mmed = str(Query.quotes[7]) + '|' + str(Query.quotes[10])
                mlow = str(Query.quotes[8]) + '|' + str(Query.quotes[11])

                msgs.append('```asciidoc\n' + '= ' + Query.name.title() + '(2 Days|15 Days)')
                msgs.append('\n%-10s %-10s %-10s\n' % ('Low', 'Med', 'High'))
                msgs.append('%-10s %-10s %-10s\n' % (low, med, high))

                msgs.append('\n= Maxed\n')
                msgs.append('%-10s %-10s %-10s\n' % ('Low', 'Med', 'High'))
                msgs.append('%-10s %-10s %-10s\n' % (mlow, mmed, mhigh))

            else:
                high = str(Query.quotes[0]) + '|' + str(Query.quotes[3])
                med = str(Query.quotes[1]) + '|' + str(Query.quotes[4])
                low = str(Query.quotes[2]) + '|' + str(Query.quotes[5])

                msgs.append('```asciidoc\n' + '= ' + Query.name.title() + '(2 Days|15 Days)')
                msgs.append('\n%-10s %-10s %-10s\n' % ('Low', 'Med', 'High'))
                msgs.append('%-10s %-10s %-10s\n' % (low, med, high))

            #buy low
            msgs.append('\n= Lowest online player selling prices:')
            playerCount = 0
            for x in range(len(Query.dealOnline)):
                user = Query.dealOnline[x]
                if user['order_type'] == 'sell':
                    msgs.append('\n' + str(user['platinum']) + ' - ' + user['user']['ingame_name'] + ' ('
                                + user['user']['region'].upper() + ')')
                    if playerCount == 3:
                        break
                    playerCount += 1

            if playerCount == 0:
                msgs.append('\nNone online')
            playerCount = 0
            if Query._isMod:
                msgs.append('\n= Maxed:')
                for x in range(len(Query.dealOnlineMaxed)):
                    user = Query.dealOnlineMaxed[x]
                    if user['order_type'] == 'sell':
                        msgs.append('\n' + str(user['platinum']) + ' - ' + user['user']['ingame_name'] + ' ('
                                    + user['user']['region'].upper() + ')')
                        if playerCount == 3:
                            break
                        playerCount += 1
                if playerCount == 0:
                    msgs.append('\nNone online')
                playerCount = 0

            #sell high
            msgs.append('\n\n= Highest online player buying prices:')
            for x in range(len(Query.dealOnline)-1, -1, -1):
                user = Query.dealOnline[x]
                if user['order_type'] == 'buy':
                    msgs.append('\n' + str(user['platinum']) + ' - ' + user['user']['ingame_name'] + ' ('
                                + user['user']['region'].upper() + ')')
                    if playerCount == 3:
                        break
                    playerCount += 1
            if playerCount == 0:
                msgs.append('\nNone online')
            playerCount = 0

            if Query._isMod:
                msgs.append('\n= Maxed:')
                for x in range(len(Query.dealOnlineMaxed)-1, -1, -1):
                    user = Query.dealOnlineMaxed[x]
                    if user['order_type'] == 'buy':
                        msgs.append('\n' + str(user['platinum']) + ' - ' + user['user']['ingame_name'] + ' ('
                                    + user['user']['region'].upper() + ')')
                        if playerCount == 3:
                            break
                        playerCount += 1
                if playerCount == 0:
                    msgs.append('\nNone online')
                msgs.append('```')
            else:
                if Query._isSet:
                    msgs.append('```' + '\n Prices for parts:')
                    for part in Query.setNames:
                        q2 = Query(part, True)
                        q2.quote()
                        high = str(Query.quotes[0]) + '|' + str(Query.quotes[3])
                        med = str(Query.quotes[1]) + '|' + str(Query.quotes[4])
                        low = str(Query.quotes[2]) + '|' + str(Query.quotes[5])

                        msgs.append('```yaml\n' + Query.name.title())
                        msgs.append('\n%-10s %-10s %-10s\n' % ('Low', 'Med', 'High'))
                        msgs.append('%-10s %-10s %-10s\n' % (low, med, high))
                        msgs.append('```')
                else:
                    msgs.append('```')
            await message.channel.send(''.join(msgs))

client.run(TOKEN)

