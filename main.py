import time
import logging
import os
from aiogram import Bot, Dispatcher, executor, types
from docx import Document

TOKEN = "5615823301:AAEnhDpnU8T-07FkRMmnMZNNEzKYHSVrBYQ"
logging.basicConfig(level=logging.INFO, filename="logging.log", filemode="w")
bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot)
ingame = False  #
document_with_rules = Document()
game_database = []


@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    user_id = message.from_user.id
    user_full_name = message.from_user.full_name
    logging.info(f'{user_id=} {user_full_name=} {time.asctime()}')
    global ingame
    global game_database
    game_database = get_database()
    ingame = False

    await message.reply(f"������, {message.from_user.first_name}!\n����� ���������� � �������� �����������! "
                        f"\n� ����� ������ ���� ������ ����������� �� �������� ��������� ��� ���������� ���.\n"
                        f"��������� ���� ����� ��� ������������� ��������. ������� ������, �������!", reply_markup = types.ReplyKeyboardRemove())


@dp.message_handler(commands=['allgames']) # ���������� ������� ���������
async def all_games_handler(message: types.Message):
    global game_database
    await message.answer(f"� ���� ����� {len(game_database)} ���(�):")
    for file in game_database:
        game_name = str(file)
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text=game_name, callback_data=game_name))
        await message.answer("������� ��� ������ ����", reply_markup=keyboard)


@dp.message_handler(commands=['help'])
async def start_handler(message: types.Message):
    await message.answer("����� ������� ����, ����� � ��������, ���� ����� � � ������ ���� ��������� ��� ���.\n"
                         "��� ������ ����, ��� ��������� �� ��������, � ������ ���� ������ �� �����.\n"
                         "����� ������� ������ ���� - ����� ������ start � ����, � ����� ����� �� ��� ������ �������.")


@dp.message_handler(commands=['addgame'])
async def start_handler(message: types.Message):
    await message.answer("������� �� ����� ���� � �� ��� ����� �����, � ����� - ������ :(\n"
                         "�� ���� ������ ������, �� ������� ����� ����������� �� ����� ������ � ��������� �� �� �����, ����� � ����� ������������ �� ������ ������� � ����!\n"
                         "�����-���� ����������� �� ��������� ���� ��� �� �������� ���� ������ ����� ���������� ���� ��, ����� ���� �������� ����� :)")


@dp.callback_query_handler()  # ���������� ������ ��� ������ ���� ���
async def answer_to_button(call: types.CallbackQuery):
    global ingame
    global document_with_rules
    if ingame == False:  # ������, ���������� �� ����� ���� � ����, ���������� ������ ���������� ����
        request_answer = get_rules(call.data)
        if isinstance(request_answer, str):
            await call.message.answer(request_answer)
        else:
            document_with_rules = request_answer  # �������� � ���������� (���������)
            newkeyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            for row in document_with_rules.tables[0].rows:  # ������ ������
                button = types.KeyboardButton(text=row.cells[0].text.strip())
                newkeyboard.add(button)
            ingame = True
            bot.send_photo('C:/Users/Squeed/Desktop/LazyRules/speedtest.jpg')
            await call.message.answer('���, ������! ��� �� ������ ���� ����� ������ � ����������� ���������� � �� ���������!', reply_markup=newkeyboard)



    #await call.message.answer(call.data)

# ������� ������� �� ���������
@dp.message_handler(content_types=["text"])
async def answer_to_user(message: types.Message):
    global ingame
    global document_with_rules
    if ingame == False:  # ������, ���������� �� ����� ���� � ����, ���������� ������ ���������� ����
        request_answer = get_rules(message.text)
        if isinstance(request_answer, str):
            await message.answer(request_answer)
        else:
            document_with_rules = request_answer  # �������� � ���������� (���������)
            newkeyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            for row in document_with_rules.tables[0].rows:  # ������ ������
                button = types.KeyboardButton(text=row.cells[0].text.strip())
                newkeyboard.add(button)
            ingame = True
            await message.answer('���, ������\n����� ����� �� ����� ���� ����� ������ start � ���� �����', reply_markup=newkeyboard)

# ������������ ������ ��������� �������
    elif ingame == True:
        # ��������� ������ �� ������ � ���������� �� ����� ��
        button_rule = []
        answer_rule = []
        for i in range(0, len(document_with_rules.tables[0].rows)):
            button_rule.append(document_with_rules.tables[0].rows[i].cells[0].text.strip())
            answer_rule.append(document_with_rules.tables[0].rows[i].cells[1].text.strip())

        for i in range(0, len(button_rule)):
            if message.text == button_rule[i]:
                await message.answer(answer_rule[i])
            else:
                pass


# ������� ������ ���������� ���������� ����� ���� + ������� �� ��������. ����� ��� � ������ ������ �����������
def get_game_name(user_request):

    global game_database
    answer = ('����� ���� � ��� �� ����! '
                '\n���� ������, �� ������ ���������� � ������ � ���������� ��� � ����!')
    cor_name = ''

    for games in game_database:
        if user_request.lower() in games.lower():
            cor_name = games
        else:
            pass

    if cor_name in game_database:
        answer = f'���� ������� ����. Ÿ ���������� �������� - {cor_name}'
    else:
        pass

    return answer


# ��������������� ������ ��������� ���� � ��������� ��� ���������� ������ ������ ���
def get_rules(user_request):
    global game_database
    correct_name = ''

    for games in game_database:
        if user_request.lower() == games.lower():
            correct_name = games
        else:
            pass

    if correct_name != '':
        path = (f'C:/Users/Squeed/Desktop/LazyRules/{user_request}.docx');
        return (Document(path))
    else:
        return get_game_name(user_request)


# ��������� ���� ������
def get_database():
    files = os.listdir('C:/Users/Squeed/Desktop/LazyRules/')
    database = []
    for file in files:
        game_name = str(file)[:-5:]
        database.append(game_name)
    return database


if __name__ == '__main__':
    executor.start_polling(dp)