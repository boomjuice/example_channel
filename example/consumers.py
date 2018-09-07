from channels import Group
from  datetime import datetime
import json
from channels.auth import channel_session_user, channel_session_user_from_http

# 当连接上时，发回去一个connect字符串
@channel_session_user_from_http
def ws_connect(message):
    print('connect')
    print(datetime.now())
    room = message.content['path'].strip("/")
    print(room)
    # message.reply_channel.send({'accept': True})
    Group('users').add(message.reply_channel)
    Group('users').send({
        'text': json.dumps({
            'username': message.user.username,
            'is_logged_in': True,
            'online_user_num': 1
        })
    })

# 将发来的信息原样返回
@channel_session_user
def ws_message(message):
    print('message')
    print(message.channel)
    print(datetime.now())
    # message.reply_channel.send({
    #     "text": message.content['text'],
    # })
    if message.content['text']:
        Group('users').send({
            'text': json.dumps({
                'message': True,
                "text": message.content['text'],
                "user": message.user.username,
            })
        })


# 断开连接时发送一个disconnect字符串，当然，他已经收不到了
@channel_session_user
def ws_disconnect(message):
    print('disconnect')
    print(datetime.now())

    Group('users').send({
        'text': json.dumps({
            'username': message.user.username,
            'is_logged_in': False,
            'online_user_num': 1
        })
    })
    Group('users').discard(message.reply_channel)
    # message.reply_channel.send({'accept': True})
