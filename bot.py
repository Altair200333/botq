import telegram
import logging
from telegram.ext import CommandHandler
from telegram.ext import Updater
import random

students_prior = ["vadim", "stepan", "tania"]
students_main = ["fedya", "max", "miha", "sergei", "vania"]
students_last = ["gosha", "leha", "arkadii"]

def mix_all():
    random.shuffle(students_prior)
    random.shuffle(students_main)
    random.shuffle(students_last)

def get_students_string():
    return "First wave: " + ' '.join(students_prior)+"\n"+"Main wave: "+' '.join(students_main)+"\n"+"Last wave: "+' '.join(students_last)

def list_students(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=get_students_string())

def start(update, context):
    #text_caps = ' '.join(context.args)
    context.bot.send_message(chat_id=update.effective_chat.id, text="/students List students \n/mix Shuffle all \n/p <name> Move to priority queue\n/m <name> Move to main queue \n/l <name> Move to the end")

def mix_students(update, context):
    mix_all()
    context.bot.send_message(chat_id=update.effective_chat.id, text="Shuffled students are: \n" + get_students_string())

def delete_student(whom):
    exists = 0
    if whom in students_last:
        students_last.remove(whom)
        exists = 1
    if whom in students_main:
        students_main.remove(whom)
        exists = 1
    if whom in students_prior:
        students_prior.remove(whom)
        exists = 1
    return exists

def prior_student(update, context):
    who = context.args[0]
    exists = delete_student(who)
    if exists == 0:
        context.bot.send_message(chat_id=update.effective_chat.id, text="There is no " + who)
        return
    students_prior.append(who)
    context.bot.send_message(chat_id=update.effective_chat.id, text="Prior student " + str(who))

def main_student(update, context):
    who = context.args[0]
    exists = delete_student(who)
    if exists == 0:
        context.bot.send_message(chat_id=update.effective_chat.id, text="There is no "+who)
        return
    students_main.append(who)
    context.bot.send_message(chat_id=update.effective_chat.id, text="Student " + str(who)+" moved to main")

def last_student(update, context):
    who = context.args[0]
    exists = delete_student(who)
    if exists == 0:
        context.bot.send_message(chat_id=update.effective_chat.id, text="There is no " + who)
        return
    students_last.append(who)
    context.bot.send_message(chat_id=update.effective_chat.id, text="Student " + str(who)+" moved to last")


Token = '1098247693:AAHxzHd-naoxSpaQN_6Olkva_tQW7gSK9aQ'
updater = Updater(token=Token, use_context=True)
dispatcher = updater.dispatcher

start_handler = CommandHandler('start', start)
all_handler = CommandHandler('students', list_students)
mix_handler = CommandHandler('mix', mix_students)
prior_handler = CommandHandler('p', prior_student)
main_handler = CommandHandler('m', main_student)
last_handler = CommandHandler('l', last_student)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(all_handler)
dispatcher.add_handler(mix_handler)
dispatcher.add_handler(prior_handler)
dispatcher.add_handler(main_handler)
dispatcher.add_handler(last_handler)

updater.start_polling()

#print(bot.get_me())

