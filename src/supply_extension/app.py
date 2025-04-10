from flask import Flask, render_template
from supply_data import fetch_hotels_in_bangkok
from ai_logic import recommend_top_hotels

app = Flask(__name__)

@app.route('/supply-dashboard')
def supply_dashboard():
    try:
        hotels = fetch_hotels_in_bangkok()  
        print("HOTELS DATA:", hotels)
        recommendations = recommend_top_hotels(hotels)  

        hotel_names = [h['name'] for h in recommendations]
        hotel_ratings = [h['rating'] for h in recommendations]

        return render_template(
            "supply_dashboard.html",
            hotels=recommendations,
            hotel_names=hotel_names,
            hotel_ratings=hotel_ratings
        )
    
    except Exception as e:
        return f"<h2 style='color:red;'>🔥 Error loading dashboard:</h2><pre>{e}</pre>"

if __name__ == "__main__":
    app.run(debug=True)
