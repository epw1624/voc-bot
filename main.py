# this is the file to run for the bot to come online in the server

# desired functionality:
    # on receiving a message with the !verify command, generate a url to the voc login with the "destination" parameter set to the api endpoint

import discord
import verify
import os

BOT_FUNCTIONS = {
    'Verification' : "Use the command '!voc-bot verify' to begin the verification process in a direct message, or '!voc-bot verify <email> <VOC ID>' to begin the verification process in this channel"
    }

client = discord.Client(intents=discord.Intents.all())

@client.event
async def on_ready():
    print("VOC bot is online!")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith("!voc-bot"):
        content = message.content.split(' ')
        if content[1] == "verify":
            if len(content) == 4:
                await message.channel.send(verify.verify_member(client, message))
            elif len(content) == 2:
                verify.verify_member_dm(client, message.author, message.guild)
            else:
                message.channel.send('Invalid format\nTry "!voc-bot verify <email> <VOC ID>" or "!voc-bot verify"')
        elif content[1] == 'help':
            return_message = ""
            for function in BOT_FUNCTIONS.keys():
                return_message += function.upper() + '\n\n' + BOT_FUNCTIONS[function] + '\n\n'
            await message.channel.send(return_message)
        else:
            await message.channel.send("Invalid command! Try '!voc-bot help' for more information")


client.run(os.getenv('SECRET_KEY'))

    