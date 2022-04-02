# axie-scholars-telegram-payout-bot

---
ES
---
BOT para realizar pagos, generacion de QRs y otros para los becados en plataforma Telegram.
- Este BOT debe ser integrado junto a Amazon Web Services AWS (Lambda y DocumentDB) + Webhook Token en Telegram.
---
USO e Integracion *

- Tener o Crear cuenta en Telegram y luego crear un Webhook y obtener token -> documentation: https://core.telegram.org/bots/api.
- Tener o Crear cuenta AWS -> link: https://aws.amazon.com:
  - Crear Lambda en Python 3.7+ e integrar el codigo (link lambda: https://aws.amazon.com/lambda) .
  - Crear Documentdb para guarda datos de los becados, tales como PIN, Wallet de Pago, usuario telegrarm, etc (link documentdb: https://aws.amazon.com/documentdb).


- Crear file payments.json y luego llenar con los datos de los becados y el manager,  tomando como referencia el file payments-sample.json.
- Crear file secrets.json y luego llenar wallet de la cuenta becada + su privateKey, tomando como referencia el file secrets-sample.json.
- Crear file util-messages.py, tomando como referencia el file util-messages-sample.py.
---
EN
---
BOT to make payments, generate QRs and others for scholarship recipients on the Telegram platform.
- This BOT must be integrated with Amazon Web Services AWS (Lambda and DocumentDB) + Webhook Token in Telegram.
---
USE and Integration *

- Have or Create Telegram account and then create a Webhook and get token -> documentation: https://core.telegram.org/bots/api.
- Have or Create an AWS account -> link: https://aws.amazon.com:
   - Create Lambda in Python 3.7+ and integrate the code (link lambda: https://aws.amazon.com/lambda) .
   - Create Documentdb to save scholarship holders' data, such as PIN, Payment Wallet, telegram user, etc. (documentdb link: https://aws.amazon.com/documentdb).


- Create the file payments.json and then fill in the data of the scholarship holders and the manager, taking the payments-sample.json file as a reference.
- Create file secrets.json and then fill wallet of the scholarship account + its privateKey, taking as reference the file secrets-sample.json.
- Create file util-messages.py, taking as reference the file util-messages-sample.py.
---
- Se recomienda usar https://tracker.axie.management para visualizar en tiempo real el comportamiento de tus becados !!
- It is recommended to use https://tracker.axie.management to view the behavior of your scholarships in real time !!
---


Have a Good Management !!!

Sincerily,

@Titano
