import random
from telebot import types
from main import bot

def main(message):
    field_bot = [[0] * 5 for i in range(5)]
    field_user = [[0] * 5 for i in range(5)]
    count_mines = 0
    for i in range(5):
        if count_mines == 10:
            break
        for j in range(5):
            field_bot[i][j] = random.randint(0,1)
            if field_bot[i][j] == 1:
                count_mines += 1
                if count_mines == 10:
                    break

    for i in range(5):
        for j in range(5):
            if field_bot[i][j] == 1:
                if j + 1 <= 4 and field_user[i][j] < 9 and field_bot[i][j + 1] == 0:
                    field_user[i][j + 1] += 1
                if j - 1 >= 0 and field_user[i][j] < 9 and field_bot[i][j - 1] == 0:
                    field_user[i][j - 1] += 1
                if j + 1 <= 4 and i - 1 >= 0 and field_user[i][j] < 9 and field_bot[i - 1][j + 1] == 0:
                    field_user[i - 1][j + 1] += 1
                if j + 1 <= 4 and i + 1 <= 4 and field_user[i][j] < 9 and field_bot[i + 1][j + 1] == 0:
                    field_user[i + 1][j + 1] += 1
                if i + 1 <= 4 and field_user[i][j] < 9 and field_bot[i + 1][j] == 0:
                    field_user[i + 1][j] += 1
                if i + 1 >= 4 and j - 1 >= 0 and field_user[i][j] < 9 and field_bot[i + 1][j - 1] == 0:
                    field_user[i + 1][j - 1] += 1
                if i - 1 >= 0 and field_user[i][j] < 9 and field_bot[i - 1][j] == 0:
                    field_user[i - 1][j] += 1
                if i - 1 >= 0 and j - 1 >= 0 and field_user[i][j] < 9 and field_bot[i - 1][j - 1] == 0:
                    field_user[i - 1][j - 1] += 1
                field_user[i][j] = 9

    for i in range(5):
        print(field_bot[i])
    print("\n")
    for i in range(5):
            print(field_user[i])

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=5)
    b11 = types.KeyboardButton('1')
    b12 = types.KeyboardButton('2')
    b13 = types.KeyboardButton('3')
    b14 = types.KeyboardButton('4')
    b15 = types.KeyboardButton('5')
    b21 = types.KeyboardButton('6')
    b22 = types.KeyboardButton('7')
    b23 = types.KeyboardButton('8')
    b24 = types.KeyboardButton('9')
    b25 = types.KeyboardButton('10')
    b31 = types.KeyboardButton('11')
    b32 = types.KeyboardButton('12')
    b33 = types.KeyboardButton('13')
    b34 = types.KeyboardButton('14')
    b35 = types.KeyboardButton('15')
    b41 = types.KeyboardButton('16')
    b42 = types.KeyboardButton('17')
    b43 = types.KeyboardButton('18')
    b44 = types.KeyboardButton('19')
    b45 = types.KeyboardButton('20')
    b51 = types.KeyboardButton('21')
    b52 = types.KeyboardButton('22')
    b53 = types.KeyboardButton('23')
    b54 = types.KeyboardButton('24')
    b55 = types.KeyboardButton('25')
    markup.add(b11,b12,b13,b14,b15,b21,b22,b23,b24,b25,b31,b32,b33,b34,b35,b41,b42,b43,b44,b45,b51,b52,b53,b54,b55)


if __name__ == '__main__':
    main()

