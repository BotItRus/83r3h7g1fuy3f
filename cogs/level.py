import json
import random
import aiohttp
import discord
import math

from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from discord.ext import commands
from datetime import datetime
from discord.utils import get

from .utils import utils


async def level_up(users, user, message):
    xp = users[str(user.id)]['xp']
    lvl = int(users[str(user.id)]['level'])
    xp_end = math.floor(5 * (lvl ^ 2) + 50 * lvl + 100)
    if xp_end < xp:
        users[str(user.id)]['xp'] = 0
        users[str(user.id)]['level'] += 1
        level = users[str(user.id)]['level']
        await message.channel.send(f'**{user.display_name}** повысил свой уровень до: **{level}**')


async def add_xp(users, user, xp):
    a = utils.checkPets('pikachu', user)
    if a is True:
        users[str(user.id)]['xp'] += int(xp * 1.5)
    else:
        users[str(user.id)]['xp'] += xp


class level(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        with open('files/file/users_info.json', 'r') as f:
            users = json.load(f)

        await utils.update_data(users, member)

        utils.save_data(users)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        with open('files/file/users_info.json', 'r', encoding='utf-8') as f:
            users = json.load(f)
        with open('files/file/users_pets.json', 'r', encoding='utf-8') as f:
            pet = json.load(f)

        await utils.update_data(users, message.author)
        await utils.update_pets(pet, message.author)

        xpTime = users[str(message.author.id)]['xpTime']
        datetimeFormat = '%Y-%m-%d %H:%M:%S.%f'
        if xpTime == '':
            users[str(message.author.id)]['xpTime'] = str(datetime.utcnow())
        else:
            time_diff = datetime.strptime(str(datetime.utcnow()), datetimeFormat)\
                        - datetime.strptime(str(xpTime), datetimeFormat)
            if time_diff.seconds >= 5:
                users[str(message.author.id)]['xpTime'] = str(datetime.utcnow())
                await add_xp(users, message.author, random.randint(8, 12))
                await level_up(users, message.author, message)

        if str(message.author.id) in users:
            lvl = users[str(message.author.id)]['level']
            role = get(message.author.guild.roles, name='Задрот')
            role_adm = get(message.author.guild.roles, name='Админка')

            if lvl >= 10 and not role in message.author.roles:
                await message.channel.send(
                    f'{message.author.display_name} достиг {lvl} уровня и получил роль: **Задрот**')
                await message.author.add_roles(role)
                await utils.update_money(users, message.author, 10000)
                return print(f'Gave role "Задрот" is {message.author}')
            elif lvl >= 30 and not role_adm in message.author.roles:
                await message.channel.send(
                    f'{message.author.display_name} достиг {lvl} уровня и получил роль: **Админка**')
                await message.author.add_roles(role_adm)
                await utils.update_money(users, message.author, 30000)
                return print(f'Gave role "Админка" is {message.author}')

        utils.save_data(users)

    # Команды
    @commands.command(name='лвл', aliases=['ранг'])
    async def level_info(self, ctx, member: discord.Member = None):
        with open('files/file/users_info.json', 'r', encoding='utf-8') as f:
            users = json.load(f)

        await ctx.message.delete()

        if member is None:
            member = ctx.author

        await utils.update_data(users, member)

        lvl = users[str(member.id)]['level']
        xp = users[str(member.id)]['xp']
        xp_end = math.floor(5 * (lvl ^ 2) + 50 * lvl + 100)
        name = users[str(member.id)]['name']

        img = Image.open('files/img/back.png')
        font = ImageFont.truetype("files/img/calibri.ttf", 62)  # Числа
        font1 = ImageFont.truetype("files/img/calibri.ttf", 24)  # Опыт
        font2 = ImageFont.truetype("files/img/calibri.ttf", 26)  # Лвл
        font3 = ImageFont.truetype("files/img/calibri.ttf", 42, encoding='utf-8')
        async with aiohttp.ClientSession() as session:
            async with session.get(str(member.avatar_url)) as response:
                image = await response.read()
        icon = Image.open(BytesIO(image)).convert("RGBA")
        size = (156, 156)
        # icon = utils.crop(icon, size)
        # icon.putalpha(utils.prepare_mask(size, 4))
        img.paste(icon.resize(size), (50, 60))
        result = int(xp / xp_end * 100)
        img = utils.draw_progress(img, result)
        draw = ImageDraw.Draw(img)

        rank = utils.find_rank(users, member)

        if lvl < 10:
            draw.text((780, 75), 'LEVEL', (255, 20, 147), font=font2)
            draw.text((850, 50), f"{str(lvl)}", (255, 20, 147), font=font)
            draw.text((610, 75), "RANK", (255, 255, 255), font=font2)
            draw.text((680, 50), f"#{rank}", (255, 255, 255), font=font)
        elif 10 <= lvl < 100:
            draw.text((760, 75), 'LEVEL', (255, 20, 147), font=font2)
            draw.text((830, 50), f"{str(lvl)}", (255, 20, 147), font=font)
            draw.text((590, 75), "RANK", (255, 255, 255), font=font2)
            draw.text((660, 50), f"#{rank}", (255, 255, 255), font=font)
        elif 100 <= lvl < 1000:
            draw.text((730, 75), 'LEVEL', (255, 20, 147), font=font2)
            draw.text((800, 50), f"{str(lvl)}", (255, 20, 147), font=font)
            draw.text((560, 75), "RANK", (255, 255, 255), font=font2)
            draw.text((630, 50), f"#{rank}", (255, 255, 255), font=font)

        draw.text((760, 142), f"{str(xp)} / {xp_end} XP", (255, 255, 255), font=font1)
        draw.text((260, 128), f"{name}", (255, 255, 255), font=font3)
        img.save('files/img/infoimg2.png')
        ffile = discord.File("files/img/infoimg2.png")
        await ctx.send(file=ffile)

    @level_info.error
    async def levelInfo_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            embed = discord.Embed(title='Использовать:',
                                  description='.лвл {ник}',
                                  color=utils.randomColor())
            await ctx.send(embed=embed)

    @commands.command(name='топ')
    async def top(self, ctx):
        with open('files/file/users_info.json', 'r', encoding='utf-8') as f:
            users = json.load(f)

        await ctx.message.delete()

        # if value != 'лвл' and value != 'коины':
        #     embed = discord.Embed(title='Использовать:',
        #                           description='.топ {коины/лвл}',
        #                           color=discord.Color.blue())
        #     return await ctx.send(embed=embed)
        value = 'коины'
        if value == 'коины':
            page = 1
            start = ((page - 1) * 10) + 1
            end = page * 5
            number = 1
            message = ''
            high_score_list = sorted(users, key=(lambda x: users[x]['balance']), reverse=True)
            for Name in high_score_list:
                if number < start:
                    number += 1
                    continue
                if number <= end:
                    IDname = users[str(Name)]['name']
                    if len(str(number)) > 1:
                        message += ((('[' + str(number)) + '] Ник: ') + f'**{IDname}**')
                    else:
                        message += ((('[' + str(number)) + '] Ник: ') + f'**{IDname}**')
                    usersCoins = users[Name]['balance']
                    message += "\n         Коинов: " + str(usersCoins) + ' коинов\n'
                else:
                    break
                number += 1
            number += 1
            return await ctx.send(message)

    @top.error
    async def top_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            embed = discord.Embed(title='Использовать:',
                                  description='.топ {коины/лвл}',
                                  color=utils.randomColor())
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(level(bot))
