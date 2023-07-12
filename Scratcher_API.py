import requests
from flask import Flask, jsonify, request
import re
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from mysql.connector import MySQLConnection, Error
from selenium.common.exceptions import StaleElementReferenceException
from flask_cors import CORS

import mysql.connector

app = Flask(__name__)
CORS(app) 



# Establishes a connection with CA Lottery website, uses Solenium to cycle pages and scratchers, 
# and Beautiful Soup to parse for info
def retrieve_scratcher():

    #initalize webdriver
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    options.page_load_strategy = 'eager'
    options.add_argument('--headless=new')
    driver = webdriver.Chrome(options=options)

    
    driver.get("https://www.calottery.com/scratchers")

    scratcher_info = []

    for i in range(2, 7):
          
        
        #Find page buttons
        pages = driver.find_elements(By.CLASS_NAME, "page-link")

        #initialize BeautifulSoup, find links to all scratcher pages
        main_page = driver.page_source
        soup = BeautifulSoup(main_page, 'html.parser')
        results = soup.find(id="scratchers-results")
        cards = results.find_all("a", href=True)


        #Scrape the URL for each scratcher
        for card in cards:
            href = card.get("href")
            try:
                #find scratcher info and add it to list
                scratcher_info.append(get_info("https://www.calottery.com" + href))
            except Exception as e:
                print(e)
                continue

    
        

        
        driver.execute_script("arguments[0].click();", pages[i])

        #wait for page to load
        time.sleep(1)

    driver.close()

    #insert scratcher info into MySQL table

    sql = "INSERT INTO scratchers (scratcher_name, price, odds, Top_Prize, Top_Prizes_left, Top_Prize_Odds, img_source) " \
      "VALUES (%s, %s, %s, %s, %s, %s, %s) " \
      "ON DUPLICATE KEY UPDATE odds = VALUES(odds), " \
      "Top_Prizes_left = VALUES(Top_Prizes_left), " \
      "Top_Prize_Odds = VALUES(Top_Prize_Odds)"
    
    cnx = mysql.connector.connect(
        host='localhost',
        user='root',
        password='12345',
        database='scratchers'
    )

    #connect to server
    if cnx.is_connected():
        print('Connected to MySQL server')

    cursor = cnx.cursor()

    #Execute query
    cursor.executemany(sql, scratcher_info)

    cnx.commit()

    cursor.close()
    cnx.close()     

   #print(scratcher_info)


#Scrapes scratcher page for info, such as odds, name, price, prizes, and img source
def get_info(URL):
    
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, 'html.parser')

    results = soup.find(id="content")

    #Retrieve name
    scratcher_name = results.find("h1", class_="page-title--text field-title")
    print(scratcher_name.text)
  

    #Retrieve odds
    odds = results.find("p", class_="scratchers-game-detail__info-feature-item scratchers-game-detail__info-feature-item--cash-odds")
    
    odds_string = str(odds.text)

    colon_index = odds_string.index(":")
    substring = odds_string[colon_index + 1:].strip()

    #Parse integer from statement
    parts = substring.split("in")

    # Turn odds string into decimal
    integer_part = parts[0].strip()
    float_part = parts[1].strip()

    integer_value = int(integer_part)
    float_value = float(float_part)

    #Odds in decimal form
    decimal_result = integer_value / float_value

    print("Odds: " + str(decimal_result))

   
    #Retrieve Top Prize, Top Prize Odds, Top Prizes Left 

    prize = results.find("tr", class_="odds-available-prizes__table__body")

    #Parse lines for relevant information
    lines = prize.text.splitlines()
    print("Top prize: $" + lines[1])
    prize_num = int(''.join(filter(str.isdigit, lines[1])))

    print("Top Prize Odds: 1 in " + str(lines[2]))
    match = re.search(r'\d+', lines[4])

    if match:
        first_number = int(match.group())

    print("Top prizes left: " + str(first_number))

    #Retrieve Image Source
    img = results.find("img", class_="scratchers-game-detail__card-img scratchers-game-detail__card-img--unscratched")
    
    src = img.get("src")
    print("Image source: " + str(src))

    #Retrieve Price
    price = results.find("p", class_="scratchers-game-detail__info-price")
    price_str = str(price.text)

    colon_index = price_str.index("$")
    substring = price_str[colon_index + 1:].strip()

    print("Price: $" + str(substring))
    print("")
    return (scratcher_name.text, substring, decimal_result, prize_num, first_number,  lines[2], src)

#API call will return scratchers with best odds at requested price point



@app.route('/api/scratchers/best-odds', methods=['GET'])
def get_scratcher_with_best_odds():
    try:
        
        scratcher_best_odds = []
        # Get the price point from the query parameters

        prices = request.args.get('prices').split(',')
        # Establish a connection to the MySQL server
        cnx = mysql.connector.connect(
            host='localhost',
            user='root',
            password='12345',
            database='scratchers'
        )
        # Create a cursor object    
        cursor = cnx.cursor()
        print(prices)

        # Execute a SELECT query to fetch the scratcher with the best odds at the specified price point
        for price in prices:
            query = "SELECT * FROM scratchers WHERE price = %s ORDER BY odds DESC LIMIT 1"
            cursor.execute(query, (price,))

            # Fetch the row of the result
            row = cursor.fetchone()

        # Check if a scratcher was found at the specified price point
            if row is not None:
                scratcher_best_odds.append({
                    'scratcher_name': row[0],
                    'price': row[1],
                    'odds': row[2],
                    'Top_Prize': row[3],
                    'Top_Prizes_Left': row[4],
                    'Top_Prize_Odds': row[5],
                    'img_source': row[6],
                })
        cursor.close()
        cnx.close()
        print(scratcher_best_odds)
        return jsonify(scratcher_best_odds), 200

    except mysql.connector.Error as err:
        # Handle MySQL errors and return appropriate error code and message
        error_message = "There was an error retrieving scratcher data from MySQL database"
        return jsonify({'error': error_message}), 500

    except Exception as e:
        # Handle other unexpected exceptions and return a generic error response
        err = "error"
        return jsonify({'An error occurred': err}), 500


#Retrieve MySQL scratcher table
@app.route('/api/scratchers', methods=['GET'])
def get_scratchers():
    try:
        app = Flask(__name__)

        cnx = mysql.connector.connect(
            host='localhost',
            user='root',
            password='12345',
            database='scratchers'
        )
        
        # Create a cursor object
        cursor = cnx.cursor()
        
        # Execute a SELECT query to fetch data from the table
        query = "SELECT * FROM scratchers"
        cursor.execute(query)
        
        # Fetch all rows of the result
        rows = cursor.fetchall()
        
        # Convert the rows to a list of dictionaries
        data = []
        for row in rows:
            data.append({
                'scratcher_name': row[0],
                'price': row[1],
                'odds': row[2],
                'Top_Prize': row[3],
                'Top_Prizes_Left': row[4],
                'Top_Prize_Odds': row[5],
                'img_source': row[6],
            })
        
        # Close the cursor and connection
        cursor.close()
        cnx.close()

        print(data)
        
        # Return the data as JSON
        return jsonify(data), 200

    except mysql.connector.Error as err:
        # Handle MySQL errors and return appropriate error code and message
        error_message = "There was an error retrieving scratcher data from MySQL database"
        return jsonify({'error': error_message}), 500

    except Exception as e:
        # Handle other unexpected exceptions and return a generic error response
        return jsonify({'error': 'An error occurred.'}), 500
    


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    # Return a custom error response for the undefined routes
    return jsonify({'error': 'Route not found'}), 404


app.run()
