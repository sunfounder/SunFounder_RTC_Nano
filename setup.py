from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'DESCRIPTION.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='rtc_nano',
    version='1.0.0',
    description='RTC Nano from SunFounder',
    long_description=long_description,
    url='https://github.com/sunfounder/SunFounder_RTC_Nano',

    author='sunfounder',
    author_email='support@sunfounder.com',

    license='GNU',
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Stable',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        'License :: OSI Approved :: GNU License',

        'Programming Language :: Python :: 2.7',
    ],

    keywords='rtc sunfounder raspberry pi ds18b20 temperature sensor',

    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    package_data={
        'config': ['config.dat'],
    },
    entry_points={
        'console_scripts': [
            'rtc-nano=rtc_nano:main',
        ],
    },
)
