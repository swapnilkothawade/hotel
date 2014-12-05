import jinja2
import os
import models
import webapp2
from google.appengine.ext import db

JE = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

#defining class called MainPage
class MainPage(webapp2.RequestHandler):
    # defining single argument
    def get(self):
        # fetching reviews from datastore
        q = db.GqlQuery("SELECT * FROM Review")
        # generating template
        template = JE.get_template('templates/index.html')
        # creating dictionary called context
        context = {
            'reviews': q,
        }
        # render response
        self.response.write(template.render(context))

#defining class called SecondPage
class SecondPage(webapp2.RequestHandler):
    # defining single argument
    def post(self):
        #calling the data from datastore and storing it in a variable
        review = models.Review()
        # fetching requested data
        review.hotel_name = self.request.get('hotel_name')
        review.content = self.request.get('content')
        review.numeric_rating = self.request.get('numeric_rating')
        
        # validating requested data
        error_message = ""
        message = ""
        messageerror = ""
        x = review.content
        word1 = len(x.split())
        y = review.hotel_name
        word2 = len(y.split())
        if word2<1:
            error_message= "Hotel name has to be a word!! Enter Again"
            # generate response page containing all the data as in the get request
            # including the error message
        elif word1<1:
            message="Word count for review less than 1!! Enter Again"
        elif word2<1 and word1<1:
            messageerror="Both the fields are empty!! Enter Again" 
        else:
            review.put()
        # fetching reviews from datastore    
        all_reviews = db.GqlQuery("SELECT * FROM Review")
        # generating template
        template = JE.get_template('templates/index.html')
         #creating dictionary called context
        context = {
            'reviews': all_reviews,
            'error_message': error_message,
            'word2': word2,
            'word1': word1,
            'message': message,
            'messageerror': messageerror,
        }    
        # render response
        self.response.write(template.render(context))

#defining class called delete
class delete(webapp2.RequestHandler):
    def get(self, id=None):
        #function get_by_id retrieves the object specifically
        d = models.Review.get_by_id(long(id))
        #delete review by ID
        d.delete()
        #redirecting it to the mainpage
        self.redirect('/')

#defining class called display
class display(webapp2.RequestHandler):
    #defining two arguments
    def get(self,hotelname):
        hotelName = hotelname
        bb = db.GqlQuery("SELECT * FROM Review WHERE hotel_name = :hotelNamez ", hotelNamez = hotelName )

        #make cumulative as float
        cumulative = 0.0
        #initialize counter to 0
        counter = 0
        #checking for the hotelname
        for rev in bb:
            #increment counter by 1
            counter +=1
            #adding all the rating
            cumulative = cumulative + int(rev.numeric_rating)

        #dividing cumulative bt counter
        cumulative = cumulative / counter
        #roundiung upto 2 decimal places
        round_cumulative = round(cumulative, 2)        
        # generating template
        template = JE.get_template('templates/display.html')
        #creating dictionary called context
        context = {
            'reviews': bb,'hotelName':hotelName,'cum_rate':round_cumulative
            }
        # render response
        self.response.write(template.render(context))
        
#defining class called hotel_list
class hotel_list(webapp2.RequestHandler):
    #defining single argument
    def get(self):
        #query filters distinct hotel names
        a = db.GqlQuery("SELECT DISTINCT hotel_name FROM Review")
        #generating template
        template = JE.get_template('templates/listreviews.html')
        #creating dictionary called context
        context = {
            'lists': a,
            }
        # render response
        self.response.write(template.render(context))

#defining class called sort_date
class sort_date(webapp2.RequestHandler):
    #defining two arguments
    def get(self,hotelname):
        hotelName = hotelname
        #query list review for selected hotel by date in descending order
        dd = db.GqlQuery("SELECT * FROM Review WHERE hotel_name = :hotelNamez ORDER BY date DESC", hotelNamez = hotelName )
        #generating template
        template = JE.get_template('templates/sortdate.html')
        #creating dictionary called context
        context = {
            'reviews': dd,'hotelName':hotelName,
            }
        # render response
        self.response.write(template.render(context))

#defining class called sort_num
class sort_num(webapp2.RequestHandler):
    #defining two arguments
    def get(self,hotelname):
        hotelName = hotelname
        #query list review for selected hotel numeric rating in descending order
        dd = db.GqlQuery("SELECT * FROM Review WHERE hotel_name = :hotelNamez ORDER BY numeric_rating DESC", hotelNamez = hotelName )
        #generating template
        template = JE.get_template('templates/sortnum.html')
        #creating dictionary called context
        context = {
            'reviews': dd,'hotelName':hotelName,
            }
        # render response
        self.response.write(template.render(context))

