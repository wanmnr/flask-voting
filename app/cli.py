# app/cli.py

import click
import time
from flask import current_app
from flask.cli import with_appcontext

@click.group(name='assets')
def assets_cli():
    """Asset management commands"""
    pass

@assets_cli.command()
@with_appcontext
def build():
    """Build all assets"""
    assets = current_app.extensions['assets']
    assets.build()
    click.echo('Assets built successfully')

# Add this function for direct calling
def build_assets_command():
    """Build assets programmatically"""
    assets = current_app.extensions['assets']
    assets.build()

@assets_cli.command()
@with_appcontext
def clean():
    """Clean all built assets"""
    assets = current_app.extensions['assets']
    for bundle in assets:
        bundle.build(force=True)
        if bundle.output:
            try:
                bundle.remove_files()
                click.echo(f'Removed {bundle.output}')
            except OSError as e:
                click.echo(f'Error removing {bundle.output}: {e}')

@assets_cli.command()
@with_appcontext
def watch():
    """Watch assets for changes and rebuild"""
    assets = current_app.extensions['assets']
    try:
        assets.auto_build = True
        while True:
            click.echo('Watching assets for changes...')
            time.sleep(1)
    except KeyboardInterrupt:
        click.echo('\nStopped watching assets')



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
    from app.models import User
    
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
        from app.models import User
        if not User.query.filter_by(username='admin').first():
            admin = User(username='admin', email='admin@example.com')
            admin.set_password('adminpassword')
            db.session.add(admin)
            db.session.commit()
            click.echo('Admin user created successfully')
        else:
            click.echo('Admin user already exists')



# Update init_cli function to include db commands
def init_cli(app):
    """Register CLI commands with Flask app"""
    app.cli.add_command(assets_cli)
    app.cli.add_command(db_cli)

