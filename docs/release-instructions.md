# Steps for creating a new release

1. Create release branch (branch name can be the target version number).
2. Update version number in `emmopy/__init__.py`.
3. Commit and push to origin (https://github.com/emmo-repo/EMMO-python.git).
4. Push the release branch to GitHub and create a pull request for merging to the master branch.
5. Once accepted, merge to master.
6. Create a release on GitHub with a short release description.

   Set the tag to the version number prefixed with `"v"` and title to the version number.
7. The PyPI distribution package is created automatically upon creation of a new release on GitHub.
