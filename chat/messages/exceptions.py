from fastapi import HTTPException, status


class MessageExceptions:

    @property
    def message_not_found(self):
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Message not found')

    @property
    def not_subscribe_error(self):
        return {
            'type': 'error',
            'text': 'You must first subscribe to the channel'
        }

    @property
    def not_subscribed_to_the_channel(self):
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You are not subscribed to this channel"
        )
