# Bingo Generator

A simple proof of concept Bingo Card generator in python using flask.

## Getting Started

### File Structure

#### bootstrap.py

The flask app and SQLAlchemy db instance are created here to avoid circular includes.

#### models.py

The models used by this application.

#### app.py

The routes and kickoff for the app server.

### Prerequisites

This was built using python 3.7, it probably works in 3.5+, maybe older versions. I'm new to this so ¯\\_(ツ)_/¯

### Installing

1. Clone this repo
1. run `virtualenv`
1. run `pip install -r requirements.txt`
1. run `FLASK_APP=app.py flask run`
1. load your local server in your browser

## Deployment

Maybe don't do that.

## Built With

* [Flask](http://flask.pocoo.org/) - Web Framework
* [SQLAlchemy](https://www.sqlalchemy.org/) - ORM

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

* **Alessandro Craig D'Amelio**

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

Props go to:

* [Hara Gopal](https://www.udemy.com/flask-is-fun-and-easy-from-basics-to-building-scalable-apps/) - It's not the best course, but it did the job.
* [The Bechdel Cast](http://www.bechdelcast.com/) - The witty banter and in-jokes led to me wanting to build a generic solution for this "problem".
