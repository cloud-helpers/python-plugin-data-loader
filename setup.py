# -*- encoding: utf-8 -*-
import glob
import os
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='data-loader-plugin',
    version='0.0.1.post1',
    license='MIT',
    description='Python plugin/extra to load data files from an external source (such as AWS S3) to a local directory',
    long_description_content_type='text/markdown',
    long_description=long_description,
    author='Stanislav Khrapov',
    author_email='khrapovs@gmail.com',
    url='https://github.com/cloud-helpers/python-plugin-data-loader',
    packages=setuptools.find_packages(),
    py_modules=[os.path.splitext(os.path.basename(path))[0] for path in glob.glob('data_loader_plugin/{base,copyfile,s3}.py')],
    include_package_data=True,
    classifiers=[
        # complete classifier list: http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Utilities',
    ],
    project_urls={
        'Documentation': 'https://github.com/cloud-helpers/python-plugin-data-loader',
        'Issue Tracker': 'https://github.com/cloud-helpers/python-plugin-data-loader/issues',
    },
    keywords=[
        'data', 'machine-learning', 'data-loader', 'ml',
    ],
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*',
    install_requires=[
        'boto3',
    ],
    extras_require={
        # eg:
        #   'rst': ['docutils>=0.11'],
        #   ':python_version=="2.6"': ['argparse'],
    },
    entry_points={
    },
)

