
# AI IN A BOX

The **AI IN A BOX** is a multi-functional tool that integrates with a Large Language Model (LLM) to perform various file operations and interact with its environment,uses virtual environments.
---

## Features

### 1. **File Operations**
- **Read**: View the contents of a file.
- **Write**: Write content to certain file types. (overwrites already existing content)
- **Delete**: Move files to a trash folder instead of permanent deletion.
- **List**: Display the directory structure.
- **Run**: Execute Python scripts.

### 2. **Virtual Environment Management**
- Create and delete virtual environments using the `Virtual_env_creation_and_deletion.py` script.
- Install dependencies from `requirements.txt`.

### 3. **Authentication System**
- User registration and login using FastAPI.
- OTP-based email verification.
- JWT-based authentication for protected routes.
- Includes a Streamlit-based UI for user interaction.

### 4. **Logging**
- Logs all actions with timestamps.
- Supports colored logging for better visibility.

### 5. **Rate Limiting**
- Configurable delay between API requests to avoid rate limits.

---

## Project Structure

```
├── LLM_CLI_FILEACCESS/
│   ├── sandbox/
│   │   ├── read.txt
│   │   ├── test.csv
│   │   ├── test.py
│   │   └── folder/
│   ├── .env
│   ├── file_serialisation.py
│   ├── main_code.py
│   ├── README.md
│   ├── requirements.txt
│   └── Virtual_env_creation_and_deletion.py
```

---

## Installation

### Prerequisites
- Python 3.10 or higher
- PostgreSQL (for the Postgres project)
- SMTP server credentials (for email functionality)

### Steps

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-repo/LLM_logger_project.git
   cd LLM_logger_project
   ```

2. **Set Up Virtual Environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r LLM_CLI_FILEACCESS/requirements.txt
   ```

4. **Set Up Environment Variables**:
   - Create a `.env` file in the `LLM_CLI_FILEACCESS` and `authentication_system` directories.
   - Add the following variables:
     ```
     _APIGROQ_KEY=<your_groq_api_key>
     SECRET_KEY=<your_jwt_secret_key>
     ALGORITHM=HS256
     ```

5. **Run the Main Script**:
   ```bash
   python main_code.py
   ```

---

## Usage

### 1. **File Operations**
- Use the CLI to interact with the LLM for file operations.
- Example commands:
  - `Action:List`: List the directory structure.
  - `Action:Read <filepath>`: Read a file.
  - `Action:WriteToEx <filepath> <content>`: Write content to a file.
  - `Action:Delete <filepath>`: Move a file to the trash folder.

### 2. **Virtual Environment Management**
- Run the `Virtual_env_creation_and_deletion.py` script to create or remove a virtual environment:
  ```bash
  python Virtual_env_creation_and_deletion.py
  ```

## Configuration

### Logging
- Logs are saved to a file with a timestamped filename:
  ```
  LLM_actions_YYYY-MM-DD_HH-MM-SS.log
  ```

### Rate Limiting
- Adjust the delay between API requests by modifying the `delay` variable in `main_code.py`:
  ```python
  delay = 30  # 30seconds
  ```

---

## Dependencies

### Python Packages
- `groq==0.9.0`
- `httpx==0.24.1`
- `python-dotenv==1.0.1`
- `colorlog==6.9.0`
- `coloredlogs==15.0.1`

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## Contributing

Feel free to submit issues or pull requests to improve the project.

---

## Acknowledgments

- **Groq API**: For LLM integration.

```

---

