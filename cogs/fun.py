import json
import random
import aiohttp
import discord

from discord.ext import commands

from .utils import utils


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession()

    @commands.command(name='аниме')
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def anime(self, ctx):
        await ctx.message.delete()
        await ctx.trigger_typing()
        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://nekobot.xyz/api/v2/image/animepic') as r:
                res = await r.json()
        image = res["message"]
        em = discord.Embed()
        await ctx.send(embed=em.set_image(url=image))

    @commands.command(name='фотка')
    async def image(self, ctx, msg):
        await ctx.message.delete()
        v_0 = ['андрюша', 'бодя', 'пидоры', 'даун', 'дьявол', 'фгб', 'забив', 'красотка']
        if not msg in v_0:
            embed = discord.Embed(title='Использовать:',
                                  description='.фотка {андрюша, бодя, пидоры, даун, дьявол, фгб, забив, красотка}',
                                  color=utils.randomColor())
            return await ctx.send(embed=embed)

        if msg == 'андрюша':
            return await ctx.send(file=discord.File('img/Ou9PF8QH1OY.jpg'))
        if msg == 'бодя':
            return await ctx.send(file=discord.File('img/PqDhAjmi1fg.jpg'))
        if msg == 'пидоры':
            return await ctx.send(file=discord.File('img/pKvLTfbq21k.jpg'))
        if msg == 'даун':
            return await ctx.send(file=discord.File('img/K_BffXqOu7c.png'))
        if msg == 'дьявол':
            return await ctx.send(file=discord.File('img/uizmI9UZyNM.jpg'))
        if msg == 'фгб':
            return await ctx.send(file=discord.File('img/SguNgHiZFsk.jpg'))
        if msg == 'забив':
            return await ctx.send(file=discord.File('img/XCHLmfVZJVQ.jpg'))
        if msg == 'красотка':
            return await ctx.send(file=discord.File('img/JeWPaaIegpw.jpg'))

    @image.error
    async def img_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title='Использовать:',
                                  description='.фотка {андрюша, бодя, пидоры, даун, дьявол, фгб, забив, красотка}',
                                  color=utils.randomColor())
            await ctx.send(embed=embed)

    async def nekobot(self, imgtype: str):
        async with self.session.get('https://nekobot.xyz/api/image?type=%s' % imgtype) as res:
            res = await res.json()
        return res.get('message')

    @commands.command(name='хентай')
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def hentai(self, ctx):
        with open('files/file/users_info.json', 'r') as f:
            users = json.load(f)

        money = users[str(ctx.author.id)]['balance']

        if money < 500:
            res = 500 - money
            await ctx.send(f'Тебе нехватает: {res} коинов')
        else:
            await ctx.message.delete()
            await utils.update_money(users, ctx.author, -500)
            image = await self.nekobot("hentai")
            em = discord.Embed()
            await ctx.send(embed=em.set_image(url=image))

        utils.save_data(users)

    @hentai.error
    async def hentai_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send('Повтори попытку через {}с'.format(int(error.retry_after)))

    @commands.command(name='неко')
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def neko(self, ctx):
        with open('files/file/users_info.json', 'r') as f:
            users = json.load(f)

        money = users[str(ctx.author.id)]['balance']

        if money < 500:
            res = 500 - money
            await ctx.send(f'Тебе нехватает: {res} коинов')
        else:
            await ctx.message.delete()
            image = await self.nekobot("lewdkitsune")
            await utils.update_money(users, ctx.author, -500)
            em = discord.Embed()
            await ctx.send(embed=em.set_image(url=image))

        utils.save_data(users)

    @neko.error
    async def neko_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send('Повтори попытку через {}с'.format(int(error.retry_after)))

    @commands.command(name='мирослав', aliases=['гей'])
    async def gay(self, ctx):
        gay = ['https://rt.pornhub.com/view_video.php?viewkey=ph5d68e1b5e94b2',
               'https://rt.pornhub.com/view_video.php?viewkey=ph5d970dd28da70',
               'https://rt.pornhub.com/view_video.php?viewkey=ph5d975beacc375',
               'https://rt.pornhub.com/view_video.php?viewkey=ph5d952a9251197',
               'https://rt.pornhub.com/view_video.php?viewkey=ph5cae60a094e16',
               'https://rt.pornhub.com/view_video.php?viewkey=ph5d361f5774f52',
               'https://rt.pornhub.com/view_video.php?viewkey=ph5d6f347c53d2a',
               'https://rt.pornhub.com/view_video.php?viewkey=ph5d9919bbb1fb6',
               'https://rt.pornhub.com/view_video.php?viewkey=ph5cf25f872d5e9']

        await ctx.send(random.choice(gay))

    @commands.command(name='сооб')
    async def say(self, ctx, *message):
        await ctx.message.delete()
        msg = ' '.join(message)

        for channel in ctx.guild.channels:
            if isinstance(channel, discord.TextChannel):
                await channel.send(msg)

    @commands.command(name='кнб')
    async def rsp(self, ctx, value: str):
        words = ['камень', 'ножницы', 'бумага']
        if not value in words:
            embed = discord.Embed(title='Использовать:',
                                  description='.кнб {камень,ножницы,бумага}',
                                  color=utils.randomColor())
            return await ctx.send(embed=embed)
        v_0 = random.choice(words)

        if value == v_0:
            return await ctx.send('Ничья')

        if value == 'камень' and v_0 == 'бумага':
            return await ctx.send('Андрюшка выиграл!')
        if value == 'ножницы' and v_0 == 'камень':
            return await ctx.send('Андрюшка выиграл!')
        if value == 'бумага' and v_0 == 'ножницы':
            return await ctx.send('Андрюшка выиграл!')

        if value == 'камень' and v_0 == 'ножницы':
            return await ctx.send(f'{ctx.author.display_name} выиграл!')
        if value == 'ножницы' and v_0 == 'бумага':
            return await ctx.send(f'{ctx.author.display_name} выиграл!')
        if value == 'бумага' and v_0 == 'камень':
            return await ctx.send(f'{ctx.author.display_name} выиграл!')


def setup(bot):
    bot.add_cog(Fun(bot))
