from aiogram import Router, F
from aiogram.types import Message,CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext
from libs import words as wd
from libs.menu import mBack, mMath
from libs.states import Form
from time import sleep

from plugins.pillow import createImage
from plugins.notion import notion_post, notion_update, notion_get
from plugins.postgresql import get_lang, Appeal, Users

from sqlalchemy import Select, Update
from . import conn

router = Router()

@router.callback_query(F.data == 'op_start')
async def op_step_1(callback:CallbackQuery, state:FSMContext): # Кнопка "Ввести операнды"
    await state.set_state(Form.operands1) # Включаем машину ожидания 1
    
    async with await conn() as session: # Подключаем БД
        lang = await get_lang(session,callback.from_user.id) # Получаем язык из БД
        await state.set_data({'lang',lang}) # Отправляем язык в машину ожидания
    
    await callback.message.answer(getattr(wd,f"wMath_{lang}").a1) # "Введите первый операнд"
    
@router.message(Form.operands1)
async def op_step_2(message:Message, state:FSMContext): # Ответ от пользователя в машине ожидания 1
    await state.update_data(step_1=message.text) # Обновляем шаг
    dict = await state.get_data()
    
    lang = dict['lang'] # Получаем язык из прошлой машины ожидания
    
    await message.answer(getattr(wd,f"wMath_{lang}").a3,reply_markup=mMath.a1) # "Выберите оператор"


@router.callback_query(F.data.startswith('ops_'))
async def op_step_3(callback:CallbackQuery, state:FSMContext): # Ответ от пользователя при выборе оператора
    await state.update_data(step_2=callback.data.split('_')[1]) # Обновляем шаг
    dict = await state.get_data() # Получаем словарь из машины ожидания 1
    
    lang = dict['lang'] # Получаем язык из прошлой машины ожидания
    
    await state.set_state(Form.operands3) # Объявляем машину ожидания 2
    await state.set_data(dict) # Обновляем словарь
    
    
    await callback.message.answer(getattr(wd,f"wMath_{lang}").a2) # "Выберите второй операнд"
    
@router.message(Form.operands3)
async def op_finally(message:Message, state:FSMContext): # Ответ от машины ожидания 2
    async with await conn() as session: # Подключаем БД
        lang = lang = dict['lang'] # Получаем язык из прошлой машины ожидания
        
        await state.update_data(step_3=message.text) # Обновляем шаг
        dict = await state.get_data() # Получаем словарь
        
        not_err = True # Если не ошибка...
        point = 0 # Поинтов по умолчанию 0
        try:
            ops = f"{dict['step_1']}{dict['step_2']}{dict['step_3']}" # Записываем запрос в одну строку
            result_eval = eval(ops) # Обрабатываем запрос
            
            if dict['step_2'] == '+': point = 1 # Если +, то 1 поинт
            if dict['step_2'] == '-': point = 2 # Если -, то 2 поинта
            if dict['step_2'] == '/': point = 3 # Если /, то 3 поинта
            if dict['step_2'] == '*': point = 4 # Если *, то 4 поинта
        except ZeroDivisionError: # Если деление на ноль
            result_eval = getattr(wd,f"wErrors_{lang}").a1 # Ошибка
            not_err = False # Это ошибка
            
            result = f'{getattr(wd,f"wErrors_{lang}").a3}{getattr(wd,f"wErrors_{lang}").a1}' # Ошибка: ...
        except (SyntaxError, NameError): # Если другие ошибки
            result_eval = getattr(wd,f"wErrors_{lang}").a2 # Ошибка
            not_err = False # Это ошибка
            
            result = f'{getattr(wd,f"wErrors_{lang}").a3}{getattr(wd,f"wErrors_{lang}").a2}' # Ошибка: ...
        
        img = None # Фотографии по умолчанию нет
        if not_err: # Если нет ошибки
            img = createImage(message.from_user,ops,str(result_eval)) # Создаём фото
            result = f'{getattr(wd,f"wMath_{lang}").a4}{result_eval}' # Ответ: ...
        
            sleep(1) # Ждём 1 секунду
            photo = FSInputFile(img,filename='test.jpg') # Получаем фото и для Telegram присваеваем временное название test.jpg
        
        await notion_post('Обращение',params={
                        'title':['text',str(message.message_id)],
                        'tg_id':['number',message.from_user.id],
                        'operands':['text',ops],
                        'status':['checkbox',not_err],
                        'result':['text',str(result_eval)],
                        'photo':['text',img.split('files/')[1] if img != None else ''],
                        'point':['number',point]
                    }) # Отправляем обращение в Notion
        
        num = await notion_get('Пользователи',str(message.from_user.id),['num_try']) # Получаем количество попыток пользователю
        await notion_update('Пользователи',str(message.from_user.id),{'num_try':['number', num['num_try'][1] + point]}) # Записываем новое значение, зависимо от поинтов
        
        session.add(Appeal(
            msg_id = message.message_id,
            tg_id = message.from_user.id,
            operands = ops,
            status = not_err,
            result = str(result_eval),
            photo = img.split('files/')[1] if img != None else '',
            point = point
        )) # Записываем обращение в БД
        await session.commit() # Отправляем запрос в БД
        
        get_user_num = await session.execute(Select(Users.num_try).where(Users.tg_id == message.from_user.id)) # Получаем количество попыток пользователю
        await session.execute(Update(Users).where(Users.tg_id == message.from_user.id).values(num_try= get_user_num.first()[0] + point)) # Записываем новое значение, зависимо от поинтов
        await session.commit() # Отправляем запрос в БД

    await state.clear() # Закрываем машину ожидания
    
    await message.answer(result,reply_markup=mBack.a1 if lang == 'ru' else mBack.a2) # Отвечаем в зависимости от ответа и языка
    if not_err: # Если не ошибка
        await message.bot.send_photo(message.chat.id,photo) # Отправляем фото