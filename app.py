from flask import Flask, render_template, request, jsonify, send_file
from reportlab.pdfgen import canvas
from io import BytesIO
from flask import send_file

app = Flask(__name__)

# -------------------------------
# Food Recommendations
# -------------------------------

food_recommendations = {

    "Underweight": {
        "foods": [
            "🥚 Eggs - 2 eggs (140 kcal)",
            "🍌 Banana - 1 medium (105 kcal)",
            "🍚 Rice - 1 cup (200 kcal)",
            "🥜 Nuts - 30 grams (170 kcal)",
            "🍗 Chicken - 100 grams (165 kcal)",
            "🫘 Beans - 1 cup (120 kcal)"
        ],
        "total_calories": "Approx 900 kcal"
    },

    "Normal Weight": {
        "foods": [
            "🥗 Green Vegetables - 1 bowl (80 kcal)",
            "🍎 Apple - 1 medium (95 kcal)",
            "🍚 Brown Rice - 1 cup (215 kcal)",
            "🍗 Lean Chicken - 100 grams (165 kcal)",
            "🐟 Fish - 100 grams (150 kcal)",
            "🥛 Low-fat Milk - 1 glass (120 kcal)",
            "🥜 Nuts - 30 grams (170 kcal)"
        ],
        "total_calories": "Approx 995 kcal"
    },

    "Overweight": {
        "foods": [
            "🥗 Salad - 1 bowl (40 kcal)",
            "🥒 Cucumber - 1 medium (30 kcal)",
            "🍎 Apple - 1 medium (95 kcal)",
            "🍊 Orange - 1 medium (60 kcal)",
            "🥦 Broccoli - 1 bowl (55 kcal)",
            "🥣 Oats - 40 grams (150 kcal)",
            "🍵 Green Tea - 1 cup (2 kcal)"
        ],
        "total_calories": "Approx 430 kcal"
    },

    "Obese": {
        "foods": [
            "🥦 Broccoli - 1 bowl (55 kcal)",
            "🥬 Spinach - 1 bowl (40 kcal)",
            "🥒 Cucumber - 1 medium (30 kcal)",
            "🍅 Tomato - 1 medium (22 kcal)",
            "🍎 Apple - 1 medium (95 kcal)",
            "🥣 Oats - 40 grams (150 kcal)",
            "🐟 Grilled Fish - 100 grams (150 kcal)"
        ],
        "total_calories": "Approx 540 kcal"
    }

}

# -------------------------------
# BMI Details
# -------------------------------

def get_bmi_details(bmi):

    if bmi < 18.5:
        status = "Underweight"
        recommendation = "Eat healthy foods and increase calorie intake."

    elif bmi < 25:
        status = "Normal Weight"
        recommendation = "Maintain your healthy diet and continue regular exercise."

    elif bmi < 30:
        status = "Overweight"
        recommendation = "Reduce junk food and do regular cardio."

    else:
        status = "Obese"
        recommendation = "Follow a proper diet plan and regular workout routine."

    food_data = food_recommendations[status]

    return (
        status,
        recommendation,
        food_data["foods"],
        food_data["total_calories"]
    )

# -------------------------------
# Home
# -------------------------------

@app.route("/")
def home():
    return render_template("index.html")


# -------------------------------
# Calculate BMI
# -------------------------------

@app.route("/calculate", methods=["POST"])
def calculate():

    data = request.get_json()

    height = float(data["height"]) / 100
    weight = float(data["weight"])

    bmi = round(weight / (height * height), 2)

    status, recommendation, foods, total_calories = get_bmi_details(bmi)

    return jsonify({

        "bmi": bmi,
        "status": status,
        "recommendation": recommendation,
        "foods": foods,
        "total_calories": total_calories

    })
# -------------------------------
# Download BMI Report
# -------------------------------

@app.route("/download_report", methods=["POST"])
def download_report():

    data = request.get_json()

    name = data["name"]
    height = float(data["height"])
    weight = float(data["weight"])

    height_m = height / 100

    bmi = round(weight / (height_m * height_m), 2)

    status, recommendation, foods, total_calories = get_bmi_details(bmi)

    buffer = BytesIO()
 
    pdf = canvas.Canvas(buffer)

    # Title
    pdf.setTitle("BMI Health Report")

    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawString(180, 800, "BMI HEALTH REPORT")

    # User Details
    pdf.setFont("Helvetica", 12)

    pdf.drawString(50, 760, f"Name : {name}")
    pdf.drawString(50, 735, f"Height : {height} cm")
    pdf.drawString(50, 710, f"Weight : {weight} kg")
    pdf.drawString(50, 685, f"BMI : {bmi}")
    pdf.drawString(50, 660, f"Status : {status}")

    # Recommendation
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(50, 630, "Recommendation:")

    pdf.setFont("Helvetica", 11)
    pdf.drawString(70, 610, recommendation)

    # Foods
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(50, 580, "Recommended Foods:")

    pdf.setFont("Helvetica", 11)

    y = 560

    for food in foods:
        pdf.drawString(70, y, food)
        y -= 18

    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(50, y - 10, f"Total Calories : {total_calories}")

    # Footer
    pdf.setFont("Helvetica-Oblique", 10)
    pdf.drawString(
        50,
        50,
        "Note: This report is for educational purposes only and is not a medical diagnosis."
    )

    pdf.save()

    buffer.seek(0)

    return send_file(
    buffer,
    as_attachment=True,
    download_name="BMI_Report.pdf",
    mimetype="application/pdf"
)

# -------------------------------
# Run Application
# -------------------------------

if __name__ == "__main__":
    app.run(debug=True)