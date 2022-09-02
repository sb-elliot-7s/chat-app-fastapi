from fastapi import HTTPException, status


class MessageExceptions:

    @property
    def message_not_found(self):
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Message not found'
        )
