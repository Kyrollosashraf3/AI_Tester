# AI Tester

A FastAPI-based application for testing AI chat systems, analyzing logs, and generating reports on conversation quality.

## Features

- Automated AI chat testing with configurable parameters
- Log analysis and error detection
- Turn-based conversation orchestration
- Web interface for easy access
- Integration with OpenAI models

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up environment variables:
   - `OPENAI_API_KEY`: Your OpenAI API key

## Usage

1. Run the application:
   ```bash
   uvicorn main:app --reload
   ```

2. Open your browser to `http://localhost:8000` for the web interface

3. Use the API endpoint:
   - POST `/run`: Run the AI tester and get a report

## Configuration

Edit `app/config/settings.py` to configure:
- API URLs
- Model settings
- Timeouts and limits
- Initial messages

## Project Structure

- `main.py`: FastAPI application entry point
- `app/routes/`: API routes
- `app/core/`: Core logic (LLM, orchestration, logs)
- `app/clients/`: API clients for chat and logs
- `app/config/`: Configuration and types
- `templates/`: HTML templates
