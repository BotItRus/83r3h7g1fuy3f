import discord

from discord.ext import commands, tasks
from itertools import cycle

TOKEN = 'NjMwNzQzNTY2OTYwMDMzODAy.XnNrFA.L65oYPKHRMvd6iD8Zld2hTVc1j4'
status = cycle(['.хелп', 'бодя гей', 'макс натурал'])

extensions = ['cogs.commands', 'cogs.level', 'cogs.moderation',
              'cogs.help', 'cogs.fun', 'cogs.economy',
              'cogs.pet']

bot = commands.Bot(command_prefix='.')

bot.remove_command('help')

if __name__ == '__main__':
    for extension in extensions:
        try:
            bot.load_extension(extension)
            print(f'Loaded {extension}')
        except Exception as error:
            print(f'{extension} cannot be loaded. [{error}]')


@bot.event
async def on_ready():
    change_status.start()
    print('----------------------------')
    print('Logged in as:')
    print('Name: ' + str(bot.user.name))
    print('ID: ' + str(bot.user.id))
    print('Version Discord: ' + str(discord.__version__))
    print('----------------------------')


@tasks.loop(seconds=30)
async def change_status():
    await bot.change_presence(activity=discord.Game(next(status)))


@bot.command(name='rl', aliases=['reload'])
@commands.has_permissions(administrator=True)
async def reload(ctx, cog):
    bot.unload_extension(cog)
    bot.load_extension(cog)
    await ctx.send(f'{cog} был перезагружен')
    print(f'Reloaded {cog}')


@reload.error
async def reload_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Ты забыл ввести файл!')
    if isinstance(error, commands.BadArgument):
        await ctx.send('Такого файла нет!')


bot.run(TOKEN)
