from aiogram import types, executor
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext

import menu
import utils
from loader import bot, dp, db

from handlers import register, edit, find, photo


@dp.message_handler(commands=['start', 'profile'], state='*')
async def start(msg: Message, state: FSMContext):
    if utils.is_register(msg.from_user.id):
        if msg.get_args():
            photo, text, kb = menu.MainMenu().find_partner(msg.from_user.id, partner_id=msg.get_args())

            await msg.answer_photo(photo=photo, caption=text, parse_mffode='MARKDOWN')
            return

        photo, text, kb = menu.MainMenu().get_profile(msg.from_user.id)

        await bot.send_photo(msg.from_user.id, photo=photo, caption=text, reply_markup=kb, parse_mode='MARKDOWN')
        await state.reset_state(with_data=True)
        pass
    else:
        if msg.get_args():
            await state.update_data(with_user=msg.get_args())
            parent_username = db.get_data(table='users', filters={'id': msg.get_args()})[0]['username']

            await msg.answer(
                f'👋 Привет! Чтобы проверить свою совместимость с @{parent_username} необходимо пройти тест \n\n'
                f'Выбери свой пол:', reply_markup=menu.Register().get_gender_menu())
        else:
            await msg.answer('👋 Привет! Мы с тобой не знакомы \n\n'
                             'Выбери свой пол:', reply_markup=menu.Register().get_gender_menu())

        await state.set_state('register:gender')


@dp.message_handler(commands=['partner'])
async def p(msg: Message, state: FSMContext):
    photo, text, kb = menu.MainMenu().find_partner(msg.from_user.id)
    if photo:
        await msg.answer_photo(photo=photo, caption=text, reply_markup=kb, parse_mode='MARKDOWN')
        

@dp.message_handler(commands=['clear_history'])
async def c(msg: Message, state: FSMContext):
    db.update_data(table='users', data={'black_list': ''}, filters={'id': msg.from_user.id})

    for user in db.get_data(table='users'):
        l = user['black_list'].split()
        if msg.from_user.id in l:
            l.remove(msg.from_user.id)
            db.update_data(table='users', data={'black_list': ' '.join(l)}, filters={'id': user['id']})

    photo, text, kb = menu.MainMenu().find_partner(msg.from_user.id)
    if photo:
        await msg.answer_photo(photo=photo, caption=text, reply_markup=kb, parse_mode='MARKDOWN')    


@dp.message_handler(commands=['answers'])
async def answers(msg: Message):
    utils.get_users_answers()

    await msg.answer_document(types.InputFile('answers.txt'))


@dp.message_handler(commands=['link'], state='*')
async def link(msg: Message, state: FSMContext):
    username = await bot.get_me()
    username = username.username

    link = f'https://t.me/{username}?start={msg.from_user.id}'

    text = (f'Отправь ссылку ниже своим друзьям 👇 \n\n'
            f'`🧩 Проверь совместимость со мной здесь: {link}`')

    await msg.answer(text, parse_mode='MARKDOWN')
    await state.reset_state(with_data=True)


@dp.message_handler(commands=['restart'], state='*')
async def restart(msg: Message, state: FSMContext):
    db.delete(table='users', filters={'id': msg.from_user.id})

    await msg.answer('✅ Данные успешно удалены \n\n'
                     'Давай познакомимся заново, укажи свой пол 😉', reply_markup=menu.Register().get_gender_menu())

    await state.reset_state(with_data=True)

    await state.set_state('register:gender')


@dp.callback_query_handler(state='*')
async def callback(call: CallbackQuery, state: FSMContext):
    print(call.data)

    if call.data == 'edit_profile':
        await call.message.delete()
        await state.update_data(is_edit=True)

        await call.message.answer("Укажи свой пол:", reply_markup=menu.Register().get_gender_menu())
        await state.set_state('register:gender')

    elif call.data.startswith('back'):
        photo, text, kb = menu.MainMenu().get_profile(call.from_user.id)

        if call.data.split(':')[1] == 'del':
            await call.message.delete()
            await bot.send_photo(call.from_user.id, photo=photo, caption=text, reply_markup=kb, parse_mode='MARKDOWN')
        else:
            await call.message.edit_media(types.InputMediaPhoto(media=photo, caption=text, parse_mode='MARKDOWN'),
                                          reply_markup=kb)

        await state.reset_state(with_data=True)

    elif call.data == 'find_partner':
        photo, text, kb = menu.MainMenu().find_partner(call.from_user.id)

        if not photo:
            await call.answer('😔 Мне не удалось подобрать партнера. Попробуй позже', show_alert=True)
            return

        await call.message.delete()
        await bot.send_photo(call.from_user.id, photo=photo, caption=text, reply_markup=kb, parse_mode='MARKDOWN')

    elif call.data == 'rework':
        await state.update_data(is_rework=True)
        user_gender = db.get_data(table='users', filters={'id': call.from_user.id})[0]['gender']

        await call.message.delete()

        text, kb = menu.Register().test_1_menu(gender=user_gender, quest=0)

        await call.message.answer(text, reply_markup=kb, parse_mode='MARKDOWN')

        await state.update_data(test_1='', gender=user_gender)
        await state.set_state('register:test_1')

    elif call.data == 'photo_menu':
        user_data = db.get_data(table='users', filters={'id': call.from_user.id})[0]

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

        await call.message.answer('Твои фото 👇', reply_markup=kb)

        media_group = []

        for photo in user_data['photo'].split():
            media_group.append(types.InputMediaPhoto(photo))

        await call.message.answer_media_group(media=media_group)

        await state.set_state('photo_menu')


executor.start_polling(dp)
