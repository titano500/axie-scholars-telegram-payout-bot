import boto3
import logging

table = boto3.resource('dynamodb').Table('axie-scholar')


def put_item(item):
    response = table.put_item(
        Item={
            'username': item['username'],
            'wronin': item['wronin'],
            'account': item['account'],
            'token_exp': item['token_exp'],
            'jwt': item['jwt'],
            'pin': item['pin']
        }
    )
    logging.info(f'Scholar Saved PIN on MONGODB -> {response} !!')


def get_item(username):
    response = table.get_item(Key={'username': username})
    logging.info(f'Requesting item Scholar username -> {username} !!')
    logging.info(f'Requesting item Scholar on MONGODB -> {response} !!')

    if "Item" in response:
        item = response['Item']
        # response = table.put_item(Item=item)
        logging.info(f'Item Scholar on MONGODB -> {item} !!')
        return True, item
    else:
        logging.critical(f'NO Existe SCHOLAR -> {response} !!')
        # item = {
        #     "username": {
        #         "S": ""
        #     },
        #     "wronin": {
        #         "S": ""
        #     },
        #     "jwt": {
        #         "S": ""
        #     },
        #     "pin": {
        #         "S": ""
        #     },
        #     "account": {
        #         "S": ""
        #     },
        #     "token_exp": {
        #         "N": ""
        #     }
        # }
        return False, None


def update_item(item, exp, token_jwt):
    item['last_token_exp'] = item['token_exp']
    item['token_exp'] = exp
    item['jwt'] = token_jwt
    response = table.put_item(Item=item)
    logging.info(f'Scholar Updated on MONGODB -> {response} !!')
