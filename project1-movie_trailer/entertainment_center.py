import media
import fresh_tomatoes

#create several instances of movies that will be displayed

#__init__(self, title, poster_art, trailer_link, lead_star, director):
Interstellar = media.Movie("Interstellar",
							"http://upload.wikimedia.org/wikipedia/en/thumb/b/bc/Interstellar_film_poster.jpg/220px-Interstellar_film_poster.jpg",
							"https://www.youtube.com/watch?v=zSWdZVtXT7E",
							"Matthew McConaughey",
							"Christopher Nolan")
							
Kingsman = media.Movie("Kingsman: The Secret Service",
						"http://upload.wikimedia.org/wikipedia/en/thumb/8/8b/Kingsman_The_Secret_Service_poster.jpg/220px-Kingsman_The_Secret_Service_poster.jpg",
						"www.youtube.com/watch?v=xkX8jKeKUEA",
						"Colin Firth",
						"Matthew Vaughn")

Avengers_Ultron = media.Movie("Avengers: Age of Ultron",
								"http://upload.wikimedia.org/wikipedia/en/thumb/1/1b/Avengers_Age_of_Ultron.jpg/220px-Avengers_Age_of_Ultron.jpg",
								"www.youtube.com/watch?v=JAUoeqvedMo",
								"Robert Downey Jr.",
								"Joss Whedon")


movies = [Interstellar, Kingsman, Avengers_Ultron]


#print movies[0].title, '\n', movies[0].trailer_youtube_url, '\n',
#	movies[0].lead_star, '\n',movies[0].director

#movies[0].show_trailer()


fresh_tomatoes.open_movies_page(movies)
