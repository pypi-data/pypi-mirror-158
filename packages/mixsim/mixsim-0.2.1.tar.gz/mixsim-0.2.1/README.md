<div align="center">
    <h1>
        MixSim
    </h1>
    <p>
        <em>A Realistic Speech Mixture Simulator</em>
    </p>
    <a href="https://github.com/haoxiangsnr/mixsim/"><img src="https://img.shields.io/github/stars/haoxiangsnr/mixsim?color=yellow&amp;label=MixSim&amp;logo=github" alt="Generic badge"></a>
    <a href="https://andrew-team-realistic-speech-mixture-simulator.readthedocs-hosted.com/en/latest/?badge=latest"><img src="https://readthedocs.com/projects/andrew-team-realistic-speech-mixture-simulator/badge/?version=latest&amp;token=085e2cf349f92379fd8efee9d47bfcfcdf1180e1cc8e3c6d4f2ccf014787ab85"
    alt="Documentation Status"></a>
    <a href="https://codecov.io/gh/haoxiangsnr/mixsim"><img src="https://codecov.io/gh/haoxiangsnr/mixsim/branch/main/graph/badge.svg?token=DD043IL1UZ" alt="codecov"></a>
    <a href="https://badge.fury.io/py/mixsim"><img src="https://badge.fury.io/py/mixsim.svg" alt="PyPI version"></a>
    <a href="https://pypi.org/project/mixsim/"><img src="https://img.shields.io/pypi/pyversions/mixsim.svg?logo=python&amp;label=Python&amp;logoColor=gold" alt="PyPI - Python Version"></a>
</div>

MixSim is an open-source multipurpose speech mixture simulator that covers speaker localization/tracking,
dereverberation, enhancement, separation, and recognition tasks.

Documentation
-------------

See [documentation](https://haoxiangsnr.github.io/mixsim/) for more
details.

A Simple Example
----------------

First, install MixSim using:

```shell
pip install -U mixsim

mixsim --help
```

You can use the `mixsim` command to run the simulator:

```shell
mixsim \
--seed 1 \
--sample_rate 16000 \
--clean.fpath_file /path/to/clean.txt \
--noisy.fpath_file /path/to/noisy.txt
...
```

Use an additional configuration file to specify the parameters:

```shell
mixsim --config_file /path/to/config.toml
```

Use package reference to access the simulator:

```python
from mixsim import Mixer, Writer

mixture_list = Mixer(clean_file_list, noise_file_list, snr_list, output_members=["n_mix_y_rvb", "s_y", "s_transcript"])

file_writer = Writer(output_list = mixture_list)
file_writer.write()
```

Contributing
------------

For guidance on setting up a development environment and how to
contribute to MixSim, see [Contributing to
MixSim](https://haoxiangsnr.github.io/mixsim/contributing).

License
-------

MixSim is released under the [MIT license](LICENSE).