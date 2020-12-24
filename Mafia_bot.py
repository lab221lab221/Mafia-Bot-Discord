import discord
from discord.ext.commands import Bot
import json

intents = discord.Intents.all()

class MyClient(discord.Client):
    async def on_ready(self):
        global servers
        global thing
        print('Logged on as', self.user)
        print(client.guilds)
        file = open("servers.json", "r")
        servers = json.loads(file.readline())
        file.close()
        for i in client.guilds:
            hi = False
            for l in servers["servers"]:
                if i.id == l["id"]:
                    hi = True
                    break
                else:
                    continue
            if hi == False:
                servers["servers"].append({"id": i.id, "users": [{"id": 8}], "jobs": []})
                f = open('servers.json', 'w')
                f.write(json.dumps(servers))
            for h in servers["servers"]:
                if int(i.id) == int(h["id"]):
                    thing = servers["servers"].index(h)
                    break
            
            """All of the above is fine."""
            print(i.members)
            for h in i.members:
                for l in (servers["servers"][thing])["users"]:
                    hi = False
                    if h.id == l["id"]:
                        hi = True
                        break
                if hi == False:
                    (servers["servers"][thing])["users"].append({"id": h.id, "money": 2000})
                    f = open('servers.json', 'w')
                    f.write(json.dumps(servers))
        print(client.guilds[1].members)
        print(client.guilds[1].channels)
        await client.guilds[1].channels[2].send("Bot now online!")
        #print(users)
        
    async def on_message(self, message):
        # don't respond to ourselves
        for h in servers["servers"]:
            if int(message.guild.id) == int(h["id"]):
                thing = servers["servers"].index(h)
                print(thing)
                break
        
        if message.author == self.user:
            return

        if 'm!pay' in message.content:
            words = (message.content).split(" ")
            print(words)
            print(message.author.id)
            for i in range(len(words)):
                if words[i-1] == "":
                    words.pop(i-1)
            try:
                to = (words[1])[3:len(words[1])-1]
                print(to)
                amount = words[2]
                broke = False
                for i in servers["servers"][thing]["users"]:
                    if i["id"] == int(message.author.id):
                        i["money"] -= float(amount)
                        if i["money"] < 0:
                            broke = True
                            i["money"] += float(amount)
                if broke == True:
                    await message.channel.send("Sorry, I don't talk to poor people. Get a job, then talk to me.")
                elif broke == False:
                    for i in servers["servers"][thing]["users"]:
                        if i["id"] == int(to):
                            i["money"] += float(amount)
                self.update(servers)
            except Exception as e:
                await message.channel.send('Please make sure to put both user and amount of pay (e.g. "m!pay <USER> <AMOUNT>")!')
                print(e)

        if "m!money" in message.content:
            #print("Money check!!")
            for i in servers["servers"][thing]["users"]:
                #print(message.author.id)
                if i["id"] == int(message.author.id):
                    #print("Money has been checked.")
                    await message.channel.send("$" + str(i["money"]))

        if "m!help" in message.content:
            await message.channel.send("{[m!pay = pay someone],[m!money = check your own balance],[m!help = display commands]}")

        """
        if "m!jobs" in message.content:
            for i in servers["servers"][thing]["jobs"]:
                if i["id"] == int(message.author.id):
                    await message.channel.send("$" + str(i["money"]))
"""

    @staticmethod           
    def update(us):
        f = open('servers.json', 'w')
        print(us)
        f.write(json.dumps(us))

client = MyClient(intents=intents)
client.run("<TOKEN>")
