# бот by TG: @amok_golub для Алекса
# ヾ(＾-＾)ノ

import aiogram
import datetime
import random
import time
import requests
import io
from textwrap import wrap
from gtts import gTTS
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import asyncio
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.utils.helper import Helper, HelperMode, ListItem
from html import escape
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove
from aiogram.utils.exceptions import BotBlocked
import asyncio
from aiogram.utils.exceptions import Unauthorized
from aiogram.dispatcher import DEFAULT_RATE_LIMIT
from aiogram.dispatcher.handler import CancelHandler, current_handler
from aiogram.dispatcher.middlewares import BaseMiddleware
from io import StringIO
import sys
from aiogram.utils.exceptions import Throttled
import socket
from aiogram.types import ContentType
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher, FSMContext
import os
import re
import json
import base64
import asyncio
import requests
from typing import List
print("[INFO] БОТ ЗАПУЩЕН")
print("[INFO] УДАЧНОГО ИСПОЛЬЗОВАНИЯ")

import db
import cdb
import config
import texts

async def send_adm(dp):
	await bot.send_message(chat_id=config.ADMIN_ID, text='✅ Бот запущен!')

db.CreateDB()
cdb.CreateChatDB()

bot = aiogram.Bot(config.TOKEN, parse_mode='HTML')
dp = aiogram.Dispatcher(bot, storage=MemoryStorage())

@dp.message_handler(commands=['help', 'cmd', 'хелп'], commands_prefix='!./')
async def profcheck(message):
	await message.reply(f"""
Помощь по командам:

/admin_dev id - дает DEV статус (id можно узнать командой /p)
/admin_vip id - дает VIP статус (id можно узнать командой /p)
/p реплай - чекает инфу о юзере по реплаю
/ban реплай - банит
/unban реплай
/mute реплай
/unmute реплай
/help - да
/avip - выводит VIP панель
/adev - выводит панель разработчика

Группа админа: {config.ADMIN_GROUP}
""")

@dp.message_handler(commands=['p', 'п'], commands_prefix='!./')
async def profil_check(message):
	if not message.reply_to_message:
		await message.reply('Сделайте реплай!')
	mrtmfui = message.reply_to_message.from_user.id
	db.cursor.execute(f"SELECT name FROM aleks_bot where id = {mrtmfui}")
	if db.cursor.fetchone() == None:
		db.InsertValues(message.reply_to_message.from_user.first_name, message.reply_to_message.from_user.id)
		await message.reply(f"{message.reply_to_message.from_user.first_name} зарегистрирован!")
	for row in db.cursor.execute(f"SELECT vip FROM aleks_bot where id = {message.reply_to_message.from_user.id}"):
		if row[0] == 'on':
			emot = '✅'
		elif row[0] == 'off':
			emot = '❌'
		await message.reply(f"""
💯Информация о юзере💯

Имя: <code>{message.reply_to_message.from_user.first_name}</code>
Юзернейм: @{message.reply_to_message.from_user.username}
ID Пользователя: <code>{message.reply_to_message.from_user.id}</code>
VIP статус: {emot}
""")

@dp.message_handler(commands=['бан', 'ban'], commands_prefix='!./', is_chat_admin=True)
async def cmd_ban(message):
  comment = " ".join(message.text.split()[1:])
  admin_mention = message.from_user.mention
  banned_user_mention = message.reply_to_message.from_user.mention
  await bot.kick_chat_member(message.chat.id, message.reply_to_message.from_user.id, types.ChatPermissions(False))
  await message.reply(f"Администратор: {admin_mention}\nЗабанил: {banned_user_mention}\nСрок: навсегда\nПричина: {comment}")

@dp.message_handler(commands=['разбан', 'unban'], commands_prefix='!./', is_chat_admin=True)
async def cmd_unban(message):
  await bot.restrict_chat_member(message.chat.id, message.reply_to_message.from_user.id, types.ChatPermissions(True, True, True, True))
  admin_mention = message.from_user.mention
  banned_user_mention = message.reply_to_message.from_user.mention
  await message.reply(f"Администратор: {admin_mention}\nРазбанил: {banned_user_mention}")

@dp.message_handler(commands=['размут', 'unmute'], commands_prefix='!./', is_chat_admin=True)
async def cmd_unmute(message):
  await bot.restrict_chat_member(message.chat.id, message.reply_to_message.from_user.id, types.ChatPermissions(True, True, True, True))
  admin_mention = message.from_user.mention
  muted_user_mention = message.reply_to_message.from_user.mention
  await message.reply(f"Администратор: {admin_mention}\nРазмутил: {muted_user_mention}")

@dp.message_handler(commands=['мут', 'м', 'mute'], commands_prefix='!./', is_chat_admin=True)
async def cmd_mute(message):
	comment = " ".join(message.text.split()[1:])
#	mutime = int(" ".join(message.text.split()[1]))
	admin_mention = message.from_user.mention
	muted_user_mention = message.reply_to_message.from_user.mention
	await bot.restrict_chat_member(message.chat.id, message.reply_to_message.from_user.id, types.ChatPermissions(False), until_date=datetime.timedelta(hours=1))
	await message.reply(f"Администратор: {admin_mention}\nЗамутил: {muted_user_mention}\nСрок: 1ч\nПричина: {comment}")

@dp.message_handler(commands=['start', 'старт'], commands_prefix='!./')
async def cmd_start(message):
	db.cursor.execute(f"SELECT name FROM aleks_bot where id = {message.from_user.id}")
	if db.cursor.fetchone() == None:
		db.InsertValues(message.from_user.first_name, message.from_user.id)
	await message.reply('Иди отсюда, я сплю')

@dp.message_handler(commands=['admins', 'админы', 'адм'], commands_prefix='!./')
async def get_admin_list(message):
	db.cursor.execute(f"SELECT name FROM aleks_bot where id = {message.from_user.id}")
	if db.cursor.fetchone() == None:
		db.InsertValues(message.from_user.first_name, message.from_user.id)
	admins_id = [(admin.user.id, admin.user.full_name) for admin in await bot.get_chat_administrators(chat_id=message.chat.id)]
	admins_list = []
	for ids, name in admins_id:
		admins_list.append("".join(f"[{name}](tg://user?id={ids})"))
	result_list = ""
	l = admins_list
	for admins in admins_list:
		result_list += f'{l.index(admins)+1} >> ' + "".join(admins) + '\n'
	await message.reply("\n😎 Админы :\n" + result_list, parse_mode = 'MARKDOWN')

# випебля
@dp.message_handler(commands=['авип', 'avip'], commands_prefix='!./')
async def vip_cmd(message):
	db.cursor.execute(f"SELECT name FROM aleks_bot where id = {message.from_user.id}")
	if db.cursor.fetchone() == None:
		db.InsertValues(message.from_user.first_name, message.from_user.id)
	ls_vip_kb = InlineKeyboardButton('👉 ЛИЧНАЯ ПЕРЕПИСКА 👈', url=f'http://t.me/{config.BOT_USERNAME}?start')
	ls_vip_kb = InlineKeyboardMarkup().add(ls_vip_kb)
	if message.chat.type == 'supergroup':
		await message.reply('❗Команда работает только в личной переписке с ботом❗', reply_markup=ls_vip_kb)
	if message.chat.type == 'private':
		vip_menu = InlineKeyboardMarkup()
		vip_kb = InlineKeyboardButton(text = '✨ Команды', callback_data = 'vip_kb')
		vip_check_kb = InlineKeyboardButton(text = '🃏 VIP', callback_data = 'vip_check_kb')
		close_kb = InlineKeyboardButton(text = '❌ Закрыть', callback_data = 'close_vip_kb')
		vip_menu.add(vip_check_kb, vip_kb)
		vip_menu.add(close_kb)
		await message.answer('💎 VIP панель 💎', reply_markup=vip_menu)

@dp.callback_query_handler(text='vip_check_kb')
async def handle_cdel_button(c: types.CallbackQuery):
	close_check_menu = InlineKeyboardMarkup()
	close_check_kb = InlineKeyboardButton(text = '🚫 Отмена', callback_data = 'close_check_kb')
	close_check_menu.add(close_check_kb)
	for row in db.cursor.execute(f"SELECT vip FROM aleks_bot where id = {c.from_user.id}"):
		if row[0] == 'on':
			emot = 'ИМЕЕТСЯ ✅'
		elif row[0] == 'off':
			emot = f'ОТСУТСТВУЕТ ❌\n\nКупить можно в лс у {config.ADMIN_NAME}! \n Если у вас спамбан, то вам сюда\n 👉 {config.SPAMBAN_ADMIN}'
		await c.message.edit_text(f'VIP статус: {emot}', disable_web_page_preview=True, reply_markup=close_check_menu)

@dp.callback_query_handler(text='vip_kb')
async def handle_cdel_button(c: types.CallbackQuery):
	close_check_menu = InlineKeyboardMarkup()
	close_check_kb = InlineKeyboardButton(text = '🚫 Отмена', callback_data = 'close_check_kb')
	close_check_menu.add(close_check_kb)
	await c.message.edit_text(f"""
✨~ VIP команды ~✨

Кодер отдыхает, команды пригяли ислам
😌🤞😢

🏓 Предлагайте свои идеи в лс админа ({config.ADMIN_NAME})
💕 Если у вас спамбан, пишите сююда
👉 {config.SPAMBAN_ADMIN}
""", disable_web_page_preview=True, reply_markup=close_check_menu)

@dp.callback_query_handler(text='close_check_kb')
async def handle_cutton(c: types.CallbackQuery):
	vip_menu = InlineKeyboardMarkup()
	vip_kb = InlineKeyboardButton(text = '✨ Команды', callback_data = 'vip_kb')
	vip_check_kb = InlineKeyboardButton(text = '🃏 Проверка', callback_data = 'vip_check_kb')
	close_kb = InlineKeyboardButton(text = '❌ Закрыть', callback_data = 'close_vip_kb')
	vip_menu.add(vip_check_kb, vip_kb)
	vip_menu.add(close_kb)
	await c.message.edit_text('💎 VIP панель 💎', reply_markup=vip_menu)

@dp.callback_query_handler(text='close_vip_kb')
async def handle_cdel_button(c: types.CallbackQuery):
	await c.message.delete()

# девборд
@dp.message_handler(commands=['адев', 'adev'], commands_prefix='!./')
async def adm_ui(message):
	db.cursor.execute(f"SELECT name FROM aleks_bot where id = {message.from_user.id}")
	if db.cursor.fetchone() == None:
		db.InsertValues(message.from_user.first_name, message.from_user.id)
	for row in db.cursor.execute(f"SELECT id, dev FROM aleks_bot where id = {message.from_user.id}"):
			if row[1] == 'off':
				await message.reply('Недостаточно прав! 😍')
			if row[1] == 'on':
				admin_menu = InlineKeyboardMarkup()
				statistics_bt = InlineKeyboardButton(text = '📊 Статистика', callback_data = 'stat')
				test_bt = InlineKeyboardButton(text = 'TID_TEST', callback_data = 'test_eb')
				mail_bt = InlineKeyboardButton(text = '✉️ Рассылка', callback_data = 'rassilka')
				mail_bt2 = InlineKeyboardButton(text = '💬 Чат рассылка', callback_data = 'chat_rassilka')
				cancel_del_menu = InlineKeyboardMarkup()
				cancel_del_bt = InlineKeyboardButton(text = '❌ Закрыть ❌', callback_data = 'cancel_del')
				admin_menu.add(statistics_bt)
				admin_menu.add(mail_bt, mail_bt2)
				admin_menu.add(cancel_del_bt)
				await message.answer('🛠 Выберите пункт меню:', reply_markup=admin_menu)

@dp.callback_query_handler(text='cancel_del')
async def handle_cdel_button(c: types.CallbackQuery):
	for row in db.cursor.execute(f"SELECT id, dev FROM aleks_bot where id = {c.from_user.id}"):
			if row[1] == 'off':
				pass
			if row[1] == 'on':
				await c.message.delete()

@dp.callback_query_handler(text='stat')
async def handle_stat_button(c: types.CallbackQuery):
	for row in db.cursor.execute(f"SELECT id, dev FROM aleks_bot where id = {c.from_user.id}"):
		if row[1] == 'off':
			pass
		if row[1] == 'on':
			cancel_menu = InlineKeyboardMarkup()
			cancel_bt = InlineKeyboardButton(text = '🚫 Отмена', callback_data = 'cancel')
			cancel_menu.add(cancel_bt)
			db.cursor.execute("SELECT id FROM aleks_bot")
			row = db.cursor.fetchall()
			users = row
			cdb.cursor.execute("SELECT chat_id FROM chats_aleks")
			roww = db.cursor.fetchall()
			groups = roww
			await c.message.edit_text(f'👤 Юзеров в боте: {str(len(users))}\n➖➖➖➖➖➖➖➖\n💬 Чатов в боте: {str(len(groups))}', reply_markup = cancel_menu)

@dp.callback_query_handler(text='cancel')
async def cancel_wnum_button_handler(c: types.callback_query):
	for row in db.cursor.execute(f"SELECT id, dev FROM aleks_bot where id = {c.from_user.id}"):
		if row[1] == 'off':
			pass
		if row[1] == 'on':
			admin_menu = InlineKeyboardMarkup()
			statistics_bt = InlineKeyboardButton(text = '🍵 Статистика', callback_data = 'stat')
			test_bt = InlineKeyboardButton(text = 'TID_TEST', callback_data = 'test_eb')
			mail_bt = InlineKeyboardButton(text = '✉️ Рассылка', callback_data = 'rassilka')
			mail_bt2 = InlineKeyboardButton(text = '💬 Чат рассылка', callback_data = 'chat_rassilka')
			cancel_del_menu = InlineKeyboardMarkup()
			cancel_del_bt = InlineKeyboardButton(text = '❌ Закрыть ❌', callback_data = 'cancel_del')
			admin_menu.add(statistics_bt)
			admin_menu.add(mail_bt, mail_bt2)
			admin_menu.add(cancel_del_bt)
			await c.message.edit_text('🛠 Выберите пункт меню:', reply_markup=admin_menu)
			
# ддев
@dp.message_handler(commands=['admin_dev'], commands_prefix='!./')
async def give_dev(message):
	try:
		for row in db.cursor.execute(f"SELECT id, dev FROM aleks_bot where id = {message.from_user.id}"):
			dev_id_leak = int(" ".join(message.text.split()[1:]))
			if row[0] == message.from_user.id:
				if row[1] == 'off':
					await message.reply(f'Вы не разработчик 😯🖕')
				if row[1] == 'on':
					for row in db.cursor.execute(f"SELECT id, dev FROM aleks_bot where id = {dev_id_leak}"):
						if row[0] == dev_id_leak:
							if row[1] == 'on':
								db.cursor.execute(f'UPDATE aleks_bot SET dev = "off" where id = {dev_id_leak}')
								db.con.commit()
								await message.reply(f'Пользователю <code>{dev_id_leak}</code> отключен DEV статус 😘')
							if row[1] == 'off':
								db.cursor.execute(f'UPDATE aleks_bot SET dev = "on" where id = {dev_id_leak}')
								db.con.commit()
								await message.reply(f'Пользователю <code>{dev_id_leak}</code> подключен DEV статус 😎')
	except:
		await message.reply(f'Ошибка!!!')

# двип
@dp.message_handler(commands=['admin_vip'], commands_prefix='!./')
async def give_vip(message):
	try:
		for row in db.cursor.execute(f"SELECT id, dev FROM aleks_bot where id = {message.from_user.id}"):
			vip_id_leak = int(" ".join(message.text.split()[1:]))
			if row[0] == message.from_user.id:
				if row[1] == 'off':
					await message.reply(f'Вы не разработчик 😯🖕')
				if row[1] == 'on':
					for row in db.cursor.execute(f"SELECT id, vip FROM aleks_bot where id = {vip_id_leak}"):
						if row[0] == vip_id_leak:
							if row[1] == 'on':
								db.cursor.execute(f'UPDATE aleks_bot SET vip = "off" where id = {vip_id_leak}')
								db.con.commit()
								await message.reply(f'Пользователю <code>{vip_id_leak}</code> отключен VIP статус 😘')
							if row[1] == 'off':
								db.cursor.execute(f'UPDATE aleks_bot SET vip = "on" where id = {vip_id_leak}')
								db.con.commit()
								await message.reply(f'Пользователю <code>{vip_id_leak}</code> подключен VIP статус 🤑')
	except:
		await message.reply(f'Ошибка!!!')

class Rass(StatesGroup):
	msg = State()

class ChRass(StatesGroup):
	msg = State()

@dp.callback_query_handler(text="rassilka")
async def send_rass(call: types.CallbackQuery):
	for row in db.cursor.execute(f"SELECT id, dev FROM aleks_bot where id = {call.from_user.id}"):
		if row[0] == call.from_user.id:
			if row[1] == 'off':
				pass
			elif row[1] == 'on':
				id = call.from_user.id
				await call.message.answer(text='🖋 Введите текст/фото для рассылки:')
				await Rass.msg.set()

@dp.message_handler(content_types=ContentType.ANY, state=Rass.msg)
async def rassilka_msgl(message: types.Message, state: FSMContext):
	await state.finish()
	db.cursor.execute(f"SELECT id FROM aleks_bot")
	users_query = db.cursor.fetchall()
	user_ids = [user[0] for user in users_query]
	confirm = []
	decline = []
	bot_msg = await message.answer(f'Рассылка началась...')
	for i in user_ids:
		try:
			await message.copy_to(i)
			confirm.append(i)
		except:
			decline.append(i)
		await asyncio.sleep(0.3)
	await bot_msg.edit_text(f'📣 Рассылка завершена!\n\n✅ Успешно: {len(confirm)}\n❌ Неуспешно: {len(decline)}')

@dp.message_handler(content_types=ContentType.ANY, state=ChRass.msg)
async def rassilka_msgl(message: types.Message, state: FSMContext):
	await state.finish()
	cdb.cursor.execute(f"SELECT chat_id FROM chats_aleks")
	chats_query = cdb.cursor.fetchall()
	chat_ids = [chat[0] for chat in chats_query]
	confirm = []
	decline = []
	bot_msg = await message.answer(f'Рассылка началась...')
	for i in chat_ids:
		try:
			await message.copy_to(i)
			confirm.append(i)
		except:
			decline.append(i)
		await asyncio.sleep(0.3)
	await bot_msg.edit_text(f'📣 Рассылка завершена!\n\n✅ Успешно: {len(confirm)}\n❌ Неуспешно: {len(decline)}')

@dp.callback_query_handler(text="chat_rassilka")
async def send_rass(call: types.CallbackQuery):
	for row in cdb.cursor.execute(f"SELECT id, dev FROM aleks_bot where id = {call.from_user.id}"):
		if row[0] == call.from_user.id:
			if row[1] == 'off':
				pass
			if row[1] == 'on':
				id = call.from_user.id
				await call.message.answer(text='🖋 Введите текст/фото для рассылки:')
				await ChRass.msg.set()

# реггггг
@dp.message_handler(commands=['regg', 'регг'], commands_prefix='!./')
async def gg1db_join(message):
	mrtmfui = message.reply_to_message.from_user.id
	db.cursor.execute(f"SELECT name FROM aleks_bot where id = {mrtmfui}")
	if db.cursor.fetchone() == None:
		db.InsertValues(message.reply_to_message.from_user.first_name, message.reply_to_message.from_user.id)
		await message.reply(f"{message.reply_to_message.from_user.first_name} зарегистрирован!")

@dp.message_handler(commands=['reg', 'рег'], commands_prefix='!./')
async def db_join(message):
	db.cursor.execute(f"SELECT name FROM aleks_bot where id = {message.from_user.id}")
	if db.cursor.fetchone() == None:
		db.InsertValues(message.from_user.first_name, message.from_user.id)
		await message.reply(f"{message.from_user.first_name} зарегистрирован!")

@dp.message_handler(commands=['bind', 'привязать', 'привязка', 'пр'], commands_prefix='!./')
async def privazka(message):
	db.cursor.execute(f"SELECT name FROM aleks_bot where id = {message.from_user.id}")
	if db.cursor.fetchone() == None:
		db.InsertValues(message.from_user.first_name, message.from_user.id)
	if message.chat.type == 'supergroup':
		cdb.cursor.execute(f"SELECT chat_name, chat_id FROM chats_aleks where chat_id = {message.chat.id}")
		if cdb.cursor.fetchone() == None:
			cdb.InsertChatValues(message.chat.title, message.chat.id)
			await message.reply('Вы привязали бота к чату 🛡')
		else:
			await message.reply('Бот уже привязан к чату ✅')
	if message.chat.type == 'private':
		await message.reply('Введите эту команду в своем чате 👻')

@dp.message_handler(content_types=["new_chat_members"])
async def new_chat_member(message: types.Message):
	db.cursor.execute(f"SELECT name FROM aleks_bot where id = {message.from_user.id}")
	if db.cursor.fetchone() == None:
		db.InsertValues(message.from_user.first_name, message.from_user.id)
		await message.delete()
		await message.reply(f"""
👤 [{message.new_chat_members[0].full_name}](tg://user?id={message.new_chat_members[0].id})
🆔 - <code>{message.from_user.id}<\code>
🌀 Новый пользыватель зарегистрирован!
🔷Добро пожаловать в чат!
""")
	else:
		await message.delete()
		await message.reply(f"""
👤 [{message.new_chat_members[0].full_name}](tg://user?id={message.new_chat_members[0].id})
🆔 - <code>{message.from_user.id}<\code>
🔷Добро пожаловать в чат!
""", parse_mode='HTML')

@dp.message_handler(content_types=["left_chat_member"])
async def leave_chat(message: types.Message):
	await message.delete()


# все бот написан, иду нюхать бебру :D

# поллинг228
aiogram.utils.executor.start_polling(dp, on_startup=send_adm, skip_updates=True)