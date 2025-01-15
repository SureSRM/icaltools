from setuptools import setup

setup(
    name='ical',
    version='0.1',
    packages=['ical'],
    install_requires=[
        # List your dependencies here
        'ics',
    ],
    entry_points={
        'console_scripts': [
            'ical=ical.cli:main',  # Adjust as needed
        ],
    },
)
