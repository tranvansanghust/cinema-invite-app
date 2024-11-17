# Cinema Invite App

## How to Run the Project

### Using Python

1. **Install Dependencies**: Make sure you have Python and pip installed. Then, install the required dependencies:
    ```bash
    pip install fastapi uvicorn
    ```

2. **Run the Application**: Use `uvicorn` to run the FastAPI application:
    ```bash
    uvicorn main:app --reload
    ```

3. **Access the Application**: Open your browser and go to `http://127.0.0.1:8000` to see the application running.

### Using Docker

1. **Build the Docker Image**:
    ```bash
    docker build -t cinema-invite-app .
    ```

2. **Run the Docker Container**:
    ```bash
    docker run -d -p 8000:80 cinema-invite-app
    ```

3. **Access the Application**: Open your browser and go to `http://127.0.0.1:8000` to see the application running.