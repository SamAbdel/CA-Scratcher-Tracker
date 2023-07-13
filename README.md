# CA-Scratcher-Tracker

CA Lottery Scratcher Tracker

This application includes uses a MySQL server, a Python RESTful API using Flask, and a frontend developed in ReactJs. 

The objective of this project is to sample data regarding California Lottery Scratchers from the official CA Lottery website. This includes info for each scratcher including price, name, odds, top prize, and more relevant information. This data is then displayed in a ReactJs application for easy viewing of both the scratchers with the best odds, as well as all possible scratchers.

The data was sampled from CA Lottery using BeautifulSoup and Selenium, and this data was then added into a SQL database using MySQL. This database could then be requested through the Flask API. In addition, the API allows applications to request the information for the scratcher with the best odds at requested prices.

This API was then used to create a ReactJs application to display the data in a user-friendly format, including a sortable table and search function.
