
## create wheel
uv pip install -e .

## activate venv
source .venv/bin/activate

## run programms from exploration
python -m exploration.first_ui

[![Docs](https://img.shields.io/badge/docs-creatumlibre-blue?style=flat-square)](https://UMBRELLABROS.github.io/CreatumLibre/)


## build documentation (only once)
pdoc src/creatumlibre --output-dir docs

## See documentation
pdoc src/creatumlibre -n -h localhost -p 8000
