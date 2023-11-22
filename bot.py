#!venv/bin/python

import config
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from db import BotDB
# importing scanners
import wappalyzer
import nikto
import subdomains
import dirbuster


# initializing bot
bot = Bot(config.api_key)
dp = Dispatcher(bot)

# default target
target = ''

# initializing DB
BotDB = BotDB("database.db")

# default messages
help_message = '''<b>💻 Web Application Scanner</b>\n\n<i>Help List</i>\n/help - to get this menu\n/target [http://TARGET_URL] - set a website to scan\n/scan - use all scanners without nikto\n/wappalyzer - use wappalyzer scanner to scan for technologies\n/nikto - use nikto vulnerability scanner(~15min)\n/subdomains - to scan for subdomains by certificates fingerprint\n/dirbuster - to scan for directories and files'''
start_message = '''<b>💻 Web Application Scanner</b>\n<i>by: 🧛🏻‍♂️@darth_alchemist 🏎@a_nurbollat</i>\n\nFind out the technology stack of any website. Check for any security issues and misconfigurations of the website.\n\n❗️Only for legal and educational purposes only❗️\n\nℹ️ Run /help to start\n\n'''


# Start
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    # user authentication
    if(not BotDB.user_exists(message.from_user.id)):
        BotDB.add_user(message.from_user.id)
    
    await message.answer_photo('https://moonlock.com/2023/07/white-hat-hacking-header.jpeg', caption=start_message, parse_mode="html")



# Set Target
@dp.message_handler(commands=('target', 't'), commands_prefix = "/")
async def start(message: types.Message):
    text = message.text
    text = text.replace('/target ', '')
    text = text.replace('/t ', '')
    global target
    target = text

    await message.answer("Target set to: "+target, disable_web_page_preview=True)


# Help
@dp.message_handler(commands=['help'])
async def start(message: types.Message):
    await message.answer(help_message, parse_mode='html')



# Wappalyzer
@dp.message_handler(commands=['wappalyzer'])
async def start(message: types.Message):
    global target
    if target:
        await message.answer(f'Started Wappalyzer scan on {target}, please wait...', disable_web_page_preview=True)
        wappalyzer_output = wappalyzer.wappalyzer_scan(target)
        await message.answer('<b>Wappalyzer result for: '+target+'</b>\n'+wappalyzer_output, parse_mode='html', disable_web_page_preview=True)
        BotDB.add_scan(message.from_user.id, target, 'wappalyzer', wappalyzer_output)
    else:
        await message.answer("You should specify the target first!\nTo do that use: /target <target URL>")



# nikto
@dp.message_handler(commands=['nikto'])
async def start(message: types.Message):
    global target
    if target:
        await message.answer(f'Started Nikto scan on {target}, please wait...', disable_web_page_preview=True)
        nikto_output = nikto.nikto_scan(target)
        await message.answer('<b>Nikto result for: '+target+'</b>\n'+nikto_output, parse_mode='html', disable_web_page_preview=True)
        BotDB.add_scan(message.from_user.id, target, 'nikto', nikto_output)
    else:
        await message.answer("You should specify the target first!\nTo do that use: /target <target URL>")


# subdomains
@dp.message_handler(commands=['subdomains'])
async def start(message: types.Message):
    global target
    if target:
        await message.answer(f'Started searching subdomains of {target}, please wait...', disable_web_page_preview=True)
        new_target = target.split('//')[1]
        subdomains_output = subdomains.subdomains_scan(new_target)
        await message.answer('<b>Found subdomains for: '+target+'</b>\n'+subdomains_output, parse_mode='html', disable_web_page_preview=True)
        BotDB.add_scan(message.from_user.id, target, 'subdomains', subdomains_output)
    else:
        await message.answer("You should specify the target first!\nTo do that use: /target <target URL>")


# dirbuster
@dp.message_handler(commands=['dirbuster'])
async def start(message: types.Message):
    global target
    if target:
        await message.answer(f'Started directory busting of {target}, please wait...', disable_web_page_preview=True)
        dirbuster_output = dirbuster.dirbuster_scan(target)
        await message.answer('<b>Found files and directories for: '+target+'</b>\n'+dirbuster_output, parse_mode='html', disable_web_page_preview=True)
        BotDB.add_scan(message.from_user.id, target, 'dirbuster', dirbuster_output)
    else:
        await message.answer("You should specify the target first!\nTo do that use: /target <target URL>")


# get scanned targets
@dp.message_handler(commands=['get_targets'])
async def start(message: types.Message):
    targets = BotDB.get_targets(message.from_user.id)
    await message.answer('<b>All targets:</b>\n'+targets, disable_web_page_preview=True, parse_mode='html')


# get scan results
# usage: /get_results <target url>
@dp.message_handler(commands=['get_results'])
async def start(message: types.Message):
    target = message.text.split()[1]
    wappalyzer_output = BotDB.get_scans(message.from_user.id, target, 'wappalyzer')[0][0]
    subdomains_output = BotDB.get_scans(message.from_user.id, target, 'subdomains')[0][0]
    dirbuster_output = BotDB.get_scans(message.from_user.id, target, 'dirbuster')[0][0]
    
    await message.answer(f'<b><i>All results for: {target}</i></b>', disable_web_page_preview=True, parse_mode='html')
    await message.answer('<b>Wappalyzer:</b>\n'+wappalyzer_output, disable_web_page_preview=True, parse_mode='html')
    await message.answer('<b>Subdomains:</b>\n'+subdomains_output, disable_web_page_preview=True, parse_mode='html')
    await message.answer('<b>Dirbuster:</b>\n'+dirbuster_output, disable_web_page_preview=True, parse_mode='html')
    


# start the bot
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

