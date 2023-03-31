# Yet another TV database!
#### Video demo: <URL HERE>
#### Description

Yet another TV database (YaTVdb) is, like its name suggests another program to track your watched and to watch TV series or Movies.

	The user searches for a movie or series in a searchbox and the page utilizes  an API from rapid API to get information about it. After that it stores the information in a SQLite 3 database.
	The webpage runs on Flask using Python and consists of the following sections:

	Two python programs:

1. helpers.py that contains the following functions:

    1. Login_required, a decorated function that is copied from the finance problem.
    2. Apicall that makes the call in the api website and receives a JSON file with the information about the search.
    3. Parse that parses that information and stores it into the database.
    4. Dict_factory is used to receive a dictionary reply in response to a query from the SQLite3 database.
    5. Search a function to lookup keys in a dictionary. Used in order to get the id of the button that the user clicked in the search results.

2. app.py for the main program:

    app.py handles the cookies, user login logout and register functions.

    a route called search for rendering the webpage that searches the IMDB database. After the search it renders the searched route.

    once the search results are in the search route displays the information about possible matches and prompts the user to click on the image of the result to view the details.

    after an image is clicked it renders the test.html (name pending) that allows the user to add that movie or TV series in the watch list or the watched list.

    the mylist route is used then to allow the user to view all the items in both his/her lists and add or remove items from it or mark an item from the watch list as watched, deleting the relevant record from that list and adding it to watched list.

    finally the main page welcomes a user and displays a prompt for a user to watch the items on his watchlist while displaying said list.

Eight html files: