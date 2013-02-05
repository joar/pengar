from setuptools import setup, find_packages

install_requires = []

for line in open('requirements.txt', 'r'):
    if line[0] == '#':
        continue

    install_requires.append(line)


setup(
    name='pengar',
    version='0.0.1-dev',
    author='Joar Wandborg',
    author_email='joar@wandborg.se',
    install_requires=install_requires,
    entry_points={
        'console_scripts': [
            'pengar = pengar:main',
        ],
    },
    url='https://github.com/joar/pengar/')
