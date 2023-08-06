MixSim: A Realistic Speech Mixture Simulator
============================================

[![Generic
badge](https://img.shields.io/github/stars/haoxiangsnr/mixsim?color=yellow&label=MixSim&logo=github)](https://github.com/haoxiangsnr/mixsim/)
[![Documentation
Status](https://readthedocs.com/projects/andrew-team-realistic-speech-mixture-simulator/badge/?version=latest&token=085e2cf349f92379fd8efee9d47bfcfcdf1180e1cc8e3c6d4f2ccf014787ab85)](https://andrew-team-realistic-speech-mixture-simulator.readthedocs-hosted.com/en/latest/?badge=latest)
[![codecov](https://codecov.io/gh/haoxiangsnr/mixsim/branch/main/graph/badge.svg?token=DD043IL1UZ)](https://codecov.io/gh/haoxiangsnr/mixsim)
[![PyPI version](https://badge.fury.io/py/mixsim.svg)](https://badge.fury.io/py/mixsim)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/mixsim.svg?logo=python&label=Python&logoColor=gold)](https://pypi.org/project/mixsim/)


MixSim is an open-source multipurpose speech mixture simulator that covers speaker localization/tracking, dereverberation, enhancement, separation, and recognition tasks.

Documentation
-------------

See [documentation](https://haoxiangsnr.github.io/mixsim/) for more
details.

A Simple Example
----------------

First, install MixSim using:

``` {.shell}
pip install -U mixsim
```

``` {.py}
from mixsim import mixsim

output_members=["n_mix_y_rvb", "s_y", "s_transcript"]
```

Contributing
------------

For guidance on setting up a development environment and how to
contribute to MixSim, see [Contributing to
MixSim](haoxiangsnr.github.io/mixsim/contributing).

License
-------

MixSim is released under the [MIT license](LICENSE).