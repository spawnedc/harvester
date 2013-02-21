# Django 1.4 Testapp Project

This is a repo which simply contains the git submodules which you need to get up and running with a new django(appengine|-nonrel) project.

## Usage

* Check out the repo (`--recursive` flag checks out submodules too): `$ git clone <url-to-this-repo> --recursive`
* Remove the original remote: `$ git remote rm origin`
* Add your new remote, pointing at the repo which you want to push this to: `$ git remote add origin <url-to-your-new-repo>`.
* Push to your new remote: `$ git push origin master`.
* Enjoy.
