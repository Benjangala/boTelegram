
import random
import time
import os

from telebot.async_telebot import AsyncTeleBot
import asyncio
import aiohttp
import asyncio
import json

import translate_text
from ImageGenerator import lexica_ai
from SearchGoogleImage import searchImagesGoogle
from AudioVocal import getAudio
from gptben4 import QuestionAnswerer
from database import Users

with open("tokens.txt", "r") as file_tokens:
	TOKEN_BOT_TELEGRAM = file_tokens.read()[len("TOKEN_BOT_TELEGRAM") + 1:]

bot = AsyncTeleBot(TOKEN_BOT_TELEGRAM)
print(f"Le bot {bot} est en écoute....")

async def sendImages(id_user, url):
	await bot.send_photo(chat_id=id_user, photo=url)

async def sendAudio(id_user, path_audio):
	await bot.send_audio(chat_id=id_user, audio=open(path_audio, "rb"))

async def getResponse(message) -> str:
	question = message.text
	await asyncio.sleep(2)
	question_answer = QuestionAnswerer()
	response = await question_answer.ask_question(question=question)
	return response 

async def getDataUser(message):
	data_user = message.from_user
	name_user = data_user.first_name
	last_name_user = data_user.last_name
	id_telegram = data_user.id

	user_database = Users()
	postion_data = await user_database.createUser(name_user, last_name_user, id_telegram)
	if postion_data:
		print(f"L'enregistrement de: {name_user} a été fait avec succès")
	else:
		print(f"L'enregistrement de: {name_user} a été une échec")


def getTextTranslate(texte: str)->str:
	texte_translate = translate_text.translator(texte=texte)
	return texte_translate

@bot.message_handler(commands=["start", "help"])
async def welcomeMessage(message):
	msg = message.text
	await getDataUser(message)
	first_msg = """
		Welcome to the bot.
		Ask all your questions and generate your images.
		To see our services send /services
	"""
	first_msg = first_msg + "\n\n" + getTextTranslate(texte=first_msg)
	if msg == "/start" or msg == "help":
		await bot.reply_to(message,first_msg )


@bot.message_handler(commands=["services"])
async def servicesMessage(message):
	msg = message.text
	with open("FilesText/services.txt", "r") as file_service:
		msg_service = file_service.read()
	msg_service = msg_service + "\n\n" + getTextTranslate(texte=msg_service)
	if msg:
		await bot.reply_to(message, msg_service)


@bot.message_handler(commands=["img"])
async def generateImage(message):
	try:
		msg = message.text
		id_user = message.chat.id
		if msg == "/img":
			with open("FilesText/image_texte.txt", "r") as file_img:
				msg_img = file_img.read()
			msg_img = msg_img + "\n\n" + getTextTranslate(texte=msg_img)
			await bot.reply_to(message, msg_img)
		else:
			if not msg.isspace():
				response_img = "Veuillez patientez pendant que le bot créé vos images..."
				new_texte = msg[3:]
				image_data =  lexica_ai.Lexica(prompt=new_texte).images()
				urls_images = [random.choice(image_data) for i in range(5)]

				time.sleep(5)
				#Envoi des images généré
				for url in urls_images:
					await sendImages(id_user, url)
			else:
				await bot.reply_to(message, "Votre demande est vide")
	except Exception as error:
		print(f"L'erreur est dans la fonction generateImage et voici l'erreur {error}")
		print()
		pass


@bot.message_handler(commands=["simg"])
async def searchImageGoogle(message):
	try:
		msg = message.text
		id_user = message.chat.id
		if msg == "/simg":
			with open("FilesText/google_image_texte.txt", "r") as file_simg:
				msg_simg = file_simg.read()
			msg_simg = msg_simg + "\n\n" + getTextTranslate(texte=msg_simg)
			await bot.reply_to(message, msg_simg)

		else:
			msg_simg = msg[5:]
			if not msg_simg.isspace():
				urls_img_google = [random.choice(searchImagesGoogle(msg_simg)) for i in range(5)]
				for url in urls_img_google:
					await sendImages(id_user, url)
			else:
				await bot.reply_to(message, "Votre demande est vide")
	except Exception as error:
		print(f"L'errer est dans la fonction searchImagesGoogle et voici l'erreur {error}")
		print()


@bot.message_handler(commands=["tts"])
async def translateTextAudio(message):
	try:
		msg = message.text
		id_user = message.chat.id
		if msg == "/tts":
			with open("FilesText/audio_texte.txt", "r") as file_tts:
				msg_tts = file_tts.read()
			msg_tts = getTextTranslate(texte=msg_tts) + "\n\n" + msg_tts
			await bot.reply_to(message, msg_tts)
		else:
			if not msg.isspace():
				msg = msg[4:]
				path_vocale = getAudio(msg)
				print(path_vocale)
				if path_vocale:
					await sendAudio(id_user, path_vocale)
					os.remove(path_vocale)
	except Exception as error:
		print(f"Il y a eu une erreur dans la fonction translateTextAudio et l'erreur est {error}")
		print()

@bot.message_handler(commands=["askvo"])
async def getResponseAudio(message):
	msg = message.text
	id_user = message.chat.id
	if msg == "/askvo":
		bot.reply_to(message, "Cette petite fonctionnalité permert de repondre au question avec un format vocal")
	
	else:
		if not msg.isspace():
			response = getResponse(message)[5:]
			path_vocale = getAudio(response)
			if path_vocale:
				await sendAudio(id_user, path_vocale)


@bot.message_handler(func=lambda message: True)
async def getAllMessage(message):
	try:
		msg = message.text
		last_msg = await bot.reply_to(message, "Veuillez patientez pendant que je reflechi...")
		id_user = last_msg.chat.id
		id_msg = last_msg.message_id

		if msg.startswith("/"):
			msg_error = "Service non réconnu. Cliquez ici pour voir les commandes /services"
			await bot.edit_message_text(chat_id=id_user, message_id=id_msg, text=msg_error)

		else:
			if not msg.isspace():		
				response_question = asyncio.create_task(getResponse(message))
				response_question = await response_question
				if response_question:
					await bot.edit_message_text(chat_id=id_user, message_id=id_msg, text=response_question)
				else:
					await bot.edit_message_text(chat_id=id_user, message_id=id_msg, text="Veuillez renvoyer votre question")
			else:
				await bot.reply_to(message, "Votre question est vide")
	except Exception as error:
		print("Il y a eu une erreur dans la fonction getAllMessage et l'erreur est: {error}")



asyncio.run(bot.polling())



