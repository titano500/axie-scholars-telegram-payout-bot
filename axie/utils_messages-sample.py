import logging

def error_msg_data_not_correspond(chat_id, bot, typeflow):
    if "getpin" == typeflow:
        bot.send_message(chat_id,
                     "⚠️🔈𝐖𝐚𝐫𝐧𝐢𝐧𝐠 🔈⚠️\n\nRejected request !! Check your Ronin Wallet !!!\n\n--------------------------------------"
                     "\n\n⚠️🔈𝐀𝐝𝐯𝐞𝐫𝐭𝐞𝐧𝐜𝐢𝐚 🔈⚠️\n\nSolicitud Rechazada !! Verifique su Ronin Wallet !!!")
    else:
        bot.send_message(chat_id,
                         "⚠️🔈𝐖𝐚𝐫𝐧𝐢𝐧𝐠 🔈⚠️\n\nRejected request !! Check your Ronin Wallet and PIN !!!\n\n--------------------------------------"
                         "\n\n⚠️🔈𝐀𝐝𝐯𝐞𝐫𝐭𝐞𝐧𝐜𝐢𝐚 🔈⚠️\n\nSolicitud Rechazada !! Verifique su Ronin Wallet y su PIN !!!")



def error_msg_format(chat_id, bot, typeflow):
        if "getpin" == typeflow:
            logging.critical('Solicitud con Formato NO RESPETADO !!!')
            bot.send_message(chat_id,
                             "⚠️🔈𝐖𝐚𝐫𝐧𝐢𝐧𝐠 🔈⚠️\n\nRejected request !! You must respect the format of the command:"
                             "\n\n[/get_pin your_ronin_wallet] -> Sample: /get_pin ronin:mdwbdhw434tdg00nnasv\n\n to complete your request !!!\n\n--------------------------------------"
                             "\n\n⚠️🔈𝐀𝐝𝐯𝐞𝐫𝐭𝐞𝐧𝐜𝐢𝐚 🔈⚠️\n\nSolicitud Rechazada !! Debes respetar el formato del comando:"
                             "\n\n[/get_pin tu_wallet_ronin] -> Ejemplo: /get_pin ronin:mdwbdhw434tdg00nnasv\n\n para completar su solicitud !!!")
        elif "setpin" == typeflow:
            logging.critical('Solicitud con Formato NO RESPETADO !!!')
            bot.send_message(chat_id,
                             "⚠️🔈𝐖𝐚𝐫𝐧𝐢𝐧𝐠 🔈⚠️\n\nRejected request !! You must respect the format of the command:"
                             "\n\n[/set_pin your_ronin_wallet pin] -> Sample: /set_pin ronin:mdwbdhw434tdg00nnasv sfdfdn\n\n to complete your request !!!\n\n--------------------------------------"
                             "\n\n⚠️🔈𝐀𝐝𝐯𝐞𝐫𝐭𝐞𝐧𝐜𝐢𝐚 🔈⚠️\n\nSolicitud Rechazada !! Debes respetar el formato del comando:"
                             "\n\n[/set_pin tu_wallet_ronin pin] -> Ejemplo: /set_pin ronin:mdwbdhw434tdg00nnasv sfdfdn\n\n para completar su solicitud !!!")
        elif "getpay" == typeflow:
            logging.critical('Solicitud con Formato NO RESPETADO !!!')
            bot.send_message(chat_id,
                             "⚠️🔈𝐖𝐚𝐫𝐧𝐢𝐧𝐠 🔈⚠️\n\nRejected request !! You must respect the format of the command:"
                             "\n\n[/get_payout your_ronin_wallet pin] -> Sample: /get_payout ronin:mdwbdhw434tdg00nnasv sfdfdn\n\n to complete your request !!!\n\n--------------------------------------"
                             "\n\n⚠️🔈𝐀𝐝𝐯𝐞𝐫𝐭𝐞𝐧𝐜𝐢𝐚 🔈⚠️\n\nSolicitud Rechazada !! Debes respetar el formato del comando:"
                             "\n\n[/get_payout tu_wallet_ronin pin] -> Ejemplo: /get_payout ronin:mdwbdhw434tdg00nnasv sfdfdn\n\n para completar su solicitud !!!")
        else:
            logging.critical('Solicitud con Formato NO RESPETADO !!!')
            bot.send_message(chat_id,
                             "⚠️🔈𝐖𝐚𝐫𝐧𝐢𝐧𝐠 🔈⚠️\n\nRejected request !! You must respect the format of the command:"
                             "\n\n[/get_qr your_ronin_wallet pin] -> Sample: /get_qr ronin:mdwbdhw434tdg00nnasv rr1gO8\n\n to complete your request !!!"
                             "\n\n--------------------------------------\n\n⚠️🔈𝐀𝐝𝐯𝐞𝐫𝐭𝐞𝐧𝐜𝐢𝐚 🔈⚠️\n\nSolicitud Rechazada !! Debes respetar el formato del comando:"
                             "\n\n[/get_qr tu_wallet_ronin pin] -> Ejemplo: /get_qr ronin:mdwbdhw434tdg00nnasv rr1gO8\n\n para completar su solicitud !!!")



def error_msg_need_configuration(chat_id, bot, typeflow):
    bot.send_message(chat_id,
                     "⚠️🔈𝐖𝐚𝐫𝐧𝐢𝐧𝐠 🔈⚠️"
                     "\n\nYour information is not registered !!"
                     "\n\nYou must add the following in the link:"
                     "\n\n- TelegramID (username) (Required)."
                     "\n\n- Set your PIN in the BOT (Required) with the command: /set_pin ronin_wallet pin"
                     "\n\n- As far as possible all the other info that is shown in the link.\n\n"
                     "Once done, notify @E_CastroM, @titano500 or our Scholars Group !!!\n\n"
                     "LINK -> xxxxx !!!"
                     "\n\n--------------------------------------"
                     "\n\n⚠️🔈𝐀𝐝𝐯𝐞𝐫𝐭𝐞𝐧𝐜𝐢𝐚 🔈⚠️"
                     "\n\nTu informacion no esta registrada !!"
                     "\n\nDebes agregar lo siguiente en el link:"
                     "\n\n- TelegramID (username) (Obligatorio)."
                     "\n\n- Establecer tu PIN en el BOT (Obligatorio) con el comando: /set_pin ronin_wallet pin"
                     "\n\n- En lo posible toda la demas info que se muestra en el link.\n\n"
                     "Una vez realizado, notificar a @E_CastroM, @titano500 o en nuestro Grupo de Becados !!!\n\n"
                     "LINK -> xxxxx !!!")



def msg_qr_still_active(chat_id, bot, typeflow):
    bot.send_message(chat_id,
                     "⚠️🔈𝐖𝐚𝐫𝐧𝐢𝐧𝐠 🔈⚠️\n\nYour QR code is still Active, you must wait 1 week before requesting another !!!"
                     "\n\n--------------------------------------\n\n⚠️🔈𝐀𝐝𝐯𝐞𝐫𝐭𝐞𝐧𝐜𝐢𝐚 🔈⚠️\n\nTu codigo QR aun se encuentra Activo, debes esperar 1 semana antes de solicitar otro !!!")



def error_msg_service(chat_id, bot, typeflow):
    bot.send_message(chat_id,
                     "⚠️🔈𝐖𝐚𝐫𝐧𝐢𝐧𝐠 🔈⚠️\n\nService Error !!!\n\n--------------------------------------"
                     "\n\n⚠️🔈𝐀𝐝𝐯𝐞𝐫𝐭𝐞𝐧𝐜𝐢𝐚 🔈⚠️\n\nError en el Servicio !!!")



def msg_pin_length(chat_id, bot, typeflow):
    bot.send_message(chat_id,
                     "The PIN you want to create must be 6 characters long !!!\n\n--------------------------------------"
                     "\n\nEl PIN que quieres crear debe tener un largo de 6 caracteres !!!")


def msg_not_belong_to_scholar_group(chat_id, bot, fname_sender):
    bot.send_message(chat_id,
                     f"Sorry {fname_sender} ! you do not belong to our group of Scholarship Holders !!!\n\n--------------------------------------"
                     f"\n\nLo siento {fname_sender} ! no perteneces a nuestro grupo de Becados !!!")


def  msg_check_username(chat_id, bot, typeflow):
    bot.send_message(chat_id,
                     "⚠️🔈𝐖𝐚𝐫𝐧𝐢𝐧𝐠 🔈⚠️\n\nYou must configure your USERNAME in TELEGRAM !!!\n\nCheck this image -> https://s3.amazonaws.com/axie.scholarships/telegram_username.jpeg and then Inform the moderator @E_CastroM, @titano500 or in our Scholar Group !!!"
                     "\n\n--------------------------------------\n\n⚠️🔈𝐀𝐝𝐯𝐞𝐫𝐭𝐞𝐧𝐜𝐢𝐚 🔈⚠️\n\nDebes configurar tu USERNAME en TELEGRAM !!!\n\nRevisa esta imagen de como hacerlo -> https://s3.amazonaws.com/axie.scholarships/telegram_username.jpeg y luego Informa a la moderadora @E_CastroM, @titano500 o en nuestro Grupo de Becados !!!")



def msg_pin_must_be_create(chat_id, bot, typeflow):
    bot.send_message(chat_id,
                     "You need to create a 6 character alphanumeric PIN as long !!!\n\n--------------------------------------"
                     "\n\nEs necesario que crees un PIN alfanumerico de 6 caracteres como largo !!!")



def msg_pin_deliver(chat_id, bot, pin):
    bot.send_message(chat_id,
                     f"Your PIN code -->{pin}<-- !!!\n\n--------------------------------------\n\nTu codigo PIN -->{pin}<-- !!!")



def error_msg_pin_created(chat_id, bot):
    bot.send_message(chat_id,
                     "Before checking your PIN, you must SET IT with the following Command:\n\n/set_pin ronin_wallet pin\n\n--------------------------------------"
                     "\n\nAntes de consultar tu PIN, DEBES ESTABLECERLO con el siguiente Comando:\n\n/set_pin ronin_wallet pin")



def msg_incorrect_input_data(chat_id, bot, typeflow):
    if typeflow == "pin_error":
        bot.send_message(chat_id,
                         "The PIN entered is incorrect !!!\n\n-------------------\n\nEl PIN ingresado es incorrecto !!!")
    elif typeflow == "wronin_error":
        bot.send_message(chat_id,
                         "The Ronin Wallet entered does not correspond !!!\n\n-------------------\n\nLa Wallet Ronin ingresada no corresponde !!!")
    else:
        pass

def msg_payout_process(chat_id, bot, wallet, scholar_amount, acc_name, ronin_trx, acc_balance):
    bot.send_message(chat_id,
                     f"Payment has been processed for scholar name: {acc_name} !!"
                     f"\n\nScholar Wallet Payment: {wallet} !!"
                     f"\n\nTotal SLPs Farmed: --> {acc_balance} SLPs <-- !!!"
                     f"\n\nScholar SLPs Amount to Payout: --> {scholar_amount} SLPs <-- !!!"
                     f"\n\nRonin Explorer Transaction: -->{ronin_trx}<-- !!!"
                     f"\n\n--------------------------------------\n\n"
                     f"Pago ha sido procesado para la o el becad@ con nombre {acc_name}!!"
                     f"\n\nWallet de pago del becado: {wallet} !!"
                     f"\n\nTotal de SLPs Farmeados: --> {acc_balance} SLPs <-- !!!"
                     f"\n\nSLPs del Becado a Pagar: --> {scholar_amount} SLPs <-- !!!"
                     f"\n\nTransaccion en la Ronin Explorer: -->{ronin_trx}<-- !!!")

def msg_insufficient_funds(chat_id, bot):
    bot.send_message(chat_id,
                     f"Insufficient Funds !!! Check your CLAIM if is already.\n\n--------------------------------------\n\nFondos insuficientes !!! Revisa tu CLAIM si esta listo.")

def processing_payment(chat_id, bot):
    bot.send_message(chat_id,
                     f"Your payment is being processed, please wait...\n\n--------------------------------------\n\nSu pago se esta procesando, por favor espere...\n\n")

def processing_claim(chat_id, bot):
    bot.send_message(chat_id,
                     f"Your CLAIM is being processed, please wait...\n\n--------------------------------------\n\nSu CLAIM se esta procesando, por favor espere...\n\n")

def claim_ready(obj):
    obj.bot.send_message(obj.chat_id,
                     f"Your CLAIM is Ready !!\n\n"
                     f"The total amount of SLPs claimed in your scholarship account are {obj.balance} SLPs.\n\n"
                     f"Use the /get_payout command together with your registered payment wallet and your pin number to request your payment.\n\n"
                     f"Example: /get_payout scholar_wallet pin"
                     f"\n\n--------------------------------------\n\n"
                     f"Tu CLAIM esta listo !!\n\n"
                     f"El monto total de SLPs reclamados en tu cuenta becada es de {obj.balance} SLPs.\n\n"
                     f"Usa el comando /get_payout junto a tu wallet de pago registrada y tu numero de pin para solicitar tu pago.\n\n"
                     f"Ejemplo: /get_payout scholar_wallet pin")