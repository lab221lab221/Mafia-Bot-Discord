import discord
from discord.ext.commands import Bot
import json
import logging

intents = discord.Intents.All()

class MyClient(discord.Client):
    async def on_ready(self):
        global servers
        global thing
        print('Logged on as', self.user)
        print(client.guilds) #debugging
        await client.change_presence(activity=discord.Game('m!help'))
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
            
            for h in i.members:
                for l in (servers["servers"][thing])["users"]:
                    hi = False
                    if h.id == l["id"]:
                        hi = True
                        break
                if hi == False:
                    (servers["servers"][thing])["users"].append({"id": h.id, "money": 2000, "owner_of": []})
                    f = open('servers.json', 'w')
                    f.write(json.dumps(servers))
        print(client.guilds[0].members)

    async def on_member_join(self, member):
        global servers
        global thing
        print('Logged on as', self.user)
        print(client.guilds) #debugging
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
            
            for h in i.members:
                for l in (servers["servers"][thing])["users"]:
                    hi = False
                    if h.id == l["id"]:
                        hi = True
                        break
                if hi == False:
                    (servers["servers"][thing])["users"].append({"id": h.id, "money": 2000, "owner_of": []})
                    f = open('servers.json', 'w')
                    f.write(json.dumps(servers))
        print(client.guilds[0].members)
        
    async def on_message(self, message):
        for h in servers["servers"]:
            if int(message.guild.id) == int(h["id"]):
                thing = servers["servers"].index(h)
                break

        words = message.content.split(" ")
        command = words[0]

        # don't respond to ourselves
        if message.author == self.user:
            return

        if 'm!pay' == command:
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
                self.update(users)
            except Exception as e:
                await message.channel.send('Please make sure to put both user and amount of pay (e.g. "m!pay <USER> <AMOUNT>")!')
                print(e)
                logging.exception("message")

        if "m!money" == command:
            for i in servers["servers"][thing]["users"]:
                if i["id"] == int(message.author.id):
                    await message.channel.send("`$" + str(i["money"])+"`")

        if "m!help" == command:
            await message.channel.send("`m!pay = pay someone"+"\n"+"m!money = check your own balance"+"\n"+"m!help = display commands"+"\n"+"m!jobs = manage a job/company`")

        if "m!jobs" == command: #All commands for anything related to jobs
            try:
                if len(words) < 2 or words[1] == "help":
                    await message.channel.send("`There are lots of commands you can run within this command. Command-ception!"+"\n"+"m!jobs display: Shows available jobs in the server."+
                                               "\n"+"m!jobs add <NAME_OF_COMPANY>: Adds a job."+"\n"+"m!jobs delete <NAME_OF_COMPANY>: Deletes a job."+"\n"+"m!jobs apply <NAME_OF_COMPANY>: Applys for a job."+"\n"+"m!jobs help: Displays the message you are seeing right now.`")
            except Exception as e:
                print(e)
                logging.exception("message")
            
            try:
                if words[1] == "display": #m!jobs display shows all jobs in a server
                    for i in servers["servers"][thing]["jobs"]:
                        await message.channel.send(i["name"])
                    if len(servers["servers"][thing]["jobs"]) == 0:
                        await message.channel.send("There are no jobs in this server!")
            except Exception as e:
                print(e)
                logging.exception("message")
                return
            """All above is easy dubz"""
            try:
                if words[1] == "add":
                    name = words[2:]
                    n = ""
                    n = name[0]
                    name = name[1:]
                    for i in name:
                        n += " " + i
                    name = n
                    print(name)
                    owner = int(message.author.id)
                    found = False
                    for i in servers["servers"][thing]["jobs"]:
                        if i["name"] == name:
                            found = True
                            break
                    if found == False:
                        servers["servers"][thing]["jobs"].append({"name": name, "owner": owner, "employees": []})
                        self.update(servers)
                        for i in servers["servers"][thing]["jobs"]:
                            await message.channel.send(i["name"])
                        self.update(servers)
                    else:
                        await message.channel.send("Sorry, there is a company that already has that name! Please change that name and try again.")
            except Exception as e:
                print(e)
                logging.exception("message")
                await message.channel.send('m!jobs should be used like so: "m!jobs <ACTION> <NAME_OF_COMPANY>"\nUse "m!jobs help" if you do not know the commands within this domain.')
                return
                
            try:
                if words[1] == "delete":
                    name = words[2:]
                    n = ""
                    n = name[0]
                    name = name[1:]
                    for i in name:
                        n += " " + i
                    name = n
                    for i in servers["servers"][thing]["jobs"]:
                        if i["owner"] == int(message.author.id) and i["name"] == name:
                            hi = servers["servers"][thing]["jobs"].index(i)
                            break
                    print(hi)
                    servers["servers"][thing]["jobs"].pop(hi)
                    self.update(servers)
                    await message.channel.send("Job has been deleted!")

            except Exception as e:
                logging.exception("message")
                await message.channel.send('m!jobs should be used like so: "m!jobs <ACTION> <NAME_OF_COMPANY>"\nUse "m!jobs help" if you do not know the commands within this domain.')
                return

            try:
                if words[1] == "apply":
                    name = words[2:]
                    n = ""
                    n = name[0]
                    name = name[1:]
                    for i in name:
                        n += " " + i
                    name = n
                    print(name)
                    
            except Exception as e:
                print(e)
                logging.exception("message")
                await message.channel.send('m!jobs should be used like so: "m!jobs <ACTION> <NAME_OF_COMPANY>"\nUse "m!jobs help" if you do not know the commands within this domain.')
                return

    """
        if "m!talk" == command
    """
    @staticmethod           
    def update(us):
        f = open('servers.json', 'w')
        print(us)
        f.write(json.dumps(us))

client = MyClient(intents=intents)
client.run("<TOKEN>")
