#!/usr/bin/env bash

python setup.py bdist_wheel
twine upload dist/jumeaux-${RELEASE_VERSION}-py3-none-any.whl \
  --config-file ".pypirc" \
  -u tadashi-aikawa \
  -p ${PYPI_PASSWORD}
