from vkbottle.bot import BotLabeler, Message
from custom_rules import PersonalStateRule
from vkbottle.dispatch.rules.base import RegexRule 

bl = BotLabeler()

@bl.chat_message(regexp=r"[club217937141|@verpix]")
async def pillow_for_crying(m: Message):
    return "Да"