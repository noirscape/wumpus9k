import discord
from discord.ext import commands
import yaml
import sqlite3
import datetime
import asyncio

class wumpus9k:
    def __init__(self, bot):
        self.bot = bot
        self.conn = sqlite3.connect('wumpus9k.sqlite3')
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
                return message.author == ctx.message.author

        reply = await self.bot.wait_for('message', check=main_menucheck)
        if reply:
            if reply.content.lower().strip() == '1':
                await reply.delete()
                await self.register_channel(ctx, main_message)
            elif reply.content.lower().strip() == '2':
                await self.empty_message_db(ctx, main_message)
            elif reply.content.lower().strip() == '3':
                pass
            else:
                await main_message.edit(content='Cancelled config menu.')
        else:
            await main_message.edit(content='Cancelled config menu.')

    async def register_channel(self, ctx, main_message):
        await main_message.edit(content='''```
wumpus9k config menu > register channel

Please specify the channel to add (in the format of #channel)```''')

        def channel_check(message):
            return message.author == ctx.message.author

        cursor = self.conn.cursor()
        reply = await self.bot.wait_for('message', check=channel_check)
        if reply and reply.channel_mentions:
            reg_channel = reply.channel_mentions[0]
            cursor.execute('SELECT channel_id FROM registered_channels WHERE channel_id=?', (reg_channel.id,))
            is_registered = cursor.fetchone()
            if not is_registered:
                cursor.execute('INSERT INTO registered_channels(channel_id, registered_date, registering_member) VALUES(?,?,?)',
                    (reg_channel.id, datetime.datetime.now(), ctx.message.author.id))
                await main_message.edit(content='Registered channel {0}'.format(reg_channel.mention))
            else:
                cursor.execute('DELETE FROM registered_channels WHERE channel_id=?', (reg_channel.id,))
                await main_message.edit(content='Unregistered channel {0}'.format(reg_channel.mention))
            self.conn.commit()
        else:
            await main_message.edit(content='Invalid response or timeout. Cancelled config menu.')

    async def empty_message_db(self, ctx, main_message):
        await main_message.edit(content='''```
wumpus9k config menu > empty message database

Please specify the channel to clean the database of (in the format of #channel)```''')

        def channel_check(message):
            return message.author == ctx.message.author

        cursor = self.conn.cursor()
        reply = await self.bot.wait_for('message', check=channel_check)
        if reply and reply.channel_mentions:
            clean_channel = reply.channel_mentions[0]
            cursor.execute('SELECT channel_id FROM message_db WHERE channel_id=?', (clean_channel.id,))
            if cursor.rowcount != 0:
                cursor.execute('DELETE FROM message_db WHERE channel_id=?', (clean_channel.id,))
                await main_message.edit(content='Channel messages succesfully emptied from the database.')
            else:
                await main_message.edit(content='There were no messages in the database.')
        else:
            await main_message.edit(content='Invalid response or timeout. Cancelled config menu.')

    async def clear_user(self, ctx, main_message):
        await main_message.edit(content='''```
wumpus9k config menu > clear violations

Please specify the user to remove all violations of (in the format @user)```''')

        def channel_check(message):
            return message.author == ctx.message.author

        cursor = self.conn.cursor()
        reply = await self.bot.wait_for('message', check=channel_check)
        if reply and reply.mentions:
            cleared_user = reply.mentions[0]
            cursor.execute('SELECT user_id FROM message_db WHERE user_id=?', (cleared_user.id,))
            has_violations = cursor.fetchone()
            if has_violations:
                cursor.execute('DELETE FROM message_db WHERE user_id=?', (cleared_user.id,))
                await main_message.edit(content='User violations succesfully removed from the database.')
            else:
                await main_message.edit(content='There were no violations for this user in the database.')
        else:
            await main_message.edit(content='Invalid response or timeout. Cancelled config menu.')

    async def on_message(self, message):
        if type(message.channel) is discord.TextChannel:
            cursor = self.conn.cursor()
            cursor.execute('SELECT message_contents FROM message_db WHERE channel_id = ? AND message_contents = ? ', (message.channel.id, message.content))
            if not cursor.rowcount == 0:
                cursor.execute('INSERT INTO message_db(message_contents, channel_id) VALUES (?,?)',
                (message.content, message.channel.id))
                self.conn.commit()
            else:
                await message.delete()
                cursor.execute('SELECT user_id FROM violations WHERE user_id = ?', (message.author.id,))
                violated_before = cursor.fetchone()
                if violated_before:
                    cursor.execute('UPDATE violations SET amount_of_times_muted = amount_of_times_muted + 1 WHERE user_id = ?', (message.author.id,))
                    self.conn.commit()
                else:
                    cursor.execute('INSERT INTO violations(user_id) VALUES (?)', (message.author.id,))
                    self.conn.commit()
                self.cursor.execute('SELECT amount_of_times_muted FROM violations WHERE user_id = ?', (message.author.id,))
                mute_to_apply = cursor.fetchone()[0]
                if mute_to_apply == 1:
                    await message.author.send(content="You have attempted to send a message that has been send before in this channel. The bot has automatically removed your message.\n" +
                        "The next time this happens, you will be automatically muted in the channel {0}.".format(message.channel.mention))
                else:
                    mute_in_minutes = mute_to_apply * 2
                    await message.channel.set_permissions(message.author, read_messages=True, send_messages=False)
                    await message.author.send(content="You have attempted to send a message that has been send before in this channel. The bot has automatically removed your message.\n" +
                        "You have been automatically muted for {0} minutes.".format(mute_in_minutes))
                    await asyncio.sleep(mute_in_minutes * 60)
                    await message.author.send(content="You have been unmuted. Please do not do this again or you will be muted for longer. If you wish to have your mutes reset, please contact a moderator.")


def create_database(conn):
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS violations (
            user_id integer PRIMARY KEY,
            amount_of_times_muted integer DEFAULT 1
        );''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS registered_channels (
            channel_id integer PRIMARY KEY,
            registered_date date,
            registering_member integer
        );''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS message_db (
            message_contents text PRIMARY KEY,
            channel_id integer,
            FOREIGN KEY(channel_id) REFERENCES registered_channels(channel_id)
        );''')


def setup(bot):
    bot.add_cog(wumpus9k(bot))
