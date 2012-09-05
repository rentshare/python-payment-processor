from distutils.core import setup

setup(name='payment_processor',
      version='0.1.0',
      description='A simple payment gateway api',
      author='Rentshare Inc',
      url='http://github.com/rentshare/python-payment',
      packages=['payment_processor','payment_processor.gateways'],
      install_requires=['requests'],
     )
