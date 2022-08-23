from fastapi import APIRouter, status, Depends

chat_controllers = APIRouter(prefix='/chat', tags=['chat'])

"""
----channel----
1. create channel
2. delete channel
3. update channel name
4. get channel name
5. enter to channel
6. exit from channel
----message----
1. write message
2. delete message
3. update message
-----others-----
4. user typing
"""


@chat_controllers.post('/channel/')
async def create_channel():
    pass


@chat_controllers.get('/channel/{channel_name}')
async def get_channel(channel_name: str):
    pass


@chat_controllers.delete('/channel/{channel_name}')
async def delete_channel(channel_name: str):
    pass


@chat_controllers.patch('/channel/{channel_name}')
async def update_channel(channel_name: str):
    pass


@chat_controllers.post('/channel/{channel_name}')
async def subscribe(channel_name: str):
    pass


@chat_controllers.delete('/channel/{channel_name}')
async def unsubscribe(channel_name: str):
    pass
