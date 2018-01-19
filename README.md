## WUMPUS 9000
ROBOT9000 for Discord

## Description
This is a version of Randall Munroe's "ROBOT9000" irc chat bot to discordpy. Just like the original ROBOT9000 script, the bot checks for each message if it has been send before, and if it has, it will remove the message and warn/mute the user.

The bot can either be loaded using the `main.py` wrapper script (fill out `config.json.example` if you want to use it), or it can be loaded as an extension using the `bot.load_extension()` somewhere in your `on_ready()` call.

Config can be done by anyone with the "Manage Server" permissions, and it is possible to opt-in channels, opt-out channels, remove all stored messages for a given channel (useful if you find that a channels activity is starting to get a bit low) and remove all mutes and warns for a user (useful if someone's mute time starts to exceed a reasonable amount).

## Commands
- `[p]wumpus9kconfig` - Opens the configuration menu. Can be run by anyone with the "Manage Server" permission.

## Limitations
A single one:

- If you restart the bot, any existing mutes will be made permanent unless you clear them with the config menu.

## License
AGPLv3, see the LICENSE file for details.

Wumpus9K - ROBOT9000 for Discord
Copyright (C) 2018 Valentijn "Ev1l0rd"

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.