Release notes
-------------

Releases are marked on master branch with tags. The upload to pypi is automated as long as a merge
from development comes with a tag.

General flow

  1. Get in dev branch
  2. Update VERSION in setup.py and releases.txt file
  3. Make a commit
  4. Merge development into master (`git merge --no-ff development`)
  4. Add corresponding version as a new tag (`git tag <new_version>`) e.g. git tag v0.3.0
  5. Push everything (`git push --tags && git push`)

-
