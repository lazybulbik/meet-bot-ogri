import asyncio

from aiogram import types, executor
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext

import menu
import utils
from loader import bot, dp, db


@dp.callback_query_handler(lambda call: call.data.startswith('edit:'))
async def callback(call: CallbackQuery, state: FSMContext):
    print(call.data)

    if call.data == 'edit:name':
        await call.message.delete()
        await call.message.answer('Введи новое имя', reply_markup=menu.back_with_del_menu)
        await state.set_state('edit:name')

    elif call.data == 'edit:height':
        await call.message.delete()
        await call.message.answer('Введи новый рост в см', reply_markup=menu.back_with_del_menu)
        await state.set_state('edit:height')

    elif call.data == 'edit:age':
        await call.message.delete()
        await call.message.answer('Введи новый возраст', reply_markup=menu.back_with_del_menu)
        await state.set_state('edit:age')

    elif call.data == 'edit:partner_age':
        await call.message.delete()
        await call.message.answer('Введи новый возраст партнера \n\n*Например: 18 - 30*', reply_markup=menu.back_with_del_menu, parse_mode='MARKDOWN')
        await state.set_state('edit:partner_age')

    elif call.data == 'edit:photo':
        await call.message.delete()
        await call.message.answer('Пришли новое фото', reply_markup=menu.back_with_del_menu)
        await state.set_state('edit:photo')


@dp.message_handler(state='edit:name')
async def edit_name(msg: Message, state: FSMContext):
    db.update_data(data={'name': msg.text.title()}, filters={'id': msg.from_user.id}, table='users')

    photo, text, kb = menu.MainMenu().get_profile(msg.from_user.id)
    await msg.answer_photo(photo=photo, caption=text, reply_markup=kb, parse_mode='MARKDOWN')

    await state.reset_state(with_data=True)


@dp.message_handler(state='edit:height')
async def edit_height(msg: Message, state: FSMContext):
    if msg.text.isdigit():
        db.update_data(data={'height': msg.text}, filters={'id': msg.from_user.id}, table='users')

        photo, text, kb = menu.MainMenu().get_profile(msg.from_user.id)
        await msg.answer_photo(photo=photo, caption=text, reply_markup=kb, parse_mode='MARKDOWN')

        await state.reset_state(with_data=True)
    else:
        await msg.answer('🔴 Введите число')


@dp.message_handler(state='edit:age')
async def edit_age(msg: Message, state: FSMContext):
    if msg.text.isdigit():
        db.update_data(data={'age': msg.text}, filters={'id': msg.from_user.id}, table='users')

        photo, text, kb = menu.MainMenu().get_profile(msg.from_user.id)
        await msg.answer_photo(photo=photo, caption=text, reply_markup=kb, parse_mode='MARKDOWN')

        await state.reset_state(with_data=True)
    else:
        await msg.answer('🔴 Введите число')


@dp.message_handler(state='edit:partner_age')
async def edit_partner_age(msg: Message, state: FSMContext):
    if '-' in msg.text:
        if msg.text.split('-')[0].isdigit() and msg.text.split('-')[1].isdigit():
            if int(msg.text.split('-')[0]) <= int(msg.text.split('-')[1]):
                db.update_data(data={'partner_age': msg.text}, filters={'id': msg.from_user.id}, table='users')

                photo, text, kb = menu.MainMenu().get_profile(msg.from_user.id)
                await msg.answer_photo(photo=photo, caption=text, reply_markup=kb, parse_mode='MARKDOWN')

                await state.reset_state(with_data=True)
            else:
                await msg.answer('🔴 Используй правильный формат ввода \n\n'
                                 '*Например: 18 - 30*', parse_mode='MARKDOWN', reply_markup=menu.back_with_del_menu)
        else:
            await msg.answer('🔴 Используй правильный формат ввода \n\n'
                             '*Например: 18 - 30*', parse_mode='MARKDOWN', reply_markup=menu.back_with_del_menu)
    else:
        await msg.answer('🔴 Используй правильный формат ввода \n\n'
                         '*Например: 18 - 30*', parse_mode='MARKDOWN', reply_markup=menu.back_with_del_menu)


@dp.message_handler(state='edit:photo', content_types=['photo'])
async def edit_photo(msg: Message, state: FSMContext):
    db.update_data(data={'photo': msg.photo[-1].file_id}, filters={'id': msg.from_user.id}, table='users')

    photo, text, kb = menu.MainMenu().get_profile(msg.from_user.id)
    await msg.answer_photo(photo=photo, caption=text, reply_markup=kb, parse_mode='MARKDOWN')

    await state.reset_state(with_data=True)
