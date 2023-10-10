# Natural Language Real Estate Search Version 1.0 (latest stable)

Github repository:
https://github.com/clipqq/brookhurst-app

---

# Known Issues

-   If `Resource punkt not found` error, check: https://github.com/delip/PyTorchNLPBook/issues/14

---

## Local Development

1. Go to the application folder:
   `cd brookhurst-app`

2. Create a virtual environment for the app:
   `python3 -m venv .venv`
   `source .venv/bin/activate`

3. Install the dependencies:
   `pip install -r requirements.txt`

4. (optional) Enable Debug mode for auto refresh on save
   `export FLASK_DEBUG=1`

5. Run the app:
   `flask run`

# Architecture Overview and Best Practices

This Flask web app is built in Python 3.11

## Frontend

The frontend page views are based on a base and template structure.

-   `base.html` is the boilerplate for all pages and contains the navbar.

-   HTML forms should be created only in `templates` directory. Styling and CSS should be contained only in the `bootstrap` directory, not within any HTML files.

In the future, other frontend forms may be created in the `templates` directory that will serve other forms and features.

Guide for Flask templates: https://www.digitalocean.com/community/tutorials/how-to-use-templates-in-a-flask-application

## Backend

-   `app.py` contains all endpoint routers and should have a route and corresponding function to handle each HTML file within `templates`.

## Database

---

# Getting Started with Git

## Prerequisites

Development on Windows can be awkward because most terminal commands are for Unix. I highly recommend setting up the Linux dev environment that comes with Windows. This will allow you to natively run Unix CLI commands that are found in basically every developer tutorial and guide:
https://learn.microsoft.com/en-us/windows/wsl/setup/environment

If you followed the prerequisites above to have a Unix terminal, use the Linux/Unix commands specified in every guide from here on.

## Create Github account

https://docs.github.com/en/get-started/signing-up-for-github/signing-up-for-a-new-github-account

Install Git on your local machine

`sudo apt-get install git-all`

https://github.com/git-guides/install-git

Check Git installed

`git -v`

## Create local SSH key

As part of a development setup and work with a remote repository, it’s best to connect to Github with SSH.
https://docs.github.com/en/authentication/connecting-to-github-with-ssh
Check Git SSH connection
https://docs.github.com/en/authentication/connecting-to-github-with-ssh/testing-your-ssh-connection

## Start working on a repo

Clone repo to your local machine
Navigate to the directory you want to clone the repository into.

https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository

`git clone https://github.com/YOUR-USERNAME/YOUR-REPOSITORY`

Make sure the cloned repo is pointing to the remote repo.

`git remote add origin https://github.com/OWNER/REPOSITORY.git
git remote -v`

https://docs.github.com/en/get-started/getting-started-with-git/managing-remote-repositories#adding-a-remote-repository

Pull changes from the remote repository

`git pull`

https://docs.github.com/en/get-started/using-git/getting-changes-from-a-remote-repository

Because pull performs a merge on the retrieved changes, you should ensure that your local work is committed before running the pull command. If you run into a merge conflict you cannot resolve, or if you decide to quit the merge, you can use `git merge --abort` to take the branch back to where it was before you pulled.

Save and commit your changes to the remote Git Repository

(if new dependencies added):`pip3 freeze > requirements.txt`
`git add .`
`git commit -m 'YOUR_CHANGE_NOTES_HERE'`
`git push`

https://docs.github.com/en/get-started/using-git/pushing-commits-to-a-remote-repository

## Develop on a New Branch

`git checkout -b ‘YOUR_BRANCH_NAME’`
`// Make your code changes...`
`git add .`
`git commit -m 'YOUR_CHANGE_NOTES_HERE'`
`git push -u origin ‘YOUR_BRANCH_NAME’`

https://www.freecodecamp.org/news/how-to-create-a-local-git-branch/

## Merging Branch with Main

`git fetch`
`// Commit changes to branch code`
`git add .`
`git commit -m 'YOUR_CHANGE_NOTES_HERE'`
`git rebase`
`git checkout main`
`git pull origin main`
`git merge ‘YOUR_BRANCH_NAME’`
`git push origin main`

## Git General Help Guide:

https://docs.gitlab.com/ee/gitlab-basics/start-using-git.html
