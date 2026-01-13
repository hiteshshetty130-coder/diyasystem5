import requests
from bs4 import BeautifulSoup
import lxml
import pandas as pd
import logging

logging.basicConfig(level = logging.INFO)

class User_story_5():
    def scrap_sub_categories(self):
        try:
            url = "http://books.toscrape.com/"  # web scrapper url
            r = requests.get(url)
            response=r.text
            soup = BeautifulSoup(response,"lxml")
            sub_categories = {}
            for category in soup.select("div.side_categories ul li ul li a"):
                category_text = category.text.strip()
                sub_categories[category_text] = url+category["href"]
            return sub_categories
        
        except Exception as e:
            logging.warning("Unexcepted error!!",e)
    

    def books_tier(self,price):
        if price < 26.40:
            return "Budget"
        elif price >= 26.40 and price <= 66.00:
            return "Standard"
        else:
            return "premium"

    
    def scrap_books(self,sub,url):
        all_books = []
        rating_data = {"One":1,
                       "Two":2,
                       "Three":3,
                       "Four":4,
                       "Five":5}
        try:
            while url:
                response = requests.get(url)
                soup = BeautifulSoup(response.text,"lxml")
        
                for books in soup.select("article.product_pod"):
                    title = books.h3.a["title"]
                    price = books.select_one("p.price_color").text
                    price = float(price.replace("Â£",""))
                    price = price*1.32
                    book_tier = self.books_tier(price)
                    availability = books.select_one("p.availability").text.strip()
                    rating_list = books.select_one("p.star-rating")["class"]
                    rating_class = [c for c in rating_list if c!="star-rating"][0]
                    rating = rating_data[rating_class]
                    category_list = soup.select("ul.breadcrumb li a")
                    category = category_list[1].text.strip()
                

                    product_url = books.h3.a["href"]
                    all_books.append({"title":title,
                                "price":price,
                                "Book_tier":book_tier,
                                "category":category,
                                "sub_category":sub,
                                "rating":rating,
                                "availability":availability,
                                "product_url":product_url                  
                })

                #pagination
                next_page = soup.select_one("li.next a")
                if next_page:
                    href = next_page["href"]
                    base_path = url.rsplit("/",1)[0]
                    url = base_path + "/" + href
                else:
                    break

            return all_books
        
        except Exception as er:
            logging.warning("Sorry Unexcepted error occured!!",er)

def main():
    books = []
    us = User_story_5()
    result = us.scrap_sub_categories()
    for sub,url in result.items():
        ex_books = us.scrap_books(sub,url)
        books.extend(ex_books)

    df = pd.DataFrame(books)
    df.to_excel("books_data.xlsx")
    logging.info("\n%s",df)
    

if __name__=="__main__":
    main()
