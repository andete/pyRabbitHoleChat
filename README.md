pyRabbitHoleChat created by Paul Schimmelpfenning and is licensed under the GNU AGPLv3 or Later License. See the COPYRIGHT file.

Chat client for the Rabbit Hole hackerspace for the [Tymkrs](http://tymkrs.com).

DEPENDENCIES
-----
* Python (>= 2.6, < 3.0)
* PyGTK (> 2.0)
* GTK (> 2.0, < 3.0)

How to Use
-----
To edit your default username, server address, or port address, just edit the config included.

If you do not set a default username, the program will give you the nickname "Rabbithole" with a number between 0 and 5000.

To start this program, open your terminal, go to the directory where pyRabbitHoleChat.py, GUI.xml and config file are located and type:
>python pyRabbitHoleChat.py

If that doesn't work, then you may have Python3 set as your default Python version, so just type:
>python2 pyRabbitHoleChat.py

To make pyRabbitHoleChat.py an executable file, go to the directory where pyRabbitHoleChat.py is located and type:
>chmod +x pyRabbitHoleChat.py


Special Functions
-----
/h - Displays usable commands

/help - Displays usable commands

/n - Displays online users

/nick - */nick __n__* changes your username to *__n__*

/quit - Quit pyRabbitHoleChat
