from os import path
import codecs

from setuptools import setup, find_packages

with codecs.open('README.md', 'r', 'utf8') as reader:
    long_description = reader.read()


with codecs.open('requirements.txt', 'r', 'utf8') as reader:
    install_requires = list(map(lambda x: x.strip(), reader.readlines()))

setup(
    name='bert_multitask_client',
    version='0.1.0',  # noqa
    description='A service to serve bert_multitask_learning models(Client)',
    url='https://github.com/JayYip/bert-multitask-service',
    long_description=open('README.md', 'r').read(),
    long_description_content_type='text/markdown',
    author='Jay Yip',
    author_email='junpang.yip@gmail.com',
    license='MIT',
    packages=find_packages(),
    zip_safe=False,
    install_requires=install_requires,
    classifiers=(
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
    ),
    keywords='bert nlp tensorflow machine learning sentence encoding embedding serving',
)
