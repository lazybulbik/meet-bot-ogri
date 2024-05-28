from loader import db
from questions import *


def is_register(user_id):
    all_users_id = [user['id'] for user in db.get_data(table='users')]

    return user_id in all_users_id


class Comaparator:
    def __init__(self, user_id_1, user_2_id):
        self.user_1_data = db.get_data(filters={'id': user_id_1}, table='users')[0]
        self.user_2_data = db.get_data(filters={'id': user_2_id}, table='users')[0]

        self.precent = 85

    def compare(self):
        self.precent += self.check_gender()
        # print(self.precent, 'гендер')
        self.precent += self.check_age()
        # print(self.precent, 'возраст')
        self.precent += self.check_childrens()
        # print(self.precent, 'детей')
        self.precent += self.check_test_1()
        # print(self.precent, 'тест 1')
        self.precent += self.check_test_2()
        # print(self.precent, 'тест 2')
        self.precent += self.check_test_3()
        # print(self.precent, 'тест 3')
        self.precent += self.check_test_4()
        # print(self.precent, 'тест 4')
        self.precent += self.additional_check()
        # print(self.precent, 'доп проверка')

        print(self.precent)

        if self.precent >= 500:
            return -999

        if self.precent <= 0:
            return 0

        return self.precent

    def check_gender(self):
        if self.user_1_data['gender'] == self.user_2_data['gender']:
            return 999
        else:
            return 0
        
    def check_childrens(self):
        child_1 = self.user_1_data['childrens']
        child_2 = self.user_2_data['childrens']
        p_child_1 = self.user_1_data['partner_childrens']
        p_child_2 = self.user_2_data['partner_childrens']

        if child_1 == 'Нет' and p_child_2 in ['Не важно', "Без детей"]:
            if child_2 == 'Нет' and p_child_1 in ['Не важно', "Без детей"]:
                return 0
        if child_1 == 'Есть' and p_child_2 in ['Не важно', "С детьми"]:
            if child_2 == 'Есть' and p_child_1 in ['Не важно', "С детьми"]:
                return 0
        return 999

    def check_age(self):
        user_1_age = self.user_1_data['age']
        user_2_age = self.user_2_data['age']

        user_1_partner_age = list(map(int, self.user_1_data['partner_age'].split('-')))
        user_2_partner_age = list(map(int, self.user_2_data['partner_age'].split('-')))

        if user_2_partner_age[0] <= user_1_age <= user_2_partner_age[1]:
            if user_1_partner_age[0] <= user_2_age <= user_1_partner_age[1]:
                return 0

        return 999

    def check_test_1(self):
        local_precent = 0

        if self.user_1_data['gender'] == 'Мужской':
            result_1 = self.user_1_data['test_1']
            result_2 = self.user_2_data['test_1']
        else:
            result_1 = self.user_2_data['test_1']
            result_2 = self.user_1_data['test_1']

        grade_data = [
            {
                '11': 0,
                '12': 0,
                '22': 0,
                '21': 0
            },
            {
                '11': 0,
                '22': 10,
                '12': -3,
                '21': -3
            },
            {
                '11': 0,
                '22': 0,
                '12': -5,
                '21': -5
            },
            {
                '11': 4,
                '22': 0,
                '12': -3,
                '21': -3
            }
        ]
        count = 0
        for char_1, char_2 in zip(result_1, result_2):
            local_precent += grade_data[count][char_1 + char_2]
            count += 1

        return local_precent

    def check_test_2(self):
        local_precent = 0

        if self.user_1_data['gender'] == 'Мужской':
            result_1 = self.user_1_data['test_2']
            result_2 = self.user_2_data['test_2']
        else:
            result_1 = self.user_2_data['test_2']
            result_2 = self.user_1_data['test_2']

        count = 1
        for chr_1, chr_2 in zip(result_1, result_2):
            if count == 6:
                if chr_1 == '1' and chr_2 == '1':
                    local_precent -= 1
                else:
                    local_precent += 0
            else:
                if chr_1 == chr_2:
                    local_precent += 0
                else:
                    local_precent -= 1

            count += 1

        return local_precent

    def check_test_3(self):
        local_precent = 0

        if self.user_1_data['gender'] == 'Мужской':
            result_1 = self.user_1_data['test_3']
            result_2 = self.user_2_data['test_3']
        else:
            result_1 = self.user_2_data['test_3']
            result_2 = self.user_1_data['test_3']

        for chr in result_1:
            if chr in result_2:
                local_precent += 7

        return local_precent

    def check_test_4(self):
        local_precent = 0

        if self.user_1_data['gender'] == 'Мужской':
            data_1 = self.user_1_data
            data_2 = self.user_2_data
        else:
            data_1 = self.user_2_data
            data_2 = self.user_1_data

        count = 1
        for chr_1, chr_2 in zip(data_1['test_4'], data_2['test_4']):
            if count == 4:
                chr_1 = data_1['test_4'][5]
                chr_2 = data_2['test_4'][5]
                data_sheet = {
                    '11': 0, '12': 0, '22': 0, '23': 0, '33': 0, '44': 0, '13': -5, '14': -5, '24': -5, '34': -5,
                    '11': 0, '21': 0, '22': 0, '32': 0, '33': 0, '44': 0, '31': -5, '41': -5, '42': -5, '43': -5
                }

                local_precent += data_sheet[chr_1 + chr_2]

            if count == 6:
                chr_1 = data_1['test_4'][7]
                chr_2 = data_2['test_4'][7]

                if chr_1 == chr_2:
                    local_precent += 0
                else:
                    local_precent -= 2

            if count == 3:
                if (data_2['test_4'][2] == '1' and data_2['test_1'][0] == '2') and (
                        data_1['test_1'][0] == '1' and data_1['test_2'][2] == '2' and data_1['test_2'][6] == '2'):
                    local_precent += 5

                if (data_2['test_4'][2] == '2' and data_2['test_2'][7] == '1' and data_2['test_4'][1] == '1') and (
                        data_1['test_2'][7] == '2' and data_1['test_4'][1] == '2'):
                    local_precent -= 10

                if data_2['test_4'][2] == '3' and (data_1['test_2'][1] == '2' and data_1['test_2'][2] == '2'):
                    local_precent += 5

            else:
                if chr_1 == chr_2:
                    local_precent += 0
                else:
                    local_precent -= 3

            count += 1

        return local_precent

    def additional_check(self):
        local_precent = 0

        if self.user_1_data['gender'] == 'Мужской':
            data_1 = self.user_1_data
            data_2 = self.user_2_data
        else:
            data_1 = self.user_2_data
            data_2 = self.user_1_data

        if (data_2['test_1'][0] == '1' and data_2['test_4'][5] == '3') and (
                data_1['test_1'][0] == '1' and data_1['test_4'][5] == '1'):
            local_precent -= 15

        if (data_2['test_1'][0] == '1' and data_2['test_1'][3] == '1' and data_2['test_4'][0] == '1') and (
                data_1['test_1'][0] == '2' and data_1['test_1'][3] == '1' and data_1['test_4'][0] == '1'):
            local_precent += 8

        if (data_2['test_1'][0] == '1' and data_2['test_1'][3] == '1' and data_2['test_4'][0] == '1') and (
                data_1['test_1'][0] == '1' and data_1['test_2'][4] == '1' and data_1['test_4'][0] == '1'):
            local_precent -= 10

        if (data_2['test_2'][1] == '1' and data_2['test_4'][6] == '2') and data_1['test_2'][1] == '1' and \
                data_1['test_4'][6] == '2':
            local_precent += 5

        if data_2['test_2'][1] == '2' and data_2['test_4'][6] == '1' and data_1['test_2'][1] == '2' and \
                data_1['test_4'][6] == '1':
            local_precent += 5

        if data_2['test_2'][1] == '1' and data_2['test_4'][6] == '2' and data_1['test_2'][1] == '2' and \
                data_1['test_4'][6] == '1':
            local_precent -= 10

        if data_2['test_1'][2] == '1' and '3' in data_2['test_3'] and data_1['test_1'][2] == '1' and '3' in data_1[
            'test_3']:
            local_precent += 5

        if data_2['test_1'][2] == '1' and '3' in data_2['test_3'] and data_1['test_1'][2] == '2' and '3' not in data_1[
            'test_3']:
            local_precent -= 10

        return local_precent


def find_all_compatible_users(user_id):
    result = []

    all_users = db.get_data(table='users')

    for user in all_users:
        if int(user_id) == int(user['id']):
            continue
        precent = Comaparator(user_id, user['id']).compare()

        if precent >= 0:
            result.append(user['id'])

    return result


class Decipher:
    def __init__(self, user_id):
        self.user_data = db.get_data(table='users', filters={'id': user_id})[0]
        self.gender = self.user_data['gender']
        self.test_1_data = self.user_data['test_1']
        self.test_2_data = self.user_data['test_2']
        self.test_3_data = self.user_data['test_3']
        self.test_4_data = self.user_data['test_4']
        self.test_5_data = self.user_data['test_5']

    def get_info(self):
        foramtion_text = f'👤 {self.user_data["username"]}\n' + '{}\n' * 5

        test_1_text = self.get_test_1_data()
        # print(test_1_text)

        test_2_text = self.get_test_2_data()
        # print(test_2_text)

        test_3_text = self.get_test_3_data()
        # print(test_3_text)

        test_4_text = self.get_test_4_data()
        # print(test_4_text)

        test_5_text = self.get_test_5_data()
        # print(test_5_text)

        return foramtion_text.format(test_1_text, test_2_text, test_3_text, test_4_text, test_5_text)

    def get_test_1_data(self):
        result = []
        formation_text = f'\tТест 1 \n' + '\t\t - {}\n' * len(self.test_1_data)

        for char_index in range(len(self.test_1_data)):
            char = self.test_1_data[char_index]

            btns = test_1[self.gender][char_index]['btns']

            for btn in btns:
                if btn['value'] == char:
                    result.append(btn['text'])

        return formation_text.format(*result)

    def get_test_2_data(self):
        result = []
        formation_text = f'\tТест 2 \n' + '\t\t - {}\n' * len(self.test_2_data)

        for char_index in range(len(self.test_2_data)):
            char = self.test_2_data[char_index]

            btns = test_2[self.gender][char_index]

            for btn in btns:
                if btn['value'] == char:
                    result.append(btn['text'])

        return formation_text.format(*result)

    def get_test_3_data(self):
        formation_text = (f'\tТест 3 \n'
                          f'\t\t- Категории: {", ".join(self.test_3_data)}\n')

        return formation_text

    def get_test_4_data(self):
        result = []
        formation_text = f'\tТест 4 \n' + '\t\t - {}\n' * len(self.test_4_data)

        for char_index in range(len(self.test_2_data)):
            char = self.test_4_data[char_index]

            if char == '0':
                result.append('Это вопрос для женщин')
                continue

            quest_id = char_index

            if char_index in [2, 3 ,4]:
                quest_id = 2
            elif char_index > 4:
                quest_id = char_index - 2

            btns = test_4[quest_id]['btns']

            for btn in btns:
                if btn['value'] == char:
                    if char_index in [2, 3, 4]:
                        numbers = {2: '1️⃣', 3: '2️⃣', 4: '3️⃣'}
                        result.append(f"{numbers[char_index]}{btn['text']}")
                    else:
                        result.append(btn['text'])

        return formation_text.format(*result)

    def get_test_5_data(self):
        result = []
        formation_text = f'\tТест 4 \n' + '\t\t{}\n' * len(self.test_5_data.split(';'))

        numbers = {1: '1️⃣', 2: '2️⃣', 3: '3️⃣', 4: '4️⃣', 5: '5️⃣', 6: '6️⃣', 7: '7️⃣', 8: '8️⃣', 9: '9️⃣', 10: '🔟'}

        for i in range(len(self.test_5_data.split(';'))):
            item = self.test_5_data.split(';')[i]
            i += 1
            result.append(f"{numbers[i]} {item}")

        return formation_text.format(*result)


def get_users_answers():
    users = db.get_data(table='users')
    result = []

    for user in users:
        answers = Decipher(user['id']).get_info()
        result.append(answers)

    with open('answers.txt', 'w', encoding='utf-8') as file:
        file.write('\n'.join(result))