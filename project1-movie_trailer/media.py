"""
media.py:

This file contains the Media, Movie, and Book class details.
"""

#Globals to represent object type.
MOVIE = "Movie"
BOOK = "Book"


class Media(object):
	"""
	Media constructor
	
	Attributes are self-explanatory
	"""
	
	def __init__(self, title, poster_art, media_type=None, detailed=False):
		self.title=title
		self.poster_image_url = poster_art
		self.detailed = detailed
		self.type = type


class Movie(Media):
	"""
	Movie constructor
	
	Attributes are self-explanatory
	Subclass of Media
	"""
	
	def __init__(self, title, poster_art, trailer_link, lead_star, director):
		self.trailer_youtube_url = trailer_link
		self.lead_star = lead_star
		self.director = director
		super(Movie,self).__init__(title, poster_art, media_type=MOVIE, detailed=True)	


class Book(Media):
	"""
	Book constructor

	Attributes are self-explanatory
	Subclass of Media
	(Not used in this version)
	"""
	
	def __init__(self, title, box_art, author):
		self.author = author
		self.__init__(title, box_art, media_type=BOOK, detailed=True)
