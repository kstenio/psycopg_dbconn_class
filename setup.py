#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2023 Kleydson Stenio <kleydson.stenio@gmail.com>.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/lgpl-3.0.html>.

# Imports
from pathlib import Path
from setuptools import find_packages, setup

# Settings
try:
	with Path(__file__).parent.joinpath('app', 'README_LIB.md').open('r') as f:
		long_description = f.read()
except FileNotFoundError:
	with Path.cwd().parents[1].joinpath('app', 'README_LIB.md').open('r') as f:
		long_description = f.read()

# Setuptools
setup(
	name='psycopg_dbconn_class',
	version='0.0.1',
	description='A simple class to better handle database connections using psycopg2 (PostgreSQL)',
	package_dir={'': 'app'},
	packages=find_packages(where='app'),
	long_description=long_description,
	long_description_content_type='text/markdown',
	url='https://github.com/kstenio/psycopg_dbconn_class',
	author='Kleydson Stenio',
	author_email='kleydson.stenio@gmail.com',
	classifiers=[
		'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
		'Programming Language :: Python :: 3.9',
		'Operating System :: OS Independent',
	],
	install_requires=['psycopg2-binary~=2.9.3'],
	extras_require={
		"dev": ["twine>=4.0.2"],
		},
	python_requires='>=3.9',
)

# Important info:
# 01) pip, setuptools, wheel and twine must be installed into system;
# 02) Use command `python setup.py bdist_wheel sdist` to check if build folders are created (whl/tar.gz files as well);
# 03) Use command `twine check dist/*` to check if all files are fine;
# 04) Package can also be installed locally. In this case, use command `pip install .` to test it;
# 05) Test passed? Now create user and API key for TestPyPI repository (https://test.pypi.org/);
# 06) Now make sure the env is set, saving API kei in .pypirc;
# 07) For more info on that, check the website: https://packaging.python.org/en/latest/specifications/pypirc/;
# 05) To upload the package into the TestPyPI repository, use command `twine upload -r testpypi dist/*`;
# 08) Now, we can use pip to check if package downloads fine: `pip install -i https://test.pypi.org/simple/ PKG_NAME`;
# 09) If appear the message "Successfully installed PKG_NAME", congrats! Now open python, and try to import the package;
# 10) Ok, time to go bigger and use official PyPI repository. Create account, API, and update .pypirc file;
# 11) Do any proper changes/updates into the main home project (e.g.: GitHub);
# 12) Finally, upload data to PyPI: `twine upload dist/*`;
# 13) Your package is ready!
#
# Now... if Debian (.deb) file is needed, some extra steps:
# 01) Install system dependencies: `sudo apt install python3-all fakeroot debhelper dh-python`;
# 02) Configure setup.cfg and stdeb.cfg files;
# 03) Use the revised command: `python setup.py --command-packages=stdeb.command sdist_dsc sdist bdist_wheel bdist_deb`;
# 04) Check if artifacts are properly created (deb files, etc.).
