import setuptools
from packagename.version import Version


setuptools.setup(name='methodtest',
                 version=Version('1.0.0').number,
                 description='Test assignment for Method studio',
                 long_description=open('README.md').read().strip(),
                 author='Niko Skrypnik',
                 author_email='nskrypnik@gmail.com',
                 url='http://path-to-my-packagename',
                 py_modules=['methodtest'],
                 install_requires=[],
                 license='MIT License',
                 zip_safe=False)
