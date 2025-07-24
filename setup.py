# setup.py

from setuptools import setup, find_packages

setup(
    name='ImageDatasetBuilder',
    version='1.0.0',
    author='antoningr',
    description='Tool to automatically build image datasets from web search',
    py_modules=['image_dataset_builder'],
    install_requires=[
        'ddgs',
        'pillow',
        'requests',
        'matplotlib'
    ],
    entry_points={
        'console_scripts': [
            'image-dataset-builder = image_dataset_builder:main',
        ],
    },
)
