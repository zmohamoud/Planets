from gdrive_transfer.utils import get_folder_query, NAME_FIELD


def test_get_folder_query():
    """
    Runs various tests on the get_folder_query function
    """
    # No parent and not root
    query = get_folder_query('Blah')
    assert query == "{} = 'Blah'".format(NAME_FIELD)

    # With parent
    query = get_folder_query('Blah', parent='123456789')
    assert query == "'123456789' in parents and {} = 'Blah'".format(NAME_FIELD)

    # Parent as root
    query = get_folder_query('Blah', parent='root')
    assert query == "'root' in parents and {} = 'Blah'".format(NAME_FIELD)


if __name__ == '__main__':
    test_get_folder_query()
