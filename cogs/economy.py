import asyncio
import json
import random

import discord

from discord.ext import commands
from datetime import datetime

from .utils import utils


class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='баланс', aliases=['бал', 'бл'])
    async def balance(self, ctx, member: discord.Member = None):
        with open('files/file/users_info.json', 'r', encoding='utf-8') as f:
            bl = json.load(f)

        await ctx.message.delete()
        if member is None:
            member = ctx.author

        money = bl[str(member.id)]['balance']
        embed = discord.Embed(color=utils.randomColor())

        list = sorted(bl, key=(lambda x: bl[x]['balance']))
        a = 0
        for name in list:
            usersCoins = bl[name]['balance']
            a += usersCoins

        embed.set_author(name=f'{member.display_name}')
        embed.set_thumbnail(url=member.avatar_url_as(size=64))
        embed.add_field(name='**Баланс:**', value=f'{money} коинов', inline=False)
        embed.add_field(name='**Баланс сервера:**', value=f'{a} коинов', inline=False)
        await ctx.send(embed=embed)

    @commands.command(name='дейли')
    @commands.cooldown(1, 21600, commands.BucketType.user)
    async def daily(self, ctx):
        with open('files/file/users_info.json', 'r') as f:
            bl = json.load(f)

        await ctx.message.delete()

        pika = utils.checkPets('pikachu', ctx.author)
        lexa = utils.checkPets('lexa', ctx.author)

        if pika is True:
            await utils.update_money(bl, ctx.author, 22000)
            await ctx.send('Выдал 22000 коинов, следующий раз через 6 часов')
            print(f'{ctx.author.display_name} get 22000 coins')
        elif lexa is True:
            await utils.update_money(bl, ctx.author, 1000)
            await ctx.send('Выдал 1000 коинов, следующий раз через 6 часов')
            print(f'{ctx.author.display_name} get 1000 coins')
        else:
            await utils.update_money(bl, ctx.author, 2000)
            await ctx.send('Выдал 2000 коинов, следующий раз через 6 часов')
            print(f'{ctx.author.display_name} get 2000 coins')

        return utils.save_data(bl)

    @daily.error
    async def daily_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            time = int(error.retry_after)
            seconds_to_minute = 60
            seconds_to_hour = 60 * seconds_to_minute

            hours = time // seconds_to_hour
            time %= seconds_to_hour

            min = time // seconds_to_minute
            time %= seconds_to_minute

            sec = time

            await ctx.send(f'Осталось: {hours}ч, {min}м, {sec}с')

    @commands.command(name='казино', aliases=['кз', 'каз'])
    @commands.cooldown(1, 2, type=commands.BucketType.user)
    async def casino(self, ctx, amount: int):
        with open('files/file/users_info.json', 'r') as f:
            users = json.load(f)

        await ctx.message.delete()

        money = users[str(ctx.author.id)]['balance']

        emoji = "🍎🍊🍐🍋🍉🍇🍓🍑"
        a = random.choice(emoji)
        b = random.choice(emoji)
        c = random.choice(emoji)

        slots = f"**{a} {b} {c}\n{ctx.author.name}**,"

        if money < amount:
            await ctx.send('У тебя нет денег')
            return
        if amount <= 0:
            await ctx.send('Ты дура или да')
            return

        else:
            if amount > money:
                await ctx.send(f'У тебя на счету: {money}')
            if money >= amount:
                if a == b == c:
                    await ctx.send(f"{slots} Всё совпало, вы выиграли!>_<")
                    result = amount * 5
                    await utils.update_money(users, ctx.author, result)
                elif (a == b) or (a == c) or (b == c):
                    await ctx.send(f"{slots} 2 подряд, вы выиграли!>_<")
                    result = amount * 2
                    await utils.update_money(users, ctx.author, result)
                else:
                    await ctx.send(f"{slots} К сожалению, вы проиграли(")
                    await utils.update_money(users, ctx.author, -amount)

        utils.save_data(users)

    @casino.error
    async def casino_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f'Повтори попытку через: {int(error.retry_after)}')

    @commands.command(name='перечислить', aliases=['пр'])
    async def transfer(self, ctx, amount: int, member: discord.Member):
        with open('files/file/users_info.json', 'r') as f:
            users = json.load(f)

        await ctx.message.delete()

        ctx_money = users[str(ctx.author.id)]['balance']

        if member == ctx.author:
            await ctx.send('Ты не можешь сам себе перевести коины!')
            return

        if amount <= 0:
            await ctx.send('Да-да давай в том же духе...')
            return

        if amount <= ctx_money:
            await utils.update_money(users, ctx.author, -amount)
            await utils.update_money(users, member, amount)
            await ctx.send(f'**{ctx.author.display_name}** перевёл **{member.display_name}**: **{amount} коинов**')
        else:
            await ctx.send('Ты не можешь перевести больше, чем у тебя есть!')

        utils.save_data(users)

    @transfer.error
    async def transfer_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            embed = discord.Embed(title='Использовать:',
                                  description='.перечислить(пр) {кол-во коинов} {ник}',
                                  color=utils.randomColor())
            await ctx.send(embed=embed)
        if isinstance(error, commands.CommandInvokeError):
            embed = discord.Embed(title='Использовать:',
                                  description='.перечислить(пр) {кол-во коинов} {ник}',
                                  color=utils.randomColor())
            await ctx.send(embed=embed)

    @commands.command(name='депозит', aliases=['дп'])
    @commands.cooldown(1, 14400, commands.BucketType.user)
    async def deposit(self, ctx, count: int):
        with open('files/file/users_info.json', 'r') as f:
            users = json.load(f)

        money = users[str(ctx.author.id)]['balance']
        if money < count:
            return await ctx.send('У тебя нехватает коинов!')
        if count <= 0:
            return await ctx.send('Не-а, так не работает')

        result = int(count + (count * 0.2))

        await utils.update_money(users, ctx.author, -count)
        utils.save_data(users)
        await ctx.send(f'С вашего счёта списано **{count} коинов**')
        await ctx.send(f'Спустя 4 часа вам вернуться {result}')

        await asyncio.sleep(14400)

        lexa = utils.checkPets('lexa', ctx.author)
        if lexa is True:
            rn = random.randint(1, 3)
            if rn == 1:
                return await ctx.send('Увы, лёха спиздил коины')

        await utils.update_money(users, ctx.author, result)
        await ctx.send(f'**{ctx.author.display_name}** вам вернулись ваши коины.')
        utils.save_data(users)

    @deposit.error
    async def deposit_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            time = int(error.retry_after)
            seconds_to_minute = 60
            seconds_to_hour = 60 * seconds_to_minute

            hours = time // seconds_to_hour
            time %= seconds_to_hour

            min = time // seconds_to_minute
            time %= seconds_to_minute

            sec = time

            await ctx.send(f'Осталось: {hours}ч, {min}м, {sec}с')

    @commands.command(name='рулетка', aliases=['рл'])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def roulette(self, ctx, color, count: int):
        with open('files/file/users_info.json', 'r') as f:
            users = json.load(f)

        money = users[str(ctx.author.id)]['balance']
        black = [35, 26, 28, 29, 22, 31, 20, 33, 24, 10, 8, 11, 13, 6, 17, 2, 4, 15]
        red = [3, 12, 7, 18, 9, 14, 1, 16, 5, 23, 30, 36, 27, 34, 25, 21, 19, 32]
        green = 0
        result = random.randint(0, 37)

        if color != 'чёрный' and color != 'красный' and color != 'зелёный':
            return await ctx.send('Цвета: чёрный, красный, зелёный')

        if money < count:
            return await ctx.send('У тебя нехватает коинов!')
        if count <= 0:
            return await ctx.send('Не-а, так не работает')
        await ctx.send('Итак, вы...')
        await asyncio.sleep(3)

        if color == 'чёрный' and result in black:
            res = count * 2
            await utils.update_money(users, ctx.author, res)
            await ctx.send(f'Вы выиграли! Чёрная {result}')
            await ctx.send(f'Вам начисленно **{res} коинов**')
            return utils.save_data(users)
        if color == 'красный' and result in red:
            res = count * 2
            await utils.update_money(users, ctx.author, res)
            await ctx.send(f'Вы выиграли! Красная {result}')
            await ctx.send(f'Вам начисленно **{res} коинов**')
            return utils.save_data(users)
        if color == 'зелёный' and result == green:
            res = count * 10
            await utils.update_money(users, ctx.author, res)
            await ctx.send(f'Вы выиграли! Зелёная {result}')
            await ctx.send(f'Вам начисленно **{res} коинов**')
            return utils.save_data(users)

        await utils.update_money(users, ctx.author, -count)
        utils.save_data(users)
        return await ctx.send('Увы, вы проиграли...')

    @roulette.error
    async def roulette_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(title='Использовать:',
                                  description='.рулетка {красный/чёрный/зелёный} {кол-во коинов}',
                                  color=utils.randomColor())
            await ctx.send(embed=embed)
        if isinstance(error, commands.BadArgument):
            embed = discord.Embed(title='Использовать:',
                                  description='.рулетка {красный/чёрный/зелёный} {кол-во коинов}',
                                  color=utils.randomColor())
            await ctx.send(embed=embed)
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f'Повтори попытку через: {int(error.retry_after)}')

    @commands.command(name='украсть', aliases=['укр', 'ук'])
    @commands.cooldown(1, 900, commands.BucketType.user)
    async def rob(self, ctx, member: discord.Member):
        with open('files/file/users_info.json', 'r') as f:
            users = json.load(f)

        await utils.update_data(users, member)

        moneyM = users[str(member.id)]['balance']
        r = random.randint(1, 10)

        if moneyM <= 100:
            return await ctx.send(f'Прости...У **{member}** мало коинов...')
        if member == ctx.author:
            return await ctx.send('Ты не можешь украсть у самого себя коины...')
        if member == ctx.me:
            return await ctx.send('Ты не можешь украсть у меня коины...')

        if r == 5:
            result = int(-moneyM * 20 / 100)
            await utils.update_money(users, member, result)
            await utils.update_money(users, ctx.author, result)
            return await ctx.send(
                f'**{ctx.author.display_name}** украл у **{member.display_name}**: **{result} коинов**')
        else:
            return await ctx.send('Увы тебе не повезло...')

    @rob.error
    async def rob_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            time = int(error.retry_after)
            seconds_to_minute = 60

            min = time // seconds_to_minute
            time %= seconds_to_minute

            sec = time

            await ctx.send(f'Осталось: {min}м, {sec}с')

    @commands.command(name='налоги', aliases=['нл'])
    async def tax(self, ctx):
        with open('files/file/users_info.json', 'r', encoding='utf-8') as f:
            users = json.load(f)
        with open('files/file/users_pets.json', 'r', encoding='utf-8') as f:
            pet = json.load(f)

        putin = utils.checkPets('putin', ctx.author)

        list = sorted(users, key=(lambda x: users[x]['balance']))
        a = 0
        for name in list:
            usersCoins = users[name]['balance']
            a += usersCoins

        if putin is True:
            PutinTime = pet[str(ctx.author.id)]['pets']['PutinTime']
            datetimeFormat = '%Y-%m-%d %H:%M:%S.%f'
            if PutinTime == '':
                pet[str(ctx.author.id)]['pets']['PutinTime'] = str(datetime.utcnow())
                await utils.update_money(users, ctx.author, int(a * 20 / 100))
                await ctx.send(f'Путин собрал налогов на: **{a * 20 / 100} коинов**')
                utils.save_data(users)
                return utils.save_pets(pet)
            else:
                time_diff = datetime.strptime(str(datetime.utcnow()), datetimeFormat) \
                            - datetime.strptime(str(PutinTime), datetimeFormat)
                if time_diff.seconds >= 259200:
                    pet[str(ctx.author.id)]['pets']['PutinTime'] = str(datetime.utcnow())

                    await utils.update_money(users, ctx.author, int(a * 20 / 100))
                    await ctx.send(f'Путин собрал налогов на: **{a * 20 / 100} коинов**')
                    utils.save_data(users)
                    utils.save_pets(pet)
                else:
                    res = 259200 - time_diff.seconds
                    time = int(res)
                    seconds_to_minute = 60
                    seconds_to_hour = 60 * seconds_to_minute
                    seconds_to_day = 24 * seconds_to_hour

                    day = time // seconds_to_day
                    time %= seconds_to_day

                    hours = time // seconds_to_hour
                    time %= seconds_to_hour

                    min = time // seconds_to_minute
                    time %= seconds_to_minute

                    sec = time

                    return await ctx.send(f'Осталось: {day}д, {hours}ч, {min}м, {sec}с')
        else:
            return await ctx.send('У тебя нет питомца Путин или он не активирован')


def setup(bot):
    bot.add_cog(Economy(bot))
