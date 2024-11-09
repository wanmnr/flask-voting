# app/cli.py

import click
from flask import current_app
from flask.cli import with_appcontext
from app.core.extensions import db
from app.models.user import User
from app.core.assets import assets

def register_commands(app):
    """Register CLI commands."""
    app.cli.add_command(init_db_command)
    app.cli.add_command(create_admin_command)
    app.cli.add_command(assets_command)

@click.command("init-db")
@with_appcontext
def init_db_command():
    """Initialize the database."""
    db.create_all()
    click.echo("Initialized the database.")

@click.command("create-admin")
@click.option("--username", prompt=True, help="Admin username")
@click.option("--password", prompt=True, hide_input=True, confirmation_prompt=True, help="Admin password")
@with_appcontext
def create_admin_command(username, password):
    """Create an admin user."""
    user = User(
        username=username,
        is_admin=True
    )
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    click.echo(f"Created admin user: {username}")

@click.group()
def assets_command():
    """Asset management commands."""
    pass

@assets_command.command("build")
@with_appcontext
def build_assets():
    """Build asset bundles."""
    assets.build()
    click.echo("Built asset bundles.")

@assets_command.command("clean")
@with_appcontext
def clean_assets():
    """Clean asset bundles."""
    assets.clean()
    click.echo("Cleaned asset bundles.")

@assets_command.command("watch")
@with_appcontext
def watch_assets():
    """Watch assets for changes."""
    assets.watch()
    click.echo("Watching assets for changes...")
