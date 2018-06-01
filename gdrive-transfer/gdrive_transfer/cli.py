import click

from .utils import (
    authorize, upload as gdrive_upload,
    create_or_get_folder as gdrive_create_or_get_folder,
    GDriveTransferException
)


@click.group()
def cli():
    pass


@click.command()
def init():
    """
    Initialize your configuration
    """
    authorize()


@click.command()
@click.argument('resource', type=click.Path(exists=True))
@click.option(
    '--location',
    help='The location you wish to store at in Google Drive',
    default=''
)
def upload(resource, location):
    """
    The resource to upload to Google Drive
    """
    try:
        gauth = authorize(True)
    except GDriveTransferException:
        raise click.ClickException(
            'Unable to fetch cached credentials. Please run `gdrive init` '
            'to refresh'
        )

    folder = gdrive_create_or_get_folder(location, gauth)
    gdrive_upload(resource, gauth, folder=folder)

cli.add_command(upload)
cli.add_command(init)
