# API Endpoints

- `GET /books/` - List all books
- `GET /books/<id>/` - Retrieve a book by ID
- `POST /books/create/` - Create a new book (authentication required)
- `PUT /books/<id>/update/` - Update a book (authentication required)
- `DELETE /books/<id>/delete/` - Delete a book (authentication required)

## **Testing Documentation**

### **Testing Strategy**

The testing strategy for this project involves ensuring that all key functionalities of the Book API are thoroughly tested. This includes verifying the correct implementation of endpoints for CRUD operations (Create, Retrieve, Update, Delete), as well as additional features such as filtering, searching, and ordering.

Each test case is designed to verify a specific functionality, and all test cases are run in an isolated test database to ensure they do not interfere with real data.

### **Individual Test Cases**

The following test cases have been implemented to ensure the functionality of the Book API:

| Test Case                 | Endpoint                       | Method | Expected Result                          |
|---------------------------|---------------------------------|--------|------------------------------------------|
| **Create Book**           | `/books/`                     | POST   | `201 Created` and correct response data. |
| **List Books**            | `/books/`                     | GET    | `200 OK` and list of books.              |
| **Retrieve Book**         | `/books/{id}/`                | GET    | `200 OK` and correct book details.       |
| **Update Book**           | `/books/{id}/`                | PUT    | `200 OK` and updated book details.       |
| **Delete Book**           | `/books/{id}/`                | DELETE | `204 No Content`.                        |
| **Filter Books by Title** | `/books/?title=<title>`        | GET    | `200 OK` and filtered list of books.     |
| **Search Books**          | `/books/?search=<keyword>`    | GET    | `200 OK` and search results.             |
| **Order Books by Year**   | `/books/?ordering=publication_year` | GET    | `200 OK` and correctly ordered list.     |

---

### **How to Run the Tests**

To ensure the correctness of the API and its features, you can run the tests locally by following these steps:

1. **Navigate to the project directory**:
   ```bash
   cd D:\ALX\advanced-api-project
2.Run the tests using Django's test framework:

bash
Copy code
python manage.py test api
3. Observe the test results in the console. The test results will display detailed output about each test case’s status.

Interpreting the Test Results
Here’s how to interpret the test results you will get after running the tests:

Success: If all tests pass successfully, the output will show a message like:

bash
Copy code
Ran 8 tests in 19.187s

OK
This means all your test cases have passed, and the API is functioning as expected.

Failure: If there are failures, Django will provide an error message indicating which specific test case failed and the reason for the failure. For example:

bash
Copy code
FAIL: test_create_book
AssertionError: 403 != 201
This would indicate that the POST /books/ request didn’t return the expected status code (201 Created) but instead returned a 403 Forbidden status. You would need to check the test case and ensure that the required authentication or permissions are set correctly.

Test Results from Recent Runs:

Based on the latest test runs, here’s a summary of the outcomes:

POST Request to Create a Book:

Expected Status: 201 Created
Result: 201 Created, with correct book data returned.
DELETE Request to Remove a Book:

Expected Status: 204 No Content
Result: 204 No Content, indicating successful deletion of the book.
GET Request with Filtering by Title:

Expected Status: 200 OK
Result: 200 OK, with the book list filtered by the specified title (Sample Book).
GET Request for Book List:

Expected Status: 200 OK
Result: 200 OK, returning the correct list of books.
GET Request with Ordering by Publication Year:

Expected Status: 200 OK
Result: 200 OK, returning books ordered by the publication year.
GET Request for a Single Book:

Expected Status: 200 OK
Result: 200 OK, returning the correct details of the book with ID 1.
GET Request with Search Functionality:

Expected Status: 200 OK
Result: 200 OK, with books matching the search term (Sample).
PUT Request to Update a Book:

Expected Status: 200 OK
Result: 200 OK, with updated book data.
DELETE Request to Remove a Book:

Expected Status: 204 No Content
Result: 204 No Content, indicating successful deletion.
All these tests pass successfully, confirming that the API behaves as expected.
