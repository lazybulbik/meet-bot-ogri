import asyncio

from aiogram import types, executor
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext

import menu
import utils
from loader import bot, dp, db

import questions


@dp.callback_query_handler(lambda x: x.data.startswith('admin:'), state='*')
async def admin(call: CallbackQuery, state: FSMContext):
    print(call.data)
    request = call.data.split(':')[1]

    if request == 'users':
        page = call.data.split(':')[2]

        text, kb = menu.Admin().get_users(page)

        await call.message.edit_text(text, reply_markup=kb)

    elif request == 'menu':
        text, kb = menu.Admin().get_menu()

        await call.message.edit_text(text, reply_markup=kb)

        await state.reset_state()

    elif request == 'view_user':
        user_id = call.data.split(':')[2]

        text, kb = menu.Admin().view_user(user_id=user_id)

        await call.message.edit_text(text, reply_markup=kb)

    elif request == 'block':
        user_id = call.data.split(':')[2]

        db.update_data(table='users', filters={'id': user_id}, data={'is_del': True})

        await call.answer('Пользователь заблокирован')

        text, kb = menu.Admin().view_user(user_id)
        await call.message.edit_text(text, reply_markup=kb)

    elif request == 'unblock':
        user_id = call.data.split(':')[2]

        db.update_data(table='users', filters={'id': user_id}, data={'is_del': False})

        await call.answer('Пользователь разблокирован')

        text, kb = menu.Admin().view_user(user_id)
        await call.message.edit_text(text, reply_markup=kb)      

    elif request == 'mailing':
        await call.message.edit_text('Введите сообщение для рассылки', reply_markup=menu.Admin().back_menu)

        await state.set_state('admin:mailing')


@dp.message_handler(state='admin:mailing', content_types=['photo', 'text', 'video'])
async def mailing(msg: Message, state: FSMContext):
    tech = await msg.answer('🔄 Рассылка сообщения')

    for user in db.get_data(table='users'):
        try:
            if msg.photo:
                await bot.send_photo(user['id'], photo=msg.photo[-1].file_id, caption=msg.caption, caption_entities=msg.caption_entities)
            elif msg.video:
                await bot.send_video(user['id'], video=msg.video, caption=msg.caption, caption_entities=msg.caption_entities)
            else:
                await bot.send_message(user['id'], msg.text, entities=msg.entities)
        except:
            pass

        await asyncio.sleep(1.5)

    await tech.edit_text('✅ Рассылка завершена')
    await asyncio.sleep(1.5)
    text, kb = menu.Admin().get_menu()
    await tech.edit_text(text, reply_markup=kb)

    await state.reset_state()
    