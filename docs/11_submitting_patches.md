### Before I start, here are some notes:

**Things I will *NOT* teach you:**
* C++
* Lua
* Compiling otclient, there are tutorials over here in the wiki, please check them out.

**Things I will teach you:**
* Basic usage of git.
* Testing your code before pushing.

**Another thing, before diving in, obtain a copy of Git, there are several ways to do this, here are some of them:**
* Compiling from source code (I won't do that)
* Obtaining it by your package manager (Linux or Cygwin)
* The Native way in windows, is obtaining an installer through [here](http://git-scm.com/download/win)

**Configuring git**
* Configure your email address and github user:
```sh
   git config --global user.name="your name here"
   git config --global user.email="your email here"
```
* (Optional) Configure email sending stuff:
```sh
   git config --global sendemail.smtpencryption=tls
   git config --global sendemail.smtpserver=smtp.gmail.com
   git config --global sendemail.smtpuser=example@gmail.com
   git config --global sendemail.smtpserverport=587
```

Okay, now you're ready to dive in.
* Open up Git Shell.
* Obtain a copy of otclient's source code:
```sh
   git clone https://github.com/edubart/otclient.git
```
* Change directory to otclient's source code:
```sh
   cd otclient
```
* Before you do anything, please work on a different branch than master, we will use _tutorial_.
* Tip: to see which branch you're currently working on, do:
```sh
   git branch
```
  Which should (hopefully) output:
  *  master

* Create your work branch, we will be using _tutorial_:
```sh
   git checkout -b tutorial
```
This creates new branch called tutorial and switches to it and is also a shortcut to:
```sh
   git branch tutorial
   git checkout tutorial
```
Make sure you're in the branch tutorial, do:
```sh
   git branch
```
Which should output:
   * master
   * tutorial

## The Job
* Step 1, Do some change
![code](http://i.imgur.com/d7q4K.png)

* Step 2, check our changes:
![changes](http://i.imgur.com/N44kp.png)

Like you see, nothing has been added to the repo yet, add it with:
```sh
   git add file
```
And then, commit it with:
```sh
   git commit
```
**Note**: This will open the text editor git is configured with,  to configure the text editor git uses, do:
```sh
   git config --global core.editor=vim
```
Replace vim with your text editor.

Here's an image  to demonstrate how this is done:

![add](http://i.imgur.com/WZnuR.png)

* Step 3, make a .patch file

Making a patch file is a simple process, and is done like so:
```sh
   git format-patch master..tutorial
```
Which should output the filename the patch saved to, the file contains your changes.

* Step 4, now, send the patch to some developer.
![send_patch](http://i.imgur.com/KIttX.png)

## Notes
* this step is optional (the sending email thing), alternatively you can use github issues to send patches etc. Use whatever you feel comfortable with.
* Read the manual page for git send-email if you're wondering how this is done.
* It's the developer freedom to choose whether your patch should be commited to the family tree or not, it really depends on how useful your patch is.

## Bonus
* It's good to write the signed-off-by line in your patch, to tell that this is your code, etc.  It's not of much use, however, you can use it to reward yourself a bit more.
![signedoffby](http://i.imgur.com/Kpfgh.png)

* See if your patch is good:
```sh
   git apply --check <patch file>
```
  This will tell you whether your patch file is formatted good or not. Remember to do this before sending!

Happy hacking!
