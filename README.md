# Yet another TV database!
### Video demo: <URL HERE>
### Description

- [Yet another TV database!](#yet-another-tv-database)
    - [Video demo: ](#video-demo-)
    - [Description](#description)
    - [Two python programs:](#two-python-programs)
    - [Eight html files:](#eight-html-files)
    - [One SQLite 3 database:](#one-sqlite-3-database)
    - [A static folder:](#a-static-folder)
    - [Design choices:](#design-choices)


Yet another TV database (YaTVdb) is, like its name suggests another program to track your watched and to watch TV series or Movies.

The user searches for a movie or series in a searchbox and the page utilizes  an API from rapid API to get information about it. After that it stores the information in a SQLite 3 database.
The webpage runs on Flask using Python and consists of the following sections:

### Two python programs:

1.  [helpers.py](helpers.py) that contains the following functions:

    1. Login_required, a decorated function that is copied from the finance problem.
    2. Apicall that makes the call in the api website and receives a JSON file with the information about the search.
    3. Parse that parses that information and stores it into the database.
    4. Dict_factory is used to receive a dictionary reply in response to a query from the SQLite3 database.
    5. Search a function to lookup keys in a dictionary. Used in order to get the id of the button that the user clicked in the search results.

2.  [app.py](app.py) for the main program:

    1. app.py handles the cookies, user login logout and register functions.

    2. a route called search for rendering the webpage that searches the IMDB database. After the search it renders the searched route.

    3. once the search results are in the search route displays the information about possible matches and prompts the user to click on the image of the result to view the details.

    4. after an image is clicked it renders the test.html (name pending) that allows the user to add that movie or TV series in the watch list or the watched list.

    5. the mylist route is used then to allow the user to view all the items in both his/her lists and add or remove items from it or mark an item from the watch list as watched, deleting the relevant record from that list and adding it to watched list.

    6. finally the main page welcomes a user and displays a prompt for a user to watch the items on his watchlist while displaying said list.

### Eight html files:

   1. [index.html](templates/index.html) renders the home page using Jinja and gets passed the result of the SQL query.
   2. [layout.html](templates/layout.html) has the layout with the navbar on top and footer on the bottom.
   3. [login.html](templates/login.html) for the login page.
   4. [mylist.html](templates/mylist.html) displays the watched and watch list. It also allows the user to modify this list by adding to watched items from the watchlist and removing from both lists.
   5. [register.html](templates/register.html) handles the registration of a new user.
   6. [search.html](templates/search.html) renders the search page.
   7. [searched.html](templates/searched.html) displays the parsed results in a table for the user to select a result or search again.
   8. [test.html](templates/test.html) renders the information for the movie or TV series the user has selected and allows the user to add to either watch or watched list.

### One SQLite 3 database:

[movies.db](movies.db) contains 3 tables.

1. users to store the users information (user id,username, hash of the password and name of the users).
2. favorites with the fields of  (id, user_id linked to users.id movie_id linked with the movies.id, watchlist and watched to track with a flag of either 0 or 1 if the users have a movie in their lists).
3. movies into which the results of the api query are parsed with the parse function.

### A static folder:

[Static folder](static) contains the background image of the site, the favicon to display in the browser label and styles.css

The css theme is called "Greyscale" from the Start Bootstrap site:

[https://startbootstrap.com/theme/grayscale](https://startbootstrap.com/theme/grayscale)

### Design choices:

In order to create this site I had to learn how to parse JSON files and impliment in my solution a variety of new techniques according to documentation and other research.
The biggest problem for me was passing information from the frontend to the backend successfully.

I left a lot of the print statements in the code in order to show the proccess of troubleshooting elements of my code to get the results I wanted.

As the project was completed outside of the cs50 codespace with all training wheels removed that introduced a lot of new syntax, in SQL and more.