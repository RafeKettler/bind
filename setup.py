#!/usr/bin/env python

from distutils.core import setup
import bind

setup(
    name='bind',
    version=bind.__version__,
    description='A framework for creating web API bindings in Python',
    author='Rafe Kettler',
    author_email='rafe.kettler@gmail.com',
    license='MIT',
    url='http://www.github.com/RafeKettler/bind',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Libraries :: Application Frameworks',
        ]
    requires=['httplib2'],
    packages=['bind'],
)

    
