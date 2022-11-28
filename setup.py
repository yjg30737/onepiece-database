from setuptools import setup, find_packages

setup(
    name='onepiece-database',
    version='0.0.12',
    author='Jung Gyu Yoon',
    author_email='yjg30737@gmail.com',
    license='MIT',
    packages=find_packages(),
    description='Get the One Piece characters info with one click from ONE PIECE WIKI',
    url='https://github.com/yjg30737/onepiece-database.git',
    install_requires=[
        'PyQt5',
        'pandas'
    ]
)