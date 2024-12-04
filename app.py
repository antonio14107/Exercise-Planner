from flask import Flask, render_template, request, send_file
from openai import OpenAI
from fpdf import FPDF
import os

# Initialize Flask app
app = Flask(__name__)

# Instantiate OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Confirm if API key is found
print(f"OpenAI API Key Found: {'OPENAI_API_KEY' in os.environ}")

# Route for the home page
@app.route("/")
def index():
    return render_template("index.html")

# Function to generate the fitness plan
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

    Based on this style, create a detailed weekly plan for the user:
    - Intensity Level: {intensity}
    - Workout Duration: {duration} minutes
    - Equipment Available: {equipment}
    - User Goals: {goals}
    - User Preferences: {preferences}
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You are a fitness expert."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=1000,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"An error occurred while generating the plan: {str(e)}"

# Save the plan as a PDF
def save_plan_as_pdf(plan):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, plan)
    filename = "fitness_plan.pdf"
    pdf.output(filename)
    return filename

# Route for plan generation
@app.route("/plan", methods=["POST"])
def plan():
    # Get data from form
    goals = request.form.get("goals", "General fitness")
    preferences = request.form.get("preferences", "No preferences")
    equipment = request.form.get("equipment", "No equipment")
    intensity = request.form.get("intensity", "Moderate")
    duration = request.form.get("duration", "30")

    # Generate plan
    plan = generate_fitness_plan(goals, preferences, equipment, intensity, duration)
    pdf_filename = save_plan_as_pdf(plan)
    return render_template("plan.html", plan=plan, pdf_filename=pdf_filename)

# Route to download the PDF
@app.route("/download/<filename>")
def download(filename):
    return send_file(filename, as_attachment=True)

if __name__ == "__main__":
    # Bind to 0.0.0.0 for Render compatibility
    app.run(host="0.0.0.0", port=5000)
