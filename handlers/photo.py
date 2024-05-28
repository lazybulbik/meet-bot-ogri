from aiogram import types, executor
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext

import menu
from loader import bot, dp, db

@dp.message_handler(lambda x: x.text == '◀ Назад', state='*')
async def back(msg: Message, state: FSMContext):
    await msg.answer('Твой профиль 👇', reply_markup=types.ReplyKeyboardRemove())

    photo, text, kb = menu.MainMenu().get_profile(msg.from_user.id)

    await msg.answer_photo(photo=photo, caption=text, reply_markup=kb, parse_mode='MARKDOWN')

    await state.reset_state(with_data=True)



@dp.message_handler(lambda x: x.text == '🔄 Заменить', state='photo_menu')
async def back(msg: Message, state: FSMContext):
    back = types.KeyboardButton("◀ Назад")
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True).add(back)

    await msg.answer('Отправь новое фото', reply_markup=kb)
    await state.set_state('photo_menu:replace')


@dp.message_handler(content_types=['photo'], state='photo_menu:replace')
async def replace(msg: Message, state: FSMContext):
    new_photo = [msg.photo[-1].file_id]

    db.update_data(table='users', data={'photo': ' '.join(new_photo)}, filters={'id': msg.from_user.id})

    user_data = db.get_data(table='users', filters={'id': msg.from_user.id})[0]

    count_photos = len(user_data['photo'].split())

    replace = types.KeyboardButton('🔄 Заменить')
    add = types.KeyboardButton('➕ Добавить')
    back = types.KeyboardButton("◀ Назад")

    kb = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)

    if count_photos != 1:
        btns = []

        for i in range(count_photos):
            btns.append(types.KeyboardButton(f'Удалить фото {i + 1}'))

        kb.add(*btns)

    kb.row(replace, add)
    kb.row(back)

    await msg.answer('Твои фото 👇', reply_markup=kb)

    media_group = []

    for photo in user_data['photo'].split():
        media_group.append(types.InputMediaPhoto(photo))

    await msg.answer_media_group(media=media_group)

    await state.set_state('photo_menu')


@dp.message_handler(lambda x: x.text == '➕ Добавить', state='photo_menu')
async def add(msg: Message, state: FSMContext):
    user_data = db.get_data(table='users', filters={'id': msg.from_user.id})[0]

    count_photos = len(user_data['photo'].split())

    if count_photos == 10:
        await msg.answer('Ты не можешь добавить больше фото!')
        return

    back = types.KeyboardButton("◀ Назад")
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True).add(back)

    await msg.answer('Отправь новое фото', reply_markup=kb)

    await state.set_state('photo_menu:add')


@dp.message_handler(content_types=['photo'], state='photo_menu:add')
async def add(msg: Message, state: FSMContext):
    user_data = db.get_data(table='users', filters={'id': msg.from_user.id})[0]

    new_photos = user_data['photo'].split()
    new_photos.append(msg.photo[-1].file_id)

    db.update_data(table='users', filters={'id': msg.from_user.id}, data={'photo': ' '.join(new_photos)})

    user_data = db.get_data(table='users', filters={'id': msg.from_user.id})[0]

    count_photos = len(user_data['photo'].split())

    replace = types.KeyboardButton('🔄 Заменить')
    add = types.KeyboardButton('➕ Добавить')
    back = types.KeyboardButton("◀ Назад")

    kb = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)

    if count_photos != 1:
        btns = []

        for i in range(count_photos):
            btns.append(types.KeyboardButton(f'Удалить фото {i + 1}'))

        kb.add(*btns)

    kb.row(replace, add)
    kb.row(back)

    await msg.answer('Твои фото 👇', reply_markup=kb)

    media_group = []

    for photo in user_data['photo'].split():
        media_group.append(types.InputMediaPhoto(photo))

    await msg.answer_media_group(media=media_group)

    await state.set_state('photo_menu')


@dp.message_handler(lambda x: 'Удалить фото' in x.text, state='photo_menu')
async def delete_photo(msg: Message, state: FSMContext):
    user_data = db.get_data(table='users', filters={'id': msg.from_user.id})[0]

    photo_index = int(msg.text.replace('Удалить фото ', ''))

    new_photos = user_data['photo'].split()
    new_photos.pop(photo_index - 1)

    db.update_data(table='users', data={'photo': ' '.join(new_photos)}, filters={'id': msg.from_user.id})

    user_data = db.get_data(table='users', filters={'id': msg.from_user.id})[0]

    count_photos = len(user_data['photo'].split())

    replace = types.KeyboardButton('🔄 Заменить')
    add = types.KeyboardButton('➕ Добавить')
    back = types.KeyboardButton("◀ Назад")

    kb = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)

    if count_photos != 1:
        btns = []

        for i in range(count_photos):
            btns.append(types.KeyboardButton(f'Удалить фото {i}'))

        kb.add(*btns)

    kb.row(replace, add)
    kb.row(back)

    await msg.answer('Твои фото 👇', reply_markup=kb)

    media_group = []

    for photo in user_data['photo'].split():
        media_group.append(types.InputMediaPhoto(photo))

    await msg.answer_media_group(media=media_group)

    await state.set_state('photo_menu')