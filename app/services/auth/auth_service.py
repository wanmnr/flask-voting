# app/services/auth/auth_service.py
from typing import Optional, Tuple
from datetime import datetime, timezone
from flask import current_app, request
from flask_login import login_user
from app.extensions.db import db
from app.extensions.security import user_datastore
from app.extensions.cache import cache
from app.extensions.mail import send_email
from app.models.user import User
from app.services.auth.password_service import PasswordService
from app.services.auth.token_service import TokenService

class AuthenticationService:
    def __init__(self):
        self.password_service = PasswordService()
        self.token_service = TokenService()

    @cache.memoize(timeout=300)
    def get_user_by_username(self, username: str) -> Optional[User]:
        """Get user by username with caching."""
        return User.query.filter_by(username=username).first()

    @cache.memoize(timeout=300)
    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email with caching."""
        return User.query.filter_by(email=email).first()

    def validate_login(self, username: str, password: str) -> Tuple[bool, Optional[User], str]:
        """
        Validate user login credentials.
        Returns: (success, user, message)
        """
        user = self.get_user_by_username(username)

        if not user:
            return False, None, "Invalid username or password"

        if not self.password_service.verify(password, user.password_hash):
            return False, None, "Invalid username or password"

        if not user.active:
            return False, None, "Account is not active"

        # Update login info
        user.last_login_at = datetime.now()
        user.last_login_ip = request.remote_addr
        db.session.commit()

        return True, user, "Login successful"

    def register_user(self, form_data: dict) -> Tuple[bool, str]:
        """
        Register a new user with form data.
        Returns: (success, message)
        """
        try:
            # Check if username or email already exists
            if self.get_user_by_username(form_data['username']):
                return False, "Username already exists"

            if self.get_user_by_email(form_data['email']):
                return False, "Email already exists"

            # Create new user
            user = User(
                username=form_data['username'],
                email=form_data['email'],
                first_name=form_data['first_name'],
                last_name=form_data['last_name'],
                password_hash=self.password_service.hash(form_data['password']),
                active=True,
                email_confirmed_at=datetime.now(timezone.utc),
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc)
            )

            db.session.add(user)

            # Add default role
            default_role = user_datastore.find_role("user")
            if default_role:
                user_datastore.add_role_to_user(user, default_role)

            db.session.commit()

            # Clear any cached queries for this user
            cache.delete_memoized(self.get_user_by_username, form_data['username'])
            cache.delete_memoized(self.get_user_by_email, form_data['email'])

            # Send welcome email
            try:
                send_email(
                    'Welcome to Our Platform',
                    [user.email],
                    'welcome',
                    user=user
                )
            except Exception as e:
                current_app.logger.error(f"Failed to send welcome email: {str(e)}")
                # Don't fail registration if email fails

            return True, "Registration successful"

        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Registration error: {str(e)}")
            return False, "An error occurred during registration"

    def initiate_password_reset(self, email: str) -> Tuple[bool, str]:
        """
        Initiate the password reset process.
        Returns: (success, message)
        """
        user = self.get_user_by_email(email)
        if not user:
            return False, "Email not found"

        try:
            # Generate reset token
            token = self.token_service.create_access_token(user)

            # Send password reset email
            send_email(
                'Password Reset Request',
                [user.email],
                'reset_password',
                user=user,
                token=token
            )

            return True, "Password reset instructions have been sent to your email"

        except Exception as e:
            current_app.logger.error(f"Password reset error: {str(e)}")
            return False, "Failed to process password reset request"

    def reset_password(self, token: str, new_password: str) -> Tuple[bool, str]:
        """
        Reset user password using reset token.
        Returns: (success, message)
        """
        try:
            # Validate token
            token_valid, user = self.validate_token(token)
            if not token_valid or not user:
                return False, "Invalid or expired reset token"

            # Update password
            user.password_hash = self.password_service.hash(new_password)
            user.updated_at = datetime.now(timezone.utc)
            db.session.commit()

            # Clear any cached queries for this user
            cache.delete_memoized(self.get_user_by_username, user.username)
            cache.delete_memoized(self.get_user_by_email, user.email)

            return True, "Password has been reset successfully"

        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Password reset error: {str(e)}")
            return False, "Failed to reset password"

    def validate_token(self, token: str) -> Tuple[bool, Optional[User]]:
        """
        Validate token and return associated user if valid.
        Returns: (is_valid, user)
        """
        payload = self.token_service.validate_token(token)
        if not payload:
            return False, None

        user = User.query.get(payload.get('user_id'))
        if not user or not user.active:
            return False, None

        return True, user

    def change_password(self, user: User, current_password: str, new_password: str) -> Tuple[bool, str]:
        """
        Change user password.
        Returns: (success, message)
        """
        try:
            # Verify current password
            if not self.password_service.verify(current_password, user.password_hash):
                return False, "Current password is incorrect"

            # Update password
            user.password_hash = self.password_service.hash(new_password)
            user.updated_at = datetime.now(timezone.utc)
            db.session.commit()

            # Clear any cached queries for this user
            cache.delete_memoized(self.get_user_by_username, user.username)
            cache.delete_memoized(self.get_user_by_email, user.email)

            return True, "Password changed successfully"

        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Password change error: {str(e)}")
            return False, "Failed to change password"

    def update_user_profile(self, user: User, profile_data: dict) -> Tuple[bool, str]:
        """
        Update user profile information.
        Returns: (success, message)
        """
        try:
            # Update allowed fields
            for field in ['first_name', 'last_name']:
                if field in profile_data:
                    setattr(user, field, profile_data[field])

            user.updated_at = datetime.now(timezone.utc)
            db.session.commit()

            # Clear any cached queries for this user
            cache.delete_memoized(self.get_user_by_username, user.username)
            cache.delete_memoized(self.get_user_by_email, user.email)

            return True, "Profile updated successfully"

        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Profile update error: {str(e)}")
            return False, "Failed to update profile"
