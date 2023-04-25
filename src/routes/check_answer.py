from vkbottle.bot import BotLabeler, Message
from custom_rules import PersonalStateRule
from vkbottle import VKAPIError
from state_engine import state_engine
from ctx import ctx

bl = BotLabeler()

@bl.chat_message(PersonalStateRule(state="SOLVING"))
async def check_answer(m: Message):
    expression_answer = ctx.get(f"answer-{m.peer_id}_{m.from_id}")
    if expression_answer == m.text:
        ctx.set(f"verified-{m.peer_id}_{m.from_id}", True)
        state_engine.delete(m.peer_id, m.from_id)
        return "Добро пожаловать!"
    try:
        if m.action.type.value in (
            "chat_kick_user", 
            "chat_invite_user", 
            "chat_invite_user_by_link", 
            "chat_invite_user_by_message_request"
            ):
            return
    except AttributeError:
        pass  
    try:
        pass
        await m.ctx_api.messages.delete(
            cmids=[m.conversation_message_id], 
            delete_for_all=True, 
            peer_id=m.peer_id
        )
    except VKAPIError[15] as error:
        return f"{error} ⚠"

