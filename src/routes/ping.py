from vkbottle.bot import BotLabeler, Message
from custom_rules import PersonalStateRule
from vkbottle.dispatch.rules.base import RegexRule 

bl = BotLabeler()

@bl.chat_message(PersonalStateRule(state=None), text="verpix")
async def ping(m: Message):
    return "✅"