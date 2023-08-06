# -*- coding: utf-8 -*-
# @Time    : 2022/5/6 下午4:07
# @Author  : kyq
# @Software: PyCharm

import os
import sys

try:
    from setuptools import setup, find_packages
    from setuptools.extension import Extension
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup
    from distutils.core import setup, find_packages
    from distutils.extension import Extension

extra_opts = {}

python_2 = sys.version_info < (3,)

try:
    with open("README.md", "r") as fd:
        extra_opts['long_description'] = fd.read()
except IOError:
    pass        # Install without README.md

packages = ["mongo_connector", "mongo_connector.doc_managers"]
package_metadata = {
    "name": "new_neo4j-doc-manager",
    "version": "3.0.3",
    "description": "Neo4j Doc manager for Mongo Connector",
    "long_description": "Neo4j Doc Manager is a tool that will import data in Mongodb for a " 
                        "Neo4j graph structure, via Mongo-Connector.",
    "author": "Smarter_KYQ",
    "author_email": "keyuqiangsmarter@163.com",
    "url": "https://gitee.com/Smarter_KYQ/Neo4j_doc-manager.git",
    "entry_points": {
        "console_scripts": [
            'mongo-connector = mongo_connector.connector:main',
        ],
    },
    "packages": packages,
    "install_requires": ['mongo-connector>=2.1','py2neo==2021.1.2','requests>=2.5.1'],
    "license": "Apache Software License",
    "classifiers": [
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Topic :: Database",
        "Topic :: Software Development",
    ],
}


try:
    setup(ext_modules=extension, **package_metadata)
except:
    setup(**package_metadata)
