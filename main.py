# this is the file to run for the bot to come online in the server

# desired functionality:
    # on receiving a message with the !verify command, generate a url to the voc login with the "destination" parameter set to the api endpoint

import discord
import verify

BOT_FUNCTIONS = {'Verification' : 'Use the command "!voc-bot verify" to begin the verification process'}

client = discord.Client(intents=discord.Intents(messages=True, message_content=True, manage_roles=True, dm_messages=True))

@client.event
async def on_ready():
    print("VOC bot is online!")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    elif message.content.startswith("!voc-bot"):
        content = message.content.split(' ')

        if content[1] == 'verify':
            verify.verify_member(client, message.author, message.guild)
        elif content[1] == 'help':
            return_message = "What the VOC bot can do:\n"
            for function, description in BOT_FUNCTIONS:
                message += function.upper() + '\n' + description + '\n\n'

            await message.channel.send(return_message)
        else:
            await message.channel.send("Invalid command! Try '!voc-bot help' for more information")

    