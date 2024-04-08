from PIL import Image, ImageDraw, ImageFont

from datetime import datetime
from aiogram.types import User


def createImage(user:User, operands:str, result:str): # Функция для создания фото
    img = Image.new(mode='RGB', size=(200,200),
                    color = (153, 153, 255))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("Roboto-Regular.ttf",size=14,encoding='UTF-8')
    font2 = ImageFont.truetype("Roboto-Regular.ttf",size=20,encoding='UTF-8')
    draw.text((0,0), datetime.now().strftime("%d/%m/%Y, %H:%M:%S"),font=font)
    draw.text((0,14), f"От: {user.username if user.username != None else user.full_name}",font=font)
    draw.text((0,28),f"ОП: {operands}",font=font)

    draw.rectangle([(40,60),(150,130)])
    draw.text((85,80),result,font=font2)
    
    img.save(f'files/{user.id}_{datetime.now().strftime("%d%m%Y_%H%M%S")}.jpg',format='JPEG')
    return f'files/{user.id}_{datetime.now().strftime("%d%m%Y_%H%M%S")}.jpg'