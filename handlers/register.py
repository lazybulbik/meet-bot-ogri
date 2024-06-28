import asyncio

from aiogram import types, executor
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext

import menu
import utils
from loader import bot, dp, db

import questions


@dp.message_handler(state='register:name')
async def register(msg: Message, state: FSMContext):
    async with state.proxy() as state_data:
        state_data['name'] = msg.text.title()

    await msg.answer('Укажи свой пол:', reply_markup=menu.Register().get_gender_menu())
    await state.set_state('register:gender')


@dp.callback_query_handler(state='register:gender')
async def register_gender(call: CallbackQuery, state: FSMContext):
    if call.data == 'reg_back':
        await call.message.edit_text('Введи свое имя')
        await state.set_state('register:name')
        return

    async with state.proxy() as state_data:
        state_data['gender'] = call.data

    await call.message.edit_text(f'*{call.data}*', parse_mode='MARKDOWN')
    await call.message.answer('Укажите свой возраст:', reply_markup=menu.reg_back_menu)

    await state.set_state('register:age')


@dp.callback_query_handler(state='register:age') # helpful def
async def back(call: CallbackQuery, state: FSMContext):
    if call.data == 'reg_back':
        await call.message.edit_text('Укажи свой пол:', reply_markup=menu.Register().get_gender_menu())
        await state.set_state('register:gender')


@dp.message_handler(state='register:age')
async def register_age(msg: Message, state: FSMContext):
    if msg.text.isdigit():
        async with state.proxy() as state_data:
            state_data['age'] = msg.text

        await msg.answer('Укажи желаемый возраст партнера: \n\n'
                         '*Например: 18 - 30*', parse_mode='MARKDOWN', reply_markup=menu.reg_back_menu)

        await state.set_state('register:partner_age')
    else:
        await msg.answer('🔴 Введите число')


@dp.callback_query_handler(state='register:partner_age') # helpful def
async def back(call: CallbackQuery, state: FSMContext):
    if call.data == 'reg_back':
        await call.message.edit_text('Укажи свой возраст:', reply_markup=menu.reg_back_menu)
        await state.set_state('register:age')


@dp.message_handler(state='register:partner_age')
async def register_partner_age(msg: Message, state: FSMContext):
    if '-' in msg.text:
        if msg.text.split('-')[0].isdigit() and msg.text.split('-')[1].isdigit():
            if int(msg.text.split('-')[0]) <= int(msg.text.split('-')[1]):
                async with state.proxy() as state_data:
                    state_data['partner_age'] = msg.text

                    await msg.answer('Укажи свой рост в см:', reply_markup=menu.reg_back_menu)
                    await state.set_state('register:height')
            else:
                await msg.answer('🔴 Используй правильный формат ввода \n\n'
                                 '*Например: 18 - 30*', parse_mode='MARKDOWN')
        else:
            await msg.answer('🔴 Используй правильный формат ввода \n\n'
                             '*Например: 18 - 30*', parse_mode='MARKDOWN')
    else:
        await msg.answer('🔴 Используй правильный формат ввода \n\n'
                         '*Например: 18 - 30*', parse_mode='MARKDOWN')


@dp.callback_query_handler(state='register:height') # helpful def
async def back(call: CallbackQuery, state: FSMContext):
    if call.data == 'reg_back':
        await call.message.edit_text('Укажи желаемый возраст партнера: \n\n'
                    '*Например: 18 - 30*', parse_mode='MARKDOWN', reply_markup=menu.reg_back_menu)
        await state.set_state('register:partner_age')


@dp.message_handler(state='register:height')
async def register_partner_age(msg: Message, state: FSMContext):
    if msg.text.isdigit():
        async with state.proxy() as state_data:
            state_data['height'] = msg.text

        await msg.answer('Твое отношение к алкоголю?', reply_markup=menu.Register().get_alcohol_menu())
        await state.set_state('register:alcohol')
    else:
        await msg.answer('🔴 Введите число')


@dp.callback_query_handler(state='register:alcohol')
async def register_alcohol(call: CallbackQuery, state: FSMContext):
    if call.data == 'reg_back':
        await call.message.edit_text('Укажи свой рост в см:', reply_markup=menu.reg_back_menu)
        await state.set_state('register:height')
        return

    async with state.proxy() as state_data:
        state_data['alcohol'] = call.data

    await call.message.edit_text(call.message.text + f'\n\n*{call.data}*', parse_mode='MARKDOWN')
    await call.message.answer('Твое отношение к курению?', reply_markup=menu.Register().get_smoking_menu())
    await state.set_state('register:smoking')


@dp.callback_query_handler(state='register:smoking')
async def register_smoking(call: CallbackQuery, state: FSMContext):
    if call.data == 'reg_back':
        await call.message.edit_text('Твое отношение к алкоголю?', reply_markup=menu.Register().get_alcohol_menu())
        await state.set_state('register:alcohol')
        return
    
    async with state.proxy() as state_data:
        state_data['smoking'] = call.data

    await call.message.edit_text(call.message.text + f'\n\n*{call.data}*', parse_mode='MARKDOWN')
    await call.message.answer('Твое телосложение?', reply_markup=menu.Register().get_body_menu())
    await state.set_state('register:body')


@dp.callback_query_handler(state='register:body')
async def register_body(call: CallbackQuery, state: FSMContext):
    if call.data == 'reg_back':
        await call.message.edit_text('Твое отношение к курению?', reply_markup=menu.Register().get_smoking_menu())
        await state.set_state('register:smoking')
        return

    async with state.proxy() as state_data:
        state_data['body'] = call.data

    await call.message.edit_text(call.message.text + f'\n\n*{call.data}*', parse_mode='MARKDOWN')
    await call.message.answer('У тебя есть дети?', reply_markup=menu.Register().get_childrens_menu())
    await state.set_state('register:childrens')


@dp.callback_query_handler(state='register:childrens')
async def register_childrens(call: CallbackQuery, state: FSMContext):
    if call.data == 'reg_back':
        await call.message.edit_text('Твое телосложение?', reply_markup=menu.Register().get_body_menu())
        await state.set_state('register:body')
        return

    async with state.proxy() as state_data:
        state_data['childrens'] = call.data

    await call.message.edit_text(call.message.text + f'\n\n*{call.data}*', parse_mode='MARKDOWN')
    await call.message.answer('Предпочтения к детям партнера?',
                              reply_markup=menu.Register().get_partner_childrens_menu())
    await state.set_state('register:partner_childrens')


@dp.callback_query_handler(state='register:partner_childrens')
async def register_partner_childrens(call: CallbackQuery, state: FSMContext):
    if call.data == 'reg_back':
        await call.message.edit_text('У тебя есть дети?', reply_markup=menu.Register().get_childrens_menu())
        await state.set_state('register:childrens')
        return

    async with state.proxy() as state_data:
        state_data['partner_childrens'] = call.data

        await call.message.edit_text(call.message.text + f'\n\n*{call.data}*', parse_mode='MARKDOWN')

        await call.message.answer('Из какого ты города?', reply_markup=menu.reg_back_menu)
        await state.set_state('register:city')


@dp.callback_query_handler(state='register:city') # helpful def
async def back(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text('Предпочтения к детям партнера?',
                              reply_markup=menu.Register().get_partner_childrens_menu())
    await state.set_state('register:partner_childrens')


@dp.message_handler(state='register:city')
async def register(msg: Message, state: FSMContext):
    await state.update_data(city=msg.text)

    async with state.proxy() as state_data:
        print(state_data)

        if 'is_edit' in state_data:
            new_data = {
                'gender': state_data['gender'],
                'age': state_data['age'],
                'height': state_data['height'],
                'partner_age': state_data['partner_age'],
                'alcohol': state_data['alcohol'],
                'smoking': state_data['smoking'],
                'body': state_data['body'],
                'childrens': state_data['childrens'],
                'partner_childrens': state_data['partner_childrens'],
                'city': state_data['city']
            }

            db.update_data(table='users', data=new_data, filters={'id': msg.from_user.id})

            await msg.answer('✅ Данные успешно обновлены')
            await asyncio.sleep(1)
            photo, text, kb = menu.MainMenu().get_profile(msg.from_user.id)
            await msg.answer_photo(photo, text, reply_markup=kb, parse_mode='MARKDOWN')

            await state.reset_state(with_data=True)

            return

        text, kb = menu.Register().test_1_menu(state_data['gender'], 0)
        await msg.answer(text, reply_markup=kb, parse_mode='MARKDOWN')

        await state.set_state('register:test_1')
        state_data['test_1'] = ''


@dp.callback_query_handler(lambda x: x.data.startswith('test_1:'), state='register:test_1')
async def register_test_1(call: CallbackQuery, state: FSMContext):
    if call.data.endswith('reg_back'):
        await call.message.edit_text('Из какого ты города?', reply_markup=menu.reg_back_menu)
        await state.set_state('register:city')
        return
    
    quest_id = call.data.split(':')[1]
    btn_value = call.data.split(':')[2]

    async with state.proxy() as state_data:
        if btn_value == '0':
            state_data['test_1'] = state_data['test_1'][:-1]
        else:
            state_data['test_1'] += btn_value

        if quest_id == 'finish':
            text, kb = menu.Register().test_2_menu(state_data['gender'], 0)
            await call.message.edit_text(text, reply_markup=kb, parse_mode='MARKDOWN')
            state_data['test_2'] = ''
            await state.set_state('register:test_2')
            return

        text, kb = menu.Register().test_1_menu(state_data['gender'], int(quest_id) + 1)
        await call.message.edit_text(text, reply_markup=kb, parse_mode='MARKDOWN')

        print(state_data)


@dp.callback_query_handler(lambda x: x.data.startswith('test_2:'), state='register:test_2')
async def register_test_2(call: CallbackQuery, state: FSMContext):
    if call.data.endswith('reg_back'):
        async with state.proxy() as state_data:
            state_data['test_1'] = state_data['test_1'][:-1]
            quest_id = len(questions.test_1[state_data['gender']]) - 1

            text, kb = menu.Register().test_1_menu(state_data['gender'], quest_id)
            await call.message.edit_text(text, reply_markup=kb, parse_mode='MARKDOWN')
            await state.set_state('register:test_1')
            return

    quest_id = call.data.split(':')[1]
    btn_value = call.data.split(':')[2]

    async with state.proxy() as state_data:
        if btn_value == '0':
            state_data['test_2'] = state_data['test_2'][:-1]
        else:
            state_data['test_2'] += btn_value

        if quest_id == 'finish':
            state_data['select_btns'] = []
            state_data['test_3'] = []

            text, kb = menu.Register().test_3_menu(state_data['select_btns'])
            await call.message.edit_text(text, reply_markup=kb, parse_mode='MARKDOWN')

            await state.set_state('register:test_3')
            return

        text, kb = menu.Register().test_2_menu(state_data['gender'], int(quest_id) + 1)
        await call.message.edit_text(text, reply_markup=kb, parse_mode='MARKDOWN')

        print(state_data)


@dp.callback_query_handler(lambda x: x.data.startswith('test_3:'), state='register:test_3')
async def register_test_3(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as state_data:
        if call.data.endswith('reg_back'):
            state_data['test_2'] = state_data['test_2'][:-1]
            quest_id = len(questions.test_2[state_data['gender']]) - 1

            text, kb = menu.Register().test_2_menu(state_data['gender'], quest_id)
            await call.message.edit_text(text, reply_markup=kb, parse_mode='MARKDOWN')
            await state.set_state('register:test_2')
            return

        btn_text = call.data.split(':')[1]

        if btn_text == 'done':
            state_data['select_btns'] = []
            state_data['test_3'] = ''.join(list(set(state_data['test_3'])))

            text, kb = menu.Register().test_4_menu(state_data['select_btns'], 0)

            await call.message.edit_text(text, reply_markup=kb, parse_mode='MARKDOWN')
            state_data['test_4'] = ''
            await state.set_state('register:test_4')
            return

        btn_value = call.data.split(':')[2]

        if btn_text[2:] in state_data['select_btns']:
            print('remove')
            state_data['select_btns'].remove(btn_text[2:])
            state_data['test_3'].remove(btn_value)
            print(state_data)
        else:
            if len(state_data['select_btns']) == 3:
                await call.answer('Можно выбрать только 3 категории', show_alert=True)
                return
            state_data['select_btns'].append(btn_text)
            state_data['test_3'].append(btn_value)

        text, kb = menu.Register().test_3_menu(state_data['select_btns'])
        await call.message.edit_text(text, reply_markup=kb, parse_mode='MARKDOWN')

        print(state_data)


@dp.callback_query_handler(lambda x: x.data.startswith('test_4:'), state='register:test_4')
async def register_test_4(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as state_data:
        if call.data.endswith('reg_back'):
            state_data['test_3'] = []
            state_data['select_btns'] = []

            text, kb = menu.Register().test_3_menu(state_data['select_btns'])
            await call.message.edit_text(text, reply_markup=kb, parse_mode='MARKDOWN')
            await state.set_state('register:test_3')
            return

        quest = call.data.split(':')[1]
        value = call.data.split(':')[2]

        if quest == 'finish':
            text, kb = menu.Register().test_5_menu(state_data['select_btns'], state_data['gender'])
            await call.message.edit_text(text, reply_markup=kb, parse_mode='MARKDOWN')

            state_data['test_4'] += value
            state_data['test_5'] = ''
            await state.set_state('register:test_5')

            return

        if quest == '2':
            if value in state_data['select_btns']:
                state_data['select_btns'].remove(value)
            else:
                state_data['select_btns'].append(value)

            text, kb = menu.Register().test_4_menu(state_data['select_btns'], int(quest))
            await call.message.edit_text(text, reply_markup=kb, parse_mode='MARKDOWN')

            if len(state_data['select_btns']) == 3:
                text, kb = menu.Register().test_4_menu(state_data['select_btns'], int(quest) + 1)
                await call.message.edit_text(text, reply_markup=kb, parse_mode='MARKDOWN')

                state_data['test_4'] += ''.join(state_data['select_btns'])
                state_data['select_btns'] = []

            return

        if value == '0':
            state_data['test_4'] = state_data['test_4'][:-1]
        else:
            state_data['test_4'] += value

        if quest == '1' and state_data['gender'] == 'Мужской':
            state_data['test_4'] += ''.join(['0', '0', '0'])
            state_data['select_btns'] = []

            text, kb = menu.Register().test_4_menu(state_data['select_btns'], int(quest) + 2)
            await call.message.edit_text(text, reply_markup=kb, parse_mode='MARKDOWN')
            return

        text, kb = menu.Register().test_4_menu(state_data['select_btns'], int(quest) + 1)
        await call.message.edit_text(text, reply_markup=kb, parse_mode='MARKDOWN')

        print(state_data)


@dp.callback_query_handler(lambda x: x.data.startswith('test_5:'), state='register:test_5')
async def register_test_5(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as state_data:
        if call.data.endswith('reg_back'):
            state_data['test_4'] = state_data['test_4'][:-1]
            state_data['select_btns'] = []

            quest_id = len(questions.test_4) - 1

            text, kb = menu.Register().test_4_menu(state_data['select_btns'], quest_id)
            await call.message.edit_text(text, reply_markup=kb, parse_mode='MARKDOWN')
            await state.set_state('register:test_4')
            return

        btn_text = call.data.split(':')[1]

        if btn_text in state_data['select_btns']:
            state_data['select_btns'].remove(btn_text)
        else:
            state_data['select_btns'].append(btn_text)

        text, kb = menu.Register().test_5_menu(state_data['select_btns'], state_data['gender'])
        await call.message.edit_text(text, reply_markup=kb, parse_mode='MARKDOWN')

        if len(state_data['select_btns']) == 7:
            state_data['test_5'] = ';'.join(state_data['select_btns'])
            state_data['select_btns'] = []

            text, kb = menu.Register().interests_menu(state_data['select_btns'], 0)

            await call.message.edit_text(text, reply_markup=kb, parse_mode='MARKDOWN')
            await state.set_state('register:interests')


@dp.callback_query_handler(lambda x: x.data.startswith('interests:'), state='register:interests')
async def register_interests(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as state_data:
        if call.data.endswith('reg_back'):
            state_data['test_5'] = ''
            state_data['select_btns'] = []

            text, kb = menu.Register().test_5_menu(state_data['select_btns'], state_data['gender'])
            await call.message.edit_text(text, reply_markup=kb, parse_mode='MARKDOWN')
            await state.set_state('register:test_5')
            return
        action = call.data.split(':')[1]

        if action == 'select':
            page = int(call.data.split(':')[3])
            btn_text = call.data.split(':')[2]

            if btn_text in state_data['select_btns']:
                state_data['select_btns'].remove(btn_text)
            else:
                state_data['select_btns'].append(btn_text)

            text, kb = menu.Register().interests_menu(state_data['select_btns'], page)
            await call.message.edit_text(text, reply_markup=kb, parse_mode='MARKDOWN')

        elif action == 'move':
            dest_page = int(call.data.split(':')[2])

            text, kb = menu.Register().interests_menu(state_data['select_btns'], dest_page)
            await call.message.edit_text(text, reply_markup=kb, parse_mode='MARKDOWN')

        elif action == 'done':
            if 'is_rework' in state_data:
                new_data = {
                    'test_1': state_data['test_1'],
                    'test_2': state_data['test_2'],
                    'test_3': state_data['test_3'],
                    'test_4': state_data['test_4'],
                    'test_5': state_data['test_5'],
                    'interests': ';'.join(state_data['select_btns']),
                }

                db.update_data(table='users', data=new_data, filters={'id': call.from_user.id})

                await call.message.edit_text('Тестирование завершено 🙂')
                await asyncio.sleep(1)
                photo, text, kb = menu.MainMenu().get_profile(call.from_user.id)

                await bot.send_photo(call.from_user.id, photo=photo, caption=text, reply_markup=kb, parse_mode='MARKDOWN')
                await state.reset_state(with_data=True)

                return

            text = 'Тестирование завершено 😉 \n\n Для активации профиля отправь фото 🖼'

            state_data['interests'] = ';'.join(state_data['select_btns'])

            await call.message.edit_text(text)
            await state.set_state('register:photo')


@dp.message_handler(state='register:photo', content_types=['photo'])
async def register_photo(message: Message, state: FSMContext):
    async with state.proxy() as state_data:
        state_data['photo'] = message.photo[-1].file_id

        print(state_data)

        write_data = {
            'id': message.from_user.id,
            'gender': state_data['gender'],
            'age': state_data['age'],
            'height': state_data['height'],
            'partner_age': state_data['partner_age'],
            'alcohol': state_data['alcohol'],
            'smoking': state_data['smoking'],
            'body': state_data['body'],
            'childrens': state_data['childrens'],
            'partner_childrens': state_data['partner_childrens'],
            'test_1': state_data['test_1'],
            'test_2': state_data['test_2'],
            'test_3': state_data['test_3'],
            'test_4': state_data['test_4'],
            'test_5': state_data['test_5'],
            'interests': state_data['interests'],
            'photo': state_data['photo'],
            'black_list': '',
            'username': message.from_user.username,
            'city': state_data['city'],
            'is_del': False
        }

        db.new_write(table='users', data=write_data)

        if 'with_user' in state_data:
            photo, text, kb = menu.MainMenu().find_partner(message.from_user.id, partner_id=message.get_args())

            await message.answer_photo(photo=photo, caption=text, parse_mode='MARKDOWN')

            await message.answer('Чтобы посмотреть свой профиль введи /profile')
            return

        await message.answer('Профиль успешно активирован 😎 \n\nЧтобы перейти в него введите /profile')
        await asyncio.sleep(2)
        
        # -----
        # выдача дружеской ссылки
        username = await bot.get_me()
        username = username.username

        link = f'https://t.me/{username}?start={message.from_user.id}'

        text = (f'🔗 Поделись ссылкой с другом, ведь именно с ним кто-то ждет свою идеальную совместимость! 🧩 \n\n'
                f'{link}')
        await message.answer(text)
        await asyncio.sleep(5.5)

        # -----

        photo, text, kb = menu.MainMenu().find_partner(message.from_user.id)
        if photo:
            await message.answer_photo(photo=photo, caption=text, reply_markup=kb, parse_mode='MARKDOWN')

        await state.reset_state(with_data=True)

        # -------------------------

        for user in utils.find_all_compatible_users(message.from_user.id):
            photo, text, kb = menu.MainMenu().find_partner(user)

            await bot.send_photo(user, photo=photo, caption=text, reply_markup=kb, parse_mode='MARKDOWN')