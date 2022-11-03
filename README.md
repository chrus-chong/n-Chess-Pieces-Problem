# n-Chess-Pieces-Problem
Modelled closely after the famous 8-Queens Puzzle, the two programs CSP.py and Local.py each attempts to find a satisfactory goal state where no chess pieces threaten one another. 

## How it works? (Local.py)
We are given a game board of varying size. Each such board is completely filled with chess pieces
(and obstacles). The positions of the chess pieces and obstacles are given in the input test file (refer to examples in `Source Files` directory).
The pieces and obstacles will remain static at all times (i.e., they remain in the same position
throughout the search). Each chess piece will threaten its surrounding position based on the type
of chess piece it is. Note that whilst the chess pieces can threaten each other, they will not actually
capture/eliminate other pieces. An example of the initial state of the board is shown below:

![image](https://user-images.githubusercontent.com/85006125/199653435-b233df78-05c5-42f4-a290-e780834dc5ec.png)

We are also given a positive integer k (where k ≤ n, and given that initially, there are n pieces
on the board). The objective of the game is thus to remove at most n − k pieces such that no two
pieces on the board threaten each other. 

The goal is to find a board with at least
k original pieces (i.e., pieces in their starting positions) on it, such that among these k original
pieces, no piece is threatening another. The diagram below shows an example of a goal state of the
game:

![image](https://user-images.githubusercontent.com/85006125/199653812-d9107fcf-1adf-463c-aad3-5271810d515b.png)

Local.py models this problem as a Hill-climbing problem and incorporates random restarts to obtain the solution.

**Running Local.py**
1. First create an input .txt file to specify the initial game state. Some example input files can be found in the `Source Files` directory
2. Run the following command
`python Local.py ./'Source Files'/Local1.txt`
3. You will see the optimal arrangement of the remaining pieces after at most (n-k) pieces has been removed


## How it works? (CSP.py)
The context of CSP.py is very similar to that of Local.py. However, one important change to note is that rather then removing pieces from an existing board, CSP.py takes in the number of chess pieces and returns a dictionary containing a mapping of the position of the grid to the chess piece type.

As such, there are slight changes in the input .txt file format for CSP.py

CSP.py models this problem as a Constraint Satisfaction Problem and uses the BackTracking algorithm with a Degree heuristic in order to obtain a solution.


**Running CSP.py**
1. First create an input .txt file to specify the initial game state. Some example input files can be found in the `Source Files` directory
2. Run the following command
`python CSP.py ./'Source Files'/CSP1.txt`
3. You will see the optimal arrangement of the specified pieces in the input file.
