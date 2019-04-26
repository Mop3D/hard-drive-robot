Ein paar Testscripts...




Git Zeugs:

---- git ---
https://projects.raspberrypi.org/en/projects/getting-started-with-git/5
$ sudo apt-get install git
$ git config --global user.name "olikle"
$ git config --global user.email "oliver.klepach@querplex.de"
--- Next you need to tell Git which text editor you want to use. ---
$ git config --global core.editor nano
--- get robopi ---
$ git clone https://github.com/Mop3D/hard-drive-robot.git
---  status ---
$ git status
--- add ---
$ git add README.md
or
$ git add --all
--- commit ---
$ git commit -am "my comment"
--- log file ---
$ git log README.md
$ git log -p README.md
--- git push to master ---
git push -u origin master


--- SSH ---
https://www.w3docs.com/snippets/git/how-to-generate-ssh-key-for-git.html

--- create a ssh key
$ ssh-keygen -t rsa -b 4096 -C "oliver.klepach@querplex.de"


--- check ssh agent
$ eval "$(ssh-agent -s)"
--- add new key
$ ssh-add ~/.ssh/id_rsa
--- show SSH key
$ cat .ssh/id_rsa.pub

How To Add SSH Key To Github Account
Step 1: Login into your Github's account.In the top right corner of any page, click your profile photo, then click Settings.
Step 2: In the user settings sidebar, go to SSH and GPG keys.
Step 3: Click New SSH key.
Step 4: Type Title and your SSH Key

