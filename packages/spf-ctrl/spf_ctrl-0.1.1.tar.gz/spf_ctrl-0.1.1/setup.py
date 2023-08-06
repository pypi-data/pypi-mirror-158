from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as file:
    long_description = file.read()

setup(
    name='spf_ctrl',
    version='0.1.1',
    author='Eric Tröbs',
    description='send images to Samsung photo frames from python',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/erictroebs/spf_ctrl',
    project_urls={
        'Bug Tracker': 'https://github.com/erictroebs/spf_ctrl/issues',
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',
    ],
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    python_requires='>=3.6',
    install_requires=[
        'pyusb~=1.2.1'
    ]
)
