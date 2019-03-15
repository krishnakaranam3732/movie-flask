# movie-flask

Movies added as of now are of genre: fantasy

POST /recommendation
- store a new recommendation. Payload format should include the movie title, genre, and year
created
GET /recommendation
- get a random recommendation. Recommendation's can be literally random-- pick a random
number based on how many recommendations there are, return that one. Should support a
"genre" query parameter, allowing a user to receive a recommendation for a movie within a
specific genre, i.e. comedy.
GET /statistics
- get the total number of recommendations returned and the total number of movie titles within
the system

How to Run:

1. Open Folder movie-flask
2. execute command: python app.py
3. Headove to http://127.0.0.1:5000/ for the API
