# TP-Bot - A discord bot for the ThemePlaza Discord
# Copyright (C) 2018 Valentijn "Ev1l0rd"
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
import yaml
import discord
from discord.ext import commands

config = yaml.safe_load(open('config.yaml'))
bot = commands.Bot(command_prefix=commands.when_mentioned_or(
    config['prefix']),
    description='ROBOT 9000 for Discord')


def load_cog(cog):
    try:
        bot.load_extension(cog)
    except Exception as e:
        print('Could not load cog ' + cog)
        print(e)
    finally:
        print(cog + " succesfully loaded")


@bot.event
async def on_ready():
    print('WUMPUS9K  Copyright (C) 2018  Valentijn "Ev1l0rd"\n' +
        'This program comes with ABSOLUTELY NO WARRANTY;\n' + 
        'This is free software, and you are welcome to redistribute it\n' +
        'under certain conditions;')
    print('------------')
    print('Logged in as:')
    print(bot.user.name)
    print(bot.user.id)
    print('Using prefix:')
    print(config['prefix'])
    print('------------')
    load_cog('wumpus9k')

@bot.command()
async def about(ctx):
    '''Show a quick link to the bot's Github repository.'''
    embed = discord.Embed(title='TP-Bot',
        description='A bot for the ThemePlaza discord, made by ev1l0rd.',
        url='https://github.com/ev1l0rd/tp-bot')
    embed.set_thumbnail(url='https://avatars2.githubusercontent.com/u/13433513')
    await ctx.send(embed=embed)

bot.run(config['token'])
