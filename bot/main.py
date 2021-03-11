import config
import telebot

bot = telebot.TeleBot(config.token)

buttons = telebot.types.ReplyKeyboardMarkup()
buttons.row('🥔', '✂', '📜')
players = []
players_name = {}
answers = {}
but_del = telebot.types.ReplyKeyboardRemove()


def choosing_winner(bot_telegram):
    if len(answers) == len(players):
        vals = list(answers.values())
        ans_set = set(vals)
        for player in players:
            values = answers.items()
            for value in values:
                bot_telegram.send_message(player,
                                          'Игрок под ником {0} выбрал - {1}'.format(players_name[value[0]], value[1]),
                                          reply_markup=but_del)
        if set(['🥔', '✂', '📜']).issubset(ans_set):
            for player in players:
                print('1')
                bot_telegram.send_message(player, 'Нет победителя', reply_markup=but_del)
        else:
            if not set(['🥔']).issubset(ans_set):
                print('2')
                if vals.count('✂') == 1:
                    for player in players:
                        if '✂' == answers[player]:
                            winner = player
                    for player in players:
                        bot_telegram.send_message(player, 'Победил игрок под ником {0}'.format(players_name[winner]),
                                                  reply_markup=but_del)
                else:
                    for player in players:
                        bot_telegram.send_message(player, 'Нет победителя', reply_markup=but_del)

            elif not set(['✂']).issubset(ans_set):
                print('3')
                if vals.count('📜') == 1:
                    for player in players:
                        if '📜' == answers[player]:
                            winner = player
                    for player in players:
                        bot_telegram.send_message(player, 'Победил игрок под ником {0}'.format(players_name[winner]),
                                                  reply_markup=but_del)
                else:
                    for player in players:
                        bot_telegram.send_message(player, 'Нет победителя', reply_markup=but_del)
            elif not set(['📜']).issubset(ans_set):
                print('4')
                if vals.count('🥔') == 1:
                    for player in players:
                        if '🥔' == answers[player]:
                            winner = player
                    for player in players:
                        bot_telegram.send_message(player, 'Победил игрок под ником {0}'.format(players_name[winner]),
                                                  reply_markup=but_del)
                else:
                    for player in players:
                        bot_telegram.send_message(player, 'Нет победителя', reply_markup=but_del)

        answers.clear()
        players_name.clear()
        players.clear()


@bot.message_handler(commands=['start'])
def start_message(message):
    if message.chat.id not in players:
        bot.send_message(message.chat.id, 'Вы добавлены в игру!!!!\nВыберите один из вариантов', reply_markup=buttons)
        players_name[message.chat.id] = message.from_user.first_name
        players.append(message.chat.id)
    else:
        bot.send_message(message.chat.id, 'Вы есть в игре!!!\nВыберите один из вариантов', reply_markup=buttons)


@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
    if message.text in ['🥔', '✂', '📜']:
        answers[message.chat.id] = message.text
        bot.send_message(message.chat.id, 'Вы выбрали{0}'.format(message.text))
    if len(players) >= 2:
        choosing_winner(bot)


if __name__ == '__main__':
    bot.infinity_polling()