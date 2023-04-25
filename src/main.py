from vkbottle.bot import Bot
from routes import labelers
from custom_rules import PersonalStateRule
from secret import TOKEN
import logging
import os

bot = Bot(TOKEN)
logging.basicConfig(level=logging.INFO)

for custom_labeler in labelers:
    bot.labeler.load(custom_labeler)

bot.run_forever()