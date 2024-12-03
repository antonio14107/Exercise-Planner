# AI Exercise Planner

## Description
The AI Exercise Planner is a web application that generates personalized weekly fitness plans based on user inputs such as fitness goals, preferences, available equipment, intensity, and duration. This project uses OpenAI's `gpt-4-turbo` to create detailed, tailored plans, ensuring users get the most out of their workouts.

---

## Features
- **User-Friendly Input Form:** Enter fitness goals, preferences, and equipment.
- **AI-Powered Workout Plans:** Generates detailed, actionable plans using OpenAI's API.
- **PDF Download:** Save your workout plan for offline use.
- **Loading Spinner:** Provides real-time feedback during plan generation.

---

## Technologies Used
- **Backend:** Flask (Python)
- **AI:** OpenAI API (`gpt-4-turbo`)
- **PDF Generation:** `fpdf2`
- **Frontend:** HTML, CSS, JavaScript

---

## Setup Instructions

### Prerequisites
- Python 3.7 or higher
- OpenAI API Key

### Steps
1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/exercise-planner.git
   cd exercise-planner
   ```

2. **Create a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set your OpenAI API key:**
   - **Mac/Linux:**
     ```bash
     export OPENAI_API_KEY=your_openai_api_key_here
     ```
   - **Windows (Command Prompt):**
     ```cmd
     set OPENAI_API_KEY=your_openai_api_key_here
     ```
   - **Windows (PowerShell):**
     ```powershell
     $env:OPENAI_API_KEY="your_openai_api_key_here"
     ```

5. **Run the application:**
   ```bash
   python app.py
   ```

6. **Access the app:**
   - Open your browser and navigate to: `http://127.0.0.1:5000`.
