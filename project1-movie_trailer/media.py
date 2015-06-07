#Media class details
import webbrowser

MOVIE = "Movie"
BOOK = "Book"

class Media(object):
	#basic constructor for a media object
	def __init__(self, title, poster_art, media_type=None, detailed=False):
		self.title=title
		self.poster_image_url = poster_art
		self.detailed = detailed
		self.type = type

#movie constructor, attributes are self-explanatory
class Movie(Media):
	def __init__(self, title, poster_art, trailer_link, lead_star, director):
		self.trailer_youtube_url = trailer_link
		self.lead_star = lead_star
		self.director = director
		super(Movie,self).__init__(title, poster_art, media_type=MOVIE, detailed=True)	
		
	#Function to open the browser and show the youtube trailer
	def show_trailer(self):
		webbrowser.open(self.trailer_youtube_url)

#book constructor, not used
#attributes are self-explanatory
class Book(Media):
	#book constructor
	def __init__(self, title, box_art, author):
		self.author = author
		self.__init__(title, box_art, media_type=BOOK, detailed=True)
