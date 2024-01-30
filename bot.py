import discord
from discord.ext import commands
import requests
import os
from dotenv import load_dotenv
import json
from bs4 import BeautifulSoup

load_dotenv()

def check_user(ids, key):

    resp = requests.post("https://api.vk.com/method/users.get?lang=0&user_ids="+ ids +"&fields=photo_200_orig&access_token="+ key +"&v=5.131 HTTP/1.1")
    resp_to_json = json.loads(resp.text)
    if(len(resp_to_json["response"]) < 1):
        return False
    else:
        return True
    
    
def check_group(ids, key):

    resp = requests.post("https://api.vk.com/method/groups.getById?lang=0&group_ids="+ ids +"&access_token="+ key +"&v=5.131 HTTP/1.1")
    if(resp.text.find("error") != -1):
        return False
    else:
        return True
    
    
def check_link(ids):

    key = os.environ.get("vk_service_access_key")
    if check_user(ids, key) == True:
        return (get_user_data(ids))
    elif check_group(ids, key) == True:
        return(get_group_data(ids))
    else:
        ret = []
        ret.append("Error")
        ret.append("Ошибка: ссылка недействительна.")
        return (ret)
    

def get_group_data(ids):

    key = os.environ.get("vk_service_access_key")
    resp = requests.post("https://api.vk.com/method/groups.getById?lang=0&group_ids="+ ids +"&access_token="+ key +"&v=5.131 HTTP/1.1")
    resp_to_json = json.loads(resp.text)
    name = resp_to_json["response"][0]["name"]
    id = str(resp_to_json["response"][0]["id"])
    photo_result = resp_to_json["response"][0]["photo_200"]
    ret = []
    ret.append(photo_result)
    str_result = "[Группа]\nНазвание: " + name + "\nID: " + id + "\nФото группы: "
    ret.append(str_result)
    return(ret)

def get_user_data(ids):

    ret = []
    key = os.environ.get("vk_service_access_key")
    resp = requests.post("https://api.vk.com/method/users.get?lang=0&user_ids="+ ids +"&fields=photo_200_orig&access_token="+ key +"&v=5.131 HTTP/1.1")
    resp_to_json = json.loads(resp.text)
    id = str(resp_to_json["response"][0]["id"])
    first_name = resp_to_json["response"][0]["first_name"]
    last_name = resp_to_json["response"][0]["last_name"]
    photo_result = resp_to_json["response"][0]["photo_200_orig"]

    ret.append(photo_result)
    url = "https://vk.com/foaf.php?id=" + id
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")
    create_date = soup.find("ya:created")["dc:date"]
    create_date = create_date.split('T')[0]
    # create_date = create_date.split('T')[0] + " в " + create_date.split('T')[1].split('+')[0]
    str_result = "[Пользователь]\nИмя пользователя: " + first_name + " " + last_name + "\nID: " + id + "\nДата регистрации: " + create_date + "\nАватар пользователя: "
    ret.append(str_result)
    return(ret)


intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='$', intents=intents) 
bot_token = os.environ.get("bot_token")

@bot.command()
async def info(ctx):
    await ctx.send("Чтобы получить информацию о пользователе или группе используйте команду $link и вставьте ссылку на пользователя или группу.")

@bot.command()
async def link(ctx, arg):
    if arg.find("vk.com/") == -1:
        embed = discord.Embed(color = discord.Colour.dark_green())
        embed.add_field(name="Error", value="Пожалуйста используйте следующий формат ссылки:\nvk.com/[id пользователя или группы]")
        await ctx.send(embed=embed)
    else:
        ret_str = check_link(arg[7:])
        if ret_str[0] == "Error":
            embed = discord.Embed(color = discord.Colour.dark_green())
            embed.add_field(name=ret_str[0], value=ret_str[1])
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(color = discord.Colour.dark_green())
            embed.add_field(name=info, value=ret_str[1])
            embed.set_image(url=ret_str[0])
            await ctx.send(embed=embed)

bot.run(bot_token)