from distutils.core import setup
setup(
  name = 'Results_Analysis',         # How you named your package folder (MyLib)
  packages = ['Results_Analysis'],   # Chose the same as "name"
  version = '0.9',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'allow user to test the questionnaire and compare results between questionnaire',   # Give a short description about your library
  author = 'Nina Abittan',                   # Type in your name
  author_email = 'your.email@domain.com',      # Type in your E-Mail
  url = 'https://github.com/Sinha1111/Results_Analysis',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/Sinha1111/Results_Analysis/archive/refs/tags/v_09.tar.gz',
  keywords = ['', '', ''],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'pandas',
          'openpyxl',
          'pycel',
          'IPython',
          'formulas',
          'numpy',
          'matplotlib',
          'ipywidgets',
          'pathlib',
          'dataframe_image',
          'aspose.words',
          'wordcloud',
          'scipy',
          'statsmodels',
          'wget',
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
  ],
)
