#!/usr/bin/env bash

python setup.py bdist_wheel
twine upload dist/jumeaux-${RELEASE_VERSION}-py3-none-any.whl \
  --repository-url "https://pypi.python.org/pypi" \
  --config-file ".pypirc" \
  -u tadashi-aikawa \
  -p ${PYPI_PASSWORD}
