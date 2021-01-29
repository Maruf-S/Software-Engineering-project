#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

"""
First, a few callback functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""
import mechanize
import requests
from bs4 import BeautifulSoup
import logging
import telegram
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler)

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

Username, Password, Formsubmit, Campus_Select = range(4)
competators = [
    ["VOTE ABDISA NENKO AGA", 'VOTE ABDULHAFIZ JEMAL HUSSEN', 'VOTE ANIMAW MOLLA DAGNAW', 'VOTE BEKELE ABERA MEKONEN',
     'VOTE BENYAM TIMOTEWOS AKAKO', 'VOTE DAGMAWE ASTATIKE TAFESE', 'VOTE EDEN TESFAYE GETEYE',
     'VOTE MASRESHA AYELIGN GEBRU', 'VOTE NAOL GELETA NEGASA', 'VOTE NUHAMIN HABTAMU ZEWDIE',
     'VOTE TEKTA MIDEKSA SOLOMON']]
keys_of_students = ["HSR_4336_07", "HSR_1083_11", "HSR_4277_09", "HSR_5854_08", "HSR_9367_09", "HSR_7384_09",
                    "HSR_9728_10", "HSR_2302_09", "HSR_8973_09", "HSR_7294_10", "HSR_1041_10"]
URL = "https://api.telegram.org/bot889311707:AAF4YMI90-_5m_Nd7cFiGbighvy0HB25o8U/"

##################################################################################################
##################################################################################################
def start(update, context):
    theuser = update.message.from_user
    update.message.reply_text(
        "<code>Hello Mr.{} and welcome the HSR Grade and results bot.</code>".format(theuser.first_name),parse_mode=telegram.ParseMode.HTML)
    update.message.reply_text("<code>Please send your Username. For example hsr/2218/10</code>",parse_mode=telegram.ParseMode.HTML)
    # reply_keyboard = [["AAIT"],["AAU"],["CHS"]]
    # update.message.reply_text("Which campus are you currently studying at?",reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    # reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    return Username


def username(update, context):
    print(update.message.chat_id)
    user = update.message.from_user
    the_text = update.message.text
    if the_text.count("/") == 2:
        # FETCHING USERNAME WAS SUCCESSFUL
        context.user_data['username'] = the_text
        update.message.reply_text("<code>Okay now please send me your password.</code>",parse_mode=telegram.ParseMode.HTML)
        return Password
    else:
        update.message.reply_text("<code>ID number does'nt seem to be in a correct format please send it like for example as hsr/3123/09</code>",parse_mode=telegram.ParseMode.HTML)

def password(update, context):
    import platform
    # GOT THE PASSWORD
    user = update.message.from_user
    context.user_data['password'] = update.message.text
    logger.warning('Update "%s" caused error', update)
    user_name = (context.user_data["username"])
    pass_word = (context.user_data["password"])
#    update.message.reply_text("<code>Working...</code>",parse_mode=telegram.ParseMode.HTML)
    context.bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
    Get_the_results(update.message.chat_id, user_name, pass_word, context)
    return ConversationHandler.END
#    return Formsubmit

def formsubmit(update, context):
    update.message.reply_text("<code>Invalid input please try again.</code>",parse_mode=telegram.ParseMode.HTML)
def Change_Campus(update,context):
    the_text = update.message.text
    if the_text=="CHS":
        update.message.reply_text("<code>Please use this</code> <a href='t.me/CHS_G_Robot'>link</a> <code>to access the College of Health Sciences database</code>.", parse_mode=telegram.ParseMode.HTML)
    elif the_text=="AAU":
        update.message.reply_text("<code>Please use this</code> <a href='t.me/AAU_G_Robot'>link</a> <code>to access the AAU database </code>.",parse_mode=telegram.ParseMode.HTML)
    else:
        update.message.reply_text("<code>Invalid Input</code>.",parse_mode=telegram.ParseMode.HTML)
    return ConversationHandler.END
def help(update, context):
    update.message.reply_text('<code>Please Select the Campus you are currently studying in.</code>',parse_mode=telegram.ParseMode.HTML,reply_markup=ReplyKeyboardMarkup([["CHS"],["AAU"]], one_time_keyboard=True))
    return Change_Campus
def cancel(update, context):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('<code>Conversation canceled successfully.</code>',
                              reply_markup=ReplyKeyboardRemove(),parse_mode=telegram.ParseMode.HTML)

    return ConversationHandler.END

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)
#-------------------------------------------------------------------------BACK----------------------------------------------------------------------
#parse_mode=telegram.ParseMode.HTML
def get_url(url):
    from urllib3.util.retry import Retry
    from requests.adapters import HTTPAdapter
    session = requests.Session()
    retries = Retry(total=900000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000,backoff_factor=0.3,status_forcelist=[ 500, 502, 503, 504 ])
    session.mount('http://', HTTPAdapter(max_retries=retries))
    session.mount('https://', HTTPAdapter(max_retries=retries))
    x=session.get(url)
    return (x.text)
def Get_the_results(id,username,password,context):
    try:
        br = mechanize.Browser()
        br.set_handle_robots(False)
        br.addheaders = [("User-agent", "Mozilla/5.0")]
        gitbot = br.open("http://10.21.2.12/Grade/GradeReport")
        br.select_form(nr=0)
        br["UserName"] = username
        br["Password"] = password
        sign_up = br.submit()
        rname=br.response().read()
        if ("before your account gets locked out" in str(rname)):
            ss = BeautifulSoup(rname, 'html.parser')
            check_text = ss.find('div', {'class': 'validation-summary-errors'}).find('li').text
            #Send_Text(check_text,id,request="<code>")
            context.bot.send_message(chat_id=id, text="<code>"+check_text+"</code>",parse_mode=telegram.ParseMode.HTML)
        elif ("Your account has been locked out" in str(rname)):#Send_Text('Your account has been locked out due to multiple failed login attempts.', id,request="<code>")
            context.bot.send_message(chat_id=id, text="<code>"+'Your account has been locked out due to multiple failed login attempts.'+"</code>",parse_mode=telegram.ParseMode.HTML)
        elif ("GradeReport" in str(rname)):#### it was an else before
            req = br.click_link(url="/Grade/GradeReport")
            br.open(req)
            content = (br.response().read())
            nemo=send_name(rname)
            con=(get_result(content))
            #Send_Text(nemo,id,request="<code>")
            #Send_Text(con, id,request="<code>")
            context.bot.send_message(chat_id=id, text="<code>" + nemo + "</code>",
                                     parse_mode=telegram.ParseMode.HTML)
            if (len(con) <= 4100):
                context.bot.send_message(chat_id=id, text="<code>" + con + "</code>",parse_mode=telegram.ParseMode.HTML)
            else:
                context.bot.send_message(chat_id=id, text="<code>" + con[:4000] + "</code>",
                                         parse_mode=telegram.ParseMode.HTML)
                context.bot.send_message(chat_id=id, text="<code>" + con[4000:] + "</code>",
                                         parse_mode=telegram.ParseMode.HTML)
        else:
            context.bot.send_message(chat_id=id,
                                     text="<code>" + "The username or the password is incorrect, Make sure you submitted both as for example \n Atr/2020/10,2020" + "</code>",
                                     parse_mode=telegram.ParseMode.HTML)
    except:
        context.bot.send_message(chat_id=id,
                                 text="<code>" + "An internal error has occurred please try again later." + "</code>",
                                 parse_mode=telegram.ParseMode.HTML)
        #Send_Text("The username or the password is incorrect, Make sure you submitted both as for example \n Atr/2020/10,2020",id,request="<code>")
def send_name(page):
    read = page
    soup=BeautifulSoup(read,'html.parser')
    total_list=[]
    clean_list=[]
    mesh_string=str()
    for tx in soup.find_all('td'):
        total_list.append(list(tx.stripped_strings))
    for i in total_list:
        clean_list.append(''.join(i))
    for i in clean_list:
        mesh_string+=(str(i)+"\n")
    return(mesh_string)
def get_result(page):
    read=page
    soup = BeautifulSoup(read,'html.parser')
    i_items = [["1"], ["2"], ["3"], ["4"], ["5"], ["6"], ["7"]]
    total_list = []
    clean_list = []
    for tx in soup.find_all('td'):
        total_list.append(list(tx.stripped_strings))
    if "Academic Year" in total_list:
        pass
    mesh_string = ""
    for i in total_list:
        if i == ['Assessment']:
            pass
        elif 'Academic Year' in (str(i)):
            clean_list.append(
                "---------------------------------------")
            clean_list.append(i)
            clean_list.append("---------------------------------------")
        elif "'Academic Status : " in (str(i)) and "SGPA" in (str(i)):
            x = (str(i).find("SGPA"))
            clean_list.append(''.join((str(i)[x:x + 11])))
            if "'Academic Status :" in (str(i)) and "CGPA" in (str(i)):
                x = (str(i).find("CGPA"))
                clean_list.append(''.join((str(i)[x:x + 11])))
                ass = (str(i).find("Academic Status :"))
                clean_list.append(''.join(i[ass:ass + 28]))
        elif "'Academic Status : failed" in (str(i)):
            clean_list.append(''.join("Academic Status : failed"))
        elif i in i_items:
            clean_list.append("---------------------------------------")
        else:
            clean_list.append(''.join(i))
    total_list = None
    for i in clean_list:
        mesh_string += ((str(i)) + "\n")
    return (mesh_string.replace("'",""))
def main():
    updater = Updater("980838714:AAHMrKxUsm7gteNfQ_lff4enrAu956Q8Dgk", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add convrsation handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            Username: [MessageHandler(Filters.text, username)],

            Password: [MessageHandler(Filters.text, password)],

            Formsubmit: [MessageHandler(Filters.text, formsubmit)],
#            Campus_Select:[MessageHandler(Filters.text, Change_Campus)],
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )
 #   dp.add_handler(CommandHandler("Change_Institutes", help))

    dp.add_handler(conv_handler)

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()
