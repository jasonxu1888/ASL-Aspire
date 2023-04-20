For installing packages...

Commands: (May differ depending on OS; this is for Windows. Search "how to activate venv" if errors)
python3 -m env .venv
.venv\Scripts\activate
pip install -r requirements.txt

Note:
Installing packages may take a while, be patient.
There are very likely unnecessary packages/libraries in the requirements.txt, but if it works it works. 
Cleaning up can be done, but good luck...
Using virtual environments (whether through Anaconda or etc) are the norm for installing packages.
Pipreqs library was used to help generate requirements.txt


To run the game, make sure virtual environment is activated and root dir is SP2023

Commands:
python game.py