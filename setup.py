#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name='django-fancypages',
    version=":versiontools:fancypages:",
    url='https://github.com/tangentlabs/django-fancypages',
    author="Sebastian Vetter",
    author_email="sebastian.vetter@tangentsnowball.com.au",
    description="Make content editing in Django fancier",
    long_description=open('README.rst').read(),
    keywords="django, cms, pages, flatpages",
    license='BSD',
    platforms=['linux'],
    packages=find_packages(exclude=["sandbox*", "tests*"]),
    include_package_data=True,
    install_requires=[
        'versiontools>=1.9.1',
        'Django>=1.4.5',
        'django-model-utils>=1.1.0',
        'djangorestframework>=2.1.12',
        'South>=0.7.6',
    ],
    # See http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
      'Environment :: Web Environment',
      'Intended Audience :: Developers',
      'License :: OSI Approved :: BSD License',
      'Operating System :: Unix',
      'Programming Language :: Python',
    ]
)
