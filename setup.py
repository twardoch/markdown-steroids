import os.path
from codecs import open

from setuptools import setup

try:
    from sh import pandoc

    isPandoc = True
except ImportError:
    isPandoc = False

# Get the long description from the README file
readmepath = os.path.join(os.path.realpath(os.path.dirname(__file__)), 'README.md')
long_description = ''
if os.path.exists(readmepath):
    if isPandoc:
        long_description = pandoc(readmepath, read='markdown', write='rst')
    else:
        long_description = open(readmepath, encoding='utf-8').read()

setup(
    name='mdx_steroids',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version='0.4.2',

    description='Small collection of Python Markdown extensions',
    long_description=long_description,

    # The project's main homepage.
    url='https://github.com/twardoch/markdown-steroids/',
    download_url='https://github.com/twardoch/markdown-steroids/archive/master.zip',

    # Author details
    author='Adam Twardoch',
    author_email='adam+github@twardoch.com',

    # Choose your license
    license='LICENSE',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Environment :: MacOS X',
        "Environment :: Console",
        'Operating System :: MacOS :: MacOS X',
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Text Processing',
        'Topic :: Text Processing :: Filters',
        'Topic :: Text Processing :: Markup',
        'Topic :: Text Processing :: Markup :: HTML',
        'Topic :: Software Development :: Documentation',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Natural Language :: English',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: BSD License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2.7',
    ],

    # What does your project relate to?
    keywords=['Markdown', 'typesetting', 'include', 'plugin', 'extension'],

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=['mdx_steroids'],

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=[
        'markdown>=2.6.7',
    ],
)
