from setuptools import setup, find_packages

setup(
    name = 'backtrader_hello',
    version = '0.1',
    author_email = 'syuraj@gmail.com',
    license = 'GPLv3',
    description = 'backtrader hello',
    package_data = {
        'backtrader_hello': [
            'datas/*/*/*csv'
        ],
    },
    packages = find_packages(),
    install_requires = [
        'pandas',
        'git+https://github.com/happydasch/btplotting'
    ],
    classifiers = [
        'Environment :: Console',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3 :: Only'
    ],
)