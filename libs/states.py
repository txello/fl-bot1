from aiogram.fsm.state import StatesGroup, State

class Form(StatesGroup):    
    operands1 = State()
    operands2 = State()
    operands3 = State()