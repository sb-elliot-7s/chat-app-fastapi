from fastapi import HTTPException, status


class ChannelExceptions:
    channel_not_found = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='Channel not found'
    )

    @staticmethod
    def unsubscribe(customer_id: int, channel_id: int):
        return HTTPException(
            status_code=status.HTTP_200_OK,
            detail=f'Customer {customer_id} '
                   f'unsubscribed from channel {channel_id}'
        )
