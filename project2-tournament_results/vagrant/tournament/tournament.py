#!/usr/bin/env python

"""
tournament.py -- implementation of a Swiss-system tournament.
This python program \will connect to PostgreSQL database
named tournament to perform any database updates.
"""

import psycopg2
from random import randrange


def connect():
    """Connect to the PostgreSQL database named 'tournament'.

    Returns a database connection and command cursor.
    """
    # Connect to the tournament database.
    try:
        connection = psycopg2.connect("dbname=tournament")
    except:
        print("Error attempting to connect to tournament database.")
        return

    # Open cursor which will be used to execute commands.
    try:
        cursor = connection.cursor()
        return cursor, connection
    except:
        print("Error attempting to create command cursor.")


def runCommand(command, params=None):
    """Runs the given query command.  Returns the results, if any.

    Args:
      command:  the operation that will be executed
      params:  iterable containing variables needed for the operation
    """
    # Connect to the database.
    cursor, connection = connect()

    # Execute the given command, using the paramaters if given.
    if params:
        cursor.execute(command, tuple(_ for _ in params))
    else:
        cursor.execute(command)

    # Check if there are any results.
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

    # Return the operation's results.
    return result


def deleteMatches():
    """Remove all the match records from the database."""
    command = "TRUNCATE Matches CASCADE;"
    runCommand(command)


def deletePlayers():
    """Remove all the player records from the database."""
    command = "TRUNCATE Players CASCADE;"
    runCommand(command)


def countPlayers():
    """Returns the number of players currently registered."""
    command = "SELECT * FROM PlayerCount;"
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
    runCommand(command, params=(name,))


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or
    a player tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """

    # Get all the IDs and names of players in the database.
    command = "SELECT " + \
              "Players.P_Id, " + \
              "Players.name, " + \
              "SUM(CAST(Matches.WonGame as INT)) as Wins, " + \
              "Count(Matches.P_Id_1) as Matches " + \
              "FROM Players " + \
              "LEFT JOIN Matches " + \
              "ON Players.P_Id = Matches.P_Id_1 " + \
              "GROUP BY Players.P_Id " + \
              "ORDER BY Wins DESC;"
    result = runCommand(command)

    # In case the table was empty, check for a result before returning.
    if result is None:
        return None

    # Create a placeholder for the resulting list.
    players = []

    # Iterate through all the players and check the values.
    for player in result:

        # Unpack the result row,
        p_id, name, wins, matches = player

        # Reformat the values for wins/matches if None for consistency.
        if wins is None:
            wins = 0
        if matches is None:
            matches = 0

        # Add this player to the result.
        players.append((p_id, name, wins, matches))

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
    params1 = (winner, loser)

    command2 = "INSERT INTO Matches (P_Id_1, P_Id_2, WonGame, Draw)" + \
               " VALUES (%s, %s, '0', '0');"
    params2 = (loser, winner)

    # Run commands and check for duplicates; rematches are not permitted.
    try:
        runCommand(command1, params=params1)
        runCommand(command2, params=params2)
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
        # Randomly pick a player to receive a Bye round.
        extra = standings.pop(randrange(len(standings)))

        # Unpack and repack the id and name.
        pairings.append(extra[0], extra[1], -1, "BYE")

    # Unpack and repack the id and name.
    player_1_ids, player_1_names, _, _ = zip(*standings[::2])
    player_2_ids, player_2_names, _, _ = zip(*standings[1::2])
    pairings = zip(player_1_ids, player_1_names,
                   player_2_ids, player_2_names)

    return pairings
