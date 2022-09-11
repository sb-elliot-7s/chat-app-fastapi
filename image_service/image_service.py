from dataclasses import dataclass
from fastapi import UploadFile
import aiofiles
from aiofiles import os as _os
from .interfaces.image_service_interface import ImageServiceInterface


def file_not_found(func):
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except FileNotFoundError as err:
            print('file not found', err)

    return wrapper


@dataclass
class ImageService(ImageServiceInterface):
    path: str

    @file_not_found
    async def write_image(self, file: UploadFile, filename: str):
        _filename = f'{self.path}/{filename}'
        async with aiofiles.open(file=_filename, mode='wb') as f:
            raw = await file.read()
            await f.write(raw)

    @file_not_found
    async def read_image(self, filename: str):
        _filename = f'{self.path}/{filename}'
        async with aiofiles.open(file=_filename, mode='r') as file:
            return await file.read()

    @file_not_found
    async def delete_image(self, filename: str):
        await _os.remove(f'{self.path}/{filename}')
