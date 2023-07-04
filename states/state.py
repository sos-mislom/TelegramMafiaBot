from aiogram.filters.state import State, StatesGroup

class DialogState(StatesGroup):
    wait_question = State()
    wait_anwser = State()
    stop = State()

