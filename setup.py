from setuptools import setup
from os import path

setup(
    name='mdx_steroids',
    version='0.2.0',
    author='Adam Twardoch',
    author_email='adam+github@twardoch.com',
    url = 'https://github.com/twardoch/markdown-steroids/',
    description='Small collecion of Python Markdown extensions',
    long_description=open('README.md').read(),
    download_url='https://github.com/twardoch/markdown-steroids/archive/master.zip',
    license=open('LICENSE').read(),
    packages=['mdx_steroids'],
	keywords = ['Markdown', 'typesetting', 'include', 'plugin', 'extension'],
    install_requires=[
        'markdown'
    ],

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Internet :: WWW/HTTP :: Site Management',
        'Topic :: Software Development :: Documentation',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing :: Filters',
        'Topic :: Text Processing :: Markup :: HTML',
        'Natural Language :: English',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Text Processing'
    ]
)