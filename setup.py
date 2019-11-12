from setuptools import setup

version = '1.0.3'

setup(
    name='ilock',
    packages=['ilock'],
    version=version,
    description='Inter-process named lock library',
    author='SymonSoft',
    author_email='symonsoft@gmail.com',
    url='https://github.com/symonsoft/ilock',
    download_url='https://github.com/symonsoft/ilock/tarball/{0}'.format(
        version),
    keywords=['interprocess', 'multiprocessing', 'lock', 'mutex', 'os-independent'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Utilities'
    ],
    install_requires=['portalocker']
)
