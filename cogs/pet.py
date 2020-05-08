import json
import random
import discord

from discord.ext import commands
from cogs.utils import utils

pets = ['pikachu', 'lexa', 'putin']


class Pet(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='питомец', aliases=['пт', 'пет'])
    async def _pets(self, ctx, value: str = None, p: str = None):
        with open('files/file/users_pets.json', 'r', encoding='utf-8') as f:
            pet = json.load(f)

        await utils.update_pets(pet, ctx.author)
        Jpet = pet[str(ctx.author.id)]['pets']

        if value == 'инфо':

            # Пикачу
            emPika = discord.Embed(color=discord.Color.from_rgb(255, 255, 0))
            emPika.set_author(name='Пикачу')
            emPika.set_thumbnail(url='https://leonardo.osnova.io/a52f9fb4-c017-dc22-c280-22beed1c756a/-/resize/700/')
            emPika.add_field(name='Возможности:',
                             value='Даёт X1.5 к опыту за сообщение\n' +
                                   'Бонус к ежедневным коинам + 20К\n',
                             inline=False)
            await ctx.send(embed=emPika)

            # Лёха
            emLexa = discord.Embed(color=discord.Color.from_rgb(65, 105, 255))
            emLexa.set_author(name='Лёха')
            emLexa.set_thumbnail(url='https://sun9-14.userapi.com/c857328/v857328823/12c5de/55BYA3xAM_w.jpg')
            emLexa.add_field(name='Возможности:',
                             value='Даёт меньше ежедневных коинов\n' +
                                   'Может не отдать долг(депозит может не вернуть коины)\n' +
                                   'Сразу активирован\n',
                             inline=False)
            await ctx.send(embed=emLexa)

            # Путин
            emPutin = discord.Embed(color=discord.Color.from_rgb(0, 255, 127))
            emPutin.set_author(name='Путин')
            emPutin.set_thumbnail(
                url='https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcSa9SfqGEfzJmrJKSiAeZBaJXgDpxBxPgCEEq98-zvG6ZeOhYvM&usqp=CAU')
            emPutin.add_field(name='Возможности:',
                              value='Даёт команду .налоги(нл), Путин забирает 20% от всего баланса сервера\n' +
                                    'Даёт анти-мут и анти-кик(только для команд бота)\n',
                              inline=False)
            await ctx.send(embed=emPutin)

        if value is None:
            msg = 'Твои питомцы:'
            if pets[0] in Jpet or pets[1] in Jpet or pets[2] in Jpet:
                if pets[0] in Jpet:
                    msg += '\n      Пикачу'
                if pets[1] in Jpet:
                    msg += '\n      Лёха'
                if pets[2] in Jpet:
                    msg += '\n      Путин'

                await ctx.send(msg)
            else:
                return await ctx.send('У тебя нет питомцев')

        if value == 'а':
            if p == 'пикачу' or p == 'путин':
                if Jpet['activated'] <= 2:
                    if p == 'пикачу':
                        if pets[0] in Jpet:
                            if 0 == Jpet[pets[0]]:
                                Jpet['pikachu'] += 1
                                Jpet['activated'] += 1
                                await ctx.send('Ты активировал Пикачу')
                                return utils.save_pets(pet)
                            else:
                                return await ctx.send('Питомец уже активирован')
                        else:
                            return await ctx.send('У тебя нет данного питомца')
                    if p == 'путин':
                        if pets[2] in Jpet:
                            if 0 == Jpet[pets[2]]:
                                Jpet['putin'] += 1
                                Jpet['activated'] += 1
                                await ctx.send('Ты активировал Путина')
                                return utils.save_pets(pet)
                            else:
                                return await ctx.send('Питомец уже активирован')
                        else:
                            return await ctx.send('У тебя нет данного питомца')
                else:
                    return await ctx.send('У тебя не может быть активировано больше 2-ух питомцев')
            else:
                return await ctx.send('ашиебка')

        if value == 'д':
            if p == 'пикачу' or p == 'леха' or p == 'лёха' or p == 'путин':
                if Jpet['activated'] > 0:
                    if p == 'пикачу':
                        if pets[0] in Jpet:
                            if 0 < Jpet[pets[0]] < 2:
                                Jpet['pikachu'] -= 1
                                Jpet['activated'] -= 1
                                await ctx.send('Ты деактивировал Пикачу')
                                return utils.save_pets(pet)
                            else:
                                return await ctx.send('ашебка')
                    # if p == 'лёха' or p == 'леха':
                    #     if 0 < Jpet[pets[1]] < 2:
                    #         if pets[1] in Jpet:
                    #             Jpet['lexa'] -= 1
                    #             Jpet['activated'] -= 1
                    #             await ctx.send('Ты деактивировал Лёху')
                    #             return utils.save_pets(pet)
                    #     else:
                    #         return await ctx.send('ашебка')
                    if p == 'путин':
                        if pets[2] in Jpet:
                            if 0 < Jpet[pets[2]] < 2:
                                Jpet['putin'] -= 1
                                Jpet['activated'] -= 1
                                await ctx.send('Ты деактивировал путина')
                                return utils.save_pets(pet)
                            else:
                                return await ctx.send('ашебка')
                else:
                    return await ctx.send('У тебя нет активированых питомцев')
            else:
                return await ctx.send('ашебка')

        utils.save_pets(pet)

    @_pets.error
    async def _pets_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title='Использовать:',
                                  description='.питомец(пт, пет) {инфо, а:активировать, д: отключить} {имя питомца}',
                                  color=discord.Color.blue())
            return await ctx.send(embed=embed)
        if isinstance(error, commands.BadArgument):
            embed = discord.Embed(title='Использовать:',
                                  description='.питомец(пт, пет) {инфо, а:активировать, д: отключить} {имя питомца}',
                                  color=discord.Color.blue())
            return await ctx.send(embed=embed)

    @commands.command(name='коробка', aliases=['кб'])
    async def PetsBox(self, ctx, value: str = None):
        with open('files/file/users_pets.json', 'r', encoding='utf-8') as f:
            pet = json.load(f)
        with open('files/file/users_info.json', 'r', encoding='utf-8') as f:
            users = json.load(f)

        box = pet[str(ctx.author.id)]['box']
        Jpets = pet[str(ctx.author.id)]['pets']
        money = users[str(ctx.author.id)]['balance']

        if value is None:
            return await ctx.send(f'У тебя {box} коробок')

        if value == 'о' or value == 'открыть':
            if box >= 1:
                res = random.choices(pets, weights=[5, 35, 10])
                v_0 = pets.index(str(res[0]))
                pet[str(ctx.author.id)]['box'] -= 1
                if pets[v_0] in Jpets:
                    await utils.update_money(users, ctx.author, 5000)
                    utils.save_data(users)
                    utils.save_pets(pet)
                    return await ctx.send('У тебя уже есть данный питомец, компенсация 5К коинов')

                if pets[v_0] == pets[0]:
                    Jpets['pikachu'] = 0
                    await ctx.send('Поздравляю, тебе выпал **Легендарный питомец Пикачу!**')
                    return utils.save_pets(pet)
                elif pets[v_0] == pets[1]:
                    Jpets['lexa'] = 1
                    await ctx.send('Соболезную...Тебе выпало животное Лёха...')
                    pet[str(ctx.author.id)]['pets']['activated'] = 1
                    return utils.save_pets(pet)
                elif pets[v_0] == pets[2]:
                    Jpets['putin'] = 0
                    await ctx.send('Поздравляю, тебе выпал Эпический питомец Путин!')
                    return utils.save_pets(pet)
            else:
                return await ctx.send('У тебя нет коробок')

        if value == 'к' or value == 'купить':
            if money >= 50000:
                pet[str(ctx.author.id)]['box'] += 1
                await utils.update_money(users, ctx.author, -50000)
                await ctx.send('Ты купил коробку с питомцами')
                utils.save_data(users)
                return utils.save_pets(pet)
            else:
                res = 50000 - money
                return await ctx.send(f'Тебе нехватает: **{res} коинов**')

    @PetsBox.error
    async def PetsBox_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title='Использовать:',
                                  description='.коробка(кб) {купить(к), открыть(о)}',
                                  color=utils.randomColor())
            return await ctx.send(embed=embed)
        if isinstance(error, commands.BadArgument):
            embed = discord.Embed(title='Использовать:',
                                  description='.коробка(кб) {купить(к), открыть(о)}',
                                  color=utils.randomColor())
            return await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Pet(bot))
