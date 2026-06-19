# LumenDiscord

A modern multipurpose Discord bot built with Python and discord.py.

LumenDiscord combines moderation, utility, and fun commands into a single easy-to-use bot while supporting both prefix and slash commands.

## Features

### Moderation

* Ban members
* Unban members
* Kick members
* Timeout members
* Remove timeouts
* Clear messages
* Lock channels
* Unlock channels
* Manage roles
* Change nicknames

### Utility

* User information
* Server information
* Avatar viewer
* Banner viewer
* Custom help system
* AFK System
* Permission-aware error handling

### Fun

* Coin Flip
* Dice Roll
* Random Number Generator
* Random Jokes
* Random Facts

## Commands
All commands are developed as both **prefix and slash** commands. Use / to access slash commands.

### Moderation Commands

| Command    | Description              |
| ---------- | ------------------------ |
| !ban       | Ban a member             |
| !unban     | Unban a member           |
| !kick      | Kick a member            |
| !timeout   | Timeout a member         |
| !untimeout | Remove a timeout         |
| !clear     | Delete messages          |
| !lock      | Lock a channel           |
| !unlock    | Unlock a channel         |
| !role      | Add or remove roles      |
| !nickname  | Change a user's nickname |

### Utility Commands

| Command         | Description              |
| --------------- | ------------------------ |
| !userinfo       | View user information    |
| !serverinfo     | View server information  |
| !avatar         | View a user's avatar     |
| !banner         | View a user's banner     |
| !help           | View help menu           |
| !help <command> | View command information |

### Fun Commands

| Command   | Description              |
| --------- | ------------------------ |
| !coinflip | Flip a coin              |
| !dice     | Roll a dice              |
| !random   | Generate a random number |
| !joke     | Get a random joke        |
| !fact     | Get a random fact        |
| !afk      | Set yourself as AFK      |

## Installation

Clone the repository:

```bash
git clone https://github.com/hasancooksfr/LumenDiscord
cd LumenDiscord
```

Create a virtual environment:

```bash
python3 -m venv venv
```

Activate the virtual environment:

Linux/macOS:

```bash
source venv/bin/activate
```

Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Configuration

Create a `.env` file:

```env
DISCORD_TOKEN=YOUR_BOT_TOKEN
```

## Running the Bot

```bash
python main.py
```

## Permissions

Recommended bot permissions:

* Administrator

Or:

* Manage Messages
* Manage Roles
* Manage Nicknames
* Moderate Members
* Kick Members
* Ban Members
* Manage Channels
* Send Messages
* Embed Links
* Read Message History
* View Channels

## Tech Stack

* Python 3.13+
* discord.py
* aiohttp
* python-dotenv

## License

This project is licensed under the MIT License.

## Author

Hasandeep Singh

Built with Python and discord.py.
