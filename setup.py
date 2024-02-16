from setuptools import setup
from version import __version__
setup(
    name='dailylog',
    version=__version__,
    py_modules=['dailylog'],
    install_requires=[
        'Click',
        'python-dateutil',
    ],
    entry_points={
        'console_scripts': [
            'dailylog = dailylog:dailylog',
        ],
    }
)
