# app/core/cli.py

import click
from flask import current_app
from flask.cli import with_appcontext
from ..extensions.db import db
from ..extensions.assets import assets


def register_commands(app):
    """Register CLI commands."""
    app.cli.add_command(init_db_command)
    app.cli.add_command(create_admin_command)
    app.cli.add_command(assets_command)
    app.cli.add_command(db_cli)



@click.group(name='db')
def db_cli():
    """Database management commands"""
    pass

@db_cli.command()
@with_appcontext
def create():
    """Create database tables"""
    db.create_all()
    click.echo('Database tables created successfully')

@db_cli.command()
@with_appcontext
def init():
    """Initialize database with default data"""
    from app.models.user import User

    # Create tables if they don't exist
    db.create_all()

    # Check if admin user exists
    if not User.query.filter_by(username='admin').first():
        admin = User(username='admin', email='admin@example.com')
        admin.set_password('adminpassword')
        db.session.add(admin)
        db.session.commit()
        click.echo('Admin user created successfully')
    else:
        click.echo('Admin user already exists')

@db_cli.command()
@with_appcontext
def drop():
    """Drop all database tables"""
    if click.confirm('Are you sure you want to drop all tables?'):
        db.drop_all()
        click.echo('Database tables dropped successfully')

@db_cli.command()
@with_appcontext
def recreate():
    """Recreate database tables (drop and create) and initialize with default data"""
    if click.confirm('Are you sure you want to recreate all tables? This will delete all data.'):
        db.drop_all()
        db.create_all()
        click.echo('Database tables recreated successfully')

        # Initialize default data
        from app.models.user import User
        if not User.query.filter_by(username='admin').first():
            admin = User(username='admin', email='admin@example.com')
            admin.set_password('adminpassword')
            db.session.add(admin)
            db.session.commit()
            click.echo('Admin user created successfully')
        else:
            click.echo('Admin user already exists')



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
    from app.models.user import User
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
