from distutils.core import setup

setup(name='payment_processor',
      version='0.1.0',
      description='A simple payment gateway api',
      author='Rentshare Inc',
      url='http://github.com/rentshare/python-payment',
      packages=['payment_processor'],
      install_requires=['requests'],
     )
