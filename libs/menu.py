from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup
from libs.words import wMenu_ru, wMenu_en

class mStart:
    langs = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="RU🇷🇺",callback_data="start_ru")
        ],
        [
            InlineKeyboardButton(text="EN🇬🇧",callback_data="start_en")
        ]
    ])
    
    a1 = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=wMenu_ru.a1,callback_data="op_start")
        ],
        [
            InlineKeyboardButton(text=wMenu_ru.a3,callback_data="lang")
        ]
    ])
    
    a2 = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=wMenu_en.a1,callback_data="op_start")
        ],
        [
            InlineKeyboardButton(text=wMenu_en.a3,callback_data="lang")
        ]
    ])


class mBack:
    a1 = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=wMenu_ru.a1,callback_data="op_start")
        ],
        [
            InlineKeyboardButton(text=wMenu_ru.a2,callback_data="m_back")
        ]
    ])
    
    a2 = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=wMenu_en.a1,callback_data="op_start")
        ],
        [
            InlineKeyboardButton(text=wMenu_en.a2,callback_data="m_back")
        ]
    ])

class mMath:
    a1 = InlineKeyboardMarkup(inline_keyboard=[
        [
            
                InlineKeyboardButton(text="+",callback_data="ops_+"),
                InlineKeyboardButton(text="-",callback_data="ops_-")
            
        ],
        [
            
                InlineKeyboardButton(text="*",callback_data="ops_*"),
                InlineKeyboardButton(text="/",callback_data="ops_/")
            
        ]
    ])