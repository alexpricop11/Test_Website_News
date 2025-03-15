from rest_framework_jwt.settings import api_settings

from .models import Users

JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER


class AuthManager:
    @staticmethod
    def generate_token(user: Users) -> str:
        payload = JWT_PAYLOAD_HANDLER(user)
        return JWT_ENCODE_HANDLER(payload)

    @staticmethod
    def get_user_by_id(user_id: str) -> Users:
        return Users.objects.get(id=user_id)
