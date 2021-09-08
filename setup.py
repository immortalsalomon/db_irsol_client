from setuptools import setup

setup(
    name='db_irsol_client',
    version='1.0',
    packages=['db_irsol', 'db_irsol.parsers', 'db_irsol.entities', 'db_irsol.entities.entities', 'db_irsol.api_gateway',
              'db_irsol.api_gateway.gateways', 'db_irsol.third_party', 'db_irsol.pre_build_functions'],
    url='',
    license='',
    author='Michel Basili',
    author_email='michel.basili@irsol.usi.ch',
    description='The client of the irsol db.'
)
