# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['physicool']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.5.1,<4.0.0',
 'numpy>=1.22.2,<2.0.0',
 'pandas>=1.4.1,<2.0.0',
 'pydantic>=1.9.1,<2.0.0',
 'scipy>=1.8.0,<2.0.0']

setup_kwargs = {
    'name': 'physicool',
    'version': '0.2.1',
    'description': 'A generalized, model-agnostic framework for model calibration in PhysiCell.',
    'long_description': '<div align="center">\n\n<h1>PhysiCOOL: A generalized framework for model Calibration and Optimization Of modeLing projects</h1>\n\n<a href="">![GitHub](https://img.shields.io/github/license/iggoncalves/PhysiCOOL)</a>\n<a href="">[![Documentation Status](https://readthedocs.org/projects/physicool/badge/?version=latest)](https://physicool.readthedocs.io/en/latest/?badge=latest)</a>\n<a href="">![Codecov](https://img.shields.io/codecov/c/gh/IGGoncalves/PhysiCOOL)</a>\n<a href="">[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.6458586.svg)](https://doi.org/10.5281/zenodo.6458586)</a>\n<a href="">[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)</a>\n\n</div>\n\n## Overview\n\nPhysiCOOL is a Python library tailored to perform model calibration studies with \n[PhysiCell](https://github.com/MathCancer/PhysiCell). \nUsing the PhysiCOOL package, PhysiCell projects can be converted into black-box models to evaluate how simulation outputs\nchange in response to variations in input values. PhysiCOOL takes advantage of Python\'s popularity and simplicity to\nmake PhysiCell studies more accessible and enables users to integrate Python-based calibration tools with their PhysiCell\nworkflows.\n\nAlthough PhysiCOOL was designed to create full model calibration workflows, its components can be used independently \naccording to the users\' needs. For instance,this novel package implements a file parser that enables users to read and \nwrite data to the PhysiCell XML configuration file using simple Python commands. Data validation is performed when \nnew information is written to the files, assuring that the new values are consistent with PhysiCell\'s requirements \nand assumptions. Furthermore, PhysiCOOL also provides new functions to process and visualize simulation outputs which \ncan be used for both parameter exploration and model calibration.\n\nCheck our [documentation](https://physicool.readthedocs.io) for some examples.\n\n## Installation\n\nPhysiCOOL is available through pip using the following command:\n\n```sh\npip install physicool\n```\n\n## Usage\n\n### Writing data to the XML configuration file\n\nThe parameters used by PhysiCell in a new simulation are defined in a configuration file with an XML structure. \nWhile it is possible to use built-in Python functions to modify these scripts, it is required to know their \nstructure and write new code to change different parameters. PhysiCOOL aims to simplify this process by letting \nusers select the parameters to be changed based on PhysiCell\'s data structures with Python objects:\n\n```python\nfrom physicool.config import ConfigFileParser\n# Parse the data from the config file\nxml_data = ConfigFileParser("config/PhysiCell_settings.xml")\n# Read the cell parameters for the "default" cell definition\ncell_data = xml_data.read_cell_data("default")\n# Update and write the new parameters to the config file\ncell_data.motility.bias = 0.5\nxml_data.write_cell_params(cell_data=cell_data)\n```\n\nAnother important PhysiCOOL component is data validation, which is not available through standard XML libraries. \nFor instance, in this code snippet, PhysiCOOL automatically checks if the new migration bias value is between 0 and 1, \nas it is defined by PhysiCell that this parameter should be inside this range.\n\n### PhysiCell as a black-box model\n\nParameter estimation and model calibration can be achieved by assuming that a model behaves as a black-box. \nIn other words, the information about the model itself can be disregarded and only the inputs and outputs are \nconsidered during calibration. PhysiCOOL allows users to connect their PhysiCell compiled scripts to Python-based \nfunctions in order to create a black-box model with three main components:\n\n- A function that updates the PhysiCell configuration file with new input parameters values;\n- The PhysiCell model;\n- A function that reads the model outputs and computes the desired output metric.\n\nThese black-box models are modular in the sense that the users can select what functions to use to update the \nconfiguration file and to process the results. For instance, users can decide to change the cells\' motility parameters \nand evaluate the effect on the distance traveled by cells over time. Alternatively, the cell cycling rates could be \nvaried to analyze the evolution of the number of cells.\n\n![black_box](docs/img/black_box)\n\n### Multilevel parameter sweep\n\nThe `MultiSweep` class exemplifies how PhysiCOOL can be used to calibrate models using some target data. \nIt enables users to run a multilevel sweep using black-box models to find the parameter values that fit the target \ndata by iteratively adapting and fitting the parameter space. To do so, at each level, the parameter space is sampled\nand value combinations are chosen. Simulations are run for all possible iterations and the results are processed to \nfind the similarity between the models outputs and the target data. Subsequently, the values that produced the best \nset of results are chosen and the parameter bounds are adapted to converge to the local solution, as shown in the \nanimation below.\n\nUsers can choose **which parameters to vary** and their initial values, as well as the **number of levels** and \nthe **number of points and ranges to explore at each level**.\n\n## Examples\n\n### General examples\n\n- **Interactive parameter estimation example:**\nA simple example of logistic growth to showcase the multilevel sweep feature.\n\n- **Data analysis and visualization:**\nExamples of data visualization scripts, including interactive examples with Jupyter Widgets.\n\n\n- **Single-cell motility:**\nFinding the best parameter values for migration bias and migration speed to model motility in the presence \nof a chemotactic gradient.\n\n- 🏗️ **Cell growth:**\nFinding the best parameter values for cell cycling rates to model population growth. It also introduces \ngradient-based approaches.\n\n## Team\n\nTool developed by Inês Gonçalves, David Hormuth, Caleb Phillips, Sandhya Prabhakaran. \nRunner-up team of the "Best Tool" prize at [PhysiCell 2021 Workshop & Hackaton](http://physicell.org/ws2021/#apply). \nGO TEAM 7!\n\n## Credits\n\n`PhysiCOOL` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) \nand the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).\n',
    'author': 'Inês Gonçalves, David Hormuth, Caleb Phillips, Sandhya Prabhakaran',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
