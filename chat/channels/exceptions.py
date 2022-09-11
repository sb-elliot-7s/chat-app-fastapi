from fastapi import HTTPException, status


class ChannelExceptions:
    @property
    def channel_not_found(self):
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Channel not found'
        )

    @classmethod
    def unsubscribe(cls, customer_id: int, channel_id: int):
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User {customer_id} is not subscribed '
                   f'to the channel {channel_id}'
        )
