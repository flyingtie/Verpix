from vkbottle.bot import BotLabeler, Message
from vkbottle import VKAPIError
from vkbottle.dispatch.rules.base import ChatActionRule
from custom_rules import PersonalStateRule
from state_engine import state_engine
from ctx import ctx
from service.get_expression import get_expression
from asyncio import sleep

bl = BotLabeler()

@bl.chat_message(ChatActionRule([
    "chat_invite_user", 
    "chat_invite_user_by_link", 
    "chat_invite_user_by_message_request"
]), PersonalStateRule(state=None))
async def send_captcha(m: Message):
    if m.action.type.value == "chat_invite_user":
        new_user_id = m.action.member_id
    else:
        new_user_id = m.from_id
        
    members = await m.ctx_api.messages.get_conversation_members(peer_id=m.peer_id)
    is_member_admin = 0
    for i in members.items:
        if i.member_id != m.from_id:
            continue
        is_member_admin = i.is_admin
        break
    if new_user_id < 0: 
        if not is_member_admin or new_user_id == -217937141:
            await m.answer("Приглашение групп в беседу запрещено! (Beta)") #TODO бд
            await m.ctx_api.messages.remove_chat_user(chat_id=m.chat_id, member_id=new_user_id)
            return 
        return

    if ctx.get(f"timer-{m.peer_id}_{new_user_id}"):
        return 
    
    state_engine.set(m.peer_id, new_user_id, "SOLVING")
    expression, expression_answer = get_expression()
    ctx.set(f"answer-{m.peer_id}_{new_user_id}", expression_answer)
    ctx.set(f"verified-{m.peer_id}_{new_user_id}", False)
    member = await m.ctx_api.users.get(new_user_id)
    await m.answer(
        f"Приветствую, @id{new_user_id}({member[0].first_name})! "+
        "Пройдите верификацию ✅\n"+
        f"Решите выражение {expression}\n"+
        "У вас есть 30 секунд! ⌛"
    )

    ctx.set(f"timer-{m.peer_id}_{new_user_id}", True)
    await sleep(30)
    if not ctx.get(f"verified-{m.peer_id}_{new_user_id}") and ctx.get(f"timer-{m.peer_id}_{new_user_id}"):
        #TODO написать текст перед киком пользователя
        try:
            await m.ctx_api.messages.remove_chat_user(chat_id=m.chat_id, member_id=new_user_id) 
        except VKAPIError[15] as error:
            await m.answer(f"{error} ⚠")
        
        state_engine.delete(m.peer_id, new_user_id)
    ctx.delete(f"timer-{m.peer_id}_{new_user_id}")
    ctx.delete(f"answer-{m.peer_id}_{new_user_id}")
    ctx.delete(f"verified-{m.peer_id}_{new_user_id}")

