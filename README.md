# netts - NETworks of Transcript Semantics

[![GitHub release](https://img.shields.io/github/v/release/alan-turing-institute/netts?include_prereleases)](https://GitHub.com/alan-turing-institute/netts/releases/)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/netts.svg)](https://pypi.python.org/pypi/netts/)
[![codecov](https://codecov.io/gh/alan-turing-institute/netts/branch/main/graph/badge.svg?token=58uMq5hbNt)](https://codecov.io/gh/alan-turing-institute/netts)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)

Toolbox for constructing semantic speech networks from speech transcripts.

## About

The algorithms in this toolbox create a semantic speech graph from transcribed speech. Speech transcripts are short paragraphs of largely raw, uncleaned speech-like text. For example:

> 'I see a man and he is wearing a jacket. He is standing in the dark against a light post. On the picture there seems to be like a park and... Or trees but in those trees there are little balls of light reflections as well. I cannot see the... Anything else because it’s very dark. But the man on the picture seems to wear a hat and he seems to have a hoodie on as well. The picture is very mysterious, which I like about it, but for me I would like to understand more about the picture.'
> -- <cite>Example Transcript</cite>

Below is the semantic speech graph constructed from this text.

![Semantic speech graph example](https://github.com/alan-turing-institute/netts/raw/main/docs/docs/img/real_example_network_with_picture_transcript.png)
*Figure 1. Semantic Speech Graph. Nodes represents an entity mentioned by the speaker (e.g. I, man, jacket). Edges represent relations between nodes mentioned by the speaker (e.g. see, has on).*

## Getting started

Read the full documentation [here](https://alan-turing-institute.github.io/netts/).

### Where to get it

You can install the latest release from [PyPi](https://pypi.org/project/netts/)

```bash
pip install netts
```

or get the latest development version from GitHub (not stable)

```bash
pip install git+https://github.com/alan-turing-institute/netts
```

### Additional dependencies

Netts requires the Java Runtime Environment. Instructions for downloading and installing for your operating system can be found [here](https://docs.oracle.com/goldengate/1212/gg-winux/GDRAD/java.htm#BGBFHBEA).

Netts also requires a few additional dependencies to work which you can download with the netts CLI that was installed by pip

```bash
netts install
```

### Basic usage

The quickest way to process a transcript is with the CLI.

```bash
netts run transcript.txt outputs
```

where `transcript.txt` is a text file containing transcribed speech and `outputs` is the name of a directory to write the outputs to. Additional logging information can be found in `netts_log.log`.

## Contributors

Netts was written by [Caroline Nettekoven](https://www.caroline-nettekoven.com) in collaboration with [Sarah Morgan](https://semorgan.org).

Netts was packaged in collaboration with [Oscar Giles](https://www.turing.ac.uk/people/researchers/oscar-giles), [Iain Stenson](https://www.turing.ac.uk/research/research-engineering/meet-the-team) and [Helen Duncan](https://www.turing.ac.uk/people/research-engineering/helen-duncan).

<!-- ## Citing netts

If you use netts in your work, please cite this paper:
> Caroline R. Nettekoven, Kelly Diederen, Oscar Giles, Helen Duncan, Iain Stenson, Julianna Olah, Nigel Collier, Petra Vertes, Tom J. Spencer, Sarah E. Morgan, and Philip McGuire. 2021. “Networks of Transcript Semantics - Netts.” -->
