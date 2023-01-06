# Author: Seth Stephanz
# GitHub username: sethstephanz
# Date: 8/11/2022
# Description: This program models a game of Ludo. The Player class creates players of the game; the game state
# is distributed among the properties of all the players. The LudoBoard contains a move algorithm, which determines
# how rolls are distributed to pieces. There are also mechanisms in place to monitor whether tokens are stacked.

class Board:
    """Because all of the players start and end in different places, it seemed easier to store the board state
    between 2/3/4 individual boards and keep track of players' positions using counters rather than try to do the same
    work later on with conditional statements when deciding where to move tokens. The Board class basically just
    stores the possible boards that players A through D would use for a game of Ludo."""

    def __init__(self):
        """Holds all boards for all possible player positions"""
        self._A_board = ['R', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16',
                         '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32',
                         '33', '34', '35', '36', '37', '38', '39', '40', '41', '42', '43', '44', '45', '46', '47', '48',
                         '49', '50', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'E', 'H']
        self._B_board = ['R', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28',
                         '29', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '40', '41', '42', '43', '44',
                         '45', '46', '47', '48', '49', '50', '51', '52', '53', '54', '55', '56', '1', '2', '3', '4',
                         '5', '6', '7', '8', 'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'E', 'H']
        self._C_board = ['R', '29', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '40', '41', '42',
                         '43', '44', '45', '46', '47', '48', '49', '50', '51', '52', '53', '54', '55', '56', '1', '2',
                         '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19',
                         '20', '21', '22', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'E', 'H']
        self._D_board = ['R', '43', '44', '45', '46', '47', '48', '49', '50', '51', '52', '53', '54', '55', '56',
                         '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17',
                         '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33',
                         '34', '35', '36', 'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'E', 'H']

        self._board_state = []

    def get_A_board(self):
        """Returns player A's board"""
        return self._A_board

    def get_B_board(self):
        """Returns player B's board"""
        return self._B_board

    def get_C_board(self):
        """Returns player C's board"""
        return self._C_board

    def get_D_board(self):
        """Returns player D's board"""
        return self._D_board


class Player:
    """Class that creates Player objects, each of which represents one player of a game of Ludo"""

    def __init__(self, player_ID):
        """Initializes properties used in each player object
        Taken together, the total token positions of each player forms a board state rather than having an
        explicit Board class"""
        self._completion_status = False  # True if player has finished game, False if player is still playing
        self._player_ID = player_ID
        self._pieces_stacked = False  # resets if at any point the pieces are kicked back to home yard
        self._board = None
        self._p_counter = -1
        self._q_counter = -1

    # getters and setters----------------------------------------------------------------------------------------------
    def set_player_ID(self, player_ID):
        """Sets player ID"""
        self._player_ID = player_ID

    def get_player_ID(self):
        """Gets player ID"""
        return self._player_ID

    def get_board(self):
        """Returns the player's board"""
        return self._board

    def set_board(self, player_board):
        """Sets the player's board (only called during initial player creation"""
        self._board = player_board

    def get_p_counter(self):
        """Returns the P token counter"""
        return self._p_counter

    def set_p_counter(self, steps):
        """Adds to the P token counter (use negative values for kicking)"""
        self._p_counter += steps

    def get_q_counter(self):
        """Returns the Q token counter"""
        return self._q_counter

    def set_q_counter(self, steps):
        """Adds to the Q token counter (use negative values for kicking)"""
        self._q_counter += steps

    def get_p_position(self):
        """Returns the position of the player's P token on that player's board"""
        board = self.get_board()
        p_counter = self.get_p_counter()
        return board[p_counter]

    def get_q_position(self):
        """Returns the position of the player's Q token on that player's board"""
        board = self.get_board()
        q_counter = self.get_q_counter()
        return board[q_counter]

    def clear_p_counter(self): # for use in bounce function
        """Used when kicking a piece. Resets the P token's counter and sends the piece back to Home Yard"""
        current_p_position = self.get_p_counter()
        self.set_p_counter(-1 * current_p_position)
        self.set_p_counter(-1)

    def clear_q_counter(self): # for use in bounce function
        """Used when kicking a piece. Resets the Q token's counter and sends the piece back to Home Yard"""
        current_q_position = self.get_q_counter()
        self.set_q_counter(-1 * current_q_position)
        self.set_q_counter(-1)

    def get_pieces_stacked(self):
        """Gets if pieces are stacked or not"""
        return self._pieces_stacked

    def set_pieces_stacked(self, Boolean):
        """Resets pieces to be unstacked"""
        self._pieces_stacked = Boolean

    def get_completed(self):
        """Returns completion status for player: False means player is still playing; True means player is done"""
        return self._completion_status

    def set_completed(self): # no conditions where a player would go from True to False
        if self.get_completed() == False:
            self._completion_status = True

    def get_space_name(self, steps):
        """Returns space name, given steps have been distributed to a particular token"""
        if steps < 58:
            player_board = self.get_board()
            token_space = player_board[steps]
            return token_space

    def get_token_p_step_count(self):
        """Returns the total steps token P has taken"""
        return self.get_p_counter()

    def get_token_q_step_count(self):
        """Returns the total steps token Q has taken"""
        return self.get_q_counter()
    # getters and setters----------------------------------------------------------------------------------------------

    # bounce logic-----------------------------------------------------------------------------------------------------
    def bounce_p_token(self):
        """If a token is bounced, this function is called, which bounces the
        p piece back to the Home Yard and unstacks the pieces"""
        if self.get_p_counter() < 51:
            self.clear_p_counter()
            self.set_pieces_stacked(False)

    def bounce_q_token(self):
        """If a token is bounced, this function is called, which bounces the
        q piece back to the Home Yard and unstacks the pieces"""
        if self.get_q_counter() < 51: # can't kick if tokens are in home squares
            self.clear_q_counter()
            self.set_pieces_stacked(False)
    # bounce logic-----------------------------------------------------------------------------------------------------

class LudoGame:
    """Produces LudoGame objects. LudoGame object represents the game as played"""

    def __init__(self):
        """
        Initializes list, which includes all player objects representing players playing a game of Ludo
        This list is where all of the information for later in the class will come from
        """
        self._player_objects = []  # list should store player objects, not strings/player IDs
        self._player_IDs = [] # for less convoluted reference for some functions

    def get_players(self):
        """"Returns the list of players for use in other functions"""
        return self._player_objects

    def set_players(self, new_player):
        """"Adds a new player to the list of players in a Ludo game"""
        self._player_objects.append(new_player)

    def set_player_IDs(self, new_player):
        """Adds new player's ID to the Player_IDs list"""
        self._player_IDs.append(new_player.get_player_ID())

    def play_game(self, player_IDs, turns):
        """Plays game of Ludo. This function adds the players (represented using Player objects) to the game.
        Then it runs an algorithm to determine which pieces are moved."""
        boards = Board()
        board_A = boards.get_A_board()
        board_B = boards.get_B_board()
        board_C = boards.get_C_board()
        board_D = boards.get_D_board()
        # player creation----------------------------------------------------------------------------------------------
        for player_ID in player_IDs:
            if player_ID in self.get_players():
                return
            elif player_ID not in ('A', 'B', 'C', 'D'):
                return
            else:
                new_player = Player(player_ID)
                if new_player.get_player_ID() == 'A':
                    new_player.set_board(board_A)
                elif new_player.get_player_ID() == 'B':
                    new_player.set_board(board_B)
                elif new_player.get_player_ID() == 'C':
                    new_player.set_board(board_C)
                elif new_player.get_player_ID() == 'D':
                    new_player.set_board(board_D)
                self.set_players(new_player) # appends the new player to the player objects list
                self.set_player_IDs(new_player) # appends the new player's ID to the list of player IDs
        # player creation----------------------------------------------------------------------------------------------

        # move logic----------------------------------------------------------------------------------------------------
        if len(turns) == 0:
            self.get_player_by_position('X')
        for turn in turns:  # turns is the list of tuples input each game
            turn_0 = str(turn[0])
            player_moving = self.get_player_by_position(turn_0)
            move = turn[1]  # this is the number part of the tuple. used to change positions of tokens
            p_counter = player_moving.get_p_counter()
            q_counter = player_moving.get_q_counter()
            projected_p_counter = p_counter + move
            projected_q_counter = q_counter + move
            if -1 < projected_p_counter < 58: # this shouldn't fire if this is true anyway, so this catch should suffice
                projected_p_position = player_moving.get_space_name(projected_p_counter)
            if -1 < projected_q_counter < 58:
                projected_q_position = player_moving.get_space_name(projected_q_counter)
            # print('turn:', turn)
            can_kick = True
            # CONDITION 1
            if p_counter == 57 and q_counter == 57:
                player_moving.set_completed()
            if player_moving.get_completed() is False:
                if move == 6 and p_counter == -1 or move == 6 and q_counter == -1:  # if at least one piece is at home, both are not stacked, so don't need IF STACKED logic
                    if p_counter == -1:
                        player_moving.set_p_counter(1)
                    elif q_counter == -1:
                        player_moving.set_q_counter(1)
                elif p_counter != -1 and q_counter != -1 and \
                        p_counter != 0 and q_counter != 0 and p_counter == q_counter \
                        and projected_p_counter < 58 and projected_q_counter < 58:
                    player_moving.set_pieces_stacked(True)
                    player_moving.set_p_counter(move)
                    player_moving.set_q_counter(move)
                elif projected_p_counter == 57:
                    player_moving.set_p_counter(move)
                elif projected_q_counter == 57:
                    player_moving.set_q_counter(move)
                else:
                    # kick logic------------------------------------------------------------------------------------------
                    for opponent in self.get_players():
                        if opponent.get_player_ID() != player_moving.get_player_ID():
                            if projected_p_position == opponent.get_space_name(opponent.get_p_counter()) and \
                                    0 < opponent.get_p_counter() < 51 and 0 < p_counter < 51: # p kicks p
                                player_moving.set_p_counter(move)
                                if opponent.get_pieces_stacked():
                                    opponent.bounce_p_token()
                                    opponent.bounce_q_token()
                                else:
                                    opponent.bounce_p_token()
                            elif projected_p_position == opponent.get_space_name(opponent.get_q_counter()) and \
                                    0 < opponent.get_q_counter() < 51 and 0 < p_counter < 51: # p kicks q
                                player_moving.set_p_counter(move)
                                if opponent.get_pieces_stacked():
                                    opponent.bounce_p_token()
                                    opponent.bounce_q_token()
                                else:
                                    opponent.bounce_q_token()
                            elif projected_q_position == opponent.get_space_name(opponent.get_p_counter()) and \
                                    0 < opponent.get_p_counter() < 51 and 0 < q_counter < 51: # q kicks p
                                player_moving.set_q_counter(move)
                                if opponent.get_pieces_stacked():
                                    opponent.bounce_p_token()
                                    opponent.bounce_q_token()
                                else:
                                    opponent.bounce_p_token()
                            elif projected_q_position == opponent.get_space_name(opponent.get_q_counter()) and \
                                    0 < opponent.get_q_counter() < 51 and 0 < q_counter < 51: # q kicks q
                                player_moving.set_q_counter(move)
                                if opponent.get_pieces_stacked():
                                    opponent.bounce_p_token()
                                    opponent.bounce_q_token()
                                else:
                                    opponent.bounce_q_token()
                            else:
                                can_kick = False
                    # kick logic----------------------------------------------------------------------------------------
                if can_kick == False:
                    if projected_p_counter > 57 and projected_q_counter < 58 and q_counter > -1:
                        player_moving.set_q_counter(move)
                    elif projected_p_counter < 58 and projected_q_counter > 57 and p_counter > -1:
                        player_moving.set_p_counter(move)
                    elif projected_p_counter > 57 and projected_p_counter > 57 and p_counter > -1:
                        bounce = -1 * (move - (58 - p_counter))
                        player_moving.set_p_counter(bounce)
                    elif player_moving.get_p_counter() > player_moving.get_q_counter():
                        if player_moving.get_q_counter() == -1:
                            player_moving.set_p_counter(move)
                        else:
                            player_moving.set_q_counter(move)
                    elif p_counter < q_counter:
                        if p_counter > -1:
                            player_moving.set_p_counter(move)
                        else:
                            player_moving.set_q_counter(move)

    # position return--------------------------------------------------------------------------------------------------
        final_list = []
        for player_to_return in self.get_players():
            p_final_pos = player_to_return.get_p_counter()
            q_final_pos = player_to_return.get_q_counter()
            final_list.append(player_to_return.get_space_name(p_final_pos))
            final_list.append(player_to_return.get_space_name(q_final_pos))
        return final_list
    # position return---------------------------------------------------------------------------------------------------

    # player return------------------------------------------------------------------------------------------------
    def get_player_by_position(self, player_ID):
        """Returns the player object that has the input ID"""
        players = self.get_players()
        if player_ID not in ('A', 'B', 'C', 'D') or player_ID == None or players == None:
            return "Player not found!"
        for player in players:
            if player_ID == player.get_player_ID():
                return player
    # player return-----------------------------------------------------------------------------------------------
