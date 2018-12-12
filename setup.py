import setuptools

setuptools.setup(
    name='munin',
    version='0.1.0',
    packages=['munin'],
    url='https://github.com/tetrau/munin',
    license='GPLv3',
    author='tetrau',
    python_requires='>=3.5.0',
    install_requires=['requests>=2.0.0'],
    author_email='tetrau01@gmail.com',
    description='requests session with persistence disk cache.'
)
