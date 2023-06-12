# Flask Scoreboard App

This is a simple Flask application that allows users to keep track of scores.

## Features

- User authentication
- Add, view, and delete scores
- Calculate scores based on user guesses

## Setup and Installation

### Local Setup

1. Clone the repository:

```bash
git clone https://github.com/yourusername/flask-scoreboard-app.git
cd flask-scoreboard-app
```

2. Create a virtual environment and install the dependencies:

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt
```

3. Run the application:

```bash
flask run
```

### Docker Setup

1. Build the Docker image:

```bash
docker build -t scoreboard-app .
```

2. Run the Docker container:

```bash
docker run -e SECRET_KEY=your_secret_key -p 5003:5003 scoreboard-app
```

3. Replace your_secret_key with your actual secret key.

The application will be available at http://localhost:5003.

## License

This project is licensed under the terms of the MIT license.

Remember to replace `yourusername` and `your_secret_key` with your actual GitHub username and your actual secret key, respectively.


