import discord
import csv
import tweepy
import configparser


#twitter section --------------

parser = configparser.ConfigParser()
parser.read("Conf/config.ini")


def confParser(section):
    if not parser.has_section(section):
        print("No section info  rmation are available in config file for", section)
        return
    # Build dict
    tmp_dict = {}
    for option, value in parser.items(section):
        option = str(option)
        value = value.encode("utf-8")
        tmp_dict[option] = value
    return tmp_dict
#get twitter OAuth data
general_conf = confParser("general_conf")
API_KEY = general_conf["api_key"].decode("utf-8")
API_KEY_SECRETE = general_conf["api_key_secrete"].decode("utf-8")
ACCESS_TOKEN = general_conf["access_token"].decode("utf-8")
ACCESS_TOKEN_SECRETE = general_conf["access_token_secrete"].decode("utf-8")

auth = tweepy.OAuthHandler(API_KEY, API_KEY_SECRETE)

# set access to user's access key and access secret
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRETE)

# Set up the API with the authentication handler
api = tweepy.API(auth)

#twitter test friends
def are_friends(source,target):
    """
    Tests if the source follows the target on twitter
    :param source: users twitter name
    :param target: the twitter name that is tested if the user follows
    :return: followTest 'a dictionary with followTest data'
    """
    status = api.get_friendship(source_screen_name=source,target_screen_name=target)
    f1_following = status[0].following
    followTest = {'twitterName':source,'testType':'follows','targetName':target,'follows':f1_following}
    
    return followTest

#end twitter section
def notrue(source,target):
    """
    Tests if the source follows the target on twitter
    :param source: users twitter name
    :param target: the twitter name that is tested if the user follows
    :return: followTest 'a dictionary with followTest data'
    """
    status = api.get_friendship(source_screen_name=source,target_screen_name=target)
    f1_following = status[0].following
    return f1_following

#Discord section ------------
def read_token():
    """
    read discord bot token
    :return:
    """
    with open("token.txt", "r") as f:
        lines = f.readlines()
        return lines[0].strip()

token = read_token()
client = discord.Client()
# enter the name of the channel the bot will check below
channel = ["get-verified"]
role_name= ["Whitelisted"]
guild_id= 976183085764861962

# enter the twitter name into the below list that are to be tested
twitterList = ['MagneticUniver']

# todo find out how to not include the header for each entry
def writeFollowers(followers):
    """
    Append the output of the returned data to csv file followsOnTwitter.csv
    :param followers:
    :return:
    """
    with open('followsOnTwitter.csv', mode='a') as csv_file:
        fieldnames = ['twitterName', 'testType', 'targetName', 'follows', 'discordName']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow(followers)
@client.event
async def on_ready():
    print("Logged in as "+client.user.name)
@client.event
async def on_message(message):
    """
    in discord check that messages are coming from channel twitter_name and tests message for follows
    :param message:
    :return:
    """
    
    if str(message.channel) in channel:
        for i in twitterList:
            followers = are_friends(message.content, i)
            nofollower = notrue(message.content, i)
            followers['discordName'] = message.author.name
            if ((nofollower == False ) and (followers['discordName'] != client.user.name)):
            	await message.channel.send("You are not following our twitter account or this name user doesn't exist please try again")
            	
            if nofollower == True :
            	guild = client.get_guild(guild_id)
            	role = discord.utils.get(message.guild.roles, name= role_name)
            	print(role)
            	member = message.author
            	print(member)
            	if member is None: return None
            	await member.add_roles( role)
            
            
            print(followers)
            writeFollowers(followers)
            

client.run(token)

#end Discord section


