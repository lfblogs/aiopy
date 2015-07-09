from distutils.core import setup

setup(
    name='aiopy',
    version='1.0.1',
    packages=[ 'aiopy', 'aiopy.db', 'aiopy.app',
              'aiopy.orm', 'aiopy.apis', 'aiopy.conf', 'aiopy.http', 'aiopy.utils'],
    url='http://github.com/lfblogs/aiopy',
    license='GUN License',
    author='lfblogs',
    author_email='13701242710@163.com',
    description='Simple Python Web Frame'
)
