import json
from models import Excerpt, db
from app import app

def load_excerpts():
    with open("excerpts/gpt_excerpts.json") as f:
        data = json.load(f)

    for ex in data:
        existing = Excerpt.query.filter_by(
            excerpt_number=ex["excerpt_number"]
        ).first()

        if not existing:
            new_excerpt = Excerpt(
                excerpt_title=ex["excerpt_title"],
                excerpt_author=ex["excerpt_author"],
                excerpt_number=ex["excerpt_number"],
                excerpt_condition=ex.get("condition"),
                excerpt_json=json.dumps(ex["excerpt_json"])  # IMPORTANT
            )
            db.session.add(new_excerpt)

    db.session.commit()
    print("Excerpts loaded!")


if __name__ == "__main__":
    with app.app_context():
        load_excerpts()