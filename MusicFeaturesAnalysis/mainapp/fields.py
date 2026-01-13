from django.db import models
from cryptography.fernet import Fernet
from django.conf import settings


class EncryptedTextField(models.TextField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fernet = Fernet(
            settings.SPOTIFY_TOKEN_ENCRYPTION_KEY.encode()
        )

    def get_prep_value(self, value):
        if value is None:
            return value
        return self.fernet.encrypt(value.encode()).decode()

    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        return self.fernet.decrypt(value.encode()).decode()

    def to_python(self, value):
        return value
