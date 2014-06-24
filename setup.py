#!/usr/bin/env python
from fancypages import __version__
from setuptools import setup, find_packages


setup(
    name='django-fancypages',
    version=__version__,
    url='https://github.com/tangentlabs/django-fancypages',
    author="Sebastian Vetter",
    author_email="sebastian.vetter@tangentsnowball.com.au",
    description="Make content editing in Django fancier",
    long_description='\n\n'.join([
        open('README.rst').read(),
        open('CHANGELOG.rst').read(),
    ]),
    keywords="django, cms, pages, flatpages",
    license='BSD',
    platforms=['linux'],
    packages=find_packages(exclude=["sandbox*", "tests*"]),
    include_package_data=True,
    install_requires=[
        'Django>=1.5',
        'South',
        'unidecode',
        'django-appconf',
        'django-treebeard',
        'django-model-utils',
        'django-shortuuidfield',
        # we are using DRF routers that are only available in
        # DRF 2.3+ so we are restricting the version here
        'djangorestframework>=2.3.10',
        'pillow',
        'sorl-thumbnail>=11.12.1b',
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
