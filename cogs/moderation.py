import asyncio
import discord

from discord.ext import commands
from discord.utils import get
from datetime import datetime

from .utils import utils as ut


async def create_mute_role(ctx):
    try:
        await ctx.guild.create_role(name='Mute')
    except discord.Forbidden:
        return await ctx.send('У меня недостаточно прав...')

    MuteRole = get(ctx.guild.roles, name='Mute')
    while not MuteRole:
        MuteRole = get(ctx.guild.roles, name='Mute')

    for channel in ctx.guild.channels:
        if isinstance(channel, discord.TextChannel):
            await channel.set_permissions(MuteRole, send_messages=False, add_reactions=False)
        elif isinstance(channel, discord.VoiceChannel):
            await channel.set_permissions(MuteRole, speak=False)


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='кик')
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, userName: discord.Member, *, reason=None):
        if not userName and not reason:
            await ctx.send("Нужно указать кого выгнать!")
            return

        putin = ut.checkPets('putin', userName)
        if putin is True:
            return await ctx.send(f'У {userName.display_name} есть питомец Путин, кикнуть его нельзя.')

        if str(userName.id) == '297725767670956032':
            return await ctx.send('Ты дура или да')

        if userName == ctx.author:
            await ctx.send("Ты не можешь сам себя выгнать!")
        elif userName == ctx.me:
            await ctx.send("Ты не можешь меня выгнать!")

        embed = discord.Embed(color=ut.randomColor(),
                              timestamp=datetime.utcnow())

        embed.add_field(name='Кикнул:', value=f'{ctx.author.display_name}', inline=True)
        embed.add_field(name='Кикнут:', value=f'{userName.mention}', inline=True)
        if reason:
            embed.add_field(name='Причина:', value=f'{reason}', inline=True)
        embed.set_thumbnail(url=userName.avatar_url)

        await userName.kick(reason=f'{ctx.author}: {reason}')
        await ctx.send(embed=embed)

    @commands.command(name='бан')
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, userName: discord.Member, *, reason=None):
        if not userName:
            await ctx.send('Нужно указать кого выгнать!')
            return

        if userName == ctx.author:
            await ctx.send('Ты не можешь себя забанить!')
            return

        if userName == ctx.me:
            await ctx.send('Ты не можешь забанить меня!')
            return
        if str(userName.id) == '297725767670956032':
            return await ctx.send('Ты дура или да')

        if reason is None:
            await ctx.send('Укажи причину')
            return

        await userName.ban(reason=f'{ctx.author}: {reason}')
        await ctx.send(f'{userName} был забанен по причине: {reason}')

    @commands.command(name='разбан', pass_context=True)
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member: discord.User):
        await ctx.message.delete()
        await ctx.guild.unban(member)
        return await ctx.send(f'{member} разбанен')

    @commands.command(name='вбан')
    @commands.has_permissions(ban_members=True)
    async def tempBan(self, ctx, user: discord.Member, time):
        await ctx.message.delete()
        if str(userName.id) == '297725767670956032':
            return await ctx.send('Ты дура или да')
        if not user:
            return await ctx.send(f'{user} нет на сервере!')
        if user == ctx.author:
            return await ctx.send('Ты не можешь сам себя забанить!')
        if user == ctx.me:
            return await ctx.send('Ты не можешь забанить меня!')
        if time is None:
            return await ctx.send('Ты забыл указать время!')

        await user.ban(reason=f'{ctx.author} забанил на время.')
        if time[-1:].lower() == 'м':
            timeS = time[:-1]
            if timeS > 60:
                return await ctx.send('Больше 60 минут нельзя!')
            await ctx.send(f'{ctx.author} забанил {user} на {timeS} минут.')
            await asyncio.sleep(int(timeS) * 60)
            await ctx.guild.unban(user)
            return print(f'{user} unbaned.')
        if time[-1:].lower() == 'ч':
            timeS = time[:-1]
            if timeS > 60:
                return await ctx.send('Больше 20 часов нельзя!')
            await ctx.send(f'{ctx.author} забанил {user} на {timeS} часов.')
            await asyncio.sleep(int(timeS)*60*60)
            await ctx.guild.unban(user)
            return print(f'{user} unbaned.')

    @commands.command(name='роль')
    @commands.has_permissions(administrator=True)
    async def giveRole(self, ctx, role, member: discord.Member):
        role = get(ctx.author.guild.roles, name=role)

        if not member:
            return await ctx.send('Ты забыл указать ник!')
        if not role in ctx.author.guild.roles:
            return await ctx.send(f'Роли {role} нету этом сервере!')
        if role in member.roles:
            return await ctx.send(f'У {member.display_name} уже есть данная роль!')

        await member.add_roles(role)
        await ctx.send(f'Добавил роль {role} пользователю {member.display_name}')
        print(f'{ctx.author} gave {member} role {role}')

    @commands.command(name='мут')
    @commands.has_permissions(administrator=True)
    async def mute(self, ctx, member: discord.Member, *, reason):
        if str(member.id) == '297725767670956032':
            return await ctx.send('Ты дура или да')
        if ctx.author.guild_permissions.mute_members:
            if member == ctx.author:
                await ctx.send('Ты не можешь замутить сам себя!')
                return

            putin = ut.checkPets('putin', member)
            if putin is True:
                return await ctx.send(f'У {member.display_name} есть питомец Путин, замутить его нельзя.')

            found = False
            for role in ctx.guild.roles:
                if role.name == 'Mute':
                    found = True
            if found is False:
                if not await create_mute_role(ctx):
                    return

            MuteRole = get(ctx.guild.roles, name='Mute')
            try:
                await member.add_roles(MuteRole)
                a = ''.join(reason)
                await ctx.send(f'**{ctx.author.display_name}** замутил {member.display_name} по причине {a}')
            except discord.Forbidden:
                return await ctx.send('У меня недостаточно прав...')
        else:
            await ctx.send('У тебя недостаточно прав')

    @commands.command(name='размут')
    @commands.has_permissions(administrator=True)
    async def unmute(self, ctx, member: discord.Member):
        if ctx.author.guild_permissions.mute_members:
            MuteRole = get(ctx.guild.roles, name='Mute')

            if not MuteRole in member.roles:
                return await ctx.send(f'{member.display_name} не в муте!')
            if member == ctx.author:
                return await ctx.send('Ты не можешь сам себя размутить!')

            await member.remove_roles(MuteRole)
            await ctx.send(f'**{ctx.author.display_name}** размутил {member.display_name}')
        else:
            await ctx.send('У тебя недостаточно прав')

    @commands.command(name='вмут')
    @commands.has_permissions(administrator=True)
    async def tempMute(self, ctx, member: discord.Member, time):
        if str(member.id) == '297725767670956032':
            return await ctx.send('Ты дура или да')
        if ctx.author.guild_permissions.mute_members:
            if member == ctx.author:
                await ctx.send('Ты не можешь замутить сам себя!')
                return

            found = False
            for role in ctx.guild.roles:
                if role.name == 'Mute':
                    found = True
            if found is False:
                await create_mute_role(ctx)

            MuteRole = get(ctx.guild.roles, name='Mute')

            await member.add_roles(MuteRole)

            if time[-1:].lower() == 'с':
                timeS = time[:-1]
                if timeS > 60:
                    return await ctx.send('Больше 60 секунд нельзя!')
                await ctx.send(f'**{member.display_name}** замучен на {timeS} секунд')
                await asyncio.sleep(int(timeS))
                if MuteRole in member.roles:
                    await member.remove_roles(MuteRole)
                    await ctx.send(f'**{member.display_name}** был размучен!')
                    return
                else:
                    return
            elif time[-1:].lower() == 'м':
                timeS = time[:-1]
                if timeS > 60:
                    return await ctx.send('Больше 60 минут нельзя!')
                await ctx.send(f'**{member.display_name}** замучен на {timeS} минут')
                await asyncio.sleep(int(timeS) * 60)
                if MuteRole in member.roles:
                    await member.remove_roles(MuteRole)
                    await ctx.send(f'**{member.display_name}** был размучен!')
                    return
                else:
                    return
            elif time[-1:].lower() == 'ч':
                timeS = time[:-1]
                if timeS > 20:
                    return await ctx.send('Больше 20 часов нельзя!')
                await ctx.send(f'**{member.display_name}** замучен на {timeS} часов')
                await asyncio.sleep(int(timeS) * 60 * 60)
                if MuteRole in member.roles:
                    await member.remove_roles(MuteRole)
                    await ctx.send(f'**{member.display_name}** был размучен!')
                    return
                else:
                    return
            else:
                await member.remove_roles(MuteRole)
        else:
            await ctx.send('У тебя недостаточно прав')

    @mute.error
    async def mute_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title='Использовать:',
                                  description='.мут {ник} {причина}',
                                  colour=ut.randomColor())
            await ctx.send(embed=embed)

    @unmute.error
    async def unmute_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title='Использовать:',
                                  description='.мут {ник}',
                                  colour=ut.randomColor())
            await ctx.send(embed=embed)

    @giveRole.error
    async def giveRole_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title='Использовать:',
                                  description='.роль {назв.роли} {ник}',
                                  colour=ut.randomColor())
            await ctx.send(embed=embed)
        if not ctx.author.guild_permissions.administrator:
            await ctx.send('У тебя нет прав')

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title='Использовать:',
                                  description='.бан {ник} {причина}',
                                  colour=ut.randomColor())
            await ctx.send(embed=embed)

    @unban.error
    async def unban_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title='Использовать:',
                                  description='.разбан {ник}',
                                  colour=ut.randomColor())
            await ctx.send(embed=embed)

    @tempBan.error
    async def tempban_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title='Использовать:',
                                  description='.вбан {ник} {время м/ч}',
                                  colour=ut.randomColor())
            await ctx.send(embed=embed)
        if isinstance(error, commands.BadArgument):
            embed = discord.Embed(title='Использовать:',
                                  description='.вбан {ник} {время м/ч}',
                                  colour=ut.randomColor())
            await ctx.send(embed=embed)

    @tempMute.error
    async def tempmute_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title='Использовать:',
                                  description='.вмут {ник} {время с/м/ч}',
                                  colour=ut.randomColor())
            await ctx.send(embed=embed)
        if isinstance(error, commands.BadArgument):
            embed = discord.Embed(title='Использовать:',
                                  description='.вмут {ник} {время с/м/ч}',
                                  colour=ut.randomColor())
            await ctx.send(embed=embed)

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title='Использовать:',
                                  description='.кик {ник} {причина}',
                                  colour=ut.randomColor())
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Moderation(bot))
