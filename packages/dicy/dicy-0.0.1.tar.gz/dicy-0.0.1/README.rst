====
dicy
====


.. image:: https://img.shields.io/pypi/v/dicy.svg
        :target: https://pypi.python.org/pypi/dicy

.. image:: https://img.shields.io/travis/M-Farag/dicy.svg
        :target: https://travis-ci.com/M-Farag/dicy

.. image:: https://readthedocs.org/projects/dicy/badge/?version=latest
        :target: https://dicy.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status




Simple Dice rolling package


* Free software: MIT license
* Documentation: https://dicy.readthedocs.io.


Features
--------

* Init as many dicy objects as you need and roll them as much as you can


Example
-------

```
from dicy import dicy as d
x = d.Dicy()
x[0] -> # Dice(face=1)
x[0].face -> # 1
```



Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
