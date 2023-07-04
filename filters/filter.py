from typing import Union, Dict, Any
from aiogram.filters import BaseFilter
from aiogram import Bot
from aiogram.types import Message, Chat
from aiogram.filters.chat_member_updated import CREATOR, ADMINISTRATOR
import config as c
from models.models import User

class TypicalFilter(BaseFilter):
    #for_replace: Union[str, list]
    def __init__(self, for_replace):
        self.for_replace: Union[str, list] = for_replace
    async def __call__(self, message: Message) -> bool:
        return any(ext in message.text.lower() for ext in self.for_replace)

class GetTagsFilter(BaseFilter):
    #for_replace: Union[str, list]
    def __init__(self, for_replace):
        self.for_replace: Union[str, list] = for_replace

    async def __call__(self, message: Message) -> Union[bool, Dict[str, Any]]:

        if message.caption is not None:
            tags = message.caption.lower()
            if any(ext in tags for ext in self.for_replace):
                for replacment_text in self.for_replace:
                    tags = tags.replace(replacment_text, "")
                if len(tags.split(" ")) > 0:
                    return {"tags": tags.split(" ")}
                return False
            return False

        if message.text is not None:
            tags = message.text.lower()
            if any(ext in tags for ext in self.for_replace):
                for replacment_text in self.for_replace:
                    tags = tags.replace(replacment_text, "")
                if len(tags.split(" ")) > 0:
                    return {"tags": tags.split(" ")}
                return False
            return False

class IsTextFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return message.text or False

class IsVoiceFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return message.voice

class IsBeInDataBaseFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        user = User(user_id=message.from_user.id)
        return not user.get_one()

class IsSpamFilter(BaseFilter):
    async def __call__(self, message: Message) -> Union[bool, Dict[str, Any]]:
        return {"spam": toBanOrNotToBan(message.text.lower(), str(message.chat.id))}

class IsReply(BaseFilter):
    async def __call__(self, message: Message) -> Union[bool, Dict[str, Any]]:
        return message.reply_to_message

class IsAdminOrCreator(BaseFilter):
    async def __call__(self, message: Message, bot: Bot) -> bool:
        member_status = await bot.get_chat_member(message.chat.id, message.from_user.id)
        private = False
        return message.from_user.id in c.ADMINS or member_status.status in ("creator", "administrator") or message.chat.type == "private"


