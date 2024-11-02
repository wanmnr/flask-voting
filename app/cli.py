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

# Function to register commands with Flask app
def init_cli(app):
    """Register CLI commands with Flask app"""
    app.cli.add_command(assets_cli)
