# netts - NETworks of Transcript Semantics in Python

[![GitHub release](https://img.shields.io/github/release/alan-turing-institute/netts.svg)](https://GitHub.com/alan-turing-institute/netts/releases/)[![PyPI pyversions](https://img.shields.io/pypi/pyversions/netts.svg)](https://pypi.python.org/pypi/netts/)
[![codecov](https://codecov.io/gh/alan-turing-institute/netts/branch/main/graph/badge.svg?token=58uMq5hbNt)](https://codecov.io/gh/alan-turing-institute/netts)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)

Toolbox for constructing semantic speech networks from speech transcripts.

## About

The algorithms in this toolbox create a semantic speech graph from transcribed speech. Speech transcripts are short paragraphs of largely raw, uncleaned speech-like text. For example:

> 'I see a man in the dark standing against a light post. It seems to be in the middle of the night; I think because the lightbulb is working. On the picture there seems to be like a park and... Or trees but in those trees there are little balls of light reflections as well. I cannot see the… Anything else because it’s very dark. But the man on the picture seems to wear a hat and, and has a jacket on and he seems to have a hoodie on as well. The picture is very, very mysterious, which I like about it, but for me I would like to understand more concept, context of the picture.'
> -- <cite>Example Transcript</cite>

Below is the semantic speech graph constructed from this text.

![Semantic speech graph example](docs/docs/img/ExampleGraph_alternative_text_pic_2.png)
*Figure 1. Semantic Speech Graph. Nodes represents an entity mentioned by the speaker (e.g. I, man, jacket). Edges represent relations between nodes mentioned by the speaker (e.g. see, has on).*

## Developer Dependencies

### Python dependencies

To get started install [Poetry](https://python-poetry.org/docs/).

Then ensure all dependencies are installed:

```bash
poetry install
```

Install additional dependencies to `~/netts`:

```bash
netts install
```

### Pre-commit

```bash
poetry run pre-commit run --all-files
```

### Unit tests

Run all unit tests excluding slow tests (require downloads) and those that write to `~/netts` (these run on GitHub Actions).

```bash
poetry run pytest --cov=netts --cov-report=xml tests -m "not ci_only"
```

### Preview docs

```bash
poetry run mkdocs serve --config-file docs/mkdocs.yml
```


## Contributors
Netts was written by [Caroline Nettekoven](https://www.caroline-nettekoven.com) in collaboration with [Sarah Morgan](https://semorgan.org).

Netts was packaged in collaboration with [Oscar Giles](https://www.turing.ac.uk/people/researchers/oscar-giles), [Iain Stenson](https://www.turing.ac.uk/research/research-engineering/meet-the-team) and [Helen Duncan](https://www.turing.ac.uk/people/research-engineering/helen-duncan).


## Citing netts

If you use netts in your work, please cite this paper:
> Caroline R. Nettekoven, Kelly Diederen, Oscar Giles, Helen Duncan, Iain Stenson, Julianna Olah, Nigel Collier, Petra Vertes, Tom J. Spencer, Sarah E. Morgan, and Philip McGuire. 2021. “Networks of Transcript Semantics - Netts.”
