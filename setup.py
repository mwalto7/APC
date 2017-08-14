from setuptools import setup

setup(
    name='APConfig',
    version='1.0',
    py_modules=['cli'],
    install_requires=[
        'Click',
        'netmiko',
        'openpyxl',
        'bcrypt',
        'pandas',
    ],
    entry_points={
        'console_scripts': [
            'apc=cli:cli',
        ],
    },
)
