"""
entertainment_center.py:

This script creates a few instances of movie and then 
calls fresh_tomatoes.open_movies_page(movies).
"""

import media
import fresh_tomatoes

# This code will create several instances of movies that will be displayed.
BASE_URL = "http://upload.wikimedia.org/wikipedia/en/thumb/"
Interstellar = media.Movie(
	"Interstellar",
	BASE_URL + "b/bc/Interstellar_film_poster.jpg/220px-Interstellar_film_poster.jpg",
	"https://www.youtube.com/watch?v=zSWdZVtXT7E",
	"Matthew McConaughey",
	"Christopher Nolan")
							
Kingsman = media.Movie(
	"Kingsman: The Secret Service",
	BASE_URL + "8/8b/Kingsman_The_Secret_Service_poster.jpg/220px-Kingsman_The_Secret_Service_poster.jpg",
	"www.youtube.com/watch?v=xkX8jKeKUEA",
	"Colin Firth",
	"Matthew Vaughn")

Avengers_Ultron = media.Movie(
	"Avengers: Age of Ultron",
	BASE_URL + "1/1b/Avengers_Age_of_Ultron.jpg/220px-Avengers_Age_of_Ultron.jpg",
	"www.youtube.com/watch?v=JAUoeqvedMo",
	"Robert Downey Jr.",
	"Joss Whedon")

# Next, create a list that will be passed to formatter function.
movies = [Interstellar, Kingsman, Avengers_Ultron]

# Funally, call the function that will create an .html file and open it.
fresh_tomatoes.open_movies_page(movies)
