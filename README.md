# Overview

In this program I am trying to accomplish that the idea of implamenting a simple SQL program to store various info about customers between two tables and display info based on what the user wants to see

This software is a customer database. You can input a new customer, modify a customer profile, and delete. All customer records can be displayed. In association with the customers you can input an order and assign it to customer. All orders can be displayed based on the customer ID. The whole program is interacted with through the terminal

The purpose of writting this program is to become more familiar with Python and identify new ways to implament additional languages into my program, which in this case is SQL

# Software Demo Video
Demo video link will be in the page submitted to canvas

# Relational Database
The relational database that I'm using is SQL and sqlite3 that is implamented directly into Python

There's two tables in my program and the structure for both is outlined below

Table #1: customers
- Column #1: ID
- Column #2: first_name
- Column #3: last_name
- Column #4: email

Table #2: orders
- Column #1: ID
- Column #2: customer_id
- Column #3: product
- Column #4: price

# Development Environment
The tools that were used to create this software were the following:
- Visual Studio Code: code editor that housed the code
- Languages: Python, SQL
- Git: Used for version control
- GitHub: Used to save the code in a repository

Programming Language Used:
- Python: The language used to execute most of the interaction in this software and interact with the user
- SQL: Used to query info from the various databases

# Useful Websites

- [Video on sqlite3 with python](https://www.youtube.com/watch?v=pd-0G0MigUA)
- [Quick overview on SQL](https://www.youtube.com/watch?v=zsjvFFKOm3c)
- [sqlite beginner video](https://www.youtube.com/watch?v=8Xyn8R9eKB8)
- [sqlite tutorial](https://www.youtube.com/watch?v=byHcYRpMgI4&t=1878s)

# Future Work

- Add statistics to the the customers table to display more customized info on the customers
- Build out a better user interface so that the user doesn't have to interact from the terminal, but an external window
- Allow it so that an order can contain more then one item

