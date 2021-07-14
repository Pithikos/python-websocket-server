Release notes
-------------

Releases are marked on master branch with tags. The upload to pypi is automated as long as a merge
from development comes with a tag.

General flow

  1. Update VERSION in setup.py from development branch and commit
  2. Merge development into master (`git merge --no-ff development`)
  3. Add corresponding version as a new tag (`git tag <new_version>`) e.g. git tag v0.3.0
  4. Push everything (`git push --tags && git push`)
