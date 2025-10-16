# escape-room
Created by Lejla Osmanovic, Sheema Ruzaik, and Thomas Mortimer<br>
Implementation of the escape room project for Programming fundamentals, to show our understanding of python coding standards.<br>
<br>
To execute the program, put your data files into the folder data/ and then execute escape<br>

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

## escaperoom

### engine

### transcript

### utils

Handles saving and loading of the current game state. It also contains common functions like converting a string to a
float and opening a file

### inventory

### rooms

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

#### vault

Solves the data\vault_dump.txt file, looking for the single lone version of a string the matches the following condition
SAFE={a-b-c} where a+b=c