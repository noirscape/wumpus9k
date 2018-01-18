import discord
from discord.ext import commands
import yaml
import sqlite3
import datetime


class wumpus9k:
    def __init__(self, bot):
        self.bot = bot
        self.conn = sqlite3.connect('wumpus9k.sqlite3')
        self.cursor = self.conn.cursor()
        create_database(self.conn)

    @commands.command()
    async def wumpus9kconfig(self, ctx):
        main_message = await ctx.send(content='''```
wumpus9k config menu

1. (un)register a channel
2. empty the message db for a channel
3. clear all violations for a user
4. exit
```
Please reply with the number for the config you wish to change.''')

        def main_menucheck(message):
            if message.content.isdigit():
                return message.author == message.author

        reply = await self.bot.wait_for('message', check=main_menucheck)
        if reply:
            if reply.content.lower().strip() == '1':
                await reply.delete()
                await self.register_channel(ctx, main_message)
            elif reply.content.lower().strip() == '2':
                pass
            elif reply.content.lower().strip() == '3':
                pass
            else:
                await main_message.edit(content='Cancelled config menu.')
        else:
            await main_message.edit(content='Cancelled config menu.')

    async def register_channel(self, ctx, main_message):
        await main_message.edit(content='''```
wumpus9k config menu > register channel

Please specify the channel to mention (in the format of #channel)```''')

        def channel_check(message):
            return message.author == message.author

        reply = await self.bot.wait_for('message', check=channel_check)
        if reply and reply.channel_mentions:
            reg_channel = reply.channel_mentions[0]
            self.cursor.execute('SELECT channel_id FROM registered_channels WHERE channel_id=?', (str(reg_channel.id),))
            is_registered = self.cursor.fetchone()
            if not is_registered:
                self.cursor.execute('INSERT INTO registered_channels(channel_id, registered_date, registering_member) VALUES(?,?,?)',
                    (str(reg_channel.id), datetime.datetime.now(), str(ctx.message.author.id)))
                await main_message.edit(content='Registered channel {0}'.format(reg_channel.mention))
            else:
                self.cursor.execute('DELETE FROM registered_channels WHERE channel_id=?', (str(reg_channel.id),))
                await main_message.edit(content='Unregistered channel {0}'.format(reg_channel.mention))
            self.conn.commit()
        else:
            await main_message.edit(content='Invalid response or timeout. Cancelled config menu.')


def create_database(conn):
    conn.execute('''
        CREATE TABLE IF NOT EXISTS violations (
            violation_id integer PRIMARY KEY AUTOINCREMENT,
            user_id integer,
            amount_of_times_muted integer
        );''')
    conn.execute(''' 
        CREATE TABLE IF NOT EXISTS registered_channels (
            channel_id text PRIMARY KEY,
            registered_date date,
            registering_member text
        );''')

    conn.execute('''
        CREATE TABLE IF NOT EXISTS message_db (
            message_contents text PRIMARY KEY,
            channel_id integer,
            FOREIGN KEY(channel_id) REFERENCES registered_channels(channel_id)
        );''')

def setup(bot):
    bot.add_cog(wumpus9k(bot))