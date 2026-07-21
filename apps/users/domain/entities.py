"""
Entidades puras do bounded context `users` — sem import de Django.
"""

import uuid
from dataclasses import dataclass
from datetime import datetime


@dataclass
class User:
    id: uuid.UUID
    email: str
    name: str
    created_at: datetime
