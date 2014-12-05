import webapp2 
import hotel
 
urls = [(r'/', hotel.MainPage), (r'/submit', hotel.SecondPage),
        (r'/delete/(.*)', hotel.delete ),(r'/listreviews', hotel.hotel_list),
        (r'/display/(.*)', hotel.display),(r'/sortnum/(.*)', hotel.sort_num),(r'/sortdate/(.*)', hotel.sort_date)] 
 
app = webapp2.WSGIApplication(urls, debug=True) 



