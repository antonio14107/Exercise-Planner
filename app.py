import os
import time
from flask import Flask, render_template, request, send_file
import openai
from fpdf import FPDF

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

# Function to generate fitness plans using OpenAI API
def generate_fitness_plan(goals, preferences, equipment, intensity, duration):
    prompt = f"""
    You are a professional fitness coach with extensive experience in creating personalized workout plans. Your goal is to provide users with a structured, effective, and safe exercise routine tailored to their fitness goals, preferences, available equipment, intensity level, and desired duration.

    Example of a weekly fitness plan:
    Monday:
    - Warm-up: 10 minutes light jogging.
    - Main workout: 
      - 3 sets of squats with dumbbells (15 reps).
      - 3 sets of push-ups (10-15 reps).
      - 3 sets of dumbbell rows (12 reps each arm).
    - Cool-down: 5 minutes light stretching.

    Tuesday:
    - Cardio: 20 minutes brisk walking or cycling.
    - Core:
      - Plank (3 sets of 30 seconds).
      - Side planks (2 sets of 20 seconds each side).
    - Cool-down: Yoga stretches (5 minutes).

    Wednesday: Rest Day

    Based on this style, create a detailed weekly plan for the user:
    - Intensity Level: {intensity}
    - Workout Duration: {duration} minutes
    - Equipment Available: {equipment}
    - User Goals: {goals}
    - User Preferences: {preferences}
    """
    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant acting as a professional fitness coach. Always prioritize safety, clear instructions, and balanced exercise routines."},
            {"role": "user", "content": prompt}
        ]
    )
    return response['choices'][0]['message']['content'].strip()

# Function to create a PDF from the plan using a unique filename
def save_plan_as_pdf(plan, filename="fitness_plan.pdf"):
    # Generate a unique filename with a timestamp
    unique_filename = f"fitness_plan_{int(time.time())}.pdf"
    file_path = os.path.join(os.path.dirname(__file__), unique_filename)
    
    font_path = os.path.join(os.path.dirname(__file__), "fonts/Arial.ttf")
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.add_font("Arial", "", font_path, uni=True)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, plan)
    pdf.output(file_path, "F")
    return unique_filename  # Return only the filename

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/plan', methods=['POST'])
def plan():
    goals = request.form['goals']
    preferences = request.form['preferences']
    equipment = request.form['equipment']
    intensity = request.form['intensity']
    duration = request.form['duration']
    plan = generate_fitness_plan(goals, preferences, equipment, intensity, duration)
    
    # Save the plan as a PDF with a unique filename
    pdf_filename = save_plan_as_pdf(plan)

    return render_template('plan.html', plan=plan, pdf_filename=pdf_filename)

@app.route('/download/<filename>')
def download(filename):
    # Construct the full path of the file
    file_path = os.path.join(os.path.dirname(__file__), filename)
    
    # Serve the PDF file
    return send_file(file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
