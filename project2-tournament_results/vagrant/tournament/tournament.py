#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
from random import randrange

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")

def runCommand(command, params = None):
    """Runs the given query command.  Returns the results, if any.
    
    Args:
      command:  the operation that will be executed
      params:  the variables needed for the operation to run
    """
    # Connect to the database.
    connection = connect()
    
    # Open cursor to perform operations.
    cursor = connection.cursor()
    
    # Execute the given command and check if there are any results.
    if params:        
        cursor.execute(command, tuple(_ for _ in params))
    else:
        cursor.execute(command)
    result = None
    try:
        result = cursor.fetchall()
    except psycopg2.ProgrammingError:
        pass
        
    # Make any changes permanent.
    connection.commit()
    
    # Cleanup the cursor and connection.
    cursor.close()
    connection.close()
    
    # Return the operation's results, if there were any.
    return result

def deleteMatches():
    """Remove all the match records from the database."""
    command = "DELETE FROM Matches;"
    runCommand(command)


def deletePlayers():
    """Remove all the player records from the database."""
    command = "DELETE FROM Players;"
    runCommand(command)


def countPlayers():
    """Returns the number of players currently registered."""
    command = "SELECT COUNT(P_Id) FROM Players;"
    result = runCommand(command)
    
    # In case the table was empty, check for a result before returning.
    if result:
        return result[0][0]
    else:
        return 0

def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    
    # If there are any ' characters, re-format the name for the query.
    if "'" in name:
        temp = ""
        for char in name:
            if char == "'":
                temp += "'"
            temp += char
        name = temp
    
    command = "INSERT INTO Players (name) VALUES (%s);"
    runCommand(command, params = (name,))


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    
    # Get all the IDs of players in the database.
    command = "SELECT " +\
                "Players.P_Id, Players.name, " + \
                "SUM(CAST(Matches.WonGame as INT)) as Wins, " + \
                "Count(Matches.P_Id_1) as Matches " + \
              "FROM Players " + \
              "LEFT JOIN Matches " + \
                "ON Players.P_Id = Matches.P_Id_1 " + \
              "GROUP BY Players.P_Id " + \
              "ORDER BY Wins DESC;"
    result = runCommand(command)
    
    # In case the table was empty, check for a result before returning.
    if result == None:
        return None
        
    # Create a placeholder for the resulting list.
    players = []
    
    # Iterate through all the players and check the values.
    for player in result:
        
        # Unpack the result row,
        P_id, name, wins, matches = player
        
        # Reformat the values for wins/matches if None for consistency.
        if wins == None:
            wins = 0
        if matches == None:
            matches = 0
        
        # Add this player to the result.
        players.append((P_id, name, wins, matches))

    return players
        
            


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    # Insert the match into the database, in both pair orders.
    command1 = "INSERT INTO Matches (P_Id_1, P_Id_2, WonGame, Draw)" + \
              " VALUES (%s, %s, '1', '0');"
    params1 =  (winner, loser)
    
    command2 = "INSERT INTO Matches (P_Id_1, P_Id_2, WonGame, Draw)" + \
              " VALUES (%s, %s, '0', '0');"
    params2 = (loser, winner)
    
    # Run the commands and check for duplicates: Rematches not permitted
    try: 
        runCommand(command1, params = params1)
        runCommand(command2, params = params2)
    except psycopg2.IntegrityError:
        err = "Error: Duplicate entry for players: (%s %s)." % (winner, loser)
        print(err)
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    # Get the ranks of all the players, ordered by win count.
    standings = playerStandings()
    
    # List to store the resulting pairings.
    pairings = []
    
    # Check for an odd number of players.
    if(len(standings) % 2 != 0):
        # Randomly take one of the players out to get a bye
        extra = standings.pop(randrange(len(standings)))
        
        # Unpack and repack the id and name.
        extra = (extra[0], extra[1])
        pairings.append((extra, "BYE"))
    
    # Iterate through the remaining players, matching players together.
    i = 0
    while i < len(standings)-1:
        # Unpack and repack the id and name.
        player_1 = standings[i]
        player_2 = standings[i+1]
        pairings.append((player_1[0], player_1[1], \
                        player_2[0], player_2[1]))
        i += 2
    
    return pairings

