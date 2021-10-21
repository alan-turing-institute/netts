# Netspy - Networks of Transcribed Speech in Python
[![GitHub release](https://img.shields.io/github/release/alan-turing-institute/netspy.svg)](https://GitHub.com/alan-turing-institute/netspy/releases/)[![PyPI pyversions](https://img.shields.io/pypi/pyversions/netspy.svg)](https://pypi.python.org/pypi/netspy/)
[![codecov](https://codecov.io/gh/alan-turing-institute/netspy/branch/main/graph/badge.svg?token=58uMq5hbNt)](https://codecov.io/gh/alan-turing-institute/netspy)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)

Toolbox for the constructing of many semantic speech networks from speech transcripts.

This toolbox was built as part of an ongoing project investigating the potential of [speech markers to predict psychosis risk](https://www.turing.ac.uk/research/research-projects/towards-incoherent-speech-predictor-psychosis-risk) funded by the [Alan Turing Institute](https://www.turing.ac.uk) and led by [Sarah Morgan](https://www.neuroscience.cam.ac.uk/directory/profile.php?SarahMorgan) at the [University of Cambridge](https://www.cam.ac.uk). Tools were written by [Caroline Nettekoven](https://www.neuroscience.cam.ac.uk/directory/profile.php?caronettekoven) at the  [Cambridge Brain Mapping Unit](http://www.bmu.psychiatry.cam.ac.uk).

The algorithms in this toolbox create a semantic speech graph from transcribed speech. Speech transcripts are short paragraphs of largely raw, uncleaned speech-like text. For example:

> 'I see a man in the dark standing against a light post. It seems to be in the middle of the night; I think because the lightbulb is working. On the picture there seems to be like a park and... Or trees but in those trees there are little balls of light reflections as well. I cannot see the… Anything else because it’s very dark. But the man on the picture seems to wear a hat and, and has a jacket on and he seems to have a hoodie on as well. The picture is very, very mysterious, which I like about it, but for me I would like to understand more concept, context of the picture.'
> -- <cite>Example Transcript</cite>

Below is the semantic speech graph constructed from this text.

![Semantic speech graph example](legacy/semantic_speech_graph_example.png)
*Figure 1. Semantic Speech Graph. Nodes represents an entity mentioned by the speaker (e.g. I, man, jacket). Edges represent relations between nodes mentioned by the speaker (e.g. see, has on).*

## Developer Dependencies

### Python dependencies

To get started install [Poetry](https://python-poetry.org/docs/).

Then ensure all dependencies are installed:

```bash
poetry install
```

Install additional dependencies to `~/netspy`:

```bash
netspy install
```

### Pre-commit

```bash
poetry run pre-commit run --all-files
```

### Unit tests

Run all unit tests excluding slow tests (require downloads) and those that write to `~/netspy` (these run on GitHub Actions).
```bash
poetry run pytest --cov=netspy --cov-report=xml tests -m "not ci_only"
```

### Preview docs
```bash
poetry run mkdocs serve --config-file docs/mkdocs.yml
```
