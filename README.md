# SpongeSplits
Aiming to create an autosplitting for bfbb.

Currently developing and testing on windows. Because we are using pynput, if using macOS one of the following must be true:
* The process must run as root.
* Your application must be white listed under Enable access for assistive devices. Note that this might require that you package your application, since otherwise the entire Python installation must be white listed.

* Use yapf to format files
* Use mypy to ensure typing


Unfortunately for me, I needed to get this working for Windows which ended up being harder than one might've thought. To get all the different dependencies to work harmoniously, people recommeneded installing the [Unofficial Windows Binaries for Python](https://www.lfd.uci.edu/~gohlke/pythonlibs/)

In the end, I was able to get all Pip-installed packages to work for the project using Python 3.6.8. My recomendation would be to use 3.6, however 3.7 **might work.** If you end up running into a DLL runtime error (on Windows), then I'd suggest to try installing these binaries. I'm keeping some of these binaries here for potential future use, but you'll likely want to download them and install for yourself from the [source](https://www.lfd.uci.edu/~gohlke/pythonlibs/).


# TODO: 
* Add tests to this
* Get larger dataset
* Add typing :)
* https://abseil.io/docs/python/quickstart for startup flags