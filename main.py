import asyncio
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler
from telegram.ext.filters import Regex, COMMAND
from passwords import TOKEN
from connector import Connector
import os
from keyboards import menu_keyboard, choice_keyboard
# TODO-REVIEW для имортов использовать тулзу isort, она их отсортирует и выровняет в правильном формате

# TODO-REVIEW для токена, паролей, адресов и прочего использовать .env файл
token = TOKEN

# TODO-REVIEW глобальные переменные плохо, предлагаю сделать отдельный пакет/сервис для работы с бд
# если пакет, то сделать метод get_database_instance которая будет синглтон бд возвращать
# если сервис, то просто вывести REST API на каждый из методов, которые нужны
con = Connector()

# TODO-REVIEW для состояний использовать библиотеку aenum и вынести в отдельный файл states
ADD_SHARE, ADD_BOND, DELETE, ANY, CHOICE, SECRITY_CHOICE = range(6)

con_established = False

# TODO-REVIEW для каждого handler сделать декоратор, который через logging будет логировать %function%user% для краткой аналитики
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # TODO-REVIEW вместо print использовать logging, там есть уровни лога, в том числе level.DEBUG, для таких строчек
    print(update.message.message_id)
    markup_key = ReplyKeyboardMarkup(menu_keyboard, one_time_keyboard=False)
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   # TODO-REVIEW все тексты в отдельный файл
                                   text="I'm a screener bot, I can show some statistics on "
                                        "different stocks and shares! You can choose any option and get a description",
                                   reply_markup=markup_key)
    
    # TODO-REVIEW ну если сделал глобальный con, то глобально и Init мог вызвать..
    if not con_established:
        await con.Init()
    return ANY


async def any_state(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(update.message.message_id)
    if "add" in update.message.text.lower():
        await update.effective_user.send_message(
            "Chose on a reply keyboard what do you want to add, bond or share. If you missed clicked tap /end",
            reply_markup=ReplyKeyboardMarkup(choice_keyboard, one_time_keyboard=False))
        return SECRITY_CHOICE
    # TODO-REVIEW elif вместо if
    if "remove" in update.message.text.lower():
        await update.effective_user.send_message(
            "Write a name of a stock you want to remove.",
            reply_markup=ReplyKeyboardRemove())
        await update.effective_user.send_message(
            "If you want to remove more than one, type the names in different "
            "messages or in one separated with ' '. To end removing type /end")
        return DELETE
    if "show" in update.message.text.lower():
        await update.effective_user.send_message("Connecting to database...")
        data = await show_user_securities(update)
    else:
        await update.effective_user.send_message(
            f"I don`t know what does {update.message.text} means, please choose on of the options on reply keyboard")
    return ANY


async def add_bond(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # TODO-REVIEW нужно проверять наличие используемых ключей secid, isin и тп, внутри метода find_bond, если АПИ изменят - бот крашнется
    data = await con.find_bond(update.message.text.strip())
    if len(data) == 0:
        await update.effective_user.send_message("We didn't find any securities on this name/ticker/isin."
                                                 " Choose what you want to add bond or share",
                                                 reply_markup=ReplyKeyboardMarkup(choice_keyboard))
        return SECRITY_CHOICE
    elif len(data) == 1:
        await update.effective_user.send_message(f"We've found security. \nTicker: <b>{data[0]['secid']}</b>"
                                                 f"\nISIN: <b>{data[0]['isin']}</b>"
                                                 f"\nShortname: <b>{data[0]['shortname']}</b>"
                                                 f"\nName: <b>{data[0]['name']}</b>"
                                                 f"\nType: <b>{data[0]['type']}</b>, it will be added"
                                                 f" to your securities", parse_mode="HTML")
        await con.add_security(update.effective_user.id, data[0]["secid"])
        await con.add_security_to_db(data[0]['secid'], data[0]['isin'], data[0]['shortname'], data[0]['name'],
                                     data[0]['type'])
        await update.effective_user.send_message("You may add any other security or /end")
        return SECRITY_CHOICE
    else:
        await update.effective_user.send_message("We've found several securities on your request. "
                                                 "Please specify which one: by typing the number. Example: 1"
                                                 " or by typing ticker or by typing secid,"
                                                 " you can stop choosing by tapping /end")
        count = len(data)

        # TODO-REVIEW не совсем понял, что тут происходит, но подозреваю что есть проблема использования context.chat_data["choice_message_ids"]
        context.chat_data["choice_message_ids"] = []
        choices = {}
        for i in range(1, count + 1):
            response = f"{i}) Ticker: <b>{data[i - 1]['secid']}</b> " \
                       f"\nISIN: <b>{data[i - 1]['isin']}</b>" \
                       f"\nShortname: <b>{data[i - 1]['shortname']}</b>" \
                       f"\nName: <b>{data[i - 1]['name']}</b>" \
                       f"\nType: <b>{data[i - 1]['type']}</b>"
            choices[str(i)] = f"{data[i - 1]['secid']}%){data[i - 1]['isin']}%)" \
                              f"{data[i - 1]['shortname']}%){data[i - 1]['name']}%){data[i - 1]['type']}"
            msg = await update.message.reply_text(response, parse_mode="HTML")
            context.chat_data["choice_message_ids"] += [msg.message_id]
        context.chat_data[f"choice_messages"] = choices
        return CHOICE


# TODO-REVIEW что то много дублирования кода, методы add_bond и add_share больно похожи, можно избавиться от дублирования думаю
async def add_share(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = await con.find_share(update.message.text.strip())
    if len(data) == 0:
        await update.effective_user.send_message("We didn't find any securities on this name/ticker/isin."
                                                 " Choose what you want to add bond or share",
                                                 reply_markup=ReplyKeyboardMarkup(choice_keyboard))
        return SECRITY_CHOICE
    elif len(data) == 1:
        await update.effective_user.send_message(f"We've found security. \nTicker: <b>{data[0]['secid']}</b>"
                                                 f"\nISIN: <b>{data[0]['isin']}</b>"
                                                 f"\nShortname: <b>{data[0]['shortname']}</b>"
                                                 f"\nName: <b>{data[0]['name']}</b>"
                                                 f"\nType: <b>{data[0]['type']}</b>, it will be added"
                                                 f" to your securities", parse_mode="HTML")
        await con.add_security(update.effective_user.id, data[0]["secid"])
        await con.add_security_to_db(data[0]['secid'], data[0]['isin'], data[0]['shortname'], data[0]['name'],
                                     data[0]['type'])
        await update.effective_user.send_message("You may add any other security or /end")
        return SECRITY_CHOICE
    else:
        await update.effective_user.send_message("We've found several securities on your request. "
                                                 "Please specify which one: by typing the number. Example: 1"
                                                 " or by typing ticker or by typing secid,"
                                                 " you can stop choosing by tapping /end")
        count = len(data)

        context.chat_data["choice_message_ids"] = []
        choices = {}
        for i in range(1, count + 1):
            response = f"{i}) Ticker: <b>{data[i - 1]['secid']}</b> " \
                       f"\nISIN: <b>{data[i - 1]['isin']}</b>" \
                       f"\nShortname: <b>{data[i - 1]['shortname']}</b>" \
                       f"\nName: <b>{data[i - 1]['name']}</b>" \
                       f"\nType: <b>{data[i - 1]['type']}</b>"
            choices[str(i)] = f"{data[i - 1]['secid']}%){data[i - 1]['isin']}%)" \
                              f"{data[i - 1]['shortname']}%){data[i - 1]['name']}%){data[i - 1]['type']}"
            msg = await update.message.reply_text(response, parse_mode="HTML")
            context.chat_data["choice_message_ids"] += [msg.message_id]
        context.chat_data[f"choice_messages"] = choices
        return CHOICE


async def choose_paper(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip().upper()
    choice = context.chat_data["choice_messages"]
    if text.isdigit():
        if (int(text) <= len(choice)) and (int(text) > 0):
            # TODO-REVIEW многовато обращений по индексу, не думаю что проверка сверху покрывает все варианты краша
            data = choice[text].split("%)")
            await con.add_security_to_db(*data)
            await con.add_security(update.effective_user.id, data[0])
            msg = f"Ticker: <b>{data[0]}</b> " \
                  f"\nISIN: <b>{data[1]}</b>" \
                  f"\nShortname: <b>{data[2]}</b>" \
                  f"\nName: <b>{data[3]} </b>" \
                  f"\nType: <b>{data[4]}</b>, was chosen ✅"
            await context.bot.editMessageText(chat_id=update.message.chat_id,
                                              message_id=context.chat_data['choice_message_ids'][0] - 1,
                                              text=msg, parse_mode="HTML")
            for i in context.chat_data['choice_message_ids']:
                await context.bot.deleteMessage(message_id=i,
                                                chat_id=update.message.chat_id)
            context.chat_data['choice_message_ids'] = []
            context.chat_data['choice_messages'] = {}
            await update.effective_user.send_message("You may add any other security or /end")
            return SECRITY_CHOICE
        else:
            await update.effective_user.send_message("Choice doesn't fit any option."
                                                     " Try again or /end")
            return CHOICE
    else:
        for i in context.chat_data["choice_message"].values():
            if text in i.upper().split("%)"):
                data = choice.split("%)")
                await con.add_security_to_db(*data)
                await con.add_security(update.effective_user.id, data[0])
                msg = f"Ticker: <b>{data[0]}</b> " \
                      f"\nISIN: <b>{data[1]}</b>" \
                      f"\nShortname: <b>{data[2]}</b>" \
                      f"\nName: <b>{data[3]} </b>" \
                      f"\nType: <b>{data[4]}</b>, was chosen ✅"
                await context.bot.editMessageText(chat_id=update.message.chat_id, message_id=choice[0] - 1,
                                                  text=msg)
                for i in context.chat_data['choice_message_ids']:
                    await context.bot.deleteMessage(message_id=i,
                                                    chat_id=update.message.chat_id)
                context.chat_data['choice_message_ids'] = []
                context.chat_data['choice_messages'] = {}
                await update.effective_user.send_message("You may add any other security or /end")
                return SECRITY_CHOICE
        else:
            await update.effective_user.send_message("Choice doesn't fit any option."
                                                     " Try again or /end")
            return CHOICE


async def security_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if "share" in update.message.text.lower():
        await update.effective_user.send_message(
            "Write a tiсker (or a name, but ticker is better) of a share you want to add.",
            reply_markup=ReplyKeyboardRemove())
        await update.effective_user.send_message(
            "If you want to add more than one, type the names in different "
            "messages or in one separated with ' '. To end adding type /end")
        return ADD_SHARE
    elif "bond" in update.message.text.lower():
        await update.effective_user.send_message(
            "Write a tiсker (or a name, but ticker is better) of a bond you want to add.",
            reply_markup=ReplyKeyboardRemove())
        await update.effective_user.send_message(
            "If you want to add more than one, type the names in different "
            "messages or in one separated with ' '. To end adding type /end")
        return ADD_BOND
    else:
        return SECRITY_CHOICE


async def end_choosing(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.deleteMessage(message_id=context.chat_data['choice_message_ids'][0] - 1,
                                    chat_id=update.message.chat_id)
    for i in context.chat_data['choice_message_ids']:
        await context.bot.deleteMessage(message_id=i,
                                        chat_id=update.message.chat_id)
    context.chat_data['choice_message_ids'] = []
    context.chat_data['choice_messages'] = {}
    markup_key = ReplyKeyboardMarkup(menu_keyboard, one_time_keyboard=False)
    await update.effective_user.send_message(text="Ok that`s it, anything else?", reply_markup=markup_key)
    return ANY


async def show_user_securities(update: Update):
    data = await con.get_user_securities(update.effective_user.id)
    for i in data:
        answer = await con.draw_price_graphic(i)
        if answer == "ok":
            await update.effective_user.send_photo(f"{i}.png")
            # TODO-REVIEW перед os.remove нужно os.exists
            os.remove(f"{i}.png")
        await update.effective_user.send_message(i)
        await update.effective_user.send_message(answer)


async def remove_paper(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await con.remove_security(update.effective_user.id, update.message.text)
    return DELETE


async def end_process(update: Update, context: ContextTypes.DEFAULT_TYPE):
    markup_key = ReplyKeyboardMarkup(menu_keyboard, one_time_keyboard=False)
    await update.effective_user.send_message(text="Ok that`s it, anything else?", reply_markup=markup_key)
    return ANY


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="Bye, if you want to restart conversation write /start",
                                   reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


def main():
    app = Application.builder().token(token).concurrent_updates(True).build()
    # TODO-REVIEW аргументы per_user, per_chat и тп
    conv_handler = ConversationHandler(entry_points=[CommandHandler("start", start_command)],
                                       states={
                                           ANY: [MessageHandler(filters.TEXT & (~ filters.COMMAND) & (
                                               ~ filters.Regex('Stop conversation')), any_state)],
                                           ADD_SHARE: [MessageHandler(filters.TEXT & (~ filters.COMMAND), add_share),
                                                       CommandHandler("end", end_process)],
                                           ADD_BOND: [MessageHandler(filters.TEXT & (~ filters.COMMAND), add_bond),
                                                      CommandHandler("end", end_process)],
                                           CHOICE: [MessageHandler(filters.TEXT & (~ filters.COMMAND), choose_paper),
                                                    CommandHandler("end", end_choosing)],
                                           DELETE: [MessageHandler(filters.TEXT & (~ filters.COMMAND), remove_paper),
                                                     CommandHandler("end", end_process)],
                                           SECRITY_CHOICE: [
                                               MessageHandler(filters.TEXT & (~ filters.COMMAND), security_choice),
                                               CommandHandler("end", end_process)]

                                       },
                                       fallbacks=[CommandHandler('cancel', cancel), CommandHandler('stop', cancel),
                                                  MessageHandler(filters.Regex('Stop conversation'), cancel)])
    app.add_handler(conv_handler)

    app.run_polling(poll_interval=.5)


if __name__ == "__main__":
    main()
