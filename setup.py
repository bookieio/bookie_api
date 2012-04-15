from setuptools import setup, find_packages
import sys, os

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()


version = '0.4.0b2'

install_requires = [
    # List your project dependencies here.
    # For more details, see:
    # http://packages.python.org/distribute/setuptools.html#declaring-dependencies
    'requests',
]

tests_require = [
    'coverage',
    'nose',
    'pep8',
]


setup(name='bookie_api',
    version=version,
    description="Api and command line client for Bookie",
    long_description=README,
    classifiers=[
      # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    ],
    keywords='bookmarks api client command line',
    author='Rick Harding',
    author_email='rharding@mitechie.com',
    url='http://docs.bmark.us',
    license='AGPL',
    packages=find_packages('src'),
    package_dir = {'': 'src'},
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    tests_require=tests_require,
    extras_require={'test': tests_require},
    entry_points={
        'console_scripts':
            ['bookie=bookie_api:client.main']
    }
)
