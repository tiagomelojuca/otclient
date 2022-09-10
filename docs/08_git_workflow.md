### Clone a new repository
```sh
git clone git://github.com/edubart/otclient.git
```

### Update your fork
Remember to always update your fork before making a pull request.
Make sure that you have the remote upstream, if you does not have it yet, create now.
```sh
git remote add upstream git://github.com/edubart/otclient.git
git fetch upstream
```

### Update your fork before pull requests
Make sure that you are pulling from upstream with rebase if you pretend to make pull requests on the upstream.
```sh
git pull --rebase upstream master  # pull new upstream changes to your local repository
git push -f                        # this may overwrite your fork
```

### Reset your repository
```sh
git stash                        # save any changes
git fetch                        # update remote repository information
git reset --hard origin/master   # reset your local ranch making identical to the remote master
git stash pop                    # restore changes
```

### Reset your fork
This is just like the instructions above, but with a different remote.
```sh
git stash                        # save any changes
git fetch                        # update remote repository information
git reset --hard upstream/master   # reset your local ranch making identical to the remote master
git stash pop                    # restore changes
```

### Commit new changes
```sh
git add file                     # add new files
git commit -a                    # commit all modified files
git pull --rebase                # update your local repository before pushing
git push                         # push your changes to the master
```

### Redo last commit
If you commited anything wrong and **didn't push yet**, instead of doing another commit to fix,
you can redo the previous commit.
```sh
git commit -a --amend            # append new changes to the latest commit
```

### Save current changes for later
You can use stash for storing changes in a temporarly without needing to store then on a new branch.
```sh
git stash
```

To restore just pop latest stash.
```sh
git stash pop
```

### Joining commits
Use with care, rebase will rewrite the commit history, so make sure that you didn't pushed the commits that you are joining yet.
```sh
git rebase -i HEAD~2               # will enter in interactive rebase in the latest 2 commits
```

Now in the interactive rebase, mark the commits that you want to join with "squash", in rebase you can also
delete commits, change commits order, commit messages and more. If anything goes wrong use git rebase --abort
to cancel.

### Checking changes
There are many tools that can be used to check current changes and commit history,
in the web you can also find graphical good tools, the next ones generially comes with git, and I usually
get what I want with gitk.
```sh
git status
git diff
gitk
```

### Branchs
Create new branch 'tmp' based on the current branch and change to it.
```sh
git checkout -b tmp
```

Change to branch master.
```sh
git checkout master
```

Merge commits from branch tmp into the current branch.
```sh
git merge tmp
```
