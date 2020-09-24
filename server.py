import discord

import json
import os
import numpy as np
import tensorflow as tf

import model, sample, encoder

model_name=os.getenv('MODEL_NAME')
seed=None
nsamples=1
batch_size=1
length=500
temperature=1
top_k=40
top_p=0.0

enc = encoder.get_encoder(model_name)
hparams = model.default_hparams()
with open(os.path.join('models', model_name, 'hparams.json')) as f:
    hparams.override_from_dict(json.load(f))

if length is None:
    length = hparams.n_ctx
elif length > hparams.n_ctx:
    raise ValueError("Can't get samples longer than window size: %s" % hparams.n_ctx)

sess = tf.Session(graph=tf.Graph())
sess.__enter__()
np.random.seed(seed)
tf.set_random_seed(seed)

context = tf.placeholder(tf.int32, [batch_size, None])
output = sample.sample_sequence(
    hparams=hparams, length=length,
    # start_token=enc.encoder['<|endoftext|>'],
    context=context,
    batch_size=batch_size,
    temperature=temperature, top_k=top_k, top_p=top_p
)[:, 1:]

saver = tf.train.Saver()
ckpt = tf.train.latest_checkpoint(os.path.join('models', model_name))
saver.restore(sess, ckpt)

async def generate_quote(quote_input):
    text = ""
    generated = 0
    context_tokens = enc.encode(quote_input)
    while nsamples == 0 or generated < nsamples:
        out = sess.run(output, feed_dict={
            context: [context_tokens for _ in range(batch_size)]
        })[:, len(context_tokens):]
        for i in range(batch_size):
            generated += batch_size
            text = enc.decode(out[i])
    return text

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)
        await self.change_presence(activity=discord.Game(name='GEE PEE TEE TWO'))

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        content = message.content.split(' ', 1)

        if len(content) > 0 and content[0] == '!quote':
            await message.channel.send('2 secs m8')
            context = ''
            if len(content) > 1:
                context = '[' + message.created_at.strftime("%d-%b-%y %H:%M %p") + '] ' + message.author.name + '#' + str(message.author.discriminator)  + '\n' + content[1]
            quote = await generate_quote(context)
            await message.channel.send('```' + context + quote + '```')

client = MyClient()

client.run(os.getenv('DISCORD_TOKEN'))