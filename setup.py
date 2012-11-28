from distutils.core import setup

setup(name='payment_processor',
      version=open('VERSION').read().strip(),
      description='A simple payment gateway api',
      author='Rentshare Inc',
      url='http://github.com/rentshare/python-payment',
      packages=['payment_processor','payment_processor.gateways'],
      install_requires=['requests'],
     )
