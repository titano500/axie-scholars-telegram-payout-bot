# axie-scholars-telegram-payout-bot
- BOT para realizar pagos, generacion de QRs y otros para los becados en plataforma Telegram -

- Este BOT debe ser integrado junto a Amazon Web Services AWS (Lambda y DocumentDB) + Webhook Token en Telegram.

* USO e Integracion *

- Tener cuenta en Telegram y crear un Webhook.
- Crear cuenta AWS:
  - Crear Lambda en Python 3.7+ e integrar el codigo.
  - Crear Documentdb para guarda datos de los becados, tales como PIN, Wallet de Pago, usuario telegrarm, etc.


- Crear file payments.json y luego llenar con los datos de los becados y el manager,  tomando como referencia el file payments-sample.json.
- Crear file secrets.json y luego llenar wallet de la cuenta becada + su privateKey, tomando como referencia el file secrets-sample.json .
- Crear file util-messages.py, tomando como referencia el file util-messages-sample.py.



---

Se recomienda usar https://tracker.axie.management/ para visualizar en tiempo real el comportamiento de tus becados !!

Have a Good Management !!!

Sincerily,

@Titano
