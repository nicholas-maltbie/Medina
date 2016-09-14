# Medina #
An attempt to utilize machine learning to play the board game Medina

## The Game ##
*Media* is a board game published by Stronghold Games (
[more information here](https://boardgamegeek.com/boardgame/167270/medina-second-edition), 
[official website for game](https://strongholdgames.com/store/board-games/medina/) )
and designed by Stefan Dorra. I claim to have no ownership of the game and this 
project is only an attempt to use machine learning to play the game.

The game is played by two to four players and the players all build a city 
together. While building the city, players can claim buildings for points. 
Buildings near the well, market or walls are worth more points than buildings 
not close to anything important in the city. 

A game being played

![Game in progress](https://cf.geekdo-images.com/images/pic2613390_md.jpg)

Image from Board Game Geek by Julian Pombo uploaded on 2015-08-03
[image source](https://boardgamegeek.com/image/2613390/medina-second-edition?size=medium)

Each player is given a limited amount of resources and on each of thier turns, 
players can build the city or claim a building; players can take a total of two 
actions on each of their turns. There are four different colors of buildings and 
each player can only claim one of each color. After every player has claimed a 
building of each color or no more actions can be taken, the game ends.

A player can place any two or two of the same pieces from the following list on 
each of their turns:

 1. _Buildings_ : can be used to start a new building or grow an existing, 
unclaimed building. Four colors of buildings: Grey, Brown, Orange and Purple.
 2. _Rooftops_ : can be used to claim an unclaimed building currently on the 
board. A player can only own one of each color building.
 3. _Stables_ : can be attached to an existing claimed building and grows the 
building for purposes of ardency and scoring.
 4. _Merchant_ : merchants build in a claim across the board and award extra 
points to buildings that the merchants are next to.
 5. _Walls_ : walls are built around the edge of the board growing out from 
towers at the corners. Walls that are adjacent to buildings award extra points 
to the building for each wall touching the building. 

While building, there are a few restrictions that players can utilize to take 
advantage of the current board and further their own score or hurt other players 
ability to play. For example, only one unclaimed building of each color can be 
built at a time and once a building is claimed it can only be extended by 
attaching stables.

Once the game has ended, the buildings each player has claimed scores based on 
the position and elements around the building (walls, the well, merchants and 
stables all give additional points). For the full rules and scoring of the game, 
view [this pdf](http://www.boardspace.net/medina/english/WGG_Medina_Rules_GB_Web.pdf)

## Objective ##
My objective is this project is to:
* Implement the game in Python with a GUI interface and allow players to play 
the game.
* Make the game a network game so multiple players could play the same game on 
different machines.
* Add an AI to the game that utilizes machine learning and pattern recognition 
to make moves and become better at playing the game as time goes on.
* Give the AI the ability to watch and learn from records of games.
* Train the AI to the point in which it can consistently play the game and get 
a decent score.
* Possibly develop different versions of the AI that can play the game with 
different strategies (aggressive, risky, impatient) and difficulty.

## Purpose ##
This project is the project I will be doing as part of my Programming Python 
course at The Univeristy of Cincinnati Fall Semester 2016.

## Time Frame ##
*This is subject to change as many aspects of the scope and design may change 
as the project progresses*

*All code should be documented as the project is made and plans to make changes 
should be logged in a fiel in the repo*

The game should be at least implement with a partially functional GUI by October 
1st 2016 (Marks the start of the project)

_Two weeks in_ (Oct 15th): 
- The game should be fully implemented:
* the rules should be implemented, the game should be able to score the board.
* multiple players should be able to play the game on one machine.

_Four weeks in_ (Oct 29th): 
- The game should be fully implemented over a network 
- human players can join the game. A _JOSN_ format should be used to: manage all 
actions of players in the game, announce game start, and determine the winner.

_Six weeks in_ (Nov 12th): 
- An AI library should be selected and a plan written of how to implement an AI 
in the game. This inclues benchmarking completed for designing the AI and 
similar AI for playing board games or pattern recognition. 
- A new time frame should also be made by this point.

_Eight weeks in_ (Nov 26th): 
- The AI should be implemented with the ability to play a game to completion 
and play over a network.

_November 30th_: 
- The game should be completed with an AI implementation that 
can sucesfully play the game and consistantly obtain a decent score.

### Copyright ###
This code is under the MIT License Copyright (c) 2016 Nicholas Maltbie. See 
LICENSE.txt for further details.
