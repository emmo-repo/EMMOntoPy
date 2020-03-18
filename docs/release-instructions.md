Steps for creating a new release
================================
1. Create release branch
2. Update version number in emmo/__init__.py
3. Commit and push to origin
4. Create distribution package

       python3 setup.py sdist bdist_wheel

5. Upload to pypi

       python3 -m twine upload dist/*

6. Merge release branch to master on GitHub
