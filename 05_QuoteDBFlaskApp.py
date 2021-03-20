#################################################
# import dependencies
#################################################

from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt
from pandas import DataFrame
import pandas as pd
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify, render_template
from config import password

#################################################
# Database Setup
#################################################
# create engine 
engine = create_engine(f'postgresql://postgres:{password}@localhost:5432/quote_db')
connection = engine.connect()

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
author = Base.classes.author
quote = Base.classes.quote
tag = Base.classes.tag

#################################################
# Flask Setup
#################################################
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

#################################################
# Flask Routes
#################################################
@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html")
    # return (
    #     f"Welcome to Quote Database API!<br/>"
    #     f"Available Routes:<br/><br/>"
    #     f"/quotes<br/>This route will dispaly all the available quotes in the database<br/><br/>"
    #     f"/authors<br/>This route will display the information about all the authors available in the database<br/><br/>"
    #     f"/authors/Mark Twain<br/>This route will display the information about a particular author the user passes in<br/><br/>"
    #     f"/tags<br/>This route will dispaly all the available tags in the database<br/><br/>"
    #     f"/tags/inspirational<br/>This route will display the information about a particual tag the user passes in<br/><br/>"
    #     f"/top10tags<br/>This route will display the information about top10 tags<br/><br/>"
        
    # )

@app.route("/quotes")
def quotes():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    #get list of all quotes
    q_result = session.query(quote.quote, author.name, quote.quote_id).join(author, quote.author_id == author.author_id).all()

    #Loop through quote list to create each quote dictionary
    dict_list = []
    for q, a, i in q_result:
        #query all tags for this quote
        #query returns a list of lists, each tag is a list of 1 item
        #loop through each list of 1 item and append each 1 item to 1 final list (loop_tag_list)
        loop_tag_list = []
        tlists = session.query(tag.tag).filter(tag.quote_id == i).all()
        for t in tlists:
            loop_tag_list.append(t[0])
 
        loop_dict = {}
        loop_dict["text"] = q.replace("\u201c","").replace("\u201d","")
        loop_dict["author name"] = a
        loop_dict["tags"] = loop_tag_list
        
        dict_list.append(loop_dict)

    #Create the outermost dictionary
    outer_dict = {}
    outer_dict["total"] = session.query(func.count(quote.quote_id)).all()[0][0]
    outer_dict["quotes"] = dict_list

    session.close()

    return jsonify(outer_dict)


@app.route("/authors")
def authors():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    #get list of all author data
    a_result = session.query(author.name, author.description, author.born, author.author_id).all()

    #Loop through your author list to create each author's dictionary
    dict_a_list = []
    for nm, d, b, ai in a_result:
        
        #for this loop's author, create dictionary of all their quotes
        q_result = session.query(quote.quote, quote.quote_id).join(author, quote.author_id == author.author_id).filter(quote.author_id == ai).all()
        dict_q_list = []
        for q, i in q_result:
            #query all tags for this quote
            #query returns a list of lists, each tag is a list of 1 item
            #loop through each list of 1 item and append each 1 item to 1 final list (loop_tag_list)
            loop_tag_list = []
            tlists = session.query(tag.tag).filter(tag.quote_id == i).all()
            for t in tlists:
                loop_tag_list.append(t[0])
    
            loop_dict = {}
            loop_dict["text"] = q.replace("\u201c","").replace("\u201d","")
            loop_dict["tags"] = loop_tag_list    

            dict_q_list.append(loop_dict)   
        
        
        #now create the author dictionary, setting quotes to the quote dictionary you created above
        loop_a_dict = {}
        loop_a_dict["name"] = nm
        loop_a_dict["description"] = d
        loop_a_dict["born"] = b
        loop_a_dict["count"] = session.query(func.count(quote.quote_id)).filter(quote.author_id == ai).all()[0][0]
        loop_a_dict["quotes"] = dict_q_list

        dict_a_list.append(loop_a_dict)

    #Create the outermost dictionary
    outer_a_dict = {}
    outer_a_dict["total"] = session.query(func.count(author.author_id)).all()[0][0]
    outer_a_dict["details"] = dict_a_list

    session.close()


    return jsonify(outer_a_dict)

@app.route("/authors/<AuthorName>")
def PassInAuthor(AuthorName):
    session = Session(engine)

    AuthorQuotes = session.query(quote.quote_id, quote.quote).join(author, quote.author_id == author.author_id).filter(author.name == AuthorName).all()
    AuthorInfo = session.query(author.name, author.description, author.born, author.author_id).filter(author.name == AuthorName).all()

    AuthorQuoteList = []
    for qt_ID,qt in AuthorQuotes:
        #query all tags for this quote
        # #query returns a list of lists, each tag is a list of 1 item
        # #loop through each list of 1 item and append each 1 item to 1 final list (loop_tag_list)
        quoteTagList = []
        quoteTags = session.query(tag.tag).filter(tag.quote_id == qt_ID).all()
        for t in quoteTags:
            quoteTagList.append(t[0])
        
        quoteloopDict = {}
        quoteloopDict["text"] = qt.replace("\u201c","").replace("\u201d","")
        quoteloopDict["tags"] = quoteTagList    

        AuthorQuoteList.append(quoteloopDict)
    
    #now create the author dictionary, setting quotes to the quote dictionary you created above
    for nm, d, b, auid in AuthorInfo:
        AuthorDict = {}
        AuthorDict["name"] = nm
        AuthorDict["description"] = d
        AuthorDict["born"] = b
        AuthorDict["number_of_quotes"] = session.query(func.count(quote.quote_id)).filter(quote.author_id == auid).all()[0][0]
        AuthorDict["quotes"] = AuthorQuoteList



    session.close()  

    return jsonify(AuthorDict)

@app.route("/tags")
def tags():
    #session = Session(engine)
​
    t_result = 'This is a test tag'
​
    #session.close()  
​
    return jsonify(t_result)



@app.route("/tags/<tag>")
def PassInTag(tag):
    #session = Session(engine)

    t_result = 'This is a test passed in tag '+tag

    #session.close()  

    return jsonify(t_result)

@app.route("/top10tags")
def top10tags():
    #session = Session(engine)

    t_result = 'This is a test in top10tags'

    #session.close()  

    return jsonify(t_result)

if __name__ == "__main__":
    app.run(debug=True)    