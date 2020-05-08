import discord
from discord.ext import commands

from .utils import utils


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='хелп')
    async def help(self, ctx, msg=None):
        await ctx.message.delete()
        embed = discord.Embed(colour=utils.randomColor())

        if msg is None:
            embed.set_author(name='Префикс:  .')
            # embed.add_field(name='**.хелп музыка**', value='Показывает команды для музыки', inline=False)
            embed.add_field(name='**.хелп фан**', value='Показывает говно а не команды', inline=False)
            embed.add_field(name='**.хелп экономика**', value='Показывает команды экономики', inline=False)
            embed.add_field(name='**.хелп лвл**', value='Показывает команды лвл', inline=False)
            embed.add_field(name='**.хелп информация**', value='Показывает команды для информации', inline=False)
            embed.add_field(name='**.хелп модерация**', value='Показывает команды для модерации', inline=False)

        # if msg == 'музыка':
        #     embed.set_author(name='Музыка:')
        #     embed.add_field(name='**.плей**', value='Проигрывает музон с ютубчика(и не только, сеня привет)',
        #                     inline=False)
        #     embed.add_field(name='**.громкость {значение(макс. 200)}**', value='Изменяет громкость', inline=False)
        #     embed.add_field(name='**.пауза**', value='Музон ставим на паузу', inline=False)
        #     embed.add_field(name='**.вб**', value='Возобновляет проигравание', inline=False)
        #     embed.add_field(name='**.стоп**', value='Остонавливает проигравание', inline=False)
        if msg == 'фан':
            embed.set_author(name='Фан:')
            embed.add_field(name='**.ава {ник}**', value='Отправляет аватар', inline=False)
            embed.add_field(name='**.мирослав**', value='Гей', inline=False)
            embed.add_field(name='**.неко**', value='Отправляет неко хули', inline=False)
            embed.add_field(name='**.хентай**', value='Отправляет хентай хули', inline=False)
            embed.add_field(name='**.аниме**', value='Отправляет аниме пикчу хули', inline=False)
            embed.add_field(name='**.ава {ник}**', value='Отправляет аватар', inline=False)
            embed.add_field(name='**.повтори {текст}**', value='Повторяет текст', inline=False)
            embed.add_field(name='**.ттс {текст}**', value='Отправляет текст с озвучкой', inline=False)
            embed.add_field(name='**.фотка {андрюша, бодя, пидоры, даун, дьявол, фгб, забив, красотка}**',
                            value='Не ебу фотки какие-то', inline=False)
            embed.add_field(name='**.шанс {чего-то(текст)}**', value='Шанс чего-либо', inline=False)
            embed.add_field(name='**.шар {чего-то(текст)}**', value='Ну это шар типа магический да...', inline=False)
            embed.add_field(name='**.напомнить {время в секундах} {текст}**',
                            value='Напоминает текст через некоторое время'
                            , inline=False)
            embed.add_field(name='**.пароль {от 1 до 1983}**', value='Генерирует пароль', inline=False)
            embed.add_field(name='**.кнб {камень/ножницы/бумага}**', value='Камень, ножницы, бумага...', inline=False)
            embed.add_field(name='**.калькулятор(кл) {+, -, /, **, кор}**', value='Простенький калькулятор',
                            inline=False)
        if msg == 'экономика':
            embed.set_author(name='Экономика:')
            embed.add_field(name='**.баланс**', value='Показывает твой баланс', inline=False)
            embed.add_field(name='**.дейли**', value='Даёт каждые 6 часов 1000 коинов', inline=False)
            embed.add_field(name='**.купить {что-то}**', value='Ну купить что-то чё не понятно то?', inline=False)
            embed.add_field(name='**.казино {кол-во коинов}**', value='Ваших коинов не будет', inline=False)
            embed.add_field(name='**.перечислить(пр) {ник} {кол-во коинов}**', value='Переводит коины другому человеку',
                            inline=False)
            embed.add_field(name='**.подписка(пд) {инфо}**', value='ну подписка как подписка', inline=False)
            embed.add_field(name='**.депозит(дп) {кол-во коинов}**', value='Вернёт через неделю ваши деньги + 20%',
                            inline=False)
            embed.add_field(name='**.рулетка(рл) {чёрный/красный/зелёный} {кол-во коинов}**',
                            value='Ваших коинов не будет', inline=False)
            # embed.add_field(name='**.инвентарь(инв) {сундук} {коины/опыт}**',
            #                 value='Твой инвентарь', inline=False)
        if msg == 'лвл':
            embed.set_author(name='Лвл:')
            embed.add_field(name='**.лвл**', value='Показывает твой лвл', inline=False)
            embed.add_field(name='**.топ {лвл/коины}**', value='Показывает топ 5 людей по уровню', inline=False)
        if msg == 'инфо':
            embed.set_author(name='Информация:')
            embed.add_field(name='**.осб {текст}**', value='Добавляет строку о себе в информации', inline=False)
            embed.add_field(name='**.инфо {ник}**', value='Показывает информацию о пользователе', inline=False)
        if msg == 'модер':
            embed.set_author(name='Модерация:')
            embed.add_field(name='**.варн {ник}**', value='Даёт предупреждение', inline=False)
            embed.add_field(name='**.кик {ник} {причина}**', value='Кикает пользователя с сервера', inline=False)
            embed.add_field(name='**.бан {ник} {причина}**', value='Банит пользователя на сервере', inline=False)
            embed.add_field(name='**.вбан {ник} {время м/ч}**', value='Банит пользователя на определённое время', inline=False)
            embed.add_field(name='**.разбан {ник}**', value='Разбанит пользователя на сервере', inline=False)
            embed.add_field(name='**.роль {роль} {ник}**', value='Даёт пользователя роль', inline=False)
            embed.add_field(name='**.цвет {роль} {номер цвета}**', value='Меняет цвет роли', inline=False)
            embed.add_field(name='**.ник {ник} {изменённый ник}**', value='Меняет ник пользователя', inline=False)
            embed.add_field(name='**.вмут {ник} {время(с,м,ч,}**', value='Мутит пользователя на время', inline=False)
            embed.add_field(name='**.мут {ник}**', value='Мутит пользователя', inline=False)

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Help(bot))
