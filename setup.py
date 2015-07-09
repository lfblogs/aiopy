from distutils.core import setup

setup(
    name='Pyaio',
    version='1.0.2',
    packages=[ 'Pyaio', 'Pyaio.db', 'Pyaio.app',
              'Pyaio.orm', 'Pyaio.apis', 'Pyaio.conf', 'Pyaio.http', 'Pyaio.utils'],
    url='http://github.com/lfblogs/Pyaio',
    license='GUN License',
    author='lfblogs',
    author_email='13701242710@163.com',
    description='Simple Python Web Frame'
)
