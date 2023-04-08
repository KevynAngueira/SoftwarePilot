SoftwarePilot
=============
SoftwarePilot is an open source middleware and API that supports aerial applications. SoftwarePilot allows users to connect consumer Parrot Anafi drones to programmable pythonscripts that provide access to the drones flight controller, camera, and navigation system as well as custom rest api and dockerfile integration.


Getting Started
---------------
Install the library:
~~~~~~~~~~~~~~~~~~~~
1. Clone the repo, or
  git clone https://github.com/boredbot2/SoftwarePilot.git
2. Pip install
  pip install SoftwarePilot

First Time Set Up:
~~~~~~~~~~~~~~~~~~
1. Pair the drone:
  1. ``Turn on`` the Parrot-Anafi drone.
  2. ``Turn on`` the Skycontroller.
  3. Connect a ``USB to USB-C`` cable to the controller and the drone respectively.
  4. Wait until the blinking light on the controller turns into a ``solid blue light``.
  5. ``Disconnect`` the controller and the drone.

2. Calibrate the drone:
  1. Download the ``FreeFlight 6`` app on your phone and perform all necesary authentication.
  2. Connect a ``USB to USB-C`` cable to the controller and the phone.
  3. Press ``Fly`` on the FreeFlight 6 app and follow the instructions on the screen.
  4. Confirm calibration by launching and then landing the drone with the ``Up and Down arrows`` button on the controller.
