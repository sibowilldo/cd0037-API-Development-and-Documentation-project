# Contents

-------

- [Backend Setup](#backend-setup)
- [Frontend Setup](#front-end-setup)
- [EndPoints](#endpoints)
- [Testing](#unit-testing)
- [Contributions](#contributing)

# Backend Setup

-------
The Backend of Udacity Trivia API is built with 🐍 Python 3.10 and Flask 2.2.2. To get started with the backend setup, we
highly recommend following the instructions below which help you set up a python virtual environment, however you're
more than welcome to use other environments you may already have on your system provided they meet the dependency
requirements included in the [requirements.txt](requirements.txt) file.

To get started make sure you are in the backend directory by running this command 📁`cd backend` on the terminal from the
root of the Application

**Upgrade pip**

```
python3 -m pip install --user --upgrade pip
```

**Install virtualenv**

```bash
python3 -m pip install --user virtualenv
```

**Create a virtual env**

```bash
python3 -m venv env
```

**Activate a virtual env**

```bash
source env/bin/activate
```

**Install Dependencies**

```bash
python3 -m pip install -r requirements.txt
```
**Set the Project Environment Variables**

The project environment variables are located in the root folder of the project. 
Simply rename or copy the ``.env-sample`` file to ``.env`` and edit the file as needed
```bash
cp .env-sample .env
```
**Set the App and Debug Parameters**

 ```bash
 export FLASK_APP=flaskr FLASK_DEBUG=True
 ```

**Run the App**

```bash
flask run
```

## Front End Setup

-----
The frontend we've provided to help you get started is a ReactJS application, but feel free to code yourself another
application using frontend frameworks such as VueJS, Angular etc.

Navigate to frontend folder by typing 📁 `cd frontend`  from the root directory of the Application.

```bash
npm install && npm start
```

# EndPoints

-----

### Base URL
> ``http://localhost:5000/api/v1``


### All Categories

Retrieved all categories.

- Method: ``GET``
- Endpoint: `/api/v1/categories`

**Response Object**
``Status: 200 OK`` 🟢

```json
{
  "categories": [
    {
      "id": 1,
      "type": "Science"
    },
    {
      "id": 2,
      "type": "Art"
    }
  ],
  "success": true
}
```

### Paginated Questions

Retrieves a paginated array of questions with a maximum number of 10 items per page. Sending the request without
the ``page`` parameter retrieves the first 10 questions. The response also includes an array of categories, a total
questions, current category and success message.

- Method: ``GET``
- Endpoint: `/api/v1/questions?page=1`

**Response Object**
``Status: 200 OK`` 🟢

```json
{
  "categories": [
    {
      "id": 1,
      "type": "Science"
    },
    {
      "id": 2,
      "type": "Art"
    }
  ],
  "questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    }
  ],
  "current_category": 1,
  "success": true,
  "total_questions": 21
}
```

### Get Questions by Category

The Get Question by Category Endpoints will return all questions for a given category, total number of returned
questions and category id that was passed as part of the URL.

- Method: ``GET``
- Endpoint: `/api/v1/categories/{categoty_id}/questions`

**Response Object**
``Status: 200 OK`` 🟢

```json
{
  "questions": [
    {
      "answer": "Escher",
      "category": 2,
      "difficulty": 1,
      "id": 16,
      "question": "Which Dutch graphic artist–initials M C was a creator of optical illusions?"
    },
    {
      "answer": "Mona Lisa",
      "category": 2,
      "difficulty": 3,
      "id": 17,
      "question": "La Giaconda is better known as what?"
    }
  ],
  "success": true,
  "current_category": 2,
  "total_questions": 4
}
```

### Search Question

This endpoint takes a very specific payload with `searchTerm` as the only parameter. A successful request will return a
list of questions, success flag, and total_questions, with a ``200`` status code.

- Method: ``POST``
- Endpoint: `/api/v1/questions`

**Payload**

```json
{
  "searchTerm": "title"
}
```

**Response Object**
``Status: 200 OK`` 🟢

```json
{
  "questions": [
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }
  ],
  "success": true,
  "current_category": null,
  "total_questions": 2
}
```

### Create a new Question

Creates a new question based on the supplied payload, it returns a ``201`` status code and success message if
successful, and a ``422`` error code if unsuccessful.

- Method: ``POST``
- Endpoint: `/api/v1/questions`

**Payload**

```json
{
  "questions": "How many countries are there in Africa?",
  "answer": "Africa has 54 countries",
  "difficulty": 3,
  "category": 3
}
```

**Response Object**
``Status: 201 CREATED`` 🟢

```json
{
  "message": "Question saved!",
  "success": true
}
```

### Play Quiz

Returns a random question object based on the provided `category` and array of question ids. Throws ``404`` if no
questions
meet the filter criteria, or ``422`` if the category is not a number or previous questions is not an array or array of
ids

- Method: ``POST``
- Endpoint: `/api/v1/quizzes`

**Payload**

```json
{
  "previous_questions": [
    5,
    9,
    12
  ],
  "quiz_category": 4
}
```

**Response Object**
``Status: 200 OK`` 🟢

```json
{
  "question": {
    "answer": "Scarab",
    "category": 4,
    "difficulty": 4,
    "id": 23,
    "question": "Which dung beetle was worshipped by the ancient Egyptians?"
  },
  "success": true
}
```

### Delete Question by ID

Deletes a question based on the ID passed as part of the endpoint. Throws 404 if the `id` is not found or 422 is not a
number.

- Method: ``DELETE``
- Endpoint:`/api/v1/questions/<int: question_id>`

**Response Object**
``Status: 200 OK`` 🟢

```json
{
  "deleted_question": 2,
  "success": true
}
```

# Unit Testing

----
Udacity Trivia API comes with Unit Test that you can run with the command below.
The test file is found in 📁 `backend` directory.

```bash
python3 test_flaskr.py
```

# Contributing

---
> Udacity Trivia API is licensed under the [Udacity License](../LICENSE.txt).