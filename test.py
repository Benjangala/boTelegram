
from telebot.async_telebot import AsyncTeleBot
import asyncio
from threading import Thread
import time
import sqlite3
from gptben4 import QuestionAnswerer


with open("tokens.txt", "r") as file_tokens:
	TOKEN_BOT_TELEGRAM = file_tokens.read()[len("TOKEN_BOT_TELEGRAM") + 1:]

token = TOKEN_BOT_TELEGRAM
pos = ["one", "two", "three"]
bot = AsyncTeleBot(token)
print("Le bot est en écoute...")

async def replyMessage():
	pass

@bot.message_handler(commands=["start", "hello"])
async def welcome(message):
	await bot.reply_to(message, "Bienvenu")

async def task(message):
	question_answer = QuestionAnswerer()
	await asyncio.sleep(3)
	response = await question_answer.ask_question(question=message.text)
	return response

@bot.message_handler(func=lambda msg: True)
async def getAllMessage(message):
	task_eb = asyncio.create_task(task(message))
	print(task_eb)
	response = await task_eb
	print(response)
	print("*"*200)
	print()


asyncio.run(bot.polling())

