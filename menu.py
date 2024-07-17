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


class MainMenu:
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


            for partner in db.get_data(table='users', filters={'is_del': 0}):
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

        
    def get_main_and_secondary_user(self, user_1_data, user_2_data):
        if user_2_data['gender'] == 'Мужской':
            return user_2_data, user_1_data
        return user_1_data, user_2_data            
    
    def get_more_info(self, user_id, partner_id):
        main_user_data = db.get_data(table='users', filters={'id': user_id})[0]
        second_user_data = db.get_data(table='users', filters={'id': partner_id})[0]
        precent = utils.Comaparator(partner_id, user_id).compare()

        gender = main_user_data['gender']
        user_1_data, user_2_data = self.get_main_and_secondary_user(main_user_data, second_user_data)

        plus = []
        minus = []

        print(user_1_data['gender'], user_2_data['gender'])

        if user_1_data['test_1'][3] == '1' and user_2_data['test_1'][3] == '1':
            if user_1_data['test_4'][0] == '1' and user_2_data['test_4'][0] == '1':
                plus.append('   💘 Вы оба цените свободу и проповедуете отношения построенные на доверии.')

        if user_1_data['test_2'][1] == '1' and user_2_data['test_2'][1] == '1':
            if user_1_data['test_4'][5] == '2' and user_2_data['test_4'][5] == '2':
                plus.append('   💘 Недосказанность - это не про вас, вы оба предпочитаете выражать свои мысли прямо, избегая недопониманий.')

        if user_1_data['test_2'][1] == '2' and user_2_data['test_2'][1] == '2':
            if user_1_data['test_4'][6] == '1' and user_2_data['test_4'][6] == '1':
                plus.append('   💘 Вы оба обладаете развитой чуткостью и эмпатией, что поможет вам вовремя понимать потребности и чувства друг друга.')

        if main_user_data['test_1'][2] == '1' and second_user_data['test_1'][2] == '1':
            if ('3' in main_user_data['test_3']) and ('3' in second_user_data['test_3']):
                plus.append('   💘 Ваше знакомство может обернуться неприкрытым интересом, а увлекательные диалоги внести разнообразие в вашу жизнь.')

        if user_2_data['test_1'][0] == '2' and user_1_data['test_1'][0] == '1':
            if user_2_data['test_4'][5] == '1' and user_2_data['test_4'][5] == '1':
                if user_2_data['test_5'].split(';')[0] == 'Муж':
                    plus.append('   💘 Ваши взгляды очень похожи, вы одинаково придерживаетесь традиционных укладов семьи.')

        if user_1_data['test_4'][1] == '2' and user_2_data['test_4'][1] == '2':
            plus.append('   💘  У вас рациональный подход к отношениям, вы оба не торопитесь проявлять излишний романтиз.')

        if 'Религия' in user_1_data['test_5'].split(';')[:3] and 'Религия' in user_2_data['test_5'].split(';')[:3]:
            plus.append('   💘 Партнер разделяет твои религиозные взгляды')

        if user_2_data['test_4'][1] == '1':
            if user_1_data['test_4'][1] == '1':
                if gender == 'Мужской':
                    plus.append('   💘 Для партнера ценна твоя способность проявлять внимание и романтичность.')
                else:
                    plus.append('   💘 Ты ценишь внимание, а партнер способен его завоевать. Не забывай благодарить его за это.')

        # if user_2_data['test_4'][2] == '3':
        #     if (user_1_data['test_5'].split(';')[0] == 'Жена') and (user_1_data['test_2'][1] == '2' or user_1_data['test_2'][2] == '2'):
        #         if gender == 'Мужской':
        #             plus.append('   💘 Партнер будет ценить твою заботливость, поэтому ты знаешь, как оправдать ее ожидания 😉')
        #         else:
        #             plus.append('   💘 Знаю, как ты ценишь заботу, поэтому мои стрелы попали в нужное сердце.')

        if user_2_data['test_4'][2] == '2':
            if user_1_data['test_2'][7] == '1':
                if gender == 'Мужской':
                    plus.append('   💘 Партнер будет ценить твою щедрость, поэтому ты знаешь, как оправдать ее ожидания 😉')
                else:
                    plus.append('   💘 Знаю, как ты ценишь щедрость, поэтому мои стрелы попали в нужное сердце.')

        if main_user_data['test_2'][3] == '2' and second_user_data['test_2'][3] == '2':
            if (main_user_data['test_2'][6] == '2' and second_user_data['test_2'][6] == '2') or (main_user_data['test_4'][7] == '1' and second_user_data['test_4'][7] == '1'):
                plus.append('   💘 Вы оба предпочитаете оставаться активными.')

        if user_1_data['test_2'][5] == '2' and user_2_data['test_2'][5] == '2':
            plus.append('   💘 Ваша неконфликтность будет способствовать стабильным и размеренным отношениям.')

        if main_user_data['test_1'][1] == '2' and main_user_data['test_4'][0] == '1':
            if second_user_data['test_1'][1] == '2' and second_user_data['test_4'][0] == '1':
                plus.append('   💘 Вы оба идете в ногу со временем и имеете прогрессивный взгляд на многие вещи.')

        if user_2_data['test_1'][1] == '1' and user_2_data['test_4'][0] == '2':
            if user_1_data['test_1'][1] == '1' and user_1_data['test_4'][0] == '2':
                plus.append('   💘 Вы консервативны, современным ценностям предпочитаете традиционные взгляды.')
        
        first = any([a_1 == a_2 for a_1, a_2 in zip(user_1_data['test_4'], user_2_data['test_4'])])
        second = user_2_data['test_4'][5] == '1' and user_1_data['test_4'][5] in ['1', '2', '3', '4']
        third = user_1_data['test_4'][5] == '2' and user_2_data['test_4'][5] in ['2', '3', '4']
        fourth = user_1_data['test_4'][5] == '3' and user_2_data['test_4'][5] in ['3', '4']
        if first or second or third or fourth:
            plus.append('   💘 Вы с легкостью распределите семейные обязанности и создадите комфортные условия для совместного быта.')

        if user_2_data['test_2'][3] == '1' and user_2_data['test_4'][7] == '2':
            if user_1_data['test_2'][3] == '1' and user_1_data['test_4'][7] == '2':
                plus.append('   💘 Вы оба любите продолжительный сон и короткие слова, например, такие как “лень”.')

        if main_user_data['test_2'][3] == '1' and main_user_data['test_2'][6] == '1':
            if second_user_data['test_2'][3] == '1' and second_user_data['test_2'][6] == '1':
                plus.append('   💘 Внезапным активностям вы скорее предпочтете уютный вечер в кругу близких.')

        if (user_2_data['test_1'][0] == '2' and user_1_data['test_1'][0] == '1') and (first or second or third or fourth):
            plus.append('   💘 У вас одинаковые взгляды на право главенства в семье, вы без труда можете принимать совместные решения и находить компромиссы.')

        if (user_2_data['test_1'][0] == '1' and user_1_data['test_1'][0] == '2') and (first or second or third or fourth):
            plus.append('   💘 У вас одинаковые взгляды на право главенства в семье, принимая совместные решения, вам важно учесть желания партнера, поэтому в любой ситуации вы без труда найдете компромисс.')

        # ---- 

        if user_2_data['test_1'][0] == '1' and user_1_data['test_1'][0] == '1':
            if user_2_data['test_4'][5] == '3' and user_1_data['test_4'][5] == '1':
                minus.append('  ⚠️ У вас разные взгляды на право главенства в семье. Каждый будет навязывать свою точку зрения, что затруднит принятие совместных решений.')

        if user_1_data['test_1'][2] == '1' and user_2_data['test_1'][2] == '2':
            if ('3' in user_1_data['test_3'] and '3' not in user_2_data['test_3']) or ('3' in user_2_data['test_3'] and '3' not in user_1_data['test_3']):
                minus.append('  ⚠️ Вероятно, из-за разности интересов ваш диалог рискует быстро себя исчерпать.')

        # if user_2_data['test_2'][7] == '1' and user_1_data['test_2'][7] == '2':
        #     if user_2_data['test_4'][1] == '1' and user_1_data['test_4'][1] == '2':
        #         if user_2_data['test_4'][2] == '2':
        #             if gender == 'Мужской':
        #                 minus.append('  ⚠️ Партнеру может не хватать твоих ухаживаний.')
        #             else:
        #                 minus.append('  ⚠️ Тебе важно чувствовать себя нужной, но не знаю, хватит ли внимания партнера расположить тебя к себе.. Это тебе и предстоит выяснить.')

        if main_user_data['test_2'][3] == '2' and second_user_data['test_2'][3] == '1':
            if (main_user_data['test_2'][6] == '2' and second_user_data['test_2'][6] == '1') or (main_user_data['test_4'][7] == '1' and second_user_data['test_4'][7] == '2'):
                minus.append('  ⚠️ Пассивность партнера может показаться тебе обременительной.')

        if second_user_data['test_2'][3] == '2' and main_user_data['test_2'][3] == '1':
            if (second_user_data['test_2'][6] == '2' and main_user_data['test_2'][6] == '1') or (second_user_data['test_4'][7] == '1' and main_user_data['test_4'][7] == '2'):
                minus.append('  ⚠️ Твоя пассивность может показаться обременительной для партнера.')                

        if 'Религия' in user_1_data['test_5'].split(';')[:4] or 'Религия' in user_2_data['test_5'].split(';')[:4]:
            if 'Религия' in user_1_data['test_5'].split(';')[-1] and 'Религия' in user_2_data['test_5'].split(';')[-1]:
                if 'Наука' in user_1_data['interests'] or 'Наука' in user_2_data['interests']:
                    minus.append('  ⚠️ Партнер может не разделять твоих религиозных предпочтений.')

        if main_user_data['test_1'][3] == '1' and main_user_data['test_4'][0] == '1':
            if (second_user_data['test_1'][3] == '2') and (second_user_data['test_4'][0] == '2' or second_user_data['test_2'][4] == '1'):
                minus.append('  ⚠️ Чрезмерный контроль партнера может подавлять тебя, заранее определите обоюдные границы личной свободы, чтобы избежать ограничений в будущем.')

        if (main_user_data['test_1'][3] == 2) and (main_user_data['test_4'][0] == '2' or main_user_data['test_2'][4] == '1'):
            if second_user_data['test_1'][3] == '1' and second_user_data['test_4'][0] == '1':
                minus.append('  ⚠️ Чрезмерный контроль с твоей стороны может подавлять партнера, заранее определите обоюдные границы, чтобы их нарушение не приводило к конфликтам.')                

        if main_user_data['test_2'][1] == '1' and main_user_data['test_4'][6] == '2':
            if second_user_data['test_2'][1] == '2' and second_user_data['test_4'][6] == '1':
                minus.append('  ⚠️ Намеки и недосказанности партнера могут казаться тебе непостижимой загадкой.')

        if main_user_data['test_2'][1] == '2' and main_user_data['test_4'][6] == '1':
            if second_user_data['test_2'][1] == '1' and second_user_data['test_4'][6] == '2':
                minus.append('  ⚠️ Прямолинейность партнера может показаться тебе неуместной.')

        if user_2_data['test_4'][1] == '1':
            if user_1_data['test_2'][7] == '2' and user_1_data['test_4'][1] == '2':
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

        if user_2_data['test_1'][0] == '1' and 'Карьера' in user_2_data['test_5'].split(';')[:3]:
            if user_1_data['test_1'][0] == '1' and user_1_data['test_4'][5] == '1' and user_1_data['test_1'][3] == '2':
                if gender == 'Мужской':
                    minus.append('  ⚠️ Ваши жизненные приоритеты могут отличаться, а амбициозные планы партнера — не совпадать с твоими ожиданиями.')
                else:
                    minus.append('  ⚠️ У вас разные жизненные приоритеты, выясни, не помешает ли партнер твоей самореализации и планам.')

        if user_2_data['test_4'][2] == '2':
            if user_1_data['test_2'][7] == '2':
                if gender == 'Мужской':
                    minus.append('  ⚠️ Рассчет это хорошо, но не забывай об эмоциях партнера.')
                else:
                    minus.append('  ⚠️ Знаю, как ты ценишь щедрость, но, вероятно, партнер не склонен к ее проявлению.')

        if user_1_data['test_2'][5] == '1' and user_2_data['test_2'][5] == '1':
            minus.append('  ⚠️ Обоюдная вспыльчивость может стать источником ваших конфликтов.')

        if user_2_data['test_4'][5] == '3' and user_1_data['test_4'][5] == '1':
            minus.append('  ⚠️ Вероятно, совместный быт станет для вас источником взаимных претензий.')

        if main_user_data['test_1'][1] == '2' and main_user_data['test_4'][0] == '1':
            if second_user_data['test_1'][1] == '2' and second_user_data['test_4'][0] == '2':
                minus.append('  ⚠️ Консервативность партнера может показаться тебе избыточной.')

        if main_user_data['test_1'][1] == '1' and main_user_data['test_4'][0] == '2':
            if second_user_data['test_1'][1] == '1' and second_user_data['test_4'][0] == '1':
                minus.append('  ⚠️ Взгляды партнера могут показаться тебе слишком прогрессивными.')

        if user_2_data['test_1'][0] == '1' and user_2_data['test_4'][5] == '2':
            if user_1_data['test_1'][0] == '1' and user_1_data['test_4'][5] == '1':
                minus.append('  ⚠️ Принятие совместных решений и поиск компромиссов могут стоить вам немалых усилий.')

        if main_user_data['test_2'][0] == '1' and main_user_data['test_2'][1] == '2':
            if second_user_data['test_2'][0] == '2':
                minus.append('  ⚠️ Партнер быстро забывает обиды, тебе это дается сложнее, поэтому при случае ты можешь напомнить о них. Попробуйте обсудить причину конфликта и сделать все возможное, чтобы его последствия не повлияли на взаимоотношения.')

        if second_user_data['test_2'][0] == '1' and second_user_data['test_2'][1] == '2':
            if main_user_data['test_2'][0] == '2':
                minus.append('  ⚠️ Ты быстро забываешь обиды, партнеру это дается сложнее, поэтому при случае он может напомнить о них. Причиной может быть как нерешенный конфликт, который нужно обсудить, так и манипуляция, которую стоит избегать.')           


        plus_list_text = '\n'.join(plus)
        minus_list_text = '\n'.join(minus)

        plus_text = '' if not plus else f'{plus_list_text}'
        minus_text = '' if not minus else f'{minus_list_text}'
        comment = ''

        if precent >= 90:
            comment = 'Кажется, вы созданы друг для друга.'

        elif 80 <= precent <= 89:
            comment = 'У вашей пары большой потенциал.'
        
        elif 70 <= precent <= 79 and len(minus) == 0 and len(plus) >= 1:
            comment = 'Не вижу ни одного аргумента против, чтобы не порекомендовать вам друг друга.'

        elif 70 <= precent <= 79 and len(minus) >= 1:
            comment = 'У вашей пары есть потенциал, но не форсируйте события, придется притереться.'

        elif 60 <= precent <= 69:
            comment = 'У вашей пары не самая высокая совместимость, но я и не таких сводил.'

        elif 50 <= precent <= 59:
            comment = 'Не лучшая совместимость, но не отчаивайся, бывает и хуже.'
        
        elif precent < 50:
            comment = 'Здесь даже мои стрелы бессильны 💘, несите сразу пистолет 🔫'
            
        
        text = f'{comment}\n\n{plus_text}\n\n{minus_text}'

        photo = types.InputFile('media/info.png')

        if text:
            return photo, text
        
        return photo, 'Мне не удалось найти плюсы или минусы'


class Admin:
    def __init__(self) -> None:
        self.back = types.InlineKeyboardButton('< Назад в меню', callback_data='admin:menu')
        self.back_menu = types.InlineKeyboardMarkup().add(self.back)

    def get_menu(self):
        users_count = len(db.get_data(table='users'))
        male_count = len(db.get_data(table='users', filters={'gender': 'Мужской'}))
        female_count = len(db.get_data(table='users', filters={'gender': 'Женский'}))

        average_age = int(sum([user['age'] for user in db.get_data(table='users')]) / users_count)

        text = (f'📊 Статистика 📊 \n\n'
                f'Всего пользователей в боте: {users_count}\n'
                f'  - Мужчин: {male_count}\n'
                f'  - Женщин: {female_count}\n\n'
                f'Средний возраст пользователей: {average_age}')
        
        btn_1 = types.InlineKeyboardButton('💬 Рассылка', callback_data='admin:mailing')
        btn_2 = types.InlineKeyboardButton('👤 Пользователи', callback_data='admin:users:1')

        kb = types.InlineKeyboardMarkup().row(btn_1).row(btn_2)

        return text, kb
    
    def get_users(self, page=1):
        page = int(page)
        users_per_page = 10
        all_users = db.get_data(table='users')
        total_users = len(all_users)
        total_pages = (total_users + users_per_page - 1) // users_per_page
        
        # Calculate the starting and ending indices for the current page
        start_idx = (page - 1) * users_per_page
        end_idx = start_idx + users_per_page
        current_users = all_users[start_idx:end_idx]
        
        kb = types.InlineKeyboardMarkup()        

        # Create the text for the current page
        text = '👤 Список пользователей 👤\n\n'
        for user in current_users:
            username = user['username'] if user['username'] else 'Инкогнито'
            btn_text = f'{username} ({user["id"]})'
            kb.row(types.InlineKeyboardButton(btn_text, callback_data=f'admin:view_user:{user["id"]}'))
        
        # Create the pagination buttons
        if page > 1:
            prev = types.InlineKeyboardButton('<', callback_data=f'admin:users:{page-1}')
        else:
            prev = types.InlineKeyboardButton('<', callback_data=f'asjh')

        count = types.InlineKeyboardButton(f'{page}/{total_pages}', callback_data='none')
        
        if page < total_pages:
            next = types.InlineKeyboardButton('>', callback_data=f'admin:users:{page+1}')
        else:
            next = types.InlineKeyboardButton('>', callback_data=f'kejfhjndsm')

        kb.row(prev, count, next)
        
        # # Add a back button to return to the main menu
        kb.row(types.InlineKeyboardButton('🔙 Назад в меню', callback_data='admin:menu'))
        
        return text, kb
    
    def view_user(self, user_id):
        user_data = db.get_data(table='users', filters={'id': user_id})[0]

        watches = len(user_data['black_list'].split())

        text = (f'👤 {user_data["username"]} ({user_data["id"]}) \n\n'
                f'Пол: {user_data["gender"]}\n'
                f'Возраст: {user_data["age"]}\n'
                f'Рост: {user_data["height"]}\n'
                f'Отношение к алкоголю: {user_data["alcohol"]} \n\n'
                f'Просмотрено акнет: {watches}')

        if user_data['is_del']:
            btn = types.InlineKeyboardButton('✅ Разблокировать', callback_data=f'admin:unblock:{user_data["id"]}')
        else:
            btn = types.InlineKeyboardButton('🚫 Заблокировать', callback_data=f'admin:block:{user_data["id"]}')

        btn_2 = types.InlineKeyboardButton('< Назад', callback_data='admin:users:1')

        kb = types.InlineKeyboardMarkup().row(btn).row(btn_2)

        return text, kb