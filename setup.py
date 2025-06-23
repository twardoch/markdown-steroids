import os.path
from setuptools import setup

# Get the long description from the README file
readmepath = os.path.join(os.path.realpath(os.path.dirname(__file__)), "README.md")
long_description = ""
if os.path.exists(readmepath):
    with open(readmepath, encoding="utf-8") as f:
        long_description = f.read()

setup(
    name="mdx_steroids",
    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version="0.7.0",
    description="Small collection of Python Markdown extensions",
    long_description=long_description,
    # The project's main homepage.
    url="https://github.com/twardoch/markdown-steroids/",
    download_url="https://github.com/twardoch/markdown-steroids/archive/master.zip",
    # Author details
    author="Adam Twardoch",
    author_email="adam+github@twardoch.com",
    # Choose your license
    license="LICENSE",
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Environment :: MacOS X",
        "Environment :: Console",
        "Operating System :: MacOS :: MacOS X",
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        "Development Status :: 3 - Alpha",
        # Indicate who your project is intended for
        "Intended Audience :: Developers",
        "Topic :: Text Processing",
        "Topic :: Text Processing :: Filters",
        "Topic :: Text Processing :: Markup",
        "Topic :: Text Processing :: Markup :: HTML",
        "Topic :: Software Development :: Documentation",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Natural Language :: English",
        # Pick your license as you wish (should match "license" above)
        "License :: OSI Approved :: BSD License",
        # Specify the Python versions you support here.
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    # What does your project relate to?
    keywords=[
        "Markdown",
        "typesetting",
        "include",
        "plugin",
        "extension",
        "python-markdown",
    ],
    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=["mdx_steroids"],
    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=[
        "markdown>=3.5.0",  # Updated to a newer version
        "mako>=1.0.7",  # Assuming Mako is still compatible; verify during testing
        "pymdown-extensions>=9.0",  # Updated to a newer version, assuming compatibility
        "cssselect>=1.0.1",  # Usually stable
        "lxml>=3.8.0",  # Usually stable, but check Python 3 specifics
        "beautifulsoup4>=4.6.0",  # Usually stable
    ],
    python_requires=">=3.8",  # Specify minimum Python version
)
