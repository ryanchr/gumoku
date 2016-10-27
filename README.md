# Go-MoKu game through Adversarial Search

This project is meant to create a program to determine the next move for a player in Go-Moku game using Greedy, Minimax, and Alpha-Beta pruning algorithms. 

**Introduction to Go-Moku**

Go-Moku or Five in line is a traditional oriental game, originally from China. The game consists of a grid of squares which can be any size as seen in the image below. Usually, it is 19x19 and no smaller than 15x15. Players choose colors of their stones and decide who will play first. When playing with traditional white and black stones, black always goes first. The board starts empty. The first player then plays a single stone on the center intersection of the grid. Players then alternate playing 1 stone per turn. 

For this project, we impose the restriction that the new stone has to be placed adjacent (horizontally, vertically, or diagonally) to any of the existing stone. This is different from the traditional play-style where the new stone can be placed anywhere on the board. The objective of the game is to get five or more stones in a row (horizontally, vertically, or diagonally). The first player to achieve this wins the game.

**Algorithm**

In this project, we wrote a program to determine the next move by implementing the following algorithms:

• Greedy

• Minimax

• Alpha-Beta

**Input**

An input file “xxx.txt” is used as a command line argument that describes the current state of the game. The structure of the input file will be as follows:

<Task#> Greedy=1, Minimax=2, Alpha-Beta=3

<Your player: 1 or 2>

<Cutting off depth: d> Cut-off depth for the search tree. 1≤d≤4 

<N> Number of horizontal and vertical lines, 15≤N≤25

<Board state> N lines specifying the current board state


**Output**

1. Greedy: The program output one file named “next_state.txt” showing the next state of the board after the greedy move.

2. Minimax:

The program output two files named “next_state.txt” showing the next state of the board after the minimax move and “traverse_log.txt” showing the traverse log of the program.

3. Alpha-Beta:

The program output two files named “next_state.txt” showing the next state of the board after the alpha-beta move and “traverse_log.txt” showing the traverse log of the program.


**Run the code**

The command to run the code would be “python gomoku{3}.py inputfile”, where you will read the input file name from the command line argument.


