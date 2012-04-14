from setuptools import setup, find_packages
import sys, os

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()


version = '0.1'

install_requires = [
    # List your project dependencies here.
    # For more details, see:
    # http://packages.python.org/distribute/setuptools.html#declaring-dependencies
    'requests',
]

test_requires = [
    'nose',
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
    package_dir = {'': 'src'},include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    tests_require=test_requires,
    entry_points={
        'console_scripts':
            ['bookie_api=bookie_api:client.main']
    }
)
