
# MARCIA - MAsking spectRosCopIc dAtacube
[![DOI](https://zenodo.org/badge/263880541.svg)](https://zenodo.org/badge/latestdoi/263880541)
[![PyPI](https://img.shields.io/badge/MARCIA-v0.1.3-blue.svg?maxAge=2592000)](https://pypi.org/project/MARCIA/)

## Extension of Manual classifier for µXRF and EDS/SEM hypercubes
 - Classification is achieved by defining masks that are linear combination of elemental intensities in spectra.
 - Classes can then be extracted and read with hyperspy or PyMca or Esprit
 - Help for the MARCIA user : file of plages = ranges for each element 


## Install Python dependencies  
Just do
```bash
python setup.py develop
```

## Use in python
```python
from MARCIA-Plages.maskSigma import Mask
```

## Gallery
![Example](https://github.com/hameye/MARCIA/blob/master/gallery.png)
