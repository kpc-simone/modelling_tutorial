# Introduction
This page outlines the prerequisites for simulating and building neurobiological models with the Nengo neural simulator. No prior programming experience is assumed. Each tool will be dealt with separately, with general applications, installation and configuration instructions, and how it supports this modelling toolchain.

Purpose
The ultimate goal of this tutorial is to spark collaboration and collective experimentation on modelling. We'll work through an example model developed with the NEF and Nengo neural simulator to illustrate the process. 

As a Python package, models built with the nengo simulator can be seamlessly interfaced with other Python scripts. While functionality offered through the nengo GUI shows how the model runs, using the 'back-end' as part of your workflow is more powerful and offers more flexibility. The tutorial will therefore require use of the command line wherever possible. 

Practical notes
Often < > are used to denote parameters for input. Don't put in the < >.

This tutorial is a beta version that has not been extensively tested. Any installation or runtime issues will be dealt with at the end of the tutorial.

First, go to kpc-simone/modelling_tutorial. Download the repository and extract files to a folder of your choice.

# Toolchain

## Cmder

### What this is: 

Cmder (pronounced Commander) is a console emulator, a programming tool with a _command line interpreter_. A command line interpreter (CLI) allows the user to interact with a program using commands in the form of text lines -- in contrast to the mouse's pointing and clicking on menus and buttons. While graphical user interfaces (GUIs) have largely replaced CLIs, they remain popular among advanced technical users due to the speed with which you can type, and the large range of commands available. 

CLIs are sometimes referred to as _shells_ when the CLI is used to run another program. Windows Explorer is technically a shell. Its name comes from how it wraps around another program.

The nengo simulation environment is accessed via a command line. We will install Cmder, which is a _console emulator_ with built-in Git functionality that can be used to start any shell we want. We'll use Cmder to run cmd.exe (Windows shell).

### To install and configure:
"Download full (with Git for Windows)" from http://cmder.net/

Configure to run as administrator: 
 Settings > Startup > Specified name task: {cmd::cmd as Admin}
 
As Nengo is a browser-based application, this will ensure you can bypass any firewall issues when you launch from the command line. 

### Check:
Run Cmder (_Cmder.exe_)

~~~
D:\Program Files\cmder
λ
~~~

The first line tells you your _working directory_. The second line is an invitation to type (command prompt). You can enter commands that the command prompt will then execute. Here are a few common ones:

List files
~~~
D:\modelling_tutorial\examples
λ ls 
~~~

Change directory. Use the following command to move up one directory in the hierarchy.
~~~
D:\modelling_tutorial\examples
λ cd <folder name>
~~~

Use the following command to move up one directory in the hierarchy.
~~~
D:\modelling_tutorial\examples
λ cd .. 
~~~

Using `ls` and `cd < >`,  navigate to modelling_tutorial\examples that you downloaded earlier.

Launch a script from the command line
The folder contains a number of example script files that further demonstrate command line capabilities. `example1.bat` and `example2.bat` are _batch files_ that contains commands that can in turn be executed by the shell. As is tradition, we will start with a Hello World application.

~~~
D:\modelling_tutorial\examples
λ example1
~~~

Files can also be run with parameters. 

Clear screen

~~~
D:\modelling_tutorial\examples
λ cls
~~~

We'll use the launch_nengo.bat file to open the GUI once it's installed.

## Anaconda

### What this is: 

Anaconda is a Python distribution. As Nengo is a Python package, your machine must first have a Python  installed to run it. 

### To install and configure

Download Python 3.7 version from https://www.anaconda.com/distribution/ 

**Ensure you check ‘configure environmental variables’ in the installation dialogue window.** This means that when you type `python` in a command prompt, Windows will use the PATH environment variables to get a list of directories to go looking for the python.exe file.

### Check

Launch the python interpreter

~~~
D:\modelling_tutorial
λ python
~~~

The command prompt will change: 
`>>>`

You are now in the Python interpreter. You can perform standard mathematical operations. 

For example,

~~~
>>> 3 + 3
6
~~~

Whereas

~~~
D:\Program Files\cmder
λ 3+3
~~~

Would yield an error
~~~
'3+3' is not recognized as an internal or external command, operable program or batch file.
~~~

A powerful feature of Cmder is support for multiple tabs running distinct shells.

## Nengo 

### What this is: 

_Nengo_ is its accompanying Python package for building and simulating large-scale, functional spiking neural architectures based on the Neural Engineering Framework (NEF).

The NEF provides methods to implement a large, useful class of mathematical operations in spiking neurons. These operations are realized with convex optimization, rather than with online 'learning methods. This is important for two reasons: First, a function specified by the user is immediately implemented in the network, rather than having to wait for a training period to complete. Second, the math that governs the convex optimization process is completely understood and can be challenged. It consists of three principles: Representation, Transformation, and Dynamics. 

Nengo models are built from `objects`: `Network`, `Node`, `Ensemble`, `Connection`, `Probe` whose built-in `solvers` do the math of the NEF. Nengo is an attractive neural simulator due to its ease of use, extensive tutorials and open-source projects, and a very active forum: https://forum.nengo.ai/top/all

### To install and configure 

In the cmd window, do:

~~~
D:\Program Files\cmder
λ pip install nengo nengo-gui
~~~

(`pip` is Python's _package manager_. This command will automatically download and install the neural simulator package to /lib/site-packages in your Python folder. )

### Check

~~~
D:\Program Files\cmder
λ nengo -P 18888
~~~

This launches `nengo-gui` in a new browser window, served at localhost, port 18888. 

Using the open file menu, navigate to built-in examples > tutorial. 

These tutorials are most relevant to us users concerned with neural architectures and dynamics:
`00-intro.py`
`01-one-neuron.py`
`03-many-neurons.py`
`04-connecting-neurons.py`
`10-transforms.py`
`11-memory.py`
`16-ensemble-properies.py`
`17-neuron-models.py`
`07-multiple-dimensions.py`

Using the Open File menu, navigate to modelling_tutorial > idb_lvs > idb_lvs.py and run it. 

## Git and GitHub

### What this is: 

Git is a source code management and version control system. GitHub is a online platform for collaborative software development. These tools are well suited to the problems of modelling collaboratively and pursuing independent simulation experiments.

### To install and configure 

Create an account on GitHub

Configure your local identity with Git, using the information used to set up your account. 

~~~
git config --global user.email <you@domain.com>
git config --global user.name <your name>
~~~

Generate public keys and give to ssh-agent. 

In the command window, do:
`ssh-keygen -t rsa -b 4096 -C <your_email@domain.com>`

When you're prompted to "Enter a file in which to save the key," press Enter. This accepts the default file location.

At the prompt, type a secure passphrase.
~~~
> Enter passphrase (empty for no passphrase): [Type a passphrase]
> Enter same passphrase again: [Type passphrase again]
~~~

Add your SSH private key to the ssh-agent.
`$ ssh-add ~/.ssh/id_rsa`

https://help.github.com/en/articles/adding-a-new-ssh-key-to-your-github-account
Copy the SSH key to your clipboard.
`$ clip < ~/.ssh/id_rsa.pub`

In the user settings sidebar, click SSH and GPG keys.

In the upper-right corner of any page, click your profile photo, then click Settings.

Click New SSH key or Add SSH key.

In the "Title" field, add a descriptive label for the new key. For example, if you're using a personal laptop PC, you might call this key "Personal Laptop PC".

Paste your key into the "Key" field.

Click Add SSH key. If prompted, confirm your GitHub password.

### Check 

The Git workflow will be explored through example in the next section, *Collaboration*.

# Collaboration

A _fork_ is a complete and independent repository of source code that can be considered a child of some parent source code repository (which is in turn complete and independent). Forks are the way that collaboration and experimentation is made possible in the open source community. For example, the Nengo repository currently has 116 forks: https://github.com/nengo/nengo/network/members.

Fork idb_lvs_model project at: https://github.com/kpc-simone/idb_lvs_model

Clone to local repository
git clone git@github.com:<your github account>/idb_lvs_model.git

Create a new branch
_Branches_ are used to organize work within a repository. 

`git checkout -b <branch-name>`

Suggestion: name-first-expt

Simulate and modify the model on your local machine.
Find idb-lvs.py in your working directory

Commit the changes and push to GitHub
`git add .`
`git commit -m <commit message>`
`git push origin <branch-name>`

Your changes will now appear on your GitHub repository, in your <branch-name> branch.

Initiate pull request

Return to https://github.com/<your account>/idb_lvs_model

Hit Compare & pull request.

On the left is the base for the comparison, my fork and branch. On the right is the head, your fork and branch, that you want to compare with it. A pull request goes from the head to the base - from right to left. You want your version, the head branch of the head fork - on the right - with some commits containing file changes, to be sent to my base repo - on the left.

Hit Pull Request
(_optional_) Add a comment
Hit Send pull request

Fetch from upstream

Powerful collaborative project management features of GitHub include Issues, Projects, and Wiki.

For example, check out Nengo's Issue board: https://github.com/nengo/nengo/issues
They host their documentation elsewhere: https://www.nengo.ai/nengo/

Create an issue:
- How could this tutorial be improved?
- What parts of this tutorial should be incorporated onto the Wiki to support collaboration?
- What would you like to see on the Wiki?

# References and further reading

## NEF

- **Book**: Eliasmith, Chris, and Charles H. Anderson. Neural engineering: Computation, representation, and dynamics in neurobiological systems. MIT press, 2004.

- **Technical summary**: http://compneuro.uwaterloo.ca/files/publications/stewart.2012d.pdf

## Nengo

- Paper: Bekolay, Trevor, et al. "Nengo: a Python tool for building large-scale functional brain models." Frontiers in neuroinformatics 7 (2014): 48.

- documentation: https://www.nengo.ai/nengo/

- forum: https://forum.nengo.ai/

- project: https://github.com/nengo/nengo

Git and GitHub

https://dont-be-afraid-to-commit.readthedocs.io/en/latest/index.html 
https://guides.github.com/
https://help.github.com/en

Cmder

https://github.com/cmderdev/cmder/blob/master/README.md

Anaconda

https://www.anaconda.com/