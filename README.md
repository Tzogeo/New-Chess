# New-Chess
A fun and unexpected twist on the famous game

It's a new variant of chess for two players where things like the name of an opening, a weird mushroom or just randomness can change the direction of the game.

## The three versions:
There are three versions of the game which are almost identical in terms of gameplay but have differences in the type of programming and user interface.
* version 1: uses pygame and is built with procedural programming as it mostly uses functions. It is the simplest version and it has limitations on possible improvements
* version 2: uses pygame and is built with object orientet programming. It is more complex that version 1 but the classes and their object can help to implement more complex ideas and twists
* version 3: it is built based on version one(procedural programming) but uses the kivy library instead of pygame. This allows the ui to be more flexible and possibly compatible with smartphones(though I haven't managed it yet)

When not specified every part of the read-me refers to all three versions.
The users can play on any of the versions they want.

## Essential libraries:
* pygame (versions1 and 2)
* kivy (version3)
* sys  (versions 1 and 2) (pre-installed with python)
* random (pre-installed with python)
* tkinter (pre-installed with python)


## How to install the project:

* Ensure you have Python installed on your system.
* Install the Pygame or  Kivy libraries by using pip install pygame or pip install kivy in Windows or the respective lines in other OS.
* Clone this repository to your local machine.
* Navigate to the directory where the program is saved.
* Run the new_chess(versionX).py file using Python.(X is 1,2,3)

## How to play the game:
The game is similar to a normal chess game. The player with the white pieces makes the first move and the player with the black pieces follows. Each player should pick a piece with their mouse and drag it(while left-click is pressed) to the desired position where the pressing should be stoped. If the movement is illegal the piece will return to its initial position and the user will be able to try another move. If the movement is legal the piece will stay on its new position and it will be the other player's turn. Sometimes a message might appear after a turn. That means that the movement was special in some regards so the position will change. The users are advised to read it and then click ok.

The pieces move (most of the times) like normal chess. One basic difference that should be noted is that there are no check-mates. The aim of the game as in many variants is to capture the king. That makes stalemates more difficult since the king can move into a square attacked by an opponent's piece.

## The differences from normal chess:
The game is different in some ways. The players in my opinion should be unaware of the differences(with the exception of the capturing of the king). That will make it a surprise when one of them appears. And it will let them discover the game by themselves and develop their own strategies.
The variant is less deterministic as it includes many elements of randomness (pseudo-randomness from the random library). That means that the results are influenced by luck and the players should be focused on having fun rather than making the correct moves(which in this variant might end up being the worst moves).

Some changes include:
* Forced en-peassant. 
* The promoted piece is decided by luck rather than the players choice
* The meet-up of two bishops causes a curse to the game which changes it

There are a lot of smaller or bigger changes which will be included in a future txt file. The players are again advised to not read that (or the code) and play the game without the knowledge of the specific changes. People interested in contributing to the game should read the file to help get some ideas (either to add similar changes or move to another direction that hasn't been changed yet)

## Advice to players from testing:
* Never give up. Luck can change things in a lot of ways.
* Try different openings and don't play the Caro-Kann. (the developer just doesn't like it)
* Read the messages that appear and then click OK. They explain what happened and why. (also the developer spent time writing them and thinks some of them are funny)
* Have a pillow or something similar near you. Punching the computer or the developer isn't usually a good idea.(There are exceptions to that)
  
## Credits:
This program is developed using Pygame or Kivy both of which are  open-source libraries for making multimedia applications.  Special thanks to the contributors of Pygame and Kivy. 
The images where taken from the web.

## Contribution:
Contributions to this project are welcome! Feel free to submit bug reports, feature requests, or even pull requests to help improve this variant.

## License:
This project is licensed under the MIT License - see the LICENSE file for details.

## Feedback:
If you have any feedback, suggestions, or issues, please reach out.

Thank you for playing the game!
