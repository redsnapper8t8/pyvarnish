from setuptools import setup, find_packages

from pyvarnish import __author__, __version__
setup(
    name='pyvarnish',
    version=__version__,
    description='Varnish Management',
    long_description=open('README.rst').read(),
    author=__author__,
    author_email='john@8t8.eu',
    url='https://github.com/redsnapper8t8/pyvarnish',
    license='BSD',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: System Administrators',
        'Topic :: System :: Monitoring',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        ]
)