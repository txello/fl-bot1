from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from libs.menu import mStart
from libs import words as wd
from . import conn

from plugins.postgresql import get_lang, Users
from plugins.notion import notion_post, notion_update

from sqlalchemy import Update, Select
from sqlalchemy.exc import IntegrityError
router = Router()

@router.message(CommandStart())
async def start_lang(message:Message): # Команда /start
    async with await conn() as session: # Подключаем БД
        db = await session.execute(Select(Users).where(Users.tg_id == message.from_user.id)) # получаем пользователя
        
        if db.first() == None: # Если пользователя нет в БД, то просим выбрать язык
            await message.answer("Choose language:",reply_markup=mStart.langs)
        else: # Если есть, то получаем выбранный язык и выводим меню
            lang = await get_lang(session,message.from_user.id)
            
            await message.answer(getattr(wd,f"wStart_{lang}").a1.format(i = message.from_user.full_name), reply_markup = mStart.a1 if lang == 'ru' else mStart.a2)
    

@router.callback_query(F.data.in_(['start_ru','start_en','m_back']))
async def start(callback:CallbackQuery): # Кнопки языка или кнопка "В главное меню"
    async with await conn() as session: # Подключаем БД
        try:
            session.add(Users(tg_id=callback.from_user.id, tg_link = callback.from_user.username, lang=callback.data.split('_')[1])) # Записываем пользователя в БД
            await session.flush() # Стабилизируем соединение
            await session.commit() # Пытаемся отправить запрос в БД
            await session.rollback() # Очищаем запрос
            
            await notion_post('Пользователи',params={
                'title':['text',str(callback.from_user.id)],
                'num_try':['number',0],
                'tg_link':['text',callback.from_user.username if callback.from_user.username != None else ''],
                'status':['checkbox',True],
                'lang':['text',callback.data.split('_')[1]]
            }) # Записываем пользователя в Notion
            
            lang = await get_lang(session,callback.from_user.id) # Получаем язык пользователя из БД
        except IntegrityError: # Если пользователь уже есть в БД:
            await session.rollback() # Очищаем запрос
            
            index = callback.data.split('_') # Получаем данные кнопки
            
            if index[0] == 'start': # Если кнопки - выбор языка, то:
                await session.execute(Update(Users).where(Users.tg_id == callback.from_user.id).values(lang = index[1])) # Меняем пользователю в БД столбец lang
                await session.commit() # Отправляем запрос в БД
                
                await notion_update('Пользователи',str(callback.from_user.id), {
                    'lang':['text',index[1]]
                }) # Меняем столбец lang в Notion для пользователя
                lang = index[1] # Получаем язык от кнопки
            else:
                lang = await get_lang(session,callback.from_user.id) # Получаем язык пользователя из БД
                
        await callback.message.answer(getattr(wd,f"wStart_{lang}").a1.format(i = callback.from_user.full_name),reply_markup= mStart.a1 if lang == 'ru' else mStart.a2) # Метод отправки сообщения
        
@router.callback_query(F.data == 'lang')
async def langs(callback:CallbackQuery): # Кнопка "Сменить язык"
    async with await conn() as session: # Подключаем БД
        lang = await get_lang(session,callback.from_user.id) # Получаем язык из БД
    
    await callback.message.answer(getattr(wd,f"wStart_{lang}").a1.format(i = callback.from_user.full_name),reply_markup=mStart.langs) # Отправляем приветственное меню на нужном языке