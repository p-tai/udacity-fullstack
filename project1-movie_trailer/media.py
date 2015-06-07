"""media.py:

Media class details
"""

#Globals, aren't used though
MOVIE = "Movie"
BOOK = "Book"

"""Media constructor

Attributes are self-explanatory
"""
class Media(object):
	def __init__(self, title, poster_art, media_type=None, detailed=False):
		self.title=title
		self.poster_image_url = poster_art
		self.detailed = detailed
		self.type = type

"""Movie constructor

Attributes are self-explanatory
Subclass of Media
"""
class Movie(Media):
	def __init__(self, title, poster_art, trailer_link, lead_star, director):
		self.trailer_youtube_url = trailer_link
		self.lead_star = lead_star
		self.director = director
		super(Movie,self).__init__(title, poster_art, media_type=MOVIE, detailed=True)	

"""Book constructor

Attributes are self-explanatory
Subclass of Media
(Not used)
"""
class Book(Media):
	#book constructor
	def __init__(self, title, box_art, author):
		self.author = author
		self.__init__(title, box_art, media_type=BOOK, detailed=True)
