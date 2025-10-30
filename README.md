# escape-room
Created by Lejla Osmanovic, Sheema Ruzaik, and Thomas Mortimer<br>
Implementation of the escape room project for Programming fundamentals,
to show our understanding of python coding standards.<br>
<br>
To execute the program, put your data files into the folder data/ and then execute escape.py<br>
Requires Python 3.12<br>

# Table of files
* [escape](#escape)
* [escaperoom](#escaperoom)
    * [engine](#engine)
    * [transcript](#transcript)
    * [utils](#utils)
    * [inventory](#inventory)
    * [rooms](#rooms)
        * [base](#base)
        * [currentroom](#currentroom)
        * [dns](#dns)
        * [malware](#malware)
        * [soc](#soc)
        * [vault](#vault)

## escape

The main python file that runs the code, welcomes the user to the game and initialises some classes.
Then asks the user what to do, via the engine.

## escaperoom

The folder holding the majority of our python code, the top level has the general engine and helper classes.

### engine

Manages the game state and will manage the commands a user enters.
One main function which is then broken down into multiple private functions depending on what action is called.

### transcript

Records the actions the user has done, also stores any solved rooms to be ready to print
in the correct file format order.

### utils

Handles saving and loading of the current game state. It also contains common functions like converting a string to a
float and opening a file.

### inventory

Holds the inventory of the user, which includes items they have solved.
If the inventory is not complete, the final gate will not be tried.

### rooms
Contains the room files, which all extend from the base.py room and implements the solve method

#### base
An abstract class holding some functions that are common among rooms, including opening of the relevant file to be solve
in the room.
Also manages the logging of data in a consistent way

#### currentroom
An enum class for handling making it easier to show which room you are in and what items are available to either inspect
or use.

#### dns

#### malware

#### soc

Solves Room 2-SOC Triage Desk <br>
Parses data\auth.log file and finds the subnet with the most failed login attempts and gets the count{COUNT}.  Amongst that subnet, finds the most common IP address and retrieves its last octet{L}.
Generates token: TOKEN={L}{COUNT}

#### vault
Solves the data\vault_dump.txt file, looking for the single lone version of a string the matches the following condition
SAFE={a-b-c} where a+b=c