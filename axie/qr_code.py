import os
import sys
import logging
import boto3
import io
import jwt
import json
from botocore.exceptions import ClientError
from datetime import datetime

import qrcode

table = boto3.resource('dynamodb').Table('axie-scholar')
bucket_name = 'axie.scholarships'

s3_client = boto3.client('s3')

from axie.utils import AxieGraphQL, load_json
from axie.mongodb_dao import *


class QRCode(AxieGraphQL):

    def __init__(self, acc_name, path, bot, chat_id, wronin, pin, gen_new_qr_mongodb, username, item, **kwargs):
        self.acc_name = acc_name
        self.path = os.path.join(path, f'{self.acc_name.lower()}-{int(datetime.timestamp(datetime.now()))}.png')
        self.bot = bot
        self.chat_id = chat_id
        self.wronin = wronin
        self.pin = pin
        self.gen_new_qr_mongodb = gen_new_qr_mongodb
        self.username = username
        self.item = item
        super().__init__(**kwargs)

    def generate_qr(self):
        token_jwt = self.get_jwt()
        logging.info(f'jwt {token_jwt}')

        decoded = jwt.decode(token_jwt, options={"verify_signature": False})  # works in PyJWT >= v2.0
        logging.info(f'decoded {decoded}')
        exp = decoded['exp']
        logging.info(f'exp {exp}')

        # response = table.get_item(Key={'username': self.wronin})
        # logging.info(f'Updating Scholar on MONGODB -> {response} !!')
        # is_item, item = get_item(self.username)
        # is_item, item = get_item(self.username)
        # item = response['Item']

        # save new QR exp time generated MONGODB
        logging.info(f'gen_new_qr_mongodb {self.gen_new_qr_mongodb}')
        if self.gen_new_qr_mongodb:
            logging.info(f'Saving Scholar on MONGODB !!')
            item_to_put = {
                'username': self.username,
                'wronin': self.wronin,
                'account': self.acc_name,
                'token_exp': exp,
                'jwt': token_jwt,
                'pin': self.item['pin']
            }
            put_item(item_to_put)
        else:
            update_item(self.item, exp, token_jwt)

        logging.info('Create QR Code')
        qr = qrcode.make(token_jwt)
        logging.info(f'type(qr) {type(qr)}')
        logging.info(f'img.size {qr.size}')
        logging.info(f'Saving QR Code for account {self.acc_name} at {self.path}')
        buffer = io.BytesIO()
        qr.save(buffer, "PNG")
        buffer.seek(0)  # rewind pointer back to start
        s3_client.put_object(Bucket=bucket_name, Key='QRs/' + self.path, Body=buffer, ContentType='image/png')

        url = "https://s3.amazonaws.com/%s/%s" % (bucket_name, "QRs/" + self.path)
        logging.info(f'URL QR {url}')
        logging.info('QR GENERADO, GUARDADO y ENVIADO  !!')
        self.bot.send_photo(self.chat_id, url)


class QRCodeManager:

    def __init__(self, payments_file, secrets_file, bot, chat_id, wronin, pin, username, pin_db, item):
        # self.is_ronin = True
        self.bot = bot
        self.chat_id = chat_id
        self.wronin = wronin
        self.pin = pin
        self.pin_db = pin_db
        self.username = username
        self.item = item
        self.gen_new_qr_mongodb = False
        self.is_pin_error = False
        self.is_wronin_error = False
        self.gen_qr = False
        self.is_qr_valid = False

        self.is_not, self.secrets_file, self.acc_names, self.qr_state = self.load_secrets_and_acc_name(secrets_file,
                                                                                                       payments_file)

        logging.critical(f'self.is_not {self.is_not}')
        logging.critical(f'self.secrets_file {self.secrets_file}')
        logging.critical(f'self.acc_names {self.acc_names}')
        logging.critical(f'self.qr_state {self.qr_state}')

        if not self.is_not:
            logging.critical('if not self.is_not:')
            if self.qr_state == "qr_alive":
                logging.critical(f'QR se encuentra vigente !!')
                self.is_qr_valid = True
                self.gen_qr = False
            elif self.qr_state == "error_input":
                logging.critical(f'Solicitud Rechazada [ERROR_INPUT]')
                self.is_qr_valid = False
                self.gen_qr = False
        else:
            logging.critical('self.path = os.path.dirname(secrets_file)')
            self.path = os.path.dirname(secrets_file)
            self.is_qr_valid = False
            self.gen_qr = True

            if self.qr_state == "qr_not_exists_mongodb":
                self.gen_new_qr_mongodb = True
            elif self.qr_state == "msg_incorrect_input_data_pin":
                self.is_pin_error = True
                self.gen_qr = False
            elif self.qr_state == "msg_incorrect_input_data_wronin":
                self.is_wronin_error = True
                self.gen_qr = False

    def load_secrets_and_acc_name(self, secrets_file, payments_file):
        secrets = load_json(secrets_file)
        payments = load_json(payments_file)
        refined_secrets = {}
        acc_names = {}
        error_on_pin = False
        error_on_wronin = False

        response_values = {}

        for scholar in payments['Scholars']:
            if self.wronin == scholar['ScholarPayoutAddress'] and self.pin == self.pin_db and self.username.lower() == scholar['TelegramID'].lower():
            # if self.wronin == scholar['ScholarPayoutAddress'] and self.pin == self.pin_db:
                error_on_pin = False
                error_on_wronin = False
                # query if QR has expired or not MONGODB
                logging.info(f'ENTRA BLOQUE IF VALIDO CON ITEM ->  {self.item}')
                item = self.item

                exists_token_exp = "token_exp" in item

                logging.info(f'Table Item[Dynamodb] {item}')
                logging.info(f'is_token_exp in Item[Dynamodb] {exists_token_exp}')

                key = scholar['AccountAddress']
                refined_secrets[key] = secrets[key]
                acc_names[key] = scholar['Name']

                if exists_token_exp:
                    now = datetime.utcnow()
                    timestamp_today_utc = datetime.timestamp(now)
                    logging.info(f'TODAY UTC[timestamp] {int(timestamp_today_utc)}')
                    token_date_exp = item['token_exp']
                    logging.info(f'Item[token_exp] {int(token_date_exp)}')

                    # if int(timestamp_today_utc) > int(token_date_exp):
                    logging.info(f'QR CADUCADO !!')
                    scholar_name = scholar['Name']
                    scholar_tid = scholar['TelegramID']
                    logging.info(f'scholar[AccountAddress] {key}')
                    logging.info(f'scholar[ScholarName] {scholar_name}')
                    logging.info(f'scholar[TelegramID] {scholar_tid}')
                    response_values = True, refined_secrets, acc_names, "qr_expired"
                    break
                    # else:
                    #     logging.info(f'QR VIGENTE !!')
                    #     response_values = False, None, None, "qr_alive"
                    #     break
                else:
                    response_values = True, refined_secrets, acc_names, "qr_not_exists_mongodb"
                    break
            elif self.pin != self.pin_db:
                logging.critical(f'msg_incorrect_input_data_pin[self.pin] -> {self.pin}')
                logging.critical(f'msg_incorrect_input_data_pin[self.pin_db] -> {self.pin_db}')
                error_on_pin = True
                # return True, None, None, "msg_incorrect_input_data_pin"
            elif self.wronin != scholar['ScholarPayoutAddress']:
                scholar_ronin = scholar['ScholarPayoutAddress']
                logging.critical(f'msg_incorrect_input_data_wronin[self.wronin] -> {self.wronin}')
                logging.critical(f'msg_incorrect_input_data_wronin[ScholarPayoutAddress] -> {scholar_ronin}')
                error_on_wronin = True

        if error_on_pin:
            return True, None, None, "msg_incorrect_input_data_pin"
        elif error_on_wronin:
            return True, None, None, "msg_incorrect_input_data_wronin"
        else:
            return response_values


    def verify_inputs(self):
        validation_success = True
        # Check secrets file is not empty
        if not self.secrets_file:
            logging.warning("No secrets contained in secrets file")
            validation_success = False
        # Check keys and secrets have proper format
        for acc in self.secrets_file:
            if not acc.startswith("ronin:"):
                logging.critical(f"Public address {acc} needs to start with ronin:")
                validation_success = False
            if len(self.secrets_file[acc]) != 66 or self.secrets_file[acc][:2] != "0x":
                logging.critical(f"Private key for account {acc} is not valid, please review it!")
                validation_success = False
        if not validation_success:
            sys.exit()
        logging.info("Secret file correctly validated")

    def execute(self):
        qrcode_list = [
            QRCode(
                account=acc,
                private_key=self.secrets_file[acc],
                acc_name=self.acc_names[acc],
                path=self.path,
                bot=self.bot,
                chat_id=self.chat_id,
                wronin=self.wronin,
                pin=self.pin,
                gen_new_qr_mongodb=self.gen_new_qr_mongodb,
                username=self.username,
                item=self.item
            ) for acc in self.secrets_file
        ]
        for qr in qrcode_list:
            logging.info(f"QR ACC {qr} !!")
            qr.generate_qr()
