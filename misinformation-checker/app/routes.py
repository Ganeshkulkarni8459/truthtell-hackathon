from flask import Blueprint, request, jsonify
from app import db
from app.models import MisinformationResult
from app.utils import scrape_data, check_with_fact_check_api
from app.ml_model import get_misinformation_score

# Create a Blueprint for routes
bp = Blueprint('main', __name__)

FACT_CHECK_API_KEY = 'AIzaSyDXlQwkXSgKXz4EfwaxeSzBldtNH8ZqUlI'

@bp.route('/check', methods=['POST'])
def check_misinformation():
    data = request.get_json()
    url = data.get('url')
    if not url:
        return jsonify({"error": "URL is required"}), 400

    scraped_content = scrape_data(url)
    if not scraped_content:
        return jsonify({"error": "Failed to scrape the content"}), 400

    misinformation_score, classification = get_misinformation_score(scraped_content)
    fact_check_results = check_with_fact_check_api(scraped_content, FACT_CHECK_API_KEY)
    fact_check_summary = "\n".join(fact_check_results) if fact_check_results else "No relevant fact-checks found."

    result = MisinformationResult(
        url=url,
        misinformation_score=misinformation_score,
        classification=classification,
        fact_check_results=fact_check_summary
    )
    db.session.add(result)
    db.session.commit()

    return jsonify({
        "id": result.id,
        "Misinformation Score": misinformation_score,
        "Classification": classification,
        "Fact-Check Results": fact_check_summary,
        "url": url
    })

