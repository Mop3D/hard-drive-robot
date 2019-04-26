Ein paar Testscripts.




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

