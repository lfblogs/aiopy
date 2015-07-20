from distutils.core import setup

setup(
    name='aiopy',
    version='1.1.6',
    packages=['aiopy', 'aiopy.db', 'aiopy.api', 'aiopy.app', 'aiopy.conf', 'aiopy.http', 'aiopy.utils',
              'aiopy.required', 'aiopy.required.aiohttp', 'aiopy.required.aiomysql', 'aiopy.required.aiomysql.sa'],
    url='http://github.com/lfblogs',
    license='GUN License',
    author='Liu Fei',
    author_email='13701242710@163.com',
    description='Simple Web Frame about mysql'
)
