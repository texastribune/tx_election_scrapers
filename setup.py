from setuptools import setup, find_packages

setup(
    name='tx_elections_scrapers',
    description='Scrapers for Texas elections results',
    long_description=open('README.rst').read(),
    version='0.4.1',
    author='The Texas Tribune',
    author_email='tech@texastribune.org',
    maintainer='Chris Chang',
    maintainer_email='c@crccheck.com',
    url='https://github.com/texastribune/tx_election_scrapers',
    # use `find_packages` to make it easier to add modules in the future
    packages=find_packages(exclude=('test_*', )),
    include_package_data=True,  # automatically include things from MANIFEST.in
    entry_points={
        'console_scripts': [
            'serialize_county = tx_elections_scrapers.sos.serialize_county:main',
            'serialize_statewide = tx_elections_scrapers.sos.serialize_statewide:main',
            'interpret_county = tx_elections_scrapers.sos.interpret_county:main',
            'interpret_statewide = tx_elections_scrapers.sos.interpret_statewide:main',
        ],
    },
    install_requires=[
        'PyYAML',
        'docopt',
        'lxml',
        'python-dateutil',
    ],
    license='Apache License, Version 2.0',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],
)
