import json
import os
from datetime import datetime

import boto3
import telebot

# the environment vars have to set on lambda AWS configuration
API_KEY = os.environ['API_KEY']
print(API_KEY)
bot = telebot.TeleBot(API_KEY)

# URL of your choice
# Remember set your webhook on Telegram Account
WBH_URL = 'https://2bomdo636e.execute-api.us-east-1.amazonaws.com/default/axie-telegram-bot'
bot.set_webhook(url=WBH_URL)  # Setting the Webhook.
print(bot)

table = boto3.resource('dynamodb').Table('axie-scholar')

from axie import (
    QRCodeManager, AxiePaymentsManager, AxieClaimsManager
)

from axie.utils import load_json, CHAT_ID_SCHOLAR_GROUP

from axie.utils_messages import *
from axie.mongodb_dao import *


def lambda_handler(event, context):
    print("EVENT")
    print(event)

    # 4 PRUEBAS TEST LAMBDA
    # body = event["body"]
    # APLICA
    body = json.loads(event['body'])
    print("BODY")
    print(body)

    chat_id, fname_sender, is_text, text, is_command, username = message_check_in(body)
    print("is command?")
    print(is_command)
    logging.info(f'chat_id -> {chat_id}')
    logging.info(f'CHAT_ID_SCHOLAR_GROUP -> {CHAT_ID_SCHOLAR_GROUP}')

    # payments_file_path = args['<payments_file>']
    payments_file_path = 'payments.json'
    # secrets_file_path = args['<secrets_file>']
    secrets_file_path = 'secrets.json'
    is_public_cmd = False

    if chat_id == CHAT_ID_SCHOLAR_GROUP:
        logging.info('SOLO COMANDOS DE CARACTER PUBLICO')
        is_public_cmd = True
        logging.info(f'is_public_cmd -> {is_public_cmd}')

    if is_text:
        if is_command and not is_public_cmd:
            splitted_text = text.split()
            print('text split')
            print(splitted_text)
            command = splitted_text[0].lower().strip()
            if not exists_username(chat_id, username):
                return

            if not belong_to_scholar_group(chat_id):
                msg_not_belong_to_scholar_group(chat_id, bot, fname_sender)
                return


            if command == "/time":
                current_time = datetime.strftime(datetime.now(), "%H:%M:%S")
                logging.info('SE ENTREGA HORA')
                bot.send_message(chat_id, "Right now its {} UTC.".format(current_time))
            elif command == "/set_pin":
                logging.info('INIT SETPIN')
                set_pin(splitted_text, chat_id, username, payments_file_path)
            elif command == "/get_pin":
                logging.info('INIT GETPIN')
                get_pin(splitted_text, chat_id, username, payments_file_path)
            elif command == "/get_qr":
                logging.info('INIT GETQR')
                get_qr(splitted_text, chat_id, username, payments_file_path, secrets_file_path)
            elif command == "/get_payout":
                logging.info('INIT PAYMENT')
                get_payout(splitted_text, chat_id, username, payments_file_path, secrets_file_path, False)
            elif command == "/transfer_farmed_scholar_slp":
                logging.info('TRANSFER')
                get_payout(splitted_text, chat_id, username, payments_file_path, secrets_file_path, True)
            elif command == "/get_claim":
                logging.info('INIT CLAIM')
                get_claim(splitted_text, chat_id, username, payments_file_path, secrets_file_path)
                # payments_file_path = args['<payments_file>']
            # elif command == "/get_claim":
            #     logging.info('INIT CLAIM')
            #     bot.send_message(chat_id, "CLAIM Do It !!!")
            #     # if len(splitted_text) >= 3:
            #     #     logging.info('Requesting Payment !!!')
            #     #     logging.info('I shall help you generate your payments file')
            #     #     csv_file_path = args['<csv_file>']
            #     #     payments_file_path = args.get('<payments_file>')
            #     #     if (payments_file_path and check_file(payments_file_path) and
            #     #             check_file(csv_file_path) or not payments_file_path and check_file(csv_file_path)):
            #     #         generate_payments_file(csv_file_path, payments_file_path)
            #     #     else:
            #     #         logging.critical("Please review your file paths and re-try.")
            #     #
            #     #
            #     #     bot.send_message(chat_id, "Payment Do It !!!")
            #     # else:
            #     #     logging.info('CLAIM is not ready yet !!!')
            #     #     bot.send_message(chat_id, "CLAIM is not ready yet !!!")
            # elif command == "/get_payment":
            #     logging.info('INIT PAYMENT')
            #     # bot.send_message(chat_id, "PAYMENT Do It !!!")
            #     # if len(splitted_text) >= 3:
            #     #     logging.info('Requesting Payment !!!')
            #     #     logging.info('I shall help you generate your payments file')
            #     #     csv_file_path = args['<csv_file>']
            #     #     payments_file_path = args.get('<payments_file>')
            #     #     if (payments_file_path and check_file(payments_file_path) and
            #     #             check_file(csv_file_path) or not payments_file_path and check_file(csv_file_path)):
            #     #         generate_payments_file(csv_file_path, payments_file_path)
            #     #     else:
            #     #         logging.critical("Please review your file paths and re-try.")
            #     #
            #     #
            #     #     bot.send_message(chat_id, "Payment Do It !!!")
            #     # else:
            #     #     logging.info('CLAIM is not ready yet !!!')
            #     #     bot.send_message(chat_id, "CLAIM is not ready yet !!!")
            else:
                pass
        else:
            logging.info('Comandos Publicos')
    else:
        pass


def set_pin(splitted_text, chat_id, username, payments_file_path):
    payments = load_json(payments_file_path)

    if len(splitted_text) >= 3:
        wronin = splitted_text[1].lower().strip()
        pin = splitted_text[2]
        lpin = len(pin)
        logging.info(f'Largo del PIN -> {lpin}')
        if not lpin == 6:
            msg_pin_length(chat_id, bot, "")
            return

        response = table.get_item(Key={'username': username})
        logging.info(f'Updating Scholar on MONGODB -> {response} !!')
        is_item = 'Item' in response

        if is_item:
            item = response['Item']
            for scholar in payments['Scholars']:
                if wronin == scholar['ScholarPayoutAddress'] and username.lower() == scholar['TelegramID'].lower():
                    put_item(item)
                    bot.send_message(chat_id,
                                     "Your PIN code has been established !!!\n\n-------------------\n\nTu codigo PIN ha sido establecido !!!")
                    return
                elif wronin != scholar['ScholarPayoutAddress'] and username.lower() == scholar['TelegramID'].lower():
                    msg_incorrect_input_data(chat_id, bot, "wronin_error")
                    return
        else:
            for scholar in payments['Scholars']:
                if wronin == scholar['ScholarPayoutAddress'] and username.lower() == scholar['TelegramID'].lower():
                    item = {
                        'username': username,
                        'wronin': wronin,
                        'account': scholar['Name'],
                        'token_exp': 347383212,
                        'jwt': "",
                        'pin': pin
                    }
                    put_item(item)
                    bot.send_message(chat_id,
                                     "Your PIN code has been established !!!\n\n-------------------\n\nTu codigo PIN ha sido establecido !!!")
                    return
                else:
                    pass
        error_msg_need_configuration(chat_id, bot, None)
    else:
        error_msg_format(chat_id, bot, "setpin")


def get_pin(splitted_text, chat_id, username, payments_file_path):
    payments = load_json(payments_file_path)

    if len(splitted_text) >= 2:
        wronin = splitted_text[1].lower().strip()
        for scholar in payments['Scholars']:
            if wronin == scholar['ScholarPayoutAddress'] and username.lower() == scholar['TelegramID'].lower():
                #TODO
                response = table.get_item(Key={'username': username})
                # response = get_item(username)
                logging.info(f'Updating Scholar on MONGODB -> {response} !!')
                if "Item" in response:
                    item = response['Item']
                    pin = item['pin']
                    logging.info(f'GET Scholar PIN -> {pin} !!')
                    msg_pin_deliver(chat_id, bot, pin)
                    return
                else:
                    error_msg_pin_created(chat_id, bot)
                    return
            elif wronin != scholar['ScholarPayoutAddress'] and username.lower() == scholar['TelegramID'].lower():
                logging.warning(f'Ronin Wallet No Corresponde !!')
                error_msg_data_not_correspond(chat_id, bot, "getpin")
                return
        error_msg_need_configuration(chat_id, bot, "")
    else:
        error_msg_format(chat_id, bot, "getpin")


def get_qr(splitted_text, chat_id, username, payments_file_path, secrets_file_path):
    if len(splitted_text) >= 3:
        # Generate QR codes
        logging.info('I shall generate QR codes')
        wronin = splitted_text[1].lower().strip()
        pin_user = splitted_text[2]

        is_pin, pin_db, item = check_if_exist_pin(chat_id, username)
        if not is_pin:
            return

        logging.info(f'payments_file {payments_file_path}')
        logging.info(f'secrets_file {secrets_file_path}')
        logging.info(f'bot {bot}')
        logging.info(f'chat_id {chat_id}')
        logging.info(f'wronin {wronin}')
        logging.info(f'pin {pin_user}')
        logging.info(f'pin_db {pin_db}')
        logging.info(f'username {username}')

        if check_file(payments_file_path) and check_file(secrets_file_path):
            qr = QRCodeManager(payments_file_path, secrets_file_path, bot, chat_id, wronin, pin_user, username, pin_db, item)
            logging.info(f'IS GEN_QR {qr.gen_qr}')
            logging.info(f'is_qr_valid {qr.is_qr_valid}')
            logging.info(f'is_pin_error {qr.is_pin_error}')
            logging.info(f'is_wronin_error {qr.is_wronin_error}')

            if qr.gen_qr:
                logging.info('SE PROCEDE A SAVE QR !!!')
                if qr.is_pin_error:
                    msg_incorrect_input_data(chat_id, bot, "pin_error")
                elif qr.is_wronin_error:
                    msg_incorrect_input_data(chat_id, bot, "wronin_error")
                else:
                    qr.execute()
            else:
                if qr.is_qr_valid:
                    msg_qr_still_active(chat_id, bot, None)
                    return
                elif qr.is_pin_error:
                    msg_incorrect_input_data(chat_id, bot, "pin_error")
                    return
                elif qr.is_wronin_error:
                    msg_incorrect_input_data(chat_id, bot, "wronin_error")
                    return
                else:
                    error_msg_data_not_correspond(chat_id, bot, "")
            # logging.info('QR GENERADO !!!')
            # bot.send_message(chat_id, "new QR !!!")
        else:
            logging.critical("Please review your file paths and re-try.")
            logging.critical('SERVICE ERROR !!!')
            error_msg_service(chat_id, bot, "")
    else:
        logging.critical('Solicitud con Formato NO RESPETADO !!!')
        error_msg_format(chat_id, bot, None)

def get_payout(splitted_text, chat_id, username, payments_file_path, secrets_file_path, is_transfer):
    if len(splitted_text) >= 3 or is_transfer:
        pin_user = ""
        pin_db = ""
        item = None
        # Generate QR codes
        wronin = splitted_text[1].lower().strip()
        if not is_transfer:
            pin_user = splitted_text[2]
            is_pin, pin_db, item = check_if_exist_pin(chat_id, username)
            if not is_pin:
                return

        logging.info(f'payments_file {payments_file_path}')
        logging.info(f'secrets_file {secrets_file_path}')
        logging.info(f'bot {bot}')
        logging.info(f'chat_id {chat_id}')
        logging.info(f'wronin {wronin}')
        logging.info(f'pin {pin_user}')
        logging.info(f'pin_db {pin_db}')
        logging.info(f'username {username}')

        logging.info("I shall help you pay!")
        # payments_file_path = args['<payments_file>']
        payments_file_path = payments_file_path
        # secrets_file_path = args['<secrets_file>']
        secrets_file_path = secrets_file_path
        if check_file(payments_file_path) and check_file(secrets_file_path):
            logging.info('I shall pay my scholars!')
            # if args['--yes']:
            #     logging.info("Automatic acceptance active, it won't ask before each execution")
            apm = AxiePaymentsManager(payments_file_path, secrets_file_path, True, bot, chat_id, wronin, pin_user, username, pin_db, item, is_transfer)
            apm.verify_inputs()
            apm.prepare_payout()
        else:
            logging.critical("Please review your file paths and re-try.")
    else:
        logging.critical('Solicitud con Formato NO RESPETADO !!!')
        error_msg_format(chat_id, bot, "getpay")

def get_claim(splitted_text, chat_id, username, payments_file_path, secrets_file_path):
    if len(splitted_text) >= 3:
        # Generate QR codes
        wronin = splitted_text[1].lower().strip()
        pin_user = splitted_text[2]

        is_pin, pin_db, item = check_if_exist_pin(chat_id, username)
        if not is_pin:
            return

        logging.info(f'payments_file {payments_file_path}')
        logging.info(f'secrets_file {secrets_file_path}')
        logging.info(f'bot {bot}')
        logging.info(f'chat_id {chat_id}')
        logging.info(f'wronin {wronin}')
        logging.info(f'pin {pin_user}')
        logging.info(f'pin_db {pin_db}')
        logging.info(f'username {username}')

        payments_file_path = payments_file_path
        # secrets_file_path = args['<secrets_file>']
        secrets_file_path = secrets_file_path
        if check_file(payments_file_path) and check_file(secrets_file_path):
            # Claim SLP
            logging.info('I shall claim SLP')
            acm = AxieClaimsManager(payments_file_path, secrets_file_path, bot, chat_id, wronin, pin_user, username, pin_db)
            acm.verify_inputs()
            acm.prepare_claims()
        else:
            logging.critical("Please review your file paths and re-try.")
    else:
        logging.critical('Solicitud con Formato NO RESPETADO !!!')
        error_msg_format(chat_id, bot, "getpay")

def message_check_in(body):
    # Extract the message key over payload's body
    is_message = "message" in body
    username = ""

    print("is_message")
    print(is_message)

    if not is_message:
        return "", "", False, "", False, ""

    message = body["message"]

    # Split between three variables bellow
    chat = message['chat']  # Chat ID will guide your chatbot reply
    chat_id = chat['id']

    is_username = "username" in chat
    print("is_username")
    print(is_username)
    if is_username:
        username = chat['username']

    fname_sender = message['from']['first_name']  # Sender's first name, registered by user's telegram app
    # is_text = hasattr(message, 'text')
    is_command = False
    text = ""

    is_text = "text" in message
    is_entities = "entities" in message

    print("is_text")
    print(is_text)

    # is_entities = hasattr(message, 'entities')
    print("is_entities")
    print(is_entities)

    if is_text:
        text = message['text']
        print(text)

    if is_entities:
        type_entity = message['entities'][0]['type']
        if type_entity == "bot_command":
            is_command = True

        print(type_entity)

    return chat_id, fname_sender, is_text, text, is_command, username


def belong_to_scholar_group(chat_id):
    # timeout = None, api_kwargs = None
    is_member = False
    info_member_chat = bot.get_chat_member(CHAT_ID_SCHOLAR_GROUP, chat_id)
    logging.info(f'info_member_chat ->  {info_member_chat}')
    status = bot.get_chat_member(CHAT_ID_SCHOLAR_GROUP, chat_id).status
    logging.info(f'status ->  {status}')
    if status == 'member':
        is_member = True

    return is_member


def check_file(file):
    if not os.path.isfile(file):
        logging.critical('Please provide a correct path to the file. '
                         f'Path provided: {file}')
        return False
    return True


def exists_username(chat_id, username):
    is_username = True
    if not username:
        logging.critical('USERNAME is required!!!')
        msg_check_username(chat_id, bot, "")
        is_username = False

    return is_username


def check_if_exist_pin(chat_id, username):
    is_item, item = get_item(username)
    if item:
        if "pin" in item:
            pin = item['pin']
            return True, pin, item
        else:
            msg_pin_must_be_create(chat_id, bot, "")
            return False, None, item
    else:
        error_msg_need_configuration(chat_id, bot, "")
        return False, None, item
