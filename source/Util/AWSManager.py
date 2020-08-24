import boto3
from boto3.dynamodb.conditions import Attr


class AWSManger:
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb')
        self.userTable = self.dynamodb.Table('USERS')
        self.urlTable = self.dynamodb.Table('urlDB')

    def saveUser(self, user):
        self.userTable.put_item(Item=user)

    def getUser(self, username):
        res = self.userTable.get_item(
            Key={'username': username}
        )
        if 'Item' in res:
            return res['Item']
        return None

    def saveUserURL(self, username, shortUrl):
        self.userTable.update_item(
            Key={
                'username': username
            },
            UpdateExpression='set URLHistory = list_append(URLHistory, :val)',
            ExpressionAttributeValues={
                ':val': [shortUrl]
            }
        )

    def getByID(self, user_id):
        res = self.userTable.scan(
            FilterExpression=Attr('id').eq(user_id)
        )
        if res['Count'] == 0:
            return None
        return res['Items'][0]

    def saveURL(self, id, longURL):
        self.urlTable.put_item(
            Item={
                'id': str(id),
                'longURL': longURL
            }
        )
        print('aws saved')

    def getURL(self, id):
        res = self.urlTable.get_item(
            Key={
                'id': str(id)
            }
        )
        if 'Item' not in res:
            return None
        return res['Item']['longURL']

if __name__ == '__main__':
    aws = AWSManger()
    #print(aws.getUser('aws'))
    #aws.getByID('27f3d2a6-50asdf6b-4c77-94f0-a395b14cebad')
    print(aws.getURL(1909053068578787328))


