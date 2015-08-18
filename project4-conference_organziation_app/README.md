Author: Paul Tai
Udacity Fullstack Nanodegree Project 4
Conference Organization Application
Based on source-code available at https://github.com/udacity/ud858

TODO list
Add Sessions to a Conference
    Define the following endpoint methods
    getConferenceSessions(websafeConferenceKey) -- Given a conference, return all sessions
    getConferenceSessionsByType(websafeConferenceKey, typeOfSession) Given a conference, return all sessions of a specified type (eg lecture, keynote, workshop)
    getSessionsBySpeaker(speaker) -- Given a speaker, return all sessions given by this particular speaker, across all conferences
    createSession(SessionForm, websafeConferenceKey) -- open to the organizer of the conference

Define Session class and SessionForm
    Session name
    highlights
    speaker
    duration
    typeOfSession
    date
    start time (in 24 hour notation so it can be ordered).
    
Add Sessions to User Wishlist

Define the following Endpoints methods
    addSessionToWishlist(SessionKey) -- adds the session to the user's list of sessions they are interested in attending
    getSessionsInWishlist() -- query for all the sessions in a conference that the user is interested in

Work on indexes and queries

Create indexes
    Come up with 2 additional queries
    Solve the following query related problem: Let’s say that you don't like workshops and you don't like sessions after 7 pm. How would you handle a query for all non-workshop sessions before 7 pm? What is the problem for implementing this query? What ways to solve it did you think of?
Add a Task
Define the following endpoints method: getFeaturedSpeaker()
