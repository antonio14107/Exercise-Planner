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
    prompt = (
        f"You are a professional fitness coach. Create a detailed, structured weekly workout plan for someone whose goal is '{goals}', "
        f"prefers '{preferences}', and has access to the following equipment: '{equipment}'. The intensity level should be '{intensity}', "
        f"and the duration per session should be '{duration}'. The plan should include warm-ups, main workouts, and cool-downs."
    )
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful fitness coach."},
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
