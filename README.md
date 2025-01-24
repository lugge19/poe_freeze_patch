# poe_freeze_patch

## problem
The game **Path of Exile 2** has still to this date a bug on Windows 11 24H2 if Auto HDR is enabled (see [this steam thread](https://steamcommunity.com/app/2694490/discussions/0/598514698788283237/)).

In simple terms, it looks like Path of Exile 2 uses all CPU cores and doesn't give them back to the operating system, making the PC completely unresponsive. The PC must be restarted by power off and power on.

## fix
In order to prevent Path of Exile 2 from bricking your PC, you can reconfigure the CPU affinity of the process with the task manager after each start of the game.

For example, unticking CPU 0 and CPU 1 makes Path of Exile 2 stop using the first CPU core (physical + virtual).

Keep in mind that Path of Exile 2 still freezes sometimes, but now at least Windows is still responsive, so you can tab out of the game, kill it with the task manager and restart the game.

## project goal
This project creates an executable file for Windows (.exe file) that automatically reconfigures the CPU affinity for the Path of Exile 2 process and removes CPU 0 and CPU 1.

# build application
Tested under Windows 11 in the cmd (not powershell!)

* create venv
```bash
python -m venv venv
```

* activate venv
```bash
.\venv\Scripts\activate
```

* install dependencies
```bash
pip install -r requirements.txt
```

* build application
```bash
pyinstaller --onefile main.py
```

The executable is created in the folder **dist**

# use application
* double-click the .exe file **after** Path of Exile 2 is started
* you can check if it worked by looking at the process affinity in the task manager