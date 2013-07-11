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
        'versiontools>=1.9.1,<1.10',
        'Django>=1.4.5,<1.5',
        'django-model-utils>=1.1.0,<1.5',
        'djangorestframework>=2.1.12,<2.2',
        'South>=0.7.6,<0.9',
        'django-treebeard>=1.61,<1.7',
        'django-appconf>=0.6,<0.7',
        'django-twitter-tag>=1.1,<1.2',
        'pillow>=2.0.0,<2.1',
        'sorl-thumbnail>=11.12,<12',
        'django-compressor>=1.2,<1.4',
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
