
[![build](https://github.com/andrsd/figura/actions/workflows/build.yml/badge.svg)](https://github.com/andrsd/figura/actions/workflows/build.yml)
[![codecov](https://codecov.io/gh/andrsd/figura/branch/main/graph/badge.svg?token=J87EFHQV0C)](https://codecov.io/gh/andrsd/figura)
[![Scc Count Badge](https://sloc.xyz/github/andrsd/figura/)](https://github.com/andrsd/figura/)
[![License](http://img.shields.io/:license-mit-blue.svg)](https://andrsd.mit-license.org/)


# figura

User-friendly python scripting for creating parametrical 3D models

## Features

- Using [Open CASCADE Technology](https://www.opencascade.com/open-cascade-technology/) as the 3D modeling kernel
- User-friendly API
- Support for [STEP files](https://en.wikipedia.org/wiki/ISO_10303-21)
- Support for [STL files](https://en.wikipedia.org/wiki/STL_(file_format))

## Installation

Requirements:

- `pythonocc-core` (>=7.6.0) (available via [conda-forge](https://conda-forge.org/))

  Install it via: ```$ conda install -c conda-forge pythonocc-core```

Install figura:

```
$ cd /some/path
$ git clone https://github.com/andrsd/figura.git
$ cd figura
$ pip install .
```

## FAQs

*Q:* why is there no pip package?

*A:* `figura` depends on `pythonocc-core` which is currently (April 2023) only available via conda-forge. Once it is avialable via pip, we can deploy via pip as well.
