Steps for creating a new release
================================
1. Create release branch
2. Update version number in emmo/__init__.py
3. Commit and push to origin
4. Create distribution package

       python3 setup.py sdist bdist_wheel

5. Upload to pypi

       python3 -m twine upload dist/*

6. Push release branch to GitHub and create a pull request for merging to master

7. Once accepted, merged to master

8. Create a release on GitHub with a short release description.

   Set the tag to the version number prefixed with "v" and title to
   the version number.
