"""Модуль со вспомогательными функциями."""

from argparse import ArgumentTypeError
from random import choice
from string import ascii_letters
from typing import Optional, Union


def random_string(count: int) -> str:
    """Генерация случайной строки из count."""
    return ''.join(choice(ascii_letters) for _ in range(count))


def convert_str_to_bool(value: str) -> bool:
    """Преобразование строки в флаг."""
    if isinstance(value, bool):
        return value
    if value.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif value.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise ArgumentTypeError('Ожидался флаг (true/false)')


def convert_str_to_int(value: Optional[Union[str, bytes]]) -> Optional[int]:
    """Преобразование строки в целое число."""
    if value is None:
        return None
    if isinstance(value, bytes):
        value = value.decode('utf-8')
    try:
        return int(value)
    except ValueError:
        return None
