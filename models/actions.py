from abstract_models.abstract_models import Action
from typing import Optional
from aiogram.filters.callback_data import CallbackData

class DefaultActions(CallbackData, prefix="def"):
    action: Action
    tags: Optional[str]
    domain: Optional[str]
    chat_id: Optional[str]
