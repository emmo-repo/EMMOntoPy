Steps for creating a new release
================================

1. Create release branch (branch name can be target version number)

2. Update version number in `emmo/__init__.py`

3. Commit and push to origin

4. Push release branch to GitHub and create a pull request for merging to master

5. Once accepted, merged to master

6. Create a release on GitHub with a short release description.

   Set the tag to the version number prefixed with "v" and title to
   the version number.

7. PyPi distribution package is created automatically upon creation of new release on github.

