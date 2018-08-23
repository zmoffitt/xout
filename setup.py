from setuptools import setup

setup(
    name='xout',
    version='0.2',
    py_modules=['xout'],
    install_requires=[
        'docopt',
        'tqdm',
    ],
    entry_points={
        'console_scripts': [
            'xout=xout:main',
        ],
    }
)
