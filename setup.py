from distutils.core import setup
setup(
  name = 'depression',         # How you named your package folder (MyLib)
  packages = ['depression'],   # Chose the same as "name"
  version = '2.2',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'depression',   # Give a short description about your library
  author = 'Eddie B',                   # Type in your name
  author_email = 'eddieblevins015@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/omg-someone-actually/depression',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/omg-someone-actually/depression/archive/refs/tags/2.1.tar.gz',    # I explain this later on
  keywords = ['DEPRESSION', 'MEANINGFULL', 'LIFE'],   # Keywords that define your package best
  install_requires=[
    'time',
    'functools',
    'multiprocessing',
    'threading',
    'typing',
    'pyyaml',
    'requests',
    'statistics',
    'hashlib',
    'js2py'
    ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
  ],
)
