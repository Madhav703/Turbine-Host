from enum import Enum
import discord
import pytz
from datetime import datetime, timedelta
import config


class _Sentinel:
    def __repr__(self):
        return "<MISSING>"

MISSING = _Sentinel()
IST = pytz.timezone("Asia/Kolkata")
