from vkbottle.bot import Message
from state_engine import state_engine
from vkbottle.dispatch.rules import ABCRule

class PersonalStateRule(ABCRule[Message]):
    def __init__(self, state):
        self.state = state

    async def check(self, event: Message):
        try:
            if event.action.type.value == "chat_invite_user":
                new_user_id = event.action.member_id
            else:
                new_user_id = event.from_id
        except AttributeError:
            new_user_id = event.from_id
        
        current_state = state_engine.get(event.peer_id, new_user_id)
        if self.state == current_state:
            return True
        return False
            