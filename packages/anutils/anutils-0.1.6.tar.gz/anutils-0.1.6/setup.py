from setuptools import setup, find_packages

try:
    from pypandoc import convert_file
    long_description = convert_file('README.md', 'rst')
except:
    long_description = ''

setup(
    name='anutils',
    version='0.1.6',
    license='MIT',
    author="Aaron Ning",
    author_email='foo@bar.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},

    description='Private utilities of A. Ning. ',
    long_description=long_description, 

    url='https://github.com/AaronNing/anutils',
    keywords='anutils',
    install_requires=[
        'scipy',
        'numpy',
        'pandas', 
        'matplotlib',
        'seaborn', 
        'scanpy', 
        'getkey',
        ],
)
