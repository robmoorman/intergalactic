from setuptools import find_packages, setup


setup(
    name='intergalactic',
    package_dir={
        '': 'src'
    },
    packages=find_packages('src'),
    entry_points={
        'console_scripts': [
            'intergalactic=intergalactic.cli:execute'
        ]
    },
    include_package_data=True
)
