from setuptools import setup

version = '0.1'

description = "CLI tools for transferring files to Google Drive"

setup(
    name="gdrive_transfer",
    version=version,
    url='http://github.com/travishathaway/gdrive-transfer',
    license='BSD',
    description=description,
    author='Travis Hathaway',
    author_email='travis.j.hathaway@gmail.com',
    packages=['gdrive_transfer', ],
    install_requires=[
        'setuptools', 
        'click==6.7',
        'PyDrive==1.3.1',
        'pytest==3.0.5'
    ],
    entry_points="""
        [console_scripts]
        gdrive = gdrive_transfer.cli:cli
    """,
    classifiers=[
        'Environment :: Console',
    ],
)
