import discord
import subprocess
from tinydb import TinyDB, Query
import os

client = discord.Client()

with open("dtoken.tk","r") as token_file:
    discord_token = token_file.readline()

# set our 4 databases !!! and create data/
if not os.path.exists("debug"):
    os.makedirs("debug")

sudo = TinyDB('debug/admins.json') # admins for the shop
query = Query()

zerotwo = client.get_user(210428907386699777)
@client.event
async def on_ready():
    global zerotwo
    print("Ready to use!")
    zerotwo = client.get_user(210428907386699777)
    if str(sudo.search(query.id == zerotwo.id)) == "[]":
        sudo.insert({"id":zerotwo.id,"lvl":4}) # admin!


@client.event
async def on_message(msg):
    global zerotwo
    if msg.author.id == client.user.id:
        pass
    elif msg.content.startswith("debug."):
        if msg.content == "debug.log":
            await msg.delete()
            try:os.remove("ddungeon.log")
            except Exception as err: await msg.channel.send("Error: "+str(err)+" \nTrying to continue...")

            if str(sudo.search(query.id == msg.author.id)) != "[]" and int(sudo.search(query.id == msg.author.id)[0]['lvl']) >= 1:
                os.system("./getlogs.sh")
                # subprocess.call('./getlogs.sh')
                await msg.channel.send("**"+msg.author.name+"**, heres the log file:",file=discord.File('ddungeon.log','ddungeon.log'))
            else:
                await msg.channel.send("Youre not permitted to do that!")

        if msg.content == "debug.kill":
            await msg.delete()
            if str(sudo.search(query.id == msg.author.id)) != "[]" and int(sudo.search(query.id == msg.author.id)[0]['lvl']) >= 4:
                await zerotwo.send("Bot kill requested by: \n"+msg.author.name)
                await client.logout()
            else:
                await msg.channel.send("Youre not permitted to do that!")

        if msg.content.startswith("debug.add"):
            if str(sudo.search(query.id == msg.author.id)) != "[]" and int(sudo.search(query.id == msg.author.id)[0]['lvl']) >= 4:
                tmp =  msg.content.replace("debug.add ","")
                uid = tmp.split(";")[0]
                lvl = tmp.split(";")[1]

                
                try: 
                    uid = int(uid)
                    lvl = int(lvl)
                    user = client.get_user(int(uid))

                    if str(sudo.search(query.id == uid)) == "[]":
                        sudo.insert({"id":uid,"lvl":lvl})
                    msg = await msg.channel.send("added!")
                    await msg.delete(delay=10)
                except Exception as err:
                    await msg.channel.send("Cant continue cuz:\n "+str(err))
            else:
                await msg.channel.send("Youre not permitted to do that!")

            
client.run(discord_token)