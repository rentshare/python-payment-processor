from distutils.core import setup

setup(name='payment_processor',
      version='0.1.0',
      description='A simple payment gateway api wrapper',
      author='Ian Halpern',
	  author_email='ian@ian-halpern.com',
      url='http://github.com/rentshare/python-payment',
      packages=['payment_processor'],
      install_requires=['requests'],
     )
