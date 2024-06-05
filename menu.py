from aiogram import types

import utils
from questions import *
from loader import db

back = types.InlineKeyboardButton('◀ Назад', callback_data='back:no')
back_with_del = types.InlineKeyboardButton('◀ Назад', callback_data='back:del')
back_with_del_menu = types.InlineKeyboardMarkup().add(back_with_del)

back_in_register = types.InlineKeyboardButton('◀ Назад', callback_data='reg_back')
reg_back_menu = types.InlineKeyboardMarkup().add(back_in_register)


class Register:
    def get_gender_menu(self):
        male = types.InlineKeyboardButton('Мужcкой', callback_data='Мужской')
        female = types.InlineKeyboardButton('Женский', callback_data='Женский')

        return types.InlineKeyboardMarkup().row(male, female)

    def get_alcohol_menu(self):
        return types.InlineKeyboardMarkup().row(
            types.InlineKeyboardButton('Не пью', callback_data='Не пью'),
            types.InlineKeyboardButton('По праздникам', callback_data='По праздникам'),
        ).row(
            types.InlineKeyboardButton('По выходным', callback_data='По выходным'),
            types.InlineKeyboardButton('По вечерам', callback_data='По вечерам'),
        ).row(
            back_in_register
        )

    def get_smoking_menu(self):
        return types.InlineKeyboardMarkup().row(
            types.InlineKeyboardButton('Курю', callback_data='Курю'),
            types.InlineKeyboardButton('Не курю', callback_data='Не курю'),
        ).row(
            types.InlineKeyboardButton('Редко', callback_data='Редко'),
        ).row(
            back_in_register
        )

    def get_body_menu(self):
        return types.InlineKeyboardMarkup().row(
            types.InlineKeyboardButton('Худощавое', callback_data='Худощавое'),
            types.InlineKeyboardButton('Обычное', callback_data='Обычное'),
            types.InlineKeyboardButton('Плотное', callback_data='Плотное'),
        ).row(
            types.InlineKeyboardButton('Полное', callback_data='Полное'),
            types.InlineKeyboardButton('Стройное', callback_data='Стройное'),
            types.InlineKeyboardButton('Спортивное', callback_data='Спортивное'),
        ).row(
            types.InlineKeyboardButton('Атлетическое', callback_data='Атлетическое'),
        ).row(
            back_in_register
        )

    def get_childrens_menu(self):
        return types.InlineKeyboardMarkup().row(
            types.InlineKeyboardButton('Нет', callback_data='Нет'),
            types.InlineKeyboardButton('Есть', callback_data='Есть'),
        ).row(
            back_in_register
        )

    def get_partner_childrens_menu(self):
        return types.InlineKeyboardMarkup().row(
            types.InlineKeyboardButton('Без детей', callback_data='Без детей'),
            types.InlineKeyboardButton('С детьми', callback_data='С детьми'),
        ).row(
            types.InlineKeyboardButton('Не важно', callback_data='Не важно'),
        ).row(
            back_in_register
        )

    def test_1_menu(self, gender, quest):
        quest_data = test_1[gender][quest]
        text = quest_data['text']
        kb = types.InlineKeyboardMarkup()

        for btn in quest_data['btns']:
            if int(quest) == len(test_1[gender]) - 1:
                kb.add(types.InlineKeyboardButton(btn['text'], callback_data=f'test_1:finish:{btn["value"]}'))
            else:
                kb.add(types.InlineKeyboardButton(btn['text'], callback_data=f'test_1:{quest}:{btn["value"]}'))

        if quest == 0:
            kb.add(types.InlineKeyboardButton('⬅️ Назад', callback_data=f'test_1:reg_back'))
        else:
            kb.add(types.InlineKeyboardButton('⬅️ Назад', callback_data=f'test_1:{quest - 2}:0'))

        return text, kb

    def test_2_menu(self, gender, quest):
        text = test_2['text']
        kb = types.InlineKeyboardMarkup()

        for btn in test_2[gender][quest]:
            if int(quest) == len(test_2[gender]) - 1:
                kb.add(types.InlineKeyboardButton(btn['text'], callback_data=f'test_2:finish:{btn["value"]}'))
            else:
                kb.add(types.InlineKeyboardButton(btn['text'], callback_data=f'test_2:{quest}:{btn["value"]}'))

        if quest == 0:
            kb.add(types.InlineKeyboardButton('⬅️ Назад', callback_data=f'test_2:reg_back'))
        else:
            kb.add(types.InlineKeyboardButton('⬅️ Назад', callback_data=f'test_2:{quest - 2}:0'))                

        return text, kb

    def test_3_menu(self, select_btns):
        print(select_btns)
        text = '*Выбери 3 категории, регулярно занимающих твое свободное время*'

        btns = []

        for btn in test_3:
            btn_text = btn['text']
            value = btn['value']

            if btn_text in select_btns:
                btn_text = '🌟 ' + btn_text
                print(btn_text)

            btns.append(types.InlineKeyboardButton(btn_text, callback_data=f'test_3:{btn_text}:{value}'))

        if len(select_btns) == 3:
            done_btn = types.InlineKeyboardButton('✅ Подтвердить', callback_data=f'test_3:done')
        else:
            done_btn = types.InlineKeyboardButton('❌ Подтвердить пока нельзя', callback_data=f'Ignore')

        back_btn = types.InlineKeyboardButton('⬅️ Назад', callback_data=f'test_3:reg_back')
        kb = types.InlineKeyboardMarkup(row_width=3).add(*btns).row(done_btn).row(back_btn)

        return text, kb

    def test_4_menu(self, select_btns, quest):
        quest_data = test_4[quest]

        text = quest_data['text']

        kb = types.InlineKeyboardMarkup()

        if quest == 2:
            for btn in quest_data['btns']:
                btn_text = btn['text']
                value = btn['value']

                if value in select_btns:
                    index = select_btns.index(value)
                    number = {1: '1️⃣', 2: '2️⃣', 3: '3️⃣'}[index + 1]
                    btn_text = number + ' ' + btn_text

                kb.add(types.InlineKeyboardButton(btn_text, callback_data=f'test_4:{quest}:{value}'))

            return text, kb


        for btn in quest_data['btns']:
            if int(quest) == len(test_4) - 1:
                kb.add(types.InlineKeyboardButton(btn['text'], callback_data=f'test_4:finish:{btn["value"]}'))
            else:
                kb.add(types.InlineKeyboardButton(btn['text'], callback_data=f'test_4:{quest}:{btn["value"]}'))

        if quest == len(test_4) - 1:
            kb.add(types.InlineKeyboardButton('⬅️ Назад', callback_data=f'test_4:reg_back'))

        return text, kb

    def test_5_menu(self, select_btns, gender):
        text = 'Выберите указанные категории в порядке приоритетности (от важного к наименее важному)'

        btns = []

        for btn in test_5[gender]:
            btn_text = btn

            if btn_text in select_btns:
                index = select_btns.index(btn_text)

                number = {1: '1️⃣', 2: '2️⃣', 3: '3️⃣', 4: '4️⃣', 5: '5️⃣', 6: '6️⃣', 7: '7️⃣'}[index + 1]

                btn_text = number + ' ' + btn_text

            btns.append(types.InlineKeyboardButton(btn_text, callback_data=f'test_5:{btn}'))

        kb = types.InlineKeyboardMarkup(row_width=3).add(*btns).row(types.InlineKeyboardButton('⬅️ Назад', callback_data=f'test_5:reg_back'))

        return text, kb

    def interests_menu(self, select_btns, page):
        text = 'Укажи свои интересы и увлечения'
        data = interests[page]

        btns = []

        for btn in data:
            btn_text = btn

            if btn_text in select_btns:
                btn_text = '🌟 ' + btn_text

            btns.append(types.InlineKeyboardButton(btn_text, callback_data=f'interests:select:{btn}:{page}'))

        if page == 0:
            back_btn = types.InlineKeyboardButton('⬅️ Назад', callback_data=f'None_back')
        else:
            back_btn = types.InlineKeyboardButton('⬅️ Назад', callback_data=f'interests:move:{page - 1}')

        if page == len(interests) - 1:
            next_btn = types.InlineKeyboardButton('Вперед ➡️', callback_data=f'None')
        else:
            next_btn = types.InlineKeyboardButton('Вперед ➡️', callback_data=f'interests:move:{page + 1}')

        counter = types.InlineKeyboardButton(f'{page + 1} / {len(interests)}', callback_data=f'None_next')

        if len(select_btns) > 0:
            done = types.InlineKeyboardButton('✅ Завершить', callback_data=f'interests:done')
        else:
            done = types.InlineKeyboardButton('❌ Завершить пока нельзя', callback_data=f'None_done')

        empty = types.InlineKeyboardButton(' ', callback_data=f'None_empty')

        back = types.InlineKeyboardButton('◀ Назад', callback_data=f'interests:reg_back')
        kb = types.InlineKeyboardMarkup(row_width=3).add(*btns).row(empty).row(back_btn, counter, next_btn).row(done).row(back)

        return text, kb


class MainMenu():
    def get_profile(self, user_id):
        user_data = db.get_data(table='users', filters={'id': user_id})[0]

        city = user_data['city']
        height = user_data['height']
        age = user_data['age']
        partner_age = list(map(lambda x: x.strip(), user_data['partner_age'].split('-')))

        text = (f'🪪 *Ваш профиль* \n'
                f'----------------------------- \n'
                f"Город: {city} \n"
                f"Рост: {height} \n"
                f"Возраст: {age} \n\n"
                f"Возраст партнера: {partner_age[0]} - {partner_age[1]} лет")

        photo = user_data['photo'].split()[0]

        print(photo)

        edit = types.InlineKeyboardButton('⚙️ Редактировать личные данные', callback_data=f'edit_profile')
        revoke_anket = types.InlineKeyboardButton("📑 Перепройти анкетирование", callback_data='rework')
        photo_menu = types.InlineKeyboardButton('📷 Заменить/добавить фото', callback_data='photo_menu')

        kb = types.InlineKeyboardMarkup().add(edit).row(revoke_anket).row(photo_menu)

        return photo, text, kb

    def get_edit_menu(self):
        edit_name = types.InlineKeyboardButton('Редактировать Имя', callback_data=f'edit:name')
        edit_height = types.InlineKeyboardButton('Редактировать Рост', callback_data=f'edit:height')
        edit_age = types.InlineKeyboardButton('Редактировать Возраст', callback_data=f'edit:age')
        edit_partner_age = types.InlineKeyboardButton('Редактировать Возраст партнера', callback_data=f'edit:partner_age')
        edit_photo = types.InlineKeyboardButton('🖼 Редактировать Фото', callback_data=f'edit:photo')
        # rework = types.InlineKeyboardButton('🔄 Перепройти анкетирование', callback_data=f'rework')

        kb = types.InlineKeyboardMarkup()
        kb.row(edit_name, edit_height)
        kb.row(edit_age, edit_partner_age)
        kb.row(edit_photo)
        # kb.row(rework)
        kb.row(back)

        return kb

    def find_partner(self, user_id, partner_id=None, page=1):
        numbers = {1: '1️⃣', 2: '2️⃣', 3: '3️⃣', 4: '4️⃣', 5: '5️⃣', 6: '6️⃣', 7: '7️⃣', 8: '8️⃣', 9: '9️⃣', 10: '🔟'}

        if not partner_id:
            user_data = db.get_data(table='users', filters={'id': user_id})[0]

            pretendients = []


            for partner in db.get_data(table='users'):
                if partner['id'] != user_data['id'] and str(partner['id']) not in user_data['black_list']:
                    precent = utils.Comaparator(partner['id'], user_data['id']).compare()

                    if precent >= 0:
                        pretendients.append(partner['id'])

            if len(pretendients) == 0:
                return None, None, None
        else:
            pretendients = [partner_id]


        partner_data = db.get_data(table='users', filters={'id': pretendients[0]})[0]

        precent = utils.Comaparator(pretendients[0], user_id).compare()

        city = partner_data['city']
        age = partner_data['age']
        height = partner_data['height']
        alcohol = partner_data['alcohol']
        smoking = partner_data['smoking']
        body = partner_data['body']
        childrens = partner_data['childrens']

        priority = []

        for item in partner_data['test_5'].split(';'):
            number = partner_data['test_5'].split(';').index(item) + 1
            number = numbers[number]

            priority.append(f'{number} {item}')

        priority = '\n'.join(priority)

        interests = '\n '.join(partner_data['interests'].split(';'))

        text = (f'*🫂 Ваша совместимость: {precent}%* \n'
                f'----------------------------- \n'
                f'Город: {city} \n'
                f'Возраст: {age} \n'
                f'Рост: {height} \n'
                f'Дети: {childrens} \n\n'
                f'🍷Алоголь: {alcohol} \n'
                f'🚬Курение: {smoking} \n'
                f'🕴🏻Телосложение: {body} \n')

        prev = types.InlineKeyboardButton('<', callback_data=f'None')
        next = types.InlineKeyboardButton('>', callback_data=f'find:next:{partner_data["id"]}')
        decline = types.InlineKeyboardButton('❌', callback_data=f'find:decline:{partner_data["id"]}')
        ready = types.InlineKeyboardButton('❤️', callback_data=f'find:ready:{partner_data["id"]}')
        more_info = types.InlineKeyboardButton('Мнение Вазо', callback_data=f'find:more_info:{partner_data["id"]}')

        back = types.InlineKeyboardButton('Завершить просмотр', callback_data=f'back:del')

        kb = types.InlineKeyboardMarkup().row(prev, next).row(decline, ready).row(more_info)

        if len(partner_data['photo'].split()) >= 2:
            photo = partner_data['photo'].split()[page - 1]

        else:
            photo = partner_data['photo'].split()[0]

        if page == 2:
            text = f'Интересы: \n\n{interests}'

            prev.callback_data = f'find:prev:{partner_data["id"]}'
            next.callback_data = f'None'            
        
        return photo, text, kb


    def get_presents_menu(self, user_id, partner_id, page=1):
        pretendients = [partner_id]
        numbers = {1: '1️⃣', 2: '2️⃣', 3: '3️⃣', 4: '4️⃣', 5: '5️⃣', 6: '6️⃣', 7: '7️⃣', 8: '8️⃣', 9: '9️⃣', 10: '🔟'}

        partner_data = db.get_data(table='users', filters={'id': pretendients[0]})[0]

        precent = utils.Comaparator(pretendients[0], user_id).compare()

        city = partner_data['city']
        age = partner_data['age']
        height = partner_data['height']
        alcohol = partner_data['alcohol']
        smoking = partner_data['smoking']
        body = partner_data['body']
        childrens = partner_data['childrens']

        priority = []

        for item in partner_data['test_5'].split(';'):
            number = partner_data['test_5'].split(';').index(item) + 1
            number = numbers[number]

            priority.append(f'{number} {item}')

        priority = '\n'.join(priority)

        interests = ', '.join(partner_data['interests'].split(';'))

        text = (f'*Кто-то заинтересовался тобой👀* \n'
                f'----------------------------- \n'
                f'*🫂 Ваша совместимость: {precent}%* \n'
                f'----------------------------- \n'
                f'Город: {city} \n'
                f'Возраст: {age} \n'
                f'Рост: {height} \n'
                f'Дети: {childrens} \n\n'
                f'🍷Алоголь: {alcohol} \n'
                f'🚬Курение: {smoking} \n'
                f'🕴🏻Телосложение: {body} \n')

        prev = types.InlineKeyboardButton('<', callback_data=f'None')
        next = types.InlineKeyboardButton('>', callback_data=f'find:next:{partner_data["id"]}:present')
        decline = types.InlineKeyboardButton('❌', callback_data=f'answer:decline:{partner_data["id"]}')
        ready = types.InlineKeyboardButton('❤️', callback_data=f'answer:ready:{partner_data["id"]}')
        more_info = types.InlineKeyboardButton('Мнение Вазо', callback_data=f'find:more_info:{partner_data["id"]}:present')

        kb = types.InlineKeyboardMarkup().row(prev, next).row(decline, ready).row(more_info)

        if len(partner_data['photo'].split()) >= 2:
            photo = partner_data['photo'].split()[page - 1]

        else:
            photo = partner_data['photo'].split()[0]

        if page == 2:
            text = f'Интересы: \n\n{interests}'

            prev.callback_data = f'find:prev:{partner_data["id"]}:present'
            next.callback_data = f'None'            
        
        return photo, text, kb
    

    def get_match_text(self, user_id, partner_id, page=1):
        """
        Get match text for two users based on their IDs.
        :param user_id: int, the ID of the user
        :param partner_id: int, the ID of the partner user
        :return: tuple, containing the partner's photo and match text
        """
        pretendients = [partner_id]
        numbers = {1: '1️⃣', 2: '2️⃣', 3: '3️⃣', 4: '4️⃣', 5: '5️⃣', 6: '6️⃣', 7: '7️⃣', 8: '8️⃣', 9: '9️⃣', 10: '🔟'}

        partner_data = db.get_data(table='users', filters={'id': pretendients[0]})[0]

        precent = utils.Comaparator(pretendients[0], user_id).compare()

        city = partner_data['city']
        age = partner_data['age']
        height = partner_data['height']
        alcohol = partner_data['alcohol']
        smoking = partner_data['smoking']
        body = partner_data['body']
        childrens = partner_data['childrens']
        username = partner_data['username']

        priority = []

        for item in partner_data['test_5'].split(';'):
            number = partner_data['test_5'].split(';').index(item) + 1
            number = numbers[number]

            priority.append(f'{number} {item}')

        priority = '\n'.join(priority)

        interests = ', '.join(partner_data['interests'].split(';'))

        text = (f'*Вы и @{username} понравились друг-другу!* \n'
                f'----------------------------- \n'
                f'*🫂 Ваша совместимость: {precent}%* \n'
                f'----------------------------- \n'
                f'Город: {city} \n'
                f'Возраст: {age} \n'
                f'Рост: {height} \n'
                f'Дети: {childrens} \n\n'
                f'🍷Алоголь: {alcohol} \n'
                f'🚬Курение: {smoking} \n'
                f'🕴🏻Телосложение: {body} \n')
        
        prev = types.InlineKeyboardButton('<', callback_data=f'None')
        next = types.InlineKeyboardButton('>', callback_data=f'find:next:{partner_data["id"]}:match')

        more_info = types.InlineKeyboardButton('Мнение Вазо', callback_data=f'find:more_info:{partner_data["id"]}:match') 

        kb = types.InlineKeyboardMarkup().row(prev, next).row(more_info)       

        if len(partner_data['photo'].split()) >= 2:
            photo = partner_data['photo'].split()[page - 1]

        else:
            photo = partner_data['photo'].split()[0]

        if page == 2:
            text = f'Интересы: \n\n{interests}'

            prev.callback_data = f'find:prev:{partner_data["id"]}:match'
            next.callback_data = f'None'            
        
        return photo, text, kb        
    
    def get_more_info(self, user_id, partner_id):
        user_1_data = db.get_data(table='users', filters={'id': user_id})[0]
        user_2_data = db.get_data(table='users', filters={'id': partner_id})[0]
        precent = utils.Comaparator(partner_id, user_id).compare()

        gender = user_1_data['gender']
        main_user_data = user_1_data
        second_user_data = user_2_data

        if user_2_data['gender'] == 'Мужской':
            user_1_data, user_2_data = user_2_data, user_1_data

        plus = []
        minus = []

        if user_1_data['test_1'][0] == '2' and user_2_data['test_1'][0] == '1':
            if user_1_data['test_1'][3] == '1' and user_2_data['test_1'][3] == '1':
                if user_1_data['test_4'][0] == '1' and user_2_data['test_4'][0] == '1':
                    plus.append('   💘 Вы оба цените свободу и проповедуете отношения построенные на доверии.')

        if user_1_data['test_2'][1] == '1' and user_2_data['test_2'][1] == '1':
            if user_1_data['test_4'][5] == '2' and user_2_data['test_4'][5] == '2':
                plus.append('   💘 Недосказанность - это не про вас, вы оба предпочитаете выражать свои мысли прямо, избегая недопониманий.')

        if user_1_data['test_2'][1] == '2' and user_2_data['test_2'][1] == '2':
            if user_1_data['test_4'][6] == '1' and user_2_data['test_4'][6] == '1':
                plus.append('   💘 Вам будет легко подстроиться друг под друга, осталось поймать одну волну для общих мыслей и интересов.')

        if user_1_data['test_1'][2] == '1' and user_2_data['test_1'][2] == '1':
            if '3' in user_1_data['test_3'] and '3' in user_2_data['test_3']:
                plus.append('   💘 Для такого сапиосексуала трудно найти партнера, но я это сделал. Ваше знакомство может обернуться неприкрытым интересом, а увлекательные разговоры внести разнообразие в вашу жизнь.')

        if user_2_data['test_2'][7] == '1' and user_1_data['test_2'][7] == '1':
            if user_2_data['test_4'][1] == '1' and user_1_data['test_4'][1] == '1':
                if user_2_data['test_4'][2] == '2':
                    plus.append('   💘 У тебя есть потребность во внимании, у партнера - в его проявлении и заботе. Не забывай отвечать взаимностью')

        if user_2_data['test_1'][0] == '2' and user_1_data['test_1'][0] == '1':
            if user_2_data['test_4'][2] == '1' and user_1_data['test_2'][2] == '2':
                if user_2_data['test_2'][6] == '2':
                    plus.append('   💘 Ответственность и организованность партнера будут для тебя опорой. С такими качествами ты почувствуешь себя «как за каменной стеной».')

        if user_2_data['test_1'][0] == '2' and user_1_data['test_1'][0] == '1':
            if user_2_data['test_4'][5] == '1' and user_2_data['test_4'][5] == '1':
                if user_2_data['test_5'].split(';')[0] == 'Муж':
                    plus.append('   💘 Ваши взгляды очень похожи, вы одинаково придерживаетесь традиционных укладов семьи.')

        if user_1_data['test_2'][3] == '2' and user_2_data['test_2'][3] == '2':
            if user_1_data['test_2'][6] == '2' and user_2_data['test_2'][6] == '2':
                plus.append('   💘 Вы оба стараетесь оставаться продуктивными')

        if user_1_data['test_4'][1] == '2' and user_2_data['test_4'][1] == '2':
            plus.append('   💘 Конфетно-букетному периоду и преждевременной романтизации вы предпочитаете рациональную осмотрительность.')

        if 'Религия' in user_1_data['test_5'].split(';')[:3] and 'Религия' in user_2_data['test_5'].split(';')[:3]:
            plus.append('   💘 Партнер разделяет твои религиозные взгляды')

        if user_2_data['test_4'][1] == '1':
            if user_1_data['test_4'][1] == '1' or user_1_data['test_2'][7] == '1':
                if gender == 'Мужской':
                    plus.append('   💘 Твоя способность проявлять внимание к партнеру очень ценна для него.')
                else:
                    plus.append('   💘 Ты ценишь внимание, а партнер способен его завоевать. Не забывай благодарить его за это.')

        if user_2_data['test_4'][2] == '1':
            if (user_1_data['test_1'][0] == '1') and (user_1_data['test_2'][2] == '2' or user_1_data['test_2'][6] == '2' or user_1_data['test_2'][3] == '2'):
                if gender == 'Мужской':
                    plus.append('   💘 Партнер будет ценить твои лидерские качества, поэтому ты знаешь, как оправдать ее ожидания 😉')
                else:
                    plus.append('   💘 Знаю, как ты ценишь лидера, поэтому мои стрелы попали в нужное сердце.')

        if user_2_data['test_4'][2] == '3':
            if (user_1_data['test_5'].split(';')[0] == 'Жена') and (user_1_data['test_2'][1] == '2' or user_1_data['test_2'][2] == '2'):
                if gender == 'Мужской':
                    plus.append('   💘 Партнер будет ценить твою заботливость, поэтому ты знаешь, как оправдать ее ожидания 😉')
                else:
                    plus.append('   💘 Знаю, как ты ценишь заботу, поэтому мои стрелы попали в нужное сердце.')

        if user_2_data['test_4'][2] == '2':
            if user_1_data['test_2'][7] == '1':
                if gender == 'Мужской':
                    plus.append('   💘 Партнер будет ценить твою щедрость, поэтому ты знаешь, как оправдать ее ожидания 😉')
                else:
                    plus.append('   💘 Знаю, как ты ценишь щедрость, поэтому мои стрелы попали в нужное сердце.')

        # ---- 

        if user_2_data['test_1'][0] == '1' and user_1_data['test_1'][0] == '1':
            if user_2_data['test_4'][5] == '3' and user_2_data['test_4'][5] == '1':
                minus.append('  ⚠️ У вас разные взгляды на право главенства в семье. Каждый будет навязывать свою точку зрения, что затруднит принятие совместных решений.')

            if user_2_data['test_1'][3] == '1' and user_1_data['test_2'][4] == '1':
                if user_2_data['test_4'][0] == '1' and user_1_data['test_4'][0] == '1':
                    minus.append('  ⚠️ Чрезмерный контроль партнера может подавлять тебя, заранее определите обоюдные границы личной свободы, чтобы избежать ограничений в будущем.')

        if user_1_data['test_2'][1] == '1' and user_2_data['test_2'][1] == '2':
            if user_1_data['test_4'][6] == '2' and user_2_data['test_4'][6] == '1':
                minus.append('  ⚠️ Прямолинейность партнера может показаться тебе неуместной, а чувство безразличия - непрестанным. Изучайте и учите друг друга и, возможно, тогда чувство эмпатии и благодарности нивелируют ваши различия.')

        if user_1_data['test_1'][2] == '1' and user_2_data['test_1'][2] == '2':
            if ('3' in user_1_data['test_3'] and '3' not in user_2_data['test_3']) or ('3' in user_2_data['test_3'] and '3' not in user_1_data['test_3']):
                minus.append('  ⚠️ Из-за разности интересов ваш диалог рискует быстро исчерпать себя, попробуйте найти что то общее, а если не получится, возвращайтесь снова.')

        if user_2_data['test_2'][7] == '1' and user_1_data['test_2'][7] == '2':
            if user_2_data['test_4'][1] == '1' and user_1_data['test_4'][1] == '2':
                if user_2_data['test_4'][2] == '2':
                    minus.append('  ⚠️ Тебе важно чувствовать себя нужной, но не знаю, хватит ли внимания партнера расположить тебя к себе.. Это тебе и предстоит выяснить.')

        if user_1_data['test_2'][3] == '2' and user_2_data['test_2'][3] == '1':
            if user_1_data['test_2'][6] == '2' and user_2_data['test_2'][6] == '1':
                minus.append('  ⚠️ Пассивность партнера может показаться тебе обременительной')

        if 'Религия' in user_1_data['test_5'].split(';')[:4] or 'Религия' in user_2_data['test_5'].split(';')[:4]:
            if 'Религия' in user_1_data['test_5'].split(';')[-1] and 'Религия' in user_2_data['test_5'].split(';')[-1]:
                if 'Наука' in user_1_data['interests'] or 'Наука' in user_2_data['interests']:
                    minus.append('  ⚠️ Партнер может не разделять твоих религиозных предпочтений.')

        if user_1_data['test_1'][0] + user_2_data['test_1'][0] in ['12', '21']:
            if (user_1_data['test_1'][3] == '1' and user_2_data['test_2'][4] == '1') or (user_2_data['test_1'][3] == '1' and user_1_data['test_2'][4] == '1'):
                if user_1_data['test_4'][0] + user_2_data['test_4'][0] in ['12', '21']:
                    if gender == 'Мужской':
                        minus.append('  ⚠️ Чрезмерный контроль с твоей стороны может подавлять партнера, заранее определите обоюдные границы, чтобы их нарушение не приводило к конфликтам.')

                    else:
                        minus.append('  ⚠️ Чрезмерный контроль партнера может подавлять тебя, заранее определите обоюдные границы личной свободы, чтобы избежать ограничений в будущем.')

        if main_user_data['test_2'][1] == '1' and main_user_data['test_4'][6] == '2':
            if second_user_data['test_2'][1] == '2' and second_user_data['test_4'][6] == '1':
                minus.append('  ⚠️ Порой намеки и недосказанности партнера могут казаться непостижимой загадкой. Попробуйте найти баланс или дождись следующей пары.')

        if main_user_data['test_2'][1] == '2' and main_user_data['test_4'][6] == '1':
            if second_user_data['test_2'][1] == '1' and second_user_data['test_4'][6] == '2':
                minus.append('  ⚠️ Прямолинейность партнера может показаться для тебя неуместной. Попробуйте найти баланс или дождись следующей пары.')

        if user_2_data['test_4'][1] == '1':
            if user_1_data['test_2'][7] == '2' and user_2_data['test_4'][1] == '2':
                if gender == 'Мужской':
                    minus.append('  ⚠️ Партнеру может не хватать твоих ухаживаний.')
                else:
                    minus.append('  ⚠️ Тебе важно чувствовать себя нужной, но не знаю, хватит ли внимания партнера расположить тебя к себе.. Это тебе и предстоит выяснить.')

        if user_2_data['test_4'][2] == '1':
            if (user_1_data['test_1'][0] == '2') and (user_1_data['test_2'][2] == '1' or user_2_data['test_2'][6] == '1' or user_2_data['test_2'][3] == '1'):
                if gender == 'Мужской':
                    minus.append('  ⚠️ Партнер будет ждать от тебя решений, ответственности и инициативы.')
                else:
                    minus.append('  ⚠️ Знаю, как ты ценишь лидерство, но, вероятно, партнер не склонен к его проявлению.')

        if user_2_data['test_4'][3] == '3':
            answers_temp = [
                user_1_data['test_2'][1] == '1',
                user_1_data['test_2'][2] == '1',
                user_1_data['test_2'][6] == '1'
            ]
            if answers_temp.count(True) >= 2:
                if gender == 'Мужской':
                    minus.append('  ⚠️ Если ты забываешь проявлять заботу, то самое время прокачать свою чуткость или посмотреть на следующую анкету.')
                else:
                    minus.append('  ⚠️ Знаю, как ты ценишь заботу, но есть вероятность, что партнер не склонен к ее проявлению.')

        if user_1_data['test_1'][0] + user_2_data['test_1'][0] in ['21', '12']:
            if 'Карьера' in user_1_data['test_5'].split(';')[:3] or 'Карьера' in user_2_data['test_5'].split(';')[:3]:
                if user_1_data['test_4'][5] == '1' or user_2_data['test_4'][5] == '1':
                    if gender == 'Мужской':
                        minus.append('  ⚠️ У вас разные жизненные приоритеты, амбициозные планы партнера могут не оправдать ваших ожиданий.')
                    else:
                        minus.append('  ⚠️ У вас разные жизненные приоритеты, выясните, не помешает ли партнер вашей самореализации и планам.')

        if user_2_data['test_4'][2] == '2':
            if user_1_data['test_2'][7] == '2':
                if gender == 'Мужской':
                    minus.append('  ⚠️ Рассчет это хорошо, но не забывай об эмоциях партнера.')
                else:
                    minus.append('  ⚠️ Знаю, как ты ценишь щедрость, но, вероятно, партнер не склонен к ее проявлению.')


        plus_list_text = '\n'.join(plus)
        minus_list_text = '\n'.join(minus)

        plus_text = '' if not plus else f'Преимущества:\n{plus_list_text}'
        minus_text = '' if not minus else f'Недостатки:\n{minus_list_text}'
        comment = ''

        if len(minus) == 0 and len(plus) >= 2:
            comment = 'У вашей пары большой потенциал'
        
        elif len(minus) == 0 and len(plus) == 1:
            comment = 'Не вижу ни одного аргумента против, чтобы не порекомендовать вам друг друга'

        elif len(plus) == 0 and len(minus) == 0 and precent >= 70:
            comment = 'Не нашел ни одного аргумента против, чтобы не порекомендовать вам друг друга'

        elif (50 <= precent <= 69) or (50 <= precent <= 75 and len(minus) > len(plus)):
            comment = 'У вашей пары не самая высокая совместимость, но если стерпится, то может и слюбится'

        elif precent < 50:
            comment = 'Здесь даже мои стрелы бессильны💘, несите сразу пистолет🔫'
            
        
        text = f'{comment}\n\n{plus_text}\n\n{minus_text}'

        photo = types.InputFile('media/info.png')

        if text:
            return photo, text
        
        return photo, 'Мне не удалось найти плюсы или минусы'