def recommend_top_hotels(hotels):
    print("DEBUG: hotels received by AI logic:", hotels)

    for i, h in enumerate(hotels):
        print(f"Type of hotel[{i}]:", type(h), "| Value:", h)

    sorted_hotels = sorted(hotels, key=lambda x: x.get("rating", 0), reverse=True)
    return sorted_hotels[:3]
