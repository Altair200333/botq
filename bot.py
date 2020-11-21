import telegram
import logging
from telegram.ext import CommandHandler
from telegram.ext import Updater
import random

knowUsersList = [335563375, 384881851, 892620744]

students_prior = ["mdudar", "tania"]
students_main = ["Selektzioner", "borya", "gosha", "BearingBa1l", "goglom", "vania", "petr_mp", "SkivHisink", "vladimir", "SergeyV0", "fedya"]
students_last = []

Mike = 335563375


def log_ME(update, context, msg):
    context.bot.send_message(chat_id=Mike, text=str(update.effective_chat.username) + "\n" + msg)


def addKnown(update):
    if update.effective_chat.id not in knowUsersList:
        knowUsersList.append(update.effective_chat.id)


def mix_all():
    random.shuffle(students_prior)
    random.shuffle(students_main)
    random.shuffle(students_last)


def get_students_string():
    return "First wave: " + ', '.join(students_prior) + "\n" + "Main wave: " + ', '.join(
        students_main) + "\n" + "Last wave: " + ', '.join(students_last)


def list_students(update, context):
    addKnown(update)
    log_ME(update, context, "list all")
    context.bot.send_message(chat_id=update.effective_chat.id, text=get_students_string())


def start(update, context):
    addKnown(update)
    # text_caps = ' '.join(context.args)
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="/students List students \n/mix Shuffle all \n/p <name> Move to priority queue\n/m <name> Move to main queue \n/l <name> Move to the end\nName argument is optional if your username is public")

def logListToAll(update, context):
    for user in knowUsersList:
        if not update.effective_chat.id == user:
            context.bot.send_message(chat_id=user, text=update.effective_chat.username + " shuffled all: \n" + get_students_string())

def mix_students(update, context):
    addKnown(update)
    log_ME(update, context, "mix students")
    mix_all()
    if not(len(context.args) == 1 and context.args[0] == 's'):
        logListToAll(update, context)
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
    addKnown(update)
    who = context.args[0] if len(context.args) > 0 else update.effective_chat.username
    log_ME(update, context, "move to Prior queue " + str(who))

    exists = delete_student(who)
    if exists == 0:
        context.bot.send_message(chat_id=update.effective_chat.id, text="There is no " + who)
        return
    #students_prior.append(who)
    students_prior.insert(random.randint(0, len(students_prior)), who)
    context.bot.send_message(chat_id=update.effective_chat.id, text="Prior student " + str(who))


def main_student(update, context):
    addKnown(update)
    who = context.args[0] if len(context.args) > 0 else update.effective_chat.username
    log_ME(update, context, "move to Main queue " + str(who))

    exists = delete_student(who)
    if exists == 0:
        context.bot.send_message(chat_id=update.effective_chat.id, text="There is no " + who)
        return
    #students_main.append(who)
    students_main.insert(random.randint(0, len(students_main)), who)
    context.bot.send_message(chat_id=update.effective_chat.id, text="Student " + str(who) + " moved to main")


def last_student(update, context):
    addKnown(update)
    who = context.args[0] if len(context.args) > 0 else update.effective_chat.username
    log_ME(update, context, "move to Last queue " + str(who))

    exists = delete_student(who)
    if exists == 0:
        context.bot.send_message(chat_id=update.effective_chat.id, text="There is no " + who)
        return
    #students_last.append(who)
    students_last.insert(random.randint(0, len(students_last)), who)
    context.bot.send_message(chat_id=update.effective_chat.id, text="Student " + str(who) + " moved to last")

def know_users(update, context):
    context.bot.send_message(chat_id=Mike, text="known by me: " + ','.join(str(x) for x in knowUsersList))

def wall_all(update, context):
    if len(context.args) == 0:
        return
    for user in knowUsersList:
        context.bot.send_message(chat_id=user, text=context.args[0])

def all_main(update, context):
    for i in students_prior[:]:
        print(i)
        students_main.insert(random.randint(0, len(students_main)), i)
        students_prior.remove(i)

    for i in students_last[:]:
        stud = i
        students_main.insert(random.randint(0, len(students_main)), stud)
        students_last.remove(stud)

    list_students(update, context)

Token = '1098247693:AAHxzHd-naoxSpaQN_6Olkva_tQW7gSK9aQ'
updater = Updater(token=Token, use_context=True)
dispatcher = updater.dispatcher

start_handler = CommandHandler('start', start)
all_handler = CommandHandler('students', list_students)
mix_handler = CommandHandler('mix', mix_students)
prior_handler = CommandHandler('p', prior_student)
main_handler = CommandHandler('m', main_student)
last_handler = CommandHandler('l', last_student)
known_handler = CommandHandler('kk', know_users)
wall_handler = CommandHandler('wall', wall_all)
all_main_handler = CommandHandler('allm', all_main)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(all_handler)
dispatcher.add_handler(mix_handler)
dispatcher.add_handler(prior_handler)
dispatcher.add_handler(main_handler)
dispatcher.add_handler(last_handler)
dispatcher.add_handler(known_handler)
dispatcher.add_handler(wall_handler)
dispatcher.add_handler(all_main_handler)

updater.start_polling()

# print(bot.get_me())
