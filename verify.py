import discord
import asyncio
import requests
import os


def verify_member_dm(discord_client, discord_user, discord_server):
    def check(message):
        """
        Custom check function to ensure that DM handling code is only used for DMs from the correct user
        """
        return message.author == discord_user and message.channel.type == discord.ChannelType.private
    
    discord_user.send('What is your VOC member ID?')

    try:
        voc_id_message = discord_client.wait_for('message', check=check, timeout=120)
        voc_id = voc_id_message.content.strip()

        discord_user.send('What is your email address?\n(This must be the same email address that is registered with your VOC account)')
        email_address_message = discord_client.wait_for('message', check=check, timeout=120)
        email_address = email_address_message.content.strip()

        response = api_handler(voc_id)

        response_email = response['data']['email']

        if response_email == email_address:
            role = find_role(discord_server, "Club Members")
            add_member_role(discord_user, role)
    except asyncio.TimeoutError:
        discord_user.send("Verification process timed out. Please resend the '!verify' command in the VOC server to continue")

def verify_member(discord_client, message):
    content = message.content.split(' ')

    email = content[2]
    voc_id = content[3]

    response = api_handler(voc_id)

    if response:
        # add better error checking for all the possible cases where the api would return something but not have email as a key
        if email == response['email']:
            # role = find_role(message.guild, "Club Members")
            # add_member_role(message.author, role)
            message.channel.send("success, would add the role")
        else:
            message.channel.send("Email and ID do not match. Ensure to use the email address associated with your VOC account")
    else:
        message.channel.send('Verification failed. Please resend the "!verify" command to try again')
    

def api_handler(voc_id):
    """
    Makes the API call to ubc-voc.com/api.php using the voc_id provided
    Returns the API response in JSON format
    """
    query = os.environ['BASE_URL'] + '?id={id}'.format(id=voc_id)
    header = {
    "Authorization": "test-key"
    }
    response = requests.get(query, headers=header)
    return response.json()

def add_member_role(user, role):
    """
    Assign role_name role to the given user
    """
    user.add_roles(role)
    user.send('Role has been assigned!')

def find_role(server, role_name):
    all_roles = server.roles
    for role in all_roles:
        if role.name == role_name:
            return role
    


   