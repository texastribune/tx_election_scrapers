from setuptools import setup, find_packages

setup(
    name='tx_elections_scrapers',
    description='Scrapers for Texas elections results',
    long_description=open('README.md').read(),
    version='0.0.0',
    author='The Texas Tribune',
    author_email='tech@texastribune.org',
    maintainer='Chris Chang',
    maintainer_email='c@crccheck.com',
    url='https://github.com/texastribune/tx_election_scrapers',
    # use `find_packages` to make it easier to add modules in the future
    packages=find_packages(exclude=('test_*', )),
    include_package_data=True,  # automatically include things from MANIFEST.in
    license='Apache License, Version 2.0',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
    ],
)
