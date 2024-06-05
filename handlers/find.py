import asyncio

from aiogram import types, executor
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext

import menu
import utils
from loader import bot, dp, db


@dp.callback_query_handler(lambda call: call.data.startswith('find:'))
async def callback(call: CallbackQuery, state: FSMContext):
    print(call.data)
    partner_id = call.data.split(':')[2]

    db.update_data(table='users', data={'username': call.from_user.username}, filters={'id': call.from_user.id})

    if call.data.startswith('find:ready:'):
        partner_id = call.data.split(':')[2]

        photo, text, kb = menu.MainMenu().get_presents_menu(partner_id, call.from_user.id)
        await bot.send_photo(partner_id, photo=photo, caption=text, reply_markup=kb, parse_mode='MARKDOWN')

        user_data = db.get_data(table='users', filters={'id': call.from_user.id})[0]

        blacklist = user_data['black_list'].split()
        blacklist.append(partner_id)
        db.update_data(table='users', data={'black_list': ' '.join(blacklist)}, filters={'id': user_data['id']})

        photo, text, kb = menu.MainMenu().find_partner(call.from_user.id)

        if not photo:
            await call.answer('😉 Ты посмотрел все анкеты. Возращайся попозже', show_alert=True)
            await call.message.delete()
            photo, text, kb = menu.MainMenu().get_profile(call.from_user.id)
            await bot.send_photo(call.from_user.id, photo=photo, caption=text, reply_markup=kb, parse_mode='MARKDOWN')
            return

        await call.message.delete()
        await call.message.answer_photo(photo=photo, caption=text, parse_mode='MARKDOWN', reply_markup=kb)

    elif call.data.startswith('find:decline'):
        partner_id = call.data.split(':')[2]

        blacklist = db.get_data(table='users', filters={'id': partner_id})[0]['black_list'].split()
        blacklist.append(str(call.from_user.id))
        db.update_data(data={'black_list': ' '.join(blacklist)}, filters={'id': partner_id}, table='users')

        user_data = db.get_data(table='users', filters={'id': call.from_user.id})[0]

        blacklist = user_data['black_list'].split()
        blacklist.append(partner_id)
        db.update_data(table='users', data={'black_list': ' '.join(blacklist)}, filters={'id': user_data['id']})

        photo, text, kb = menu.MainMenu().find_partner(call.from_user.id)

        if not photo:
            await call.answer('😉 Ты посмотрел все анкеты. Возращайся попозже', show_alert=True)
            await call.message.delete()
            photo, text, kb = menu.MainMenu().get_profile(call.from_user.id)
            await bot.send_photo(call.from_user.id, photo=photo, caption=text, reply_markup=kb, parse_mode='MARKDOWN')
            return

        await call.message.delete()
        await call.message.answer_photo(photo=photo, caption=text, parse_mode='MARKDOWN', reply_markup=kb)

    elif call.data.startswith('find:more_info'):
        partner_id = call.data.split(':')[2]
        photo, text = menu.MainMenu().get_more_info(call.from_user.id, partner_id)

        if call.data.split(':')[-1] == 'present':
            prev = types.InlineKeyboardButton('<', callback_data=f'None')
            next = types.InlineKeyboardButton('>', callback_data=f'find:next:{partner_id}:present')            
            decline = types.InlineKeyboardButton('❌', callback_data=f'answer:decline:{partner_id}')
            ready = types.InlineKeyboardButton('❤️', callback_data=f'answer:ready:{partner_id}')
            more_info = types.InlineKeyboardButton('< К профилю', callback_data=f'find:back_profile:{partner_id}:present') 

            kb = types.InlineKeyboardMarkup().row(prev, next).row(decline, ready).row(more_info) 

        elif call.data.split(':')[-1] == 'match':
            prev = types.InlineKeyboardButton('<', callback_data=f'None')
            next = types.InlineKeyboardButton('>', callback_data=f'find:next:{partner_id}:match')
            more_info = types.InlineKeyboardButton('< К профилю', callback_data=f'find:back_profile:{partner_id}:match')

            kb = types.InlineKeyboardMarkup().row(prev, next).row(more_info)

        else:
            prev = types.InlineKeyboardButton('<', callback_data=f'None')
            next = types.InlineKeyboardButton('>', callback_data=f'find:next:{partner_id}')            
            decline = types.InlineKeyboardButton('❌', callback_data=f'find:decline:{partner_id}')
            ready = types.InlineKeyboardButton('❤️', callback_data=f'find:ready:{partner_id}')
            more_info = types.InlineKeyboardButton('< К профилю', callback_data=f'find:back_profile:{partner_id}')             

            kb = types.InlineKeyboardMarkup().row(prev, next).row(decline, ready).row(more_info) 

        await call.message.edit_media(media=types.InputMediaPhoto(photo, caption=text), reply_markup=kb)

    elif call.data.startswith('find:next'):
        partner_id = call.data.split(':')[2]

        if call.data.split(':')[-1] == 'present':
            photo, text, kb = menu.MainMenu().get_presents_menu(call.from_user.id, partner_id, page=2)
        elif call.data.split(':')[-1] == 'match':
            photo, text, kb = menu.MainMenu().get_match_text(call.from_user.id, partner_id, page=2)
        else:
            photo, text, kb = menu.MainMenu().find_partner(call.from_user.id, partner_id=partner_id, page=2)

        await call.message.edit_media(media=types.InputMediaPhoto(photo, caption=text), reply_markup=kb)

    elif call.data.startswith('find:prev'):
        partner_id = call.data.split(':')[2]

        if call.data.split(':')[-1] == 'present':
            photo, text, kb = menu.MainMenu().get_presents_menu(call.from_user.id, partner_id, page=1)
        elif call.data.split(':')[-1] == 'match':
            photo, text, kb = menu.MainMenu().get_match_text(call.from_user.id, partner_id, page=1)
        else:
            photo, text, kb = menu.MainMenu().find_partner(call.from_user.id, partner_id=partner_id, page=1)

        await call.message.edit_media(media=types.InputMediaPhoto(photo, caption=text, parse_mode='MARKDOWN'), reply_markup=kb)        

    elif call.data.startswith('find:back_profile'):
        partner_id = call.data.split(':')[2]

        if call.data.split(':')[-1] == 'present':
            photo, text, kb = menu.MainMenu().get_presents_menu(call.from_user.id, partner_id)
        elif call.data.split(':')[-1] == 'match':
            photo, text, kb = menu.MainMenu().get_match_text(call.from_user.id, partner_id)
        else:
            photo, text, kb = menu.MainMenu().find_partner(call.from_user.id, partner_id=partner_id)

        await call.message.edit_media(media=types.InputMediaPhoto(photo, caption=text, parse_mode='MARKDOWN'), reply_markup=kb)

@dp.callback_query_handler(lambda call: call.data.startswith('answer:'))
async def callback(call: CallbackQuery, state: FSMContext):
    print(call.data)

    db.update_data(table='users', data={'username': call.from_user.username}, filters={'id': call.from_user.id})

    if call.data.startswith('answer:ready'):
        partner_id = call.data.split(':')[2]

        user_data = db.get_data(table='users', filters={'id': call.from_user.id})[0]
        partner_data = db.get_data(table='users', filters={'id': partner_id})[0]

        blacklist = user_data['black_list'].split()
        blacklist.append(partner_id)
        db.update_data(table='users', data={'black_list': ' '.join(blacklist)}, filters={'id': user_data['id']})

        photo, text, kb = menu.MainMenu().get_match_text(user_id=call.from_user.id, partner_id=partner_id)
        await call.message.delete()
        await call.message.answer_photo(photo, caption=text, parse_mode='MARKDOWN', reply_markup=kb)

        photo, text, kb = menu.MainMenu().get_match_text(user_id=partner_id, partner_id=call.from_user.id)
        await bot.send_photo(partner_id, photo=photo, caption=text, parse_mode='MARKDOWN', reply_markup=kb)

    elif call.data.startswith('answer:decline'):
        partner_id = call.data.split(':')[2]

        user_data = db.get_data(table='users', filters={'id': call.from_user.id})[0]

        blacklist = user_data['black_list'].split()
        blacklist.append(partner_id)
        db.update_data(table='users', data={'black_list': ' '.join(blacklist)}, filters={'id': user_data['id']})

        await call.message.delete()