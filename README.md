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
pieces on the board threaten each other. This implies that the goal is to find a board with at least
k original pieces (i.e., pieces in their starting positions) on it, such that among these k original
pieces, no piece is threatening another. The diagram below shows an example of a goal state of the
game:

![image](https://user-images.githubusercontent.com/85006125/199653812-d9107fcf-1adf-463c-aad3-5271810d515b.png)



## How it works? (CSP.py)
