MixSim: A Realistic Speech Mixture Simulator
============================================

|codecov| |Documentation Status| |Generic badge|

MixSim is an open-source multipurpose speech mixture simulator that
covers speaker localization/tracking, dereverberation, enhancement,
separation, and recognition tasks.
123

Documentation
-------------

See `documentation <https://haoxiangsnr.github.io/mixsim/>`__ for more
details.

A Simple Example
----------------

First, install MixSim using:

.. code:: shell

   pip install -U mixsim

.. code:: py

   from mixsim import mixsim

   output_members=["n_mix_y_rvb", "s_y", "s_transcript"]

Contributing
------------

For guidance on setting up a development environment and how to
contribute to MixSim, see `Contributing to
MixSim <haoxiangsnr.github.io/mixsim/contributing>`__.

License
-------

MixSim is released under the `MIT license <LICENSE>`__.

.. |codecov| image:: https://codecov.io/gh/haoxiangsnr/mixsim/branch/main/graph/badge.svg?token=DD043IL1UZ
   :target: https://codecov.io/gh/haoxiangsnr/mixsim
.. |Documentation Status| image:: https://readthedocs.com/projects/andrew-team-realistic-speech-mixture-simulator/badge/?version=latest&token=085e2cf349f92379fd8efee9d47bfcfcdf1180e1cc8e3c6d4f2ccf014787ab85
   :target: https://andrew-team-realistic-speech-mixture-simulator.readthedocs-hosted.com/en/latest/?badge=latest
.. |Generic badge| image:: https://img.shields.io/github/stars/haoxiangsnr/mixsim?color=yellow&label=MixSim&logo=github&style=flat-square
   :target: https://github.com/haoxiangsnr/mixsim/
