from setuptools import setup, find_packages

setup(
    name="drug-mentions",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'pyyaml>=5.4.1',
        'charset-normalizer>=2.0.0',
    ],
    extras_require={
        'test': [
            'pytest>=6.2.5',
            'pytest-cov>=2.12.1',
            'pytest-mock>=3.6.1',
        ],
    },
)