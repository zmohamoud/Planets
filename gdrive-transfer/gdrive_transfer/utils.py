import os

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

HOME_DIR = os.path.expanduser('~')
CREDENTIALS_CACHE = os.path.join(HOME_DIR, '.gdrive_transfer.json')
FOLDER_MIME_TYPE = 'application/vnd.google-apps.folder'
NAME_FIELD = 'title'


class GDriveTransferException(Exception):
    pass


def authorize(silent=False):
    """
    This function authorizes the application. First, we check to see if
    there are cached credentials. If that is not the case, or if the credentials
    are no longer valid, we must then continue the OAuth work flow.

    :param silent: :boolean: whether this function should be expected to run 
        silently or not. If it is silent and user interaction is needed (e.g. 
        for OAuth stuff), we raise an exception.

    :returns: :GoogleAuth: gauth object
    """
    gauth = GoogleAuth()

    gauth.LoadCredentialsFile(CREDENTIALS_CACHE)

    if not gauth.credentials:
        if not silent:
            # Prompts user to complete authorization process
            gauth.CommandLineAuth()
            gauth.SaveCredentialsFile(CREDENTIALS_CACHE)
        else:
            raise GDriveTransferException('User interaction needed. Failing...')

    return gauth


def upload(resource, gauth, folder=None):
    """
    Uploads a resource to the authorized Google Drive account
    
    :param resource: :string: The resource you wish to upload
    :param gauth: :GoogleAuth:
    :param folder: :string: The location of the resource (optional)
    
    :return: :boolean:
    """
    drive = GoogleDrive(gauth)

    if os.path.isfile(resource):
        metadata = {
            'title': os.path.basename(resource)
        }

        # Sets the parent folder if provided
        if folder:
            metadata['parents'] = [{
                "kind": "drive#fileLink", "id": folder['id']
            }]

        file1 = drive.CreateFile(metadata)
        file1.SetContentFile(resource)
        file1.Upload()

        return True
    else:
        raise NotImplemented('This resource type is not implement yet')


def get_folder_query(name, parent=None):
    """
    Provided a name, parent and is_root flag, build the appropriate query
    string for the GoogleDrive API (v2). More information here:
        https://developers.google.com/drive/v2/web/search-parameters
    
    :param name: :string: name of the folder
    :param parent: :string: ID of the parent
    
    :return: :string:
    """
    queries = []

    if parent:
        queries.append("'{}' in parents".format(parent))

    queries.append("{} = '{}'".format(NAME_FIELD, name))

    return ' and '.join(queries)


def create_or_get_folder(location, gauth):
    """
    Provided a path (e.g. path/to/your/file.txt), creates or retrieves all of
    the folders along the way.
    
    :param location: A full path of folders
    
    :return: :GoogleDriveFile: the bottom most folder
    """
    drive = GoogleDrive(gauth)
    folders = os.path.split(location)
    cur_folder = {}

    for idx, folder in enumerate(filter(None, folders)):
        if idx == 0:
            parent = 'root'
        elif cur_folder.get('id'):
            parent = cur_folder['id']
        else:
            parent = None

        query = get_folder_query(
            folder, parent=parent
        )

        query_res = drive.ListFile({'q': query}).GetList()

        if len(query_res) > 0:
            cur_folder = query_res[0]
            continue

        metadata = {
            NAME_FIELD: folder,
            'mimeType': FOLDER_MIME_TYPE
        }

        if cur_folder:
            metadata['parents'] = [{
                "kind": "drive#fileLink",
                "id": cur_folder['id']
            }]

        folder = drive.CreateFile(metadata)
        folder.Upload()

        cur_folder = folder

    return cur_folder
