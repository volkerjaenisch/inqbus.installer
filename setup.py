from setuptools import setup, find_packages

version = '0.1'

setup(name='inqbus.installer',
      version=version,
      description="Installs your python code local or remote",
      long_description=open("README.txt").read() + "\n" +
                       open("HISTORY.txt").read(),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        "Intended Audience :: System Administrators",
        "License :: Other/Proprietary License",
        "Natural Language :: English",
        "Operating System :: OS Unindependent",
        "Programming Language :: Python",
                  ],
      keywords='installation python deployment',
      author='Volker Jaenisch',
      author_email='volker.jaenisch@inqbus.de',
      url='http://inqbus.de',
      download_url='',
      license='other',
      packages=find_packages('src', exclude=['ez_setup']),
      namespace_packages=['inqbus', 'inqbus.installer'],
      package_dir={'': 'src'},
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      [console_scripts]
      test_installer = inqbus.installer.test:main
      """
      )
