# services/auth/token_service.py
from typing import Optional
import jwt
from flask import current_app
from datetime import datetime, timedelta

class TokenService:
    def create_access_token(self, user) -> str:
        payload = {
            'user_id': user.id,
            'exp': datetime.now() + timedelta(days=1)
        }
        return jwt.encode(
            payload,
            current_app.config['SECRET_KEY'],
            algorithm='HS256'
        )

    def validate_token(self, token: str) -> Optional[dict]:
        try:
            return jwt.decode(
                token,
                current_app.config['SECRET_KEY'],
                algorithms=['HS256']
            )
        except jwt.InvalidTokenError:
            return None
