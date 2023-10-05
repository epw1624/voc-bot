import discord
import asyncio
import requests
import os

ROLES = {"2023": "test23", "2024": "test24"}

async def verify_member_dm(discord_client, discord_user, server):
    def check(message):
        """
        Custom check function to ensure that DM handling code is only used for DMs from the correct user
        """
        return message.author == discord_user and message.channel.type == discord.ChannelType.private
    
    await discord_user.send('Verify your account by sending "!voc-bot verify <email> <VOC ID>". Ensure to use the email address associated with your VOC account')

    try:
        message = await discord_client.wait_for('message', check=check, timeout=120)
        return_message = await verify_member(discord_client, message, server, discord_user)
        await discord_user.send(return_message)

    except asyncio.TimeoutError:
        discord_user.send("Verification process timed out. Please resend the '!voc-bot verify' command in the VOC server to continue")

async def verify_member(discord_client, message, server, user):
    content = message.content.split(' ')

    email = content[2]
    voc_id = content[3]

    if not check_id(voc_id):
        return_message = f"{user.mention} Invalid ID. No member with this ID exists"

    else:
        response = api_handler(voc_id)

        if response:
            if not response['status']:
                if response['content']['email'] == email:
                    expiry = response['content']['enddate'][:4]
                    role = find_role(server, ROLES[expiry])
                    await add_member_role(user, role)
                    return_message = f"{user.mention} is verified!" 
                else:
                    return_message = f"{user.mention} Email and ID do not match. Ensure to use the email address associated with your VOC account"
            
            elif response['status'] == 1:
                return_message = f"{user.mention} Invalid ID. No member with this ID exists"
            
            else: # the bot message for no id parameter and invalid auth key are the same because the user can't do anything about these
                return_message = f'{user.mention} Verification failed. Please resend the "!voc-bot verify" command to try again'
        else:
            return_message = f'{user.mention} Verification failed. Please resend the "!voc-bot verify" command to try again'
    return return_message
    
def check_id(id):
    """
    type-check the id parameter before making an api call
    """
    try:
        id_as_int = int(id)
        return True
    except ValueError:
        return False


def api_handler(voc_id):
    """
    Makes the API call to ubc-voc.com/api.php using the voc_id provided
    Returns the API response in JSON format
    """
    query = os.environ['BASE_URL'] + '?id={id}'.format(id=voc_id)
    header = {
    "AUTH": os.getenv("API_KEY")
    }
    response = requests.get(query, headers=header)
    return response.json()

async def add_member_role(user, role):
    """
    Assign role_name role to the given user
    """
    await user.add_roles(role)

def find_role(server, role_name):
    all_roles = server.roles
    for role in all_roles:
        if role.name == role_name:
            return role
    else:
        return "Role not found."
    


   