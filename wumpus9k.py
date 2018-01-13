import discord
from discord.ext import commands
import yaml
import sqlite3


class wumpus9k:
    def __init__(self, bot):
        self.bot = bot
        self.conn = sqlite3.connect('wumpus9k.sqlite3')
        self.cursor = self.conn.cursor()
        create_database(self.conn)

    @commands.command()
    async def wumpus9kconfig(self, ctx):
        main_message = ctx.send(content='''```
            wumpus9k config menu

            1. (un)register a channel
            2. empty the message db for a channel
            3. clear all violations for a user
            4. exit
            ```
            Please reply with the number for the config. This menu will auto-cancel after 30 seconds.''')

        def main_menucheck(message):
            return message.content > 1 and message.content < 4

        reply = await self.bot.wait_for('message', check=main_menucheck, timeout=30.0)
        if reply:
            if reply.content.lower().strip() == '1':
                self.register_channel(ctx, main_message)
            elif reply.content.lower().strip() == '2':
                pass
            elif reply.content.lower().strip() == '3':
                pass
            else:
                await main_message.edit(content='Canceled config menu.')
        else:
            await main_message.edit(content='Canceled config menu.')

    async def register_channel(self, ctx, main_message):
        main_message.edit(content='''```
            wumpus9k config menu > register channel

            Please specify the channel to mention (in the format of #channel)
            ```''')


def create_database(conn):
    conn.execute('''
        CREATE TABLE [IF NOT EXIST] violations (
            violation_id integer PRIMARY KEY AUTOINCREMENT,
            user_id integer,
            amount_of_times_muted integer
        );''')
    conn.execute(''' 
        CREATE TABLE [IF NOT EXIST] registered_channels (
            channel_id integer,
            registered_date date,
            registering_member date
        );''')

    conn.execute('''
        CREATE TABLE [IF NOT EXIST] message_db (
            message_contents text PRIMARY KEY AUTOINCREMENT,
            channel_id integer,
            FOREIGN KEY(channel_id) REFERENCES registered_channels(channel_id)
        );''')