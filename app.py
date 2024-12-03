from flask import Flask, render_template, request, send_file
import openai
from fpdf import FPDF
import os

# Initialize Flask app
app = Flask(__name__)

# OpenAI API setup
openai.api_key = os.getenv("OPENAI_API_KEY")

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

    Wednesday: Rest Day

    Based on this style, create a detailed weekly plan for the user:
    - Intensity Level: {intensity}
    - Workout Duration: {duration} minutes
    - Equipment Available: {equipment}
    - User Goals: {goals}
    - User Preferences: {preferences}
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",  # Use gpt-4 or gpt-3.5-turbo based on your API access
            messages=[
                {"role": "system", "content": "You are a professional fitness coach."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=1000,
        )
        return response.choices[0].message["content"].strip()
    except Exception as e:
        return f"An error occurred while generating the plan: {e}"

# Function to save the plan as a PDF
def save_plan_as_pdf(plan):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, plan)
    filename = os.path.join(os.getcwd(), f"fitness_plan.pdf")
    pdf.output(filename)
    return filename

# Route for generating the fitness plan
@app.route("/plan", methods=["POST"])
def plan():
    # Retrieve form data
    goals = request.form.get("goals")
    preferences = request.form.get("preferences")
    equipment = request.form.get("equipment", "None")
    intensity = request.form.get("intensity")
    duration = request.form.get("duration")

    # Generate the fitness plan
    plan = generate_fitness_plan(goals, preferences, equipment, intensity, duration)

    # Save the plan as a PDF
    pdf_filename = save_plan_as_pdf(plan)

    return render_template("plan.html", plan=plan, pdf_filename=pdf_filename)

# Route for downloading the PDF
@app.route("/download", methods=["GET"])
def download():
    filename = os.path.join(os.getcwd(), "fitness_plan.pdf")
    return send_file(filename, as_attachment=True)

# Run the app
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
