import sys

from setuptools import setup, find_packages

import gpulurker


extra_description = {}
try:
    with open('README.md', mode='r') as doc:
        extra_description['long_description'] = doc.read()
        extra_description['long_description_content_type'] = 'text/markdown'
except OSError:
    pass

setup(
    name='gpulurker',
    version=gpulurker.__version__,
    description=gpulurker.__doc__,
    **extra_description,
    license=gpulurker.__license__,
    author=gpulurker.__author__,
    author_email=gpulurker.__email__,
    url="https://github.com/RenShuhuai-Andy/gpu_lurker.git",
    packages=find_packages(include=['gpulurker', 'gpulurker.*']),
    entry_points={
        'console_scripts': [
            'gpulurker=gpulurker.main:main'
        ]
    },
    install_requires=(['windows-curses'] if sys.platform == 'windows' else []) + [
        'pynvml',
        'blessed',
        'apscheduler',
        'requests',
        'argparse'
    ],
    python_requires='>=3.5, <4',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Environment :: GPU',
        'Environment :: Console',
        'Environment :: Console :: Curses',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: System Administrators',
        'Topic :: System :: Hardware',
        'Topic :: System :: Monitoring',
        'Topic :: System :: Systems Administration',
        'Topic :: Utilities',
    ],
    keywords='nvidia, nvidia-smi, GPU, wechat, htop',
    project_urls={
        'Bug Reports': 'https://github.com/RenShuhuai-Andy/gpu_lurker/issues',
        'Source': 'https://github.com/RenShuhuai-Andy/gpu_lurker',
    },
)