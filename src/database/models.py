from tortoise.models import Model
from tortoise import fields

class User(Model):
    member_id = fields.IntField(null=False)
    pings = fields.IntField()

    def __str__(self):
        return self.name