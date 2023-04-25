from ctx import ctx

class StateEngine:
    def __init__(self):
        pass

    def set(self, peer_id, user_id, value):
        ctx.set(f"state-{peer_id}_{user_id}", value)

    def get(self, peer_id, user_id):
        return ctx.get(f"state-{peer_id}_{user_id}")
    
    def delete(self, peer_id, user_id):
        ctx.delete(f"state-{peer_id}_{user_id}")

state_engine = StateEngine()