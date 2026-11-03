# yapin

Python library for building bots on [Yapin'](https://yapin.gg/developers).

`yapin` is built on [`yapper.py`](https://github.com/our-websites/yapper.py): it installs it for you, and `import yapin` gives you everything `import yapper` does (same classes, same behaviour, updates come with new `yapper.py` releases).

## Install

```bash
pip install yapin
```

Python 3.10 or newer.

## Quick start

Make a bot token in **Settings -> Developer** (it starts with `yb_`) and put it in a `.env` file next to your bot:

```
YAPIN_BOT_TOKEN=yb_your_token_here
```

Then write `bot.py`:

```python
import yapin

bot = yapin.Bot()  # reads YAPIN_BOT_TOKEN (or YAPPER_BOT_TOKEN) from the environment or your .env file

@bot.command("ping", "Check if the bot is alive")
def ping(msg):
    msg.reply("pong")

@bot.command("vote", "Start a pizza vote")
def vote(msg):
    msg.reply(
        embeds=yapin.Embed().title("Pizza tonight?").color("blue"),
        components=yapin.Row(
            yapin.Button.success("Yes", "vote:yes"),
            yapin.Button.danger("No", "vote:no"),
        ),
    )

@bot.button("vote:")  # clicks on buttons whose custom_id starts with "vote:"
def voted(i):
    i.ephemeral("You picked " + i.custom_id[5:])

@bot.on("member_join")
def welcome(ev):
    print(f"{ev.username} joined")

bot.run()
```

Run it with `python bot.py`. People can now type `/ping` or `!ping`. Nothing to host: the bot connects out to Yapin' and gets its events pushed.

### Tokens and the `.env` file

The token is read from `YAPIN_BOT_TOKEN` or `YAPPER_BOT_TOKEN` in your environment, then from a `.env` file in the folder you run from (or a parent folder). A variable that is already set in the environment always wins over the file. You can also pass it directly: `yapin.Bot("yb_...")`.

## What you get

- **Commands, events and buttons**: `@bot.command(...)`, `@bot.on("member_join")`, `@bot.button("prefix:")`.
- **Embeds, buttons and Components V2 layouts**: `yapin.Embed`, `yapin.Button`, `yapin.Row`, `yapin.Container`, `yapin.Section` and friends, sent with `msg.reply(...)` or `bot.send_layout(...)`.
- **Cogs**: group features into `yapin.Cog` classes, one file per topic, and load a folder with `bot.load_cogs("cogs")`.
- **The whole API**: messages, members, roles, channels, moderation, voice, webhooks and more as `bot.*` methods. Every one has a docstring: `help(yapin.Bot.send)`.
- **Errors**: failed calls raise `yapin.YapperError` (also available as `yapin.YapinError`) with `.status` and `.retry_after`.

For the full tour with examples (cogs, Components V2, every `bot.*` method) see the [yapper.py README](https://github.com/our-websites/yapper.py#readme); everything there works with `yapin` in place of `yapper`. Payload details and limits are in the Yapin' docs: <https://yapin.gg/developers>

## License

GPL-3.0-only
