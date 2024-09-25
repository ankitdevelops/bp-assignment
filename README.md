# Assignment Solution

## Installations

1. **Create a Virtual Environment:**
    - Use any of the following commands:
    ```sh
    python -m venv env

    # or

    python3 -m venv env
    ```

2. **Activate the Virtual Environment:**
    - On Linux/MacOS:
    ```sh
    source env/bin/activate
    ```
    - On Windows:
    ```sh
    env\Scripts\activate
    ```

3. **Install the Requirements:**
    ```sh
    pip install -r requirements.txt
    ```

4. **Move to the `src` Directory:**
    ```sh
    cd src
    ```

5. **Add the `.env` File:**
    - Paste the `.env` file attached in the email into the `src` directory.

6. **Run Migrations:**
    - Apply the database migrations with the following command:
    - It is not required, as I am using PostgreSQL from [Neon](https://neon.tech/). I have already applied the migrations. 
    ```sh
    python manage.py migrate
    ```

7. **Start the Server:**
    ```sh
    python manage.py runserver
    ```

8. **Run the Tests:**
   - To execute the test cases, use the following command:
    ```sh
    python manage.py test
    ```
