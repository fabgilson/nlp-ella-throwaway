# Toward Smarter Project Management Tools

This project is an assessment tool for checking the quality of user stories and acceptance criteria. It uses a rules-based NLP approach to check user stories and acceptance criteria against a set of quality criteria.

## Running tests: 
There is an automated test suite for ensuring each of the rules implemented in the tool works as expected.
```console
cd src
python -m pytest
```

## Installing dependencies:
Run the following commands to install the external libraries this project is dependent on.
```console
pip install -r requirements.txt
```

For several NLP techniques, the NLP library NLTK (Natural Language Tookit) is used. These need to be installed on every new machine you plan to run this project on. To install the NLTK data, run the following:
```console
pip install certifi
python3 download_nltk_data.py
```

## Running the app:
To run the application locally, run the following command.
```console
python3 src/app.py
```

## Using the app:
The app will run on the following url:
```
http://127.0.0.1:8000/
```

To asses a user story, you can either run the UI, or use something like Postman. If you are using Postman, make a POST request at the ```/story``` endpoint with a body of JSON data in the following format:
```json
{
    "story_text": "A user story should be pasted here."
}
```

To asses a user story, you can either run the UI, or use something like Postman. If you are using Postman, make a POST request at the ```/story``` endpoint with a body of JSON data in the following format:
```json
{
    "acceptance_criteria": "An acceptance criterion should be pasted here."
}
```
