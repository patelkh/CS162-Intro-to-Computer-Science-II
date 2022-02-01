# Author: Khushboo Patel

class QuoridorGame:
    """The QuoridorGame class is a representation of a Quoridor game between 2 players. It is responsible for (1) keeping track of whose turn it is to make a move (2) verifying whether a rule is being violated, (3) moving a pawn to given location, (4) placing a fence on a given coordinate, (5) updating player’s information and (6) checking whether a move results in a win. It communicates with the QuoridorBoard class to get the general layout and setup of the game board, QuoridorPlayer class to get/set information (e.g., location, fence count, etc.) about the 2 players, and Neighbor class to identify a player’s neighbors on the board."""

    def __init__(self):
        """Creates the game object and initializes the board with fences and pawns placed in the correct positions"""
        self._gameboard = QuoridorBoard()
        self._player = QuoridorPlayer()
        self._neighbors = Neighbor()
        self._currentturn = 1
        self._fences = {"h": [],
                        "v": []}
        self._winner = None

    def get_currentturn(self):
        """Returns the player (1 or 2) who is allowed to make the next move."""
        return self._currentturn

    def set_currentturn(self, player: int):
        """Switches the turn to the next player."""
        if player == 1:
            self._currentturn = 2
        elif player == 2:
            self._currentturn = 1

    def move_type(self, location: tuple, tile: tuple):
        """Takes as parameter a tuple with coordinates of current player's pawn location and a tuple with coordinates of where pawn is being moved to. Based on the provided coordinates, the method calculates and returns the direction of the play."""
        if (location[0]+1, location[1]) == tile:
            return "Right"
        elif (location[0]-1, location[1]) == tile:
            return "Left"
        elif (location[0], location[1]-1) == tile:
            return "Up"
        elif (location[0], location[1]+1) == tile:
            return "Down"
        elif (location[0], location[1]+2) == tile:
            return "Jump Forward"
        elif (location[0], location[1]-2) == tile:
            return "Jump Backward"
        elif tile in self._neighbors.get_diagonalneighbors(location):
            return "Diagonal"
        else:
            return "Invalid"

    def move_pawn(self, player: int, tile: tuple):
        """Takes as parameter an integer representing the player (1 or 2) and a tuple with coordinates of where the pawn is being moved to. The method validates the move against a set of rules. If the rules are satisifed, the program passes the information to a sub-function for additional checks and processing. Otherwise, the method returns False and player is required to try another move."""
        playerlocation = self._player.get_playerlocation(player)
        opponentlocation = self._player.get_opponentlocation(player)
        movetype = self.move_type(playerlocation, tile)

        # Player out of turn
        if self._currentturn != player:
            #print("It's not your turn.")
            return False
        # Game already won
        elif self._winner is not None:
            #print("Game over")
            return False
        # Tile occupied by player
        elif playerlocation == tile and self._player.get_lastplay(player) == "Moved Pawn":
            #print("You can't stay in one place.")
            return False
        # Tile occupied by opponent
        elif opponentlocation == tile:
            #print("Sorry, that tile is occupied by your enemy.")
            return False
        # Tile out of range
        elif tile not in self._gameboard.get_tiles():
            #print("Stay on the grid.")
            return False
        # Tile more than 1 move away
        elif movetype == "Invalid":
            #print("Sorry, you can't travel there from your current location.")
            return False
        else:
            if movetype in ["Right", "Left"]:
                return self.move_horizontal(player, tile, playerlocation, movetype)
            elif movetype in ["Up", "Down"]:
                return self.move_vertical(player, tile, playerlocation, movetype)
            elif movetype == "Jump Forward":
                return self.jump_forward(player, tile, playerlocation, opponentlocation)
            elif movetype == "Jump Backward":
                return self.jump_backward(player, tile, playerlocation, opponentlocation)
            elif movetype == "Diagonal":
                return self.move_diagonal(player, tile, playerlocation, opponentlocation)

    def move_horizontal(self, player: int, tile: tuple, playerlocation: tuple, movetype: str):
        """Takes as parameters an integer representing the player (1 or 2), a tuple with coordinates of where the pawn is being moved to, a tuple with coordinates of where the player is located and a string indicating the type of move. Based on the direction, the method checks that the play is not blocked by a fence. If the play is NOT blocked by a fence, the method passes the parameters to a sub-function, which moves the pawn to the given coordinates and updates the necessary status of the player and the game. Otherwise, the method returns False."""
        v_fences = self.get_verticalfencesonboard()
        if movetype == "Left" and playerlocation in v_fences:
            #print("You are blocked by fence.")
            return False
        elif movetype == "Right" and tile in v_fences:
            #print("You are blocked by fence.")
            return False
        else:
            return self.update_board(player, tile, "horizontal")

    def move_vertical(self, player: int, tile: tuple, playerlocation: tuple, movetype: str):
        """Takes as parameters an integer representing the player (1 or 2), a tuple with coordinates of where the pawn is being moved to, a tuple with coordinates of where the player is located and a string indicating the type of move. Based on the direction, the method checks that the play is not blocked by a fence. If the play is NOT blocked by a fence, the method passes the parameters to a sub-function, which moves the pawn to the given coordinates and updates the necessary status of the player and the game. Otherwise, the method returns False."""
        h_fences = self.get_horizonalfencesonboard()
        if movetype == "Up" and playerlocation in h_fences:
            #print("You are blocked by fence.")
            return False
        if movetype == "Down" and tile in h_fences:
            #print("You are blocked by fence.")
            return False
        else:
            return self.update_board(player, tile, "vertical")

    def jump_forward(self, player: int, tile: tuple, playerlocation: tuple, opponentlocation: tuple):
        """Takes as parameters an integer representing the player (1 or 2), a tuple with coordinates of where the pawn is being moved to, a tuple with coordinates of where the player is located, and a tuple with coordinates of where the opponent is located. If the player is facing the opponent and a fence is NOT between them, the method passes the parameters to a sub-function, which moves the pawn to the given coordinates and updates the necessary status of the player and the game. Otherwise, the method returns False."""
        h_fences = self.get_horizonalfencesonboard()
        topfence = (playerlocation[0], playerlocation[1]+1)
        bottomfence = (playerlocation[0], playerlocation[1]+2)
        if topfence in h_fences:
            #print("You are blocked by fence.")
            return False
        elif bottomfence in h_fences:
            #print("You are blocked by fence.")
            return False
        elif opponentlocation != topfence:
            #print("You are not facing your opponent.")
            return False
        elif opponentlocation == topfence:
            return self.update_board(player,tile, "jump")

    def jump_backward(self, player: int, tile: tuple, playerlocation: tuple, opponentlocation: tuple):
        """Takes as parameters an integer representing the player (1 or 2), a tuple with coordinates of where the pawn is being moved to, a tuple with coordinates of where the player is located, and a tuple with coordinates of where the opponent is located. If the player is facing the opponent and a fence is NOT between them, the method passes the parameters to a sub-function, which moves the pawn to the given coordinates and updates the necessary status of the player and the game. Otherwise, the method returns False."""
        h_fences = self.get_horizonalfencesonboard()
        topfence = (playerlocation[0], playerlocation[1]-1)
        bottomfence = playerlocation
        if topfence in h_fences:
            #print("blocked by fence")
            return False
        elif bottomfence in h_fences:
            #print("blocked by fence")
            return False
        elif opponentlocation != topfence:
            #print("not facing your opponent")
            return False
        elif opponentlocation == topfence:
            return self.update_board(player,tile, "jump")

    def move_diagonal(self, player: int, tile: tuple, playerlocation: tuple, opponentlocation: tuple):
        """Takes as parameters an integer representing the player (1 or 2), a tuple with coordinates of where the pawn is being moved to, a tuple with coordinates of where the player is located, and a tuple with coordinates of where the opponent is located. If the player is not blocked by a fence, the method passes the parameters to a sub-function for further validation and processing."""
        h_fences = self.get_horizonalfencesonboard()
        v_fences = self.get_verticalfencesonboard()
        adjacenttoptile = (playerlocation[0], playerlocation[1]-1)
        adjacentbottomtile = (playerlocation[0], playerlocation[1]+1)
        #Validate that players are face to face
        if opponentlocation == adjacentbottomtile:
            fence = (opponentlocation[0], opponentlocation[1] + 1)
            if fence in h_fences:
                # check for vertical fences
                leftfence = opponentlocation
                rightfence = (playerlocation[0] + 1, playerlocation[1] - 1)             #there is a bug here that needs to be fixed 
                if (tile == (playerlocation[0] - 1, playerlocation[1] + 1)) and (leftfence not in v_fences):
                    return self.update_board(player, tile, "diagonal")
                elif (tile == rightfence) and (rightfence not in v_fences):
                    return self.update_board(player, tile, "diagonal")
            else:
                #print("You are blocked by a fence.")
                return False
        elif opponentlocation == adjacenttoptile:
            fence = opponentlocation
            if fence in h_fences:
                leftfence = opponentlocation
                rightfence = (playerlocation[0]+1, playerlocation[1]-1)
                if (tile == (playerlocation[0]-1, playerlocation[1]-1)) and (leftfence not in v_fences):
                    return self.update_board(player, tile, "diagonal")
                elif (tile == rightfence) and (rightfence not in v_fences):
                    return self.update_board(player, tile, "diagonal")
            else:
                #print("You are blocked by a fence.")
                return False
        else:
            #print("Invalid move!")
            return False

    def update_board(self, player: int, tile: tuple, movetype: str):
        """Takes as parameters an integer representing the player (1 or 2), a tuple with coordinates of where the pawn is being moved to, and a string indicating the type of move. The method updates the necessary status of the player and the game."""
        self._player.set_location(player, tile)
        self._player.set_lastplay(player, "Moved Pawn")
        self.currentturn = self.set_currentturn(player)
        if movetype.lower() != "horizontal":
            if tile in self._player.get_baselinetarget(player):
                self.set_winner(player)
        return True

    def place_fence(self, player: int, direction: str, fence: tuple):
        """Takes as parameters an integer that represents which player (1 or 2) is making the move, a letter indicating whether it is vertical (v) or horizontal (h) direction, and a tuple of integers that represents the position on which the fence is to be placed. The method validates the move against a set of rules. If the rules are satisifed, the program passes the information to a sub-function for additional checks and processing. Otherwise, the method returns False and player is required to try another move."""
        #Invalid direction
        if direction.lower() not in ["h", "v"]:
            print("Valid values are 'h' and 'v'. Try again.")
            return False
        #Player out of turn
        elif self._currentturn != player:
            print("It's not your turn.")
            return False
        #Game already won
        elif self._winner is not None:
            print("Game over")
            return False
        #Player out of fences
        elif self._player.get_fencecount(player) == 0:
            print("You don't have any more fences left.")
            return False
        elif direction.lower() == "v":
            #Invalid coordinates
            if fence not in self._gameboard.get_validverticalfences():
                print("Stay on the grid.")
                return False
            #Fence already in place
            elif fence in self.get_verticalfencesonboard():
                print("Fence already in place.")
                return False
            else:
                self.add_fence(direction, fence)
                self._player.set_fencecount(player)
                self._player.set_lastplay(player, "Placed a fence")
                self.currentturn = self.set_currentturn(player)
                return True
        elif direction.lower() == "h":
            #Invalid coordinates
            if fence not in self._gameboard.get_validhorizontalfences():
                print("Stay on the grid.")
                return False
            #Fence already in place
            elif fence in self.get_horizonalfencesonboard():
                print("Fence already in place.")
                return False
            #Check the play is fair
            elif fence in self._player.get_baselinetarget(self._player.get_opponent(player)) \
                and self.check_baseline(self._player.get_opponent(player)) == 8:
                print("Fair play rule violated.")
                return "breaks the fair play rule"
            else:
                self.add_fence(direction, fence)
                self._player.set_fencecount(player)
                self._player.set_lastplay(player, "Placed a fence")
                self.currentturn = self.set_currentturn(player)
                return True

    def check_baseline(self, player: int):
        """Takes as a parameter an integer representing the player (1 or 2). The method validates the fair play rule is honored."""
        count = 0
        baseline = self._player.get_baselinetarget(player)
        h_fences = self.get_horizonalfencesonboard()
        for tile in baseline:
            if tile in h_fences:
                count += 1
        return count

    def add_fence(self, direction: str, fence: tuple):
        """Takes as parameters a letter indicating the direction of the fence and a tuple with coordinates of where the fence is located. The method adds the fence to a dictionary, which is used by other methods to validate subsequent moves.  """
        if direction.lower() == "h":
            for key in self._fences:
                if key == "h":
                    self._fences[key].append((fence))
        elif direction.lower() == "v":
            for key in self._fences:
                if key == "v":
                    self._fences[key].append((fence))

    def get_verticalfencesonboard(self):
        """Takes no parameters and returns a list of fences currently on the board in vertical position."""
        verticalfences = []
        for key in self._fences:
            if key == "v":
                verticalfences += (self._fences[key])
        return verticalfences

    def get_horizonalfencesonboard(self):
        """Takes no parameters and returns a list of fences currently on the board in horizontal position."""
        horizontalfences = []
        for key in self._fences:
            if key == "h":
                horizontalfences += (self._fences[key])
        return horizontalfences

    def set_winner(self, player: int):
        """Takes as a parameter an integer representing the player (1 or 2) and returns whether the player is a winner or not."""
        self._winner = player

    def is_winner(self, player: int):
        """Takes as parameter an integer representing the player (1 or 2) and sets that player as the winner of the game."""
        if self._winner == player:
            return True
        else:
            return False

    def get_board(self):
        """Takes no parameters and returns the game board."""
        return self._gameboard.get_board()


class Neighbor:
    """The Neighbor class is a representation of a player’s neighbors on the game board. It is responsible for determining a player’s neighbors based on their current location on the board. A neighbor is considered a ‘regular’ neighbor if they sit to the right, left, behind or in front of the player or ‘diagonal’ neighbor if they sit diagonal to the player. This class communicates with the QuoridorGame class by providing a list of neighbors to validate a player’s move against."""

    def __init__(self):
        """Creates a neighbor object and intializes a blank game board to be used purely as a reference."""
        self._gameboard = QuoridorBoard()

    def get_regularneighbors(self, tile: tuple):
        """Takes as a parameter a tuple with coordinates of a player's location and returns a list of tuples with coordinates of player's regular neighbors on the board."""
        right = (tile[0]+1, tile[1])
        left = (tile[0]-1, tile[1])
        top = (tile[0], tile[1]-1)
        bottom = (tile[0], tile[1]+1)
        temp = [right, left, top, bottom]

        validneighbors = []
        for coordinate in temp:
            if coordinate not in self._gameboard.get_walls():
                validneighbors.append(coordinate)
        return validneighbors

    def get_diagonalneighbors(self, tile: tuple):
        """Takes as a parameter a tuple with coordinates of a player's location and returns a list of tuples with coordinates of player's diagonal neighbors on the board."""
        diagonallefttop = (tile[0]-1, tile[1]-1)
        diagonalleftbottom = (tile[0]-1, tile[1]+1)
        diagonalrighttop = (tile[0]+1, tile[1]-1)
        diagonalrightbottom = (tile[0]+1, tile[1]+1)
        temp = [diagonallefttop, diagonalleftbottom, diagonalrighttop, diagonalrightbottom]

        validneighbors = []
        for coordinate in temp:
            if coordinate not in self._gameboard.get_walls():
                validneighbors.append(coordinate)
        return validneighbors


class QuoridorPlayer:
    """The QuoridorPlayer class represents players and their relationship to the game and the game board. It is responsible for initializing each player’s starting location and updating the location as they move from location to another. Each player is given 10 fences to play. This class keeps track of remaining fences. The first player who reaches any of the tiles of the opposite player’s baseline wins the game. This class stores the baseline tiles in a list, one list per player. It communicates with the QuoridorGame class by providing the player’s location, fence count and baseline tiles."""

    def __init__(self):
        """Creates a player object and initializes it's data members."""
        self._player1location = (4,0)
        self._player2location = (4,8)
        self._player1lastplay = None
        self._player2lastplay = None
        self._player1fencecount = 10
        self._player2fencecount = 10
        self._player1goal = self.player1baselinetarget()
        self._player2goal = self.player2baselinetarget()

    def get_playerlocation(self, player: int):
        """Returns the given player's location on the game board."""
        location = None
        if player == 1:
            location = self._player1location
        elif player == 2:
            location = self._player2location
        return location

    def get_opponentlocation(self, player: int):
        """Returns the opponent's location on the game board."""
        location = None
        if player == 1:
            location = self._player2location
        elif player == 2:
            location = self._player1location
        return location

    def get_opponent(self, player: int):
        """Returns the player's opponent."""
        opponent = None
        if player == 1:
            opponent = 2
        elif player == 2:
            opponent = 1
        return opponent

    def get_lastplay(self, player: int):
        """Returns the player's last move."""
        playerlastplay = None
        if player == 1:
            return self._player1lastplay
        elif player == 2:
            return self._player2lastplay

    def get_fencecount(self, player: int):
        """Returns the player's fence count."""
        if player == 1:
            return self._player1fencecount
        elif player == 2:
            return self._player2fencecount

    def get_baselinetarget(self, player: int):
        """Returns a list of tuples with coordinates of where the player must reach in order to win the game."""
        if player == 1:
            return self._player1goal
        elif player == 2:
            return self._player2goal

    def set_location(self, player: int, tile: tuple):
        """Takes as parameters an integer representing the player (1 or 2) and a tuple with coordinates of player's new location. Sets the player's location to the new coordinates."""
        if player == 1:
            self._player1location = tile
        elif player == 2:
            self._player2location = tile

    def set_lastplay(self, player: int, play: str):
        """Takes as parameters an integer representing the player (1 or 2) and a string indicating the type of play "move_pawn" or "place_fence". Stores a reference to the play."""
        if player == 1:
            self._player1lastplay = play
        elif player == 2:
            self._player2lastplay = play

    def set_fencecount(self, player: int):
        """Takes as parameters an integer representing the player (1 or 2). Decreases the player's fence count by 1."""
        if player == 1:
            self._player1fencecount -= 1
        elif player == 2:
            self._player2fencecount -= 1

    def player1baselinetarget(self):
        """Takes no parameters and generates a list of tuples with coordinates player 1 must move into in order to win the game."""
        baseline = [(n,8) for n in range(0,9)]
        return baseline

    def player2baselinetarget(self):
        """Takes no parameters and generates a list of tuples with coordinates player 2 must move into in order to win the game."""
        baseline = [(n,0) for n in range(0,9)]
        return baseline


class QuoridorBoard:
    """The QuoridorBoard class represents the Quoridor game board. It is responsible for generating a 9x9 board, tracking coordinates that make up the 4 walls around the board, tracking vertical and horizontal coordinates and storing the location of each square/tile on the board. This class communicates with the QuoridorGame when the QuoridorGame class needs the initialize setup of the board. It also communicates with the Neighbor class when the Neighbor class needs a reference to the board layout."""

    def __init__(self):
        """Creates a board object and initializes its data members."""
        self._board = {"0": [],
                      "1": [],
                      "2": [],
                      "3": [],
                      "4": [],
                      "5": [],
                      "6": [],
                      "7": [],
                      "8": []}
        self.tiles()
        self._walls = self.walls()
        self._validhorizontalfences = self.validhorizontalfences()
        self._validverticalfences = self.validverticalfences()

    def tiles(self):
        """Takes no parameters. Uses a loop to add values to the self._board dictionary. No return value."""
        for row in range(0,9):
            for column in range(0,9):
                key = str(row)
                self._board[key] += [(column, row)]

    def walls(self):
        """Takes no parameters. Uses a loop to generate a list of tuples containing coordinates that make up the walls around the game board. Returns a list of tuples with coordinates that make up the 4 walls around the game."""
        left = [(-1, n) for n in range(-1, 11)]
        right = [(9, n) for n in range(-1, 11)]
        top = [(n, -1) for n in range(-1, 11)]
        bottom = [(n, 9) for n in range(-1, 11)]
        temp = [left, top, right, bottom]

        walls = []
        for list in range(0, len(temp)):
            for coordinate in temp[list]:
                walls.append(coordinate)
        return walls

    def validhorizontalfences(self):
        """Takes no parameters. Uses a loop to generate a list of tuples with coordinates where a fence can be placed horizontally."""
        fence = []
        for column in range(0, 9):
            for row in range(1, 9):
                fence += [(column, row)]
        return fence

    def validverticalfences(self):
        """Takes no parameters. Uses a loop to generate a list of tuples containing coordinates where a fence can be placed vertically."""
        fence = []
        for column in range(1, 9):
            for row in range(0, 9):
                fence += [(column, row)]
        return fence

    def get_tiles(self):
        """Takes no parameters. Uses a loop to add values to the self._board dictionary. No return value."""
        valid_tiles = []
        for coordinate in self._board:
            valid_tiles += self._board[coordinate]
        return valid_tiles

    def get_walls(self):
        """Takes no parameters. Returns a list of tuples with coordinates that make up the walls around the game board"""
        return self._walls

    def get_validhorizontalfences(self):
        """Takes no parameters. Returns a list of tuples with coordinates where a fence can be placed horizontally"""
        return self._validhorizontalfences

    def get_validverticalfences(self):
        """Takes no parameters. Returns a list of tuples with coordinates where a fence can be placed vertically."""
        return self._validverticalfences

    def get_board(self):
        """Takes no parameters. Returns a blank board."""
        return self._board



def main():
    q = QuoridorGame()
    print(q.move_pawn(2, (4, 7)))  # moves the Player2 pawn -- invalid move because only Player1 can start, returns False
    print(q.move_pawn(1, (4, 1)))  # moves the Player1 pawn -- valid move, returns True
    print(q.place_fence(1, 'h', (6, 5)))  # places Player1's fence -- out of turn move, returns False
    # print(q.move_pawn(2, (4, 7)))  # moves the Player2 pawn -- valid move, returns True
    # print(q.place_fence(1, 'h', (6, 5)))  # places Player1's fence -- returns True
    # print(q.place_fence(2, 'v', (3, 3)))  # places Player2's fence -- returns True
    # print(q.is_winner(1))  # returns False because Player 1 has not won
    # print(q.is_winner(2))  # returns False because Player 2 has not won


main()
