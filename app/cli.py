# app/core/cli.py

import email
import click
import logging
from flask import current_app
from flask.cli import with_appcontext
from werkzeug.security import generate_password_hash
from datetime import datetime, timezone
from .extensions.db import db
from .extensions.assets import assets
from .models.user import User, Role




class CLICommandBase:
    """Base class for CLI commands."""

    def __init__(self, db=db, assets=assets):
        self.logger = logging.getLogger(__name__)
        self.db = db
        self.assets = assets


class DatabaseCommands(CLICommandBase):
    """Class to handle database-related CLI commands."""

    def create_tables(self):
        """Create database tables."""
        try:
            self.db.create_all()
            self.logger.info('Database tables created successfully')
            return True
        except Exception as e:
            self.logger.error(f'Error creating database tables: {str(e)}')
            raise

    def init_db(self):
        """Initialize database with default data."""
        try:
            self.create_tables()

            # Create default roles if they don't exist
            if not Role.query.filter_by(name='admin').first():
                admin_role = Role(name='admin', description='Administrator role')
                self.db.session.add(admin_role)

            if not Role.query.filter_by(name='user').first():
                user_role = Role(name='user', description='Default user role')
                self.db.session.add(user_role)

            self.db.session.commit()

            # Create admin user if it doesn't exist
            if not User.query.filter_by(username='admin').first():
                admin = User(
                    username='admin',
                    email='admin@example.com',
                    password_hash=generate_password_hash('adminpassword'),
                    active=True,
                    first_name='Admin',
                    last_name='User',
                    confirmed_at=datetime.now(timezone.utc),
                    fs_uniquifier=str(datetime.now(timezone.utc).timestamp())
                )
                admin_role = Role.query.filter_by(name='admin').first()
                admin.roles.append(admin_role)
                self.db.session.add(admin)
                self.db.session.commit()
                self.logger.info('Admin user created successfully')
                return True
            self.logger.info('Admin user already exists')
            return False
        except Exception as e:
            self.logger.error(f'Error initializing database: {str(e)}')
            raise

    def drop_tables(self):
        """Drop all database tables."""
        try:
            self.db.drop_all()
            self.logger.info('Database tables dropped successfully')
            return True
        except Exception as e:
            self.logger.error(f'Error dropping database tables: {str(e)}')
            raise

    def recreate_tables(self):
        """Recreate database tables and initialize with default data."""
        try:
            self.drop_tables()
            return self.init_db()
        except Exception as e:
            self.logger.error(f'Error recreating database: {str(e)}')
            raise


class UserCommands(CLICommandBase):
    """Class to handle user-related CLI commands."""

    def create_admin_user(self, username: str, password: str) -> bool:
        """Create an admin user."""
        try:
            # Check if admin role exists, create if it doesn't
            admin_role = Role.query.filter_by(name='admin').first()
            if not admin_role:
                admin_role = Role(name='admin', description='Administrator role')
                self.db.session.add(admin_role)
                self.db.session.commit()

            user = User(
                username=username,
                email=email,
                password_hash=generate_password_hash(password),
                active=True,
                first_name='Admin',
                last_name='User',
                confirmed_at=datetime.now(timezone.utc),
                fs_uniquifier=str(datetime.now(timezone.utc).timestamp())
            )
            user.roles.append(admin_role)
            self.db.session.add(user)
            self.db.session.commit()
            self.logger.info(f"Created admin user: {username}")
            return True
        except Exception as e:
            self.logger.error(f'Error creating admin user: {str(e)}')
            raise


class AssetCommands(CLICommandBase):
    """Class to handle asset-related CLI commands."""

    def build_assets(self):
        """Build asset bundles."""
        try:
            self.assets.build()
            self.logger.info("Built asset bundles successfully")
            return True
        except Exception as e:
            self.logger.error(f'Error building assets: {str(e)}')
            raise

    def clean_assets(self):
        """Clean asset bundles."""
        try:
            self.assets.clean()
            self.logger.info("Cleaned asset bundles successfully")
            return True
        except Exception as e:
            self.logger.error(f'Error cleaning assets: {str(e)}')
            raise

    def watch_assets(self):
        """Watch assets for changes."""
        try:
            self.assets.watch()
            self.logger.info("Watching assets for changes...")
            return True
        except Exception as e:
            self.logger.error(f'Error watching assets: {str(e)}')
            raise


def create_cli_commands():
    """Create CLI command groups and commands."""
    db_commands = DatabaseCommands()
    user_commands = UserCommands()
    asset_commands = AssetCommands()

    @click.group(name='db')
    def db_cli():
        """Database management commands."""
        pass

    @db_cli.command()
    @with_appcontext
    def create():
        """Create database tables."""
        try:
            db_commands.create_tables()
            click.echo('Database tables created successfully')
        except Exception as e:
            click.echo(f'Error: {str(e)}')

    @db_cli.command()
    @with_appcontext
    def init():
        """Initialize database with default data."""
        try:
            db_commands.init_db()
            click.echo('Database initialized successfully')
        except Exception as e:
            click.echo(f'Error: {str(e)}')

    @db_cli.command()
    @with_appcontext
    def drop():
        """Drop all database tables."""
        try:
            if click.confirm('Are you sure you want to drop all tables?'):
                db_commands.drop_tables()
                click.echo('Database tables dropped successfully')
        except Exception as e:
            click.echo(f'Error: {str(e)}')

    @db_cli.command()
    @with_appcontext
    def recreate():
        """Recreate database tables."""
        try:
            if click.confirm('Are you sure you want to recreate all tables? This will delete all data.'):
                db_commands.recreate_tables()
                click.echo('Database recreated successfully')
        except Exception as e:
            click.echo(f'Error: {str(e)}')

    @click.command("create-admin")
    @click.option("--username", prompt=True, help="Admin username")
    @click.option("--email", prompt=True, help="Admin email")
    @click.option("--password", prompt=True, hide_input=True,
                 confirmation_prompt=True, help="Admin password")
    @with_appcontext
    def create_admin(username, email, password):
        """Create an admin user."""
        try:
            user_commands.create_admin_user(username, password, email)
            click.echo(f"Created admin user: {username}")
        except Exception as e:
            click.echo(f'Error: {str(e)}')

    @click.group(name='assets')
    def assets_cli():
        """Asset management commands."""
        pass

    @assets_cli.command("build")
    @with_appcontext
    def build_assets():
        """Build asset bundles."""
        try:
            asset_commands.build_assets()
            click.echo("Built asset bundles successfully")
        except Exception as e:
            click.echo(f'Error: {str(e)}')

    @assets_cli.command("clean")
    @with_appcontext
    def clean_assets():
        """Clean asset bundles."""
        try:
            asset_commands.clean_assets()
            click.echo("Cleaned asset bundles successfully")
        except Exception as e:
            click.echo(f'Error: {str(e)}')

    @assets_cli.command("watch")
    @with_appcontext
    def watch_assets():
        """Watch assets for changes."""
        try:
            asset_commands.watch_assets()
            click.echo("Watching assets for changes...")
        except Exception as e:
            click.echo(f'Error: {str(e)}')

    return db_cli, create_admin, assets_cli


def register_commands(app):
    """Register all CLI commands."""
    db_cli, create_admin, assets_cli = create_cli_commands()
    app.cli.add_command(db_cli)
    app.cli.add_command(create_admin)
    app.cli.add_command(assets_cli)
