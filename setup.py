from setuptools import setup

setup(
    name='icaltools',
    version='0.1',
    packages=['icaltools'],
    install_requires=[
        # List your dependencies here
        'ics==0.8.0.dev0',
    ],
    entry_points={
        'console_scripts': [
            'icaltools=icaltools.cli:main',  # Adjust as needed
        ],
    },
)
