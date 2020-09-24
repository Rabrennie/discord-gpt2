# discord-gpt2

## Commands

`!quote [optional text]`

Generates some text based on the model

## Setup
1) Train your model
    * https://colab.research.google.com/drive/1SzuGlxaFWA0w6_jF2tIq243LnpNSHbaQ?usp=sharing

2) copy model folder to models folder
    * eg `./models/discord`

3) Set up a bot account on discord
    * https://discordpy.readthedocs.io/en/latest/discord.html#discord-intro

4) Build docker image
```bash
docker build --tag discordgpt2
```

5) Run docker image
```bash
docker run -e MODEL_NAME=discord -e DISCORD_TOKEN=YOUR_DISCORD_TOKEN_FROM_STEP_3 -d discordgpt2
```

## TODO
- [ ] Single message responses
- [ ] Better error handling
- [ ] Hosted image to avoid building every time