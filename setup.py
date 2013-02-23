import os
import sys

from setuptools import setup
from setuptools import find_packages


here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()


requires = [
    'Django==1.3.7',
    'python-memcached',
    'South==0.7.3',
    'httplib2',
    'sunburnt',
    'pysolr',
    'python-dateutil',
    'django-debug-toolbar',
    'django-haystack',
    'python-twitter',
    'requests',
    'icalendar',
]

if sys.platform != "darwin":
    requires.append('psycopg2')


setup(
    name='delajozate',
    version='0.1',
    description='',
    long_description=README,
    classifiers=[
    ],
    author=u'',
    author_email='',
    url='',
    keywords='',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=requires,
    entry_points="""
    [console_scripts]
    """,
    extras_require={
        'test': [],
        'develop': [],
    },
)
