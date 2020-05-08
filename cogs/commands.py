import asyncio
import json
import random
import string
import discord
import aiohttp
import math
import corona_api
import requests as req

from bs4 import BeautifulSoup as bs
from discord.ext import commands
from discord.utils import get

from .utils import utils


async def gdz_search(request, ctx):
    soup = bs(request.content, 'lxml')
    div = soup.find('div', class_='with-overtask').find('img').get('src')
    divs = soup.findAll('div', class_='with-overtask')
    div1 = divs[0]

    if not div == div1:
        for div1 in divs:
            img = div1.img['src']
            _imgUrl = 'https:' + str(div)
            _imgUrl1 = 'https:' + str(img)
            em = discord.Embed()
            await ctx.send(embed=em.set_image(url=_imgUrl).set_image(url=_imgUrl1))
    else:
        _imgUrl = 'https:' + str(div)
        em = discord.Embed()
        await ctx.send(embed=em.set_image(url=_imgUrl))


class Commands(commands.Cog):
    def __init__(self, bot):
        self.session = aiohttp.ClientSession()
        self.bot = bot
        self.corona = corona_api.Client()

    @commands.command(name='очистить', aliases=['оч'])
    @commands.has_permissions(administrator=True)
    async def clear(self, ctx, amount: int):
        await ctx.message.delete()
        await ctx.channel.purge(limit=amount)
        await ctx.send("Мысорнул нахй: " + str(amount))
        await asyncio.sleep(5)
        await ctx.channel.purge(limit=1)

    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title='Использовать:',
                                  description='.очистить {кол-во}',
                                  colour=utils.randomColor())
            await ctx.send(embed=embed)

    @commands.command(name='аватар', aliases=['ава'])
    async def avatar(self, ctx, *, user: discord.Member = None):
        await ctx.message.delete()
        if user is None:
            user = ctx.author

        await ctx.send(f"Ава **{user.name}**\n{user.avatar_url_as(size=1024)}")

    @commands.command(name='повтори')
    async def repeat(self, ctx, *args):
        await ctx.message.delete()
        output = ' '.join(args)
        await ctx.send(output)

    @repeat.error
    async def repeat_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title='Использовать:',
                                  description='`.повтори {текст}`',
                                  color=utils.randomColor())
            await ctx.send(embed=embed)

    @commands.command(name='шар')
    async def ball(self, ctx, *args):
        v_o = [' думаю да', ' думаю нет', ' я в этом уверен', ' нет', '100%', 'не думаю']

        msg = ' '.join(args)
        await ctx.send(f'"{msg}"' + random.choice(v_o))

    @ball.error
    async def ball_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title='Использовать:',
                                  description='.шар {текст}',
                                  colour=utils.randomColor())
            await ctx.send(embed=embed)

    @commands.command(name='шанс')
    async def chance(self, ctx, *args):
        chance = ' '.join(args)
        await ctx.send(str(random.randint(0, 101)) + '% что ' + chance)

    @chance.error
    async def chance_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title='Использовать:',
                                  description='.шанс {текст}',
                                  colour=utils.randomColor())
            await ctx.send(embed=embed)

    @commands.command(name='ттс')
    @commands.has_permissions(administrator=True)
    async def tts(self, ctx, *args):
        if ctx.author.guild_permissions.administrator:
            tsm = ' '.join(args)
            await ctx.send(tsm, tts=True)
        else:
            return await ctx.send('У тебя нет прав администратора!')

    @tts.error
    async def tts_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title='Использовать:',
                                  description='.ттс {текст}',
                                  colour=utils.randomColor())
            await ctx.send(embed=embed)

    @commands.command(name='пароль')
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def password(self, ctx, amount: int):
        if amount > 1983 or amount <= 0:
            await ctx.send('О-Ш-И-Б-К-А. . .')
        else:
            character = string.ascii_letters + string.digits
            password = "".join(random.choice(character) for c in range(amount))
            await self.bot.get_user(ctx.author.id).send("Вот твой пароль: " + password)

    @password.error
    async def pass_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title='Использовать:',
                                  description='.пароль {кол-во}',
                                  colour=utils.randomColor())
            await ctx.send(embed=embed)

        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f'Повтори попытку через: {int(error.retry_after)}')

    @commands.command(name='варн')
    @commands.cooldown(1, 600, commands.BucketType.user)
    async def warn(self, ctx, member: discord.Member, *, reason=None):
        with open('files/file/users_info.json', 'r') as f:
            users = json.load(f)

        warn = users[str(member.id)]['warn']
        embed = discord.Embed(colour=utils.randomColor())

        if member == ctx.author:
            await ctx.send('Ты не можешь пожаловаться на самого себя!')
            return

        if warn == 9:
            await ctx.send(f'{member.display_name} будет кикнут через 1 предупреждение')
        if warn == 10:
            await utils.update_warn(users, member, -10)
            await member.kick(reason=f'{ctx.author}: {reason}')
            embed.set_author(name=f'{member.display_name} был кикнут')
            embed.set_thumbnail(url=member.avatar_url_as(size=64))
            embed.add_field(name='**Причина:**', value='У пользователя 10 жалоб')
            await ctx.send(embed=embed)

        if not member.guild_permissions.administrator:
            await utils.update_warn(users, member, 1)

            if reason is None:
                await ctx.send(f'У {member.display_name} {warn} предупреждений')
                return

            embed.set_author(name=f'Предупреждение для пользователя {member.display_name}')
            embed.set_thumbnail(url=member.avatar_url_as(size=64))
            embed.add_field(name='**Причина:**', value=f'{reason}')
            await ctx.send(embed=embed)
        else:
            await ctx.send(f'У {member.display_name} есть права администратора, на него нельзя пожаловаться!')

        utils.save_data(users)

    @warn.error
    async def warn_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title='Использовать:',
                                  description='.варн {ник} {причина}',
                                  color=utils.randomColor())
            await ctx.send('О-Ш-И-Б-К-А', embed=embed)
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send('Повторите попытку через {}с'.format(int(error.retry_after)))

    @commands.command(name='осб')
    async def about(self, ctx, *message):
        with open('files/file/about_info.json', 'r') as f:
            about = json.load(f)

        msg = ' '.join(message)

        if not str(ctx.author.id) in about:
            print(f'Create about user: {ctx.author}')

            about[str(ctx.author.id)] = {
            }

        about[str(ctx.author.id)]['about'] = str(msg)

        with open('files/file/about_info.json', 'w') as f:
            json.dump(about, f, indent=1)

    @about.error
    async def about_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title='Использовать:',
                                  description='.осб {текст}',
                                  colour=utils.randomColor())
            await ctx.send(embed=embed)

    @commands.command(name='инфо')
    async def info(self, ctx, *, member: discord.Member = None):
        with open('files/file/about_info.json', 'r') as f:
            about = json.load(f)
        with open('files/file/users_info.json', 'r') as f:
            users = json.load(f)

        await ctx.message.delete()

        if member is None:
            member = ctx.author

        money = users[str(member.id)]['balance']
        warn = users[str(member.id)]['warn']
        lvl = users[str(member.id)]['level']
        exp = users[str(member.id)]['xp']
        role = get(ctx.guild.roles, name='Миллионер')

        createAt = member.created_at.strftime('%d %b %Y %H:%M')
        joinedAt = member.joined_at.strftime('%d %b %Y %H:%M')

        embed = discord.Embed(color=utils.randomColor())
        embed.set_author(name=f'Информация о пользователе: \n{member.display_name}')
        embed.set_thumbnail(url=member.avatar_url_as(size=128))
        if str(member.id) in about:
            about_member = about[str(member.id)]['about']
            embed.add_field(name='О себе:', value=f'{about_member}', inline=False)
        embed.add_field(name='Основная информация:',
                        value=f'**Статус:** {member.status}\n**Зарегистрировался:** {createAt}\n' +
                              f'**Присоединился к серверу:** {joinedAt}\n**Лвл:** {lvl} (**Опыт:** {exp})\n' +
                              f'**Баланс:** {money}\n**Предупреждений:** {warn}')
        if role in member.roles:
            embed.set_footer(text='ID: ' + str(member.guild.id) + '. У него есть роль Миллионера!!!')
        else:
            embed.set_footer(text='ID: ' + str(member.guild.id))

        await ctx.send(embed=embed)

    @info.error
    async def info_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            embed = discord.Embed(title='Использовать:',
                                  description='.инфо {ник}',
                                  colour=utils.randomColor())
            await ctx.send(embed=embed)

    @commands.command(name='напомнить')
    async def recall(self, ctx, delay: int, *message):
        msg = ' '.join(message)

        await ctx.message.delete()
        await ctx.send(f'Напомнить: "{msg}" через {delay}с')
        await asyncio.sleep(delay)
        await ctx.send(f'{msg}')

    @recall.error
    async def recall_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title='Использовать:',
                                  description='.напомнить {время в секундах} {текст}',
                                  colour=utils.randomColor())
            await ctx.send(embed=embed)

    @commands.command(name='емабан')
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def chanceBan(self, ctx):
        i = random.randint(0, 8)
        if ctx.author.guild_permissions.administrator:
            return await ctx.send(f'У тебя есть права администратора...')
        if i == 1 or i == 8:
            await ctx.author.kick(reason=f'{ctx.author}: проиграл XD')
            await ctx.send(f'{ctx.author.display_name} не повезло и он улетает в бан...')
        else:
            await ctx.send('Поздравляю, тебе повезло...')

    @chanceBan.error
    async def error_chanceBan(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send('Повторите попытку через {}с'.format(int(error.retry_after)))

    @commands.command(name='цвет')
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def changeColorRole(self, ctx, role=None, color=None):
        if role is None and color is None:
            embed = discord.Embed(colour=utils.randomColor())

            embed.add_field(name='Цвета:', value=
                            '1 - Дефолт\n' +
                            '2 - Синий\n' +
                            '3 - Фиолетовый\n' +
                            '4 - Зелёный\n' +
                            '5 - Золотой\n' +
                            '6 - Оранжевый\n' +
                            '7 - Красный\n' +
                            '8 - Светло-Серый')

            return await ctx.send(embed=embed)

        role_m = get(ctx.author.guild.roles, name='Миллионер')
        c_role = get(ctx.author.guild.roles, name=role)

        if not c_role:
            await ctx.send(f'Роли {role} нет на сервере')
            return

        colors = {
            '1': discord.Colour.default(),
            '2': discord.Colour.blue(),
            '3': discord.Colour.purple(),
            '4': discord.Colour.green(),
            '5': discord.Colour.gold(),
            '6': discord.Colour.orange(),
            '7': discord.Colour.red(),
            '8': discord.Colour.light_grey()
        }

        if role_m in ctx.author.roles or ctx.author.guild_permissions.administrator:
            if color in colors:
                await c_role.edit(name=role, colour=colors[color])
                await ctx.send(f'Цвет роли "{role}" был изменён!')
                print(f'{ctx.author} has change color role "{role}"')
            else:
                await ctx.send('Такого цвета нету!')
        else:
            await ctx.send('У тебя нет роли Миллионера или ты не администратор!')

    @changeColorRole.error
    async def changeColorRole_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title='Использовать:',
                                  description='.цвет {роль} {номер цвета}',
                                  colour=utils.randomColor())
            await ctx.send(embed=embed)
        if isinstance(error, commands.BadArgument):
            embed = discord.Embed(title='Использовать:',
                                  description='.цвет {роль} {номер цвета}',
                                  colour=utils.randomColor())
            await ctx.send(embed=embed)
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send('Повторите попытку через {}с'.format(int(error.retry_after)))

    @commands.command(name='гдз', pass_context=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def gdz(self, ctx, thing, number: int, number1: int = None):
        session = req.Session()

        if number <= 0:
            return

        if thing == 'матеша' or thing == 'алгебра':
            url = f'https://gdz.ru/class-9/algebra/nikolskiy/{number}-nom/'
            request = session.get(url)

            if request.status_code == 200:
                await gdz_search(request, ctx)
            else:
                print('Error')

        if thing == 'геометрия':
            url = f'https://gdz.ru/class-7/geometria/atanasyan-7-9/{number}-nom/'
            request = session.get(url)

            if request.status_code == 200:
                await gdz_search(request, ctx)
            else:
                print('Error')

        if thing == 'руссич' or thing == 'русский':
            url = f'https://gdz.ru/class-9/russkii_yazik/ribchenkova-9/{number}-nom/'
            request = session.get(url)

            if request.status_code == 200:
                await gdz_search(request, ctx)
            else:
                print('Error')

        if thing == 'немец':
            url = f'https://gdz.ltd/content/9-class/deutch/Radchenko-Wunderkinder/exercise/Stranicy-uchebnika/{number}.jpg'

            embed = discord.Embed()
            await ctx.send(embed=embed.set_image(url=url))

        if thing == 'физика':
            url = f'https://gdz.ru/class-9/fizika/peryshkin-gutnik/{number}-nom-{number1}/'

            request = session.get(url)

            if request.status_code == 200:
                await gdz_search(request, ctx)
            else:
                print('Error')

    @gdz.error
    async def gdz_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send('Повторите попытку через {}с'.format(int(error.retry_after)))
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title='Использовать:',
                                  description='.гдз {предмет} {номер} {номер1(для физики)}',
                                  colour=utils.randomColor())
            await ctx.send(embed=embed)
        if isinstance(error, commands.BadArgument):
            embed = discord.Embed(title='Использовать:',
                                  description='.гдз {предмет} {номер} {номер1(для физики)}',
                                  colour=utils.randomColor())
            await ctx.send(embed=embed)

    @commands.command(name='ник')
    async def changeNick(self, ctx, member: discord.Member, *nick: str):
        with open('files/file/users_info.json', 'r') as f:
            users = json.load(f)

        role = get(ctx.author.guild.roles, name='Миллионер')
        money = users[str(ctx.author.id)]['balance']

        nick_str = ' '.join(nick)

        if money >= 150000:
            if role in ctx.author.roles or ctx.author.guild_permissions.administrator:
                await utils.update_money(users, ctx.author, -150000)
                await member.edit(nick=nick_str)
                await ctx.send(f'{ctx.author} изменил ник {member} на: {nick_str}')
                print(f'{ctx.author} has change nick {member} on {nick_str}')
            else:
                await ctx.send('У тебя нет роли Миллионера или ты не администратор...')
        else:
            result = 150000 - money
            await ctx.send(f'Тебе нехватает: {result} коинов')

        utils.save_data(users)

    @changeNick.error
    async def changeNick_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title='Использовать:',
                                  description='.ник {ник} {изменённый ник}',
                                  colour=utils.randomColor())
            await ctx.send(embed=embed)
        if isinstance(error, commands.BadArgument):
            embed = discord.Embed(title='Использовать:',
                                  description='.ник {ник} {изменённый ник}',
                                  colour=utils.randomColor())
            await ctx.send(embed=embed)

    @commands.command(name='рдж')
    async def rainbowNick(self, ctx):
        role = get(ctx.guild.roles, name='Радужный Ник')
        colors = [
            discord.Colour.red(),
            discord.Colour.orange(),
            discord.Colour(0x00FFFF),
            discord.Colour.green(),
            discord.Colour(0xFF0000),
            discord.Colour.blue(),
            discord.Colour.purple()
        ]

        if not role:
            try:
                await ctx.guild.create_role(name='Радужный Ник')
            except discord.Forbidden:
                await ctx.send('У меня недостаточно прав...')

        while True:
            await asyncio.sleep(4)
            await role.edit(colour=random.choice(colors))

    @rainbowNick.error
    async def rainbowNick_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send('Ошибка с ником!!!')

    @commands.command(name='калькулятор', aliases=['кал', 'кл'])        
    async def calculator(self, ctx, num1: int, operator, num2: int = None):
        if operator == '+':
            result = num1 + num2
            await ctx.send(f'Число: {result}')
        elif operator == '-':
            result = num1 - num2
            await ctx.send(f'Число: {result}')
        elif operator == '*':
            result = num1 * num2
            await ctx.send(f'Число: {result}')
        elif operator == '/':
            if num1 == 0 or num2 == 0:
                return await ctx.send('На ноль делить нельзя!')
            result = num1 / num2
            await ctx.send(f'Число: {result}')
        elif operator == '**':
            result = num1 ** num2
            await ctx.send(f'Число: {result}')
        elif operator == 'кор' or operator == 'корень':
            result = math.sqrt(num1)
            await ctx.send(f'Число: {result}')

    @calculator.error
    async def calculator_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            embed = discord.Embed(title='Использовать:',
                                  description='.кл [число] [знак] [число]',
                                  colour=utils.randomColor())
            await ctx.send(embed=embed)
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title='Использовать:',
                                  description='.кл [число] [знак] [число]',
                                  colour=utils.randomColor())
            await ctx.send(embed=embed)

    @commands.command(name='перевернуть', aliases=['прв'])
    async def reverse(self, ctx, *message):
        await ctx.message.delete()
        await ctx.send(' '.join(reversed(message)))

    @commands.command(name='Андрей', aliases=['ан'])
    async def not_adequate(self, ctx):
        not_adequete = ['https://www.youtube.com/watch?v=iGTQHchdneQ',
                        'https://www.youtube.com/watch?v=3uvLc2DfwaE',
                        'https://www.youtube.com/watch?v=VKpGF54nYHM']

        await ctx.send(random.choice(not_adequete))

    @commands.command(name='коровавирус', aliases=['кв', 'корона'])
    async def corovaVirus(self, ctx, country=None):
        if not country:
            data = await self.corona.all()
        else:
            data = await self.corona.get_country_data(country)

        embed = discord.Embed(title='Коровавирус COVID-19', colour=65280)
        embed.add_field(name='Всего случаев: ', value=corona_api.format_number(data.cases))
        embed.add_field(name='Случаев за день: ', value=corona_api.format_number(data.today_cases))
        embed.add_field(name='Всего смертей: ', value=corona_api.format_number(data.deaths))
        embed.add_field(name='Смертей за день: ', value=corona_api.format_number(data.today_deaths))
        embed.add_field(name='Всего вылечившихся: ', value=corona_api.format_number(data.recoveries))

        embed.add_field(name="Последнее обновление: ", value=corona_api.format_date(data.updated), inline=False)

        await ctx.send(embed=embed)

    @corovaVirus.error
    async def corovaVirus_error(self, ctx, error):
        return await ctx.send('Возможно эта страна не заражена или такой страны не существует')

    @commands.command()
    async def test(self, ctx):
        await ctx.send('Ты гей? Да/Нет')

        def check(m):
            return m.author.id == ctx.author.id
        response = await self.bot.wait_for('message', check=check)

        if response != 'Да' and response != 'Нет':
            return await ctx.send('Даун')

        await ctx.send(f'Ты ответил: {str(response.content)}')


def setup(bot):
    bot.add_cog(Commands(bot))
