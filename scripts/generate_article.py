#!/usr/bin/env python3
"""
Daily CBSE Class 10 article generator for cbseclass10.com
Generates a complete HTML article using Claude API and saves it to the repo.
Run via GitHub Actions on a daily schedule.
"""

import anthropic
import os
import sys
import random
from datetime import datetime

sys.path.insert(0, os.path.dirname(__file__))
import seo_utils as su

DOMAIN = "cbseclass10.com"
SITE_NAME = "CBSEClass10"

AUTHORS = ["Ananya Sharma", "Rohan Verma", "Priya Nair", "Arjun Mehta", "Sneha Iyer", "Karan Malhotra", "Divya Reddy", "Aditya Joshi"]


def add_byline(html, today_display):
    author = random.choice(AUTHORS)
    byline = (
        '<div style="max-width:800px;margin:20px auto 0;padding:0 24px;'
        'font-family:-apple-system,sans-serif;font-size:0.88rem;color:#6b7280;">'
        f'By <a href="https://padhle.in" style="color:#7C3AED;text-decoration:none;font-weight:600;">{author}</a>'
        f' &middot; \U0001F4C5 {today_display}</div>'
    )
    idx = html.find("<body")
    if idx == -1:
        return byline + html
    end = html.find(">", idx)
    if end == -1:
        return byline + html
    end += 1
    return html[:end] + byline + html[end:]


TOPICS = [
    {"slug": "cbse10-chemical-reactions-and-equations", "title": "Chemical Reactions and Equations for CBSE Class 10: Types and Balancing", "subject": "Science"},
    {"slug": "cbse10-acids-bases-and-salts", "title": "Acids, Bases and Salts for CBSE Class 10: Complete Chapter Guide", "subject": "Science"},
    {"slug": "cbse10-metals-and-non-metals", "title": "Metals and Non-Metals for CBSE Class 10: Properties and Reactions", "subject": "Science"},
    {"slug": "cbse10-carbon-and-its-compounds", "title": "Carbon and Its Compounds for CBSE Class 10: Bonding and Nomenclature", "subject": "Science"},
    {"slug": "cbse10-periodic-classification-of-elements", "title": "Periodic Classification of Elements for CBSE Class 10: Trends Explained", "subject": "Science"},
    {"slug": "cbse10-life-processes", "title": "Life Processes for CBSE Class 10: Nutrition, Respiration and Transport", "subject": "Science"},
    {"slug": "cbse10-control-and-coordination", "title": "Control and Coordination for CBSE Class 10: Nervous and Hormonal System", "subject": "Science"},
    {"slug": "cbse10-how-do-organisms-reproduce", "title": "How Do Organisms Reproduce for CBSE Class 10: Complete Chapter Guide", "subject": "Science"},
    {"slug": "cbse10-heredity-and-evolution", "title": "Heredity and Evolution for CBSE Class 10: Mendel's Laws Simplified", "subject": "Science"},
    {"slug": "cbse10-light-reflection-and-refraction", "title": "Light Reflection and Refraction for CBSE Class 10: Formulas and Ray Diagrams", "subject": "Science"},
    {"slug": "cbse10-human-eye-and-colourful-world", "title": "The Human Eye and the Colourful World for CBSE Class 10: Key Concepts", "subject": "Science"},
    {"slug": "cbse10-electricity", "title": "Electricity for CBSE Class 10: Ohm's Law and Circuit Numericals", "subject": "Science"},
    {"slug": "cbse10-magnetic-effects-of-electric-current", "title": "Magnetic Effects of Electric Current for CBSE Class 10: Complete Notes", "subject": "Science"},
    {"slug": "cbse10-sources-of-energy", "title": "Sources of Energy for CBSE Class 10: Renewable vs Non-Renewable", "subject": "Science"},
    {"slug": "cbse10-our-environment", "title": "Our Environment for CBSE Class 10: Ecosystem and Food Chains Explained", "subject": "Science"},
    {"slug": "cbse10-real-numbers", "title": "Real Numbers for CBSE Class 10 Maths: Euclid's Division Lemma Explained", "subject": "Maths"},
    {"slug": "cbse10-polynomials", "title": "Polynomials for CBSE Class 10 Maths: Zeroes and Coefficient Relations", "subject": "Maths"},
    {"slug": "cbse10-pair-of-linear-equations", "title": "Pair of Linear Equations in Two Variables for CBSE Class 10: Complete Guide", "subject": "Maths"},
    {"slug": "cbse10-quadratic-equations", "title": "Quadratic Equations for CBSE Class 10: Factorisation and Formula Method", "subject": "Maths"},
    {"slug": "cbse10-arithmetic-progressions", "title": "Arithmetic Progressions for CBSE Class 10: Nth Term and Sum Formulas", "subject": "Maths"},
    {"slug": "cbse10-triangles", "title": "Triangles for CBSE Class 10: Similarity Theorems with Proofs", "subject": "Maths"},
    {"slug": "cbse10-coordinate-geometry", "title": "Coordinate Geometry for CBSE Class 10: Distance and Section Formula", "subject": "Maths"},
    {"slug": "cbse10-introduction-to-trigonometry", "title": "Introduction to Trigonometry for CBSE Class 10: Ratios and Identities", "subject": "Maths"},
    {"slug": "cbse10-applications-of-trigonometry", "title": "Some Applications of Trigonometry for CBSE Class 10: Heights and Distances", "subject": "Maths"},
    {"slug": "cbse10-circles", "title": "Circles for CBSE Class 10: Tangent Theorems and Proofs Explained", "subject": "Maths"},
    {"slug": "cbse10-areas-related-to-circles", "title": "Areas Related to Circles for CBSE Class 10: Sector and Segment Formulas", "subject": "Maths"},
    {"slug": "cbse10-surface-areas-and-volumes", "title": "Surface Areas and Volumes for CBSE Class 10: Combined Solids Guide", "subject": "Maths"},
    {"slug": "cbse10-statistics", "title": "Statistics for CBSE Class 10: Mean, Median and Mode by Grouped Data", "subject": "Maths"},
    {"slug": "cbse10-probability", "title": "Probability for CBSE Class 10: Complete Chapter Guide with Examples", "subject": "Maths"},
    {"slug": "cbse10-nationalism-in-europe", "title": "The Rise of Nationalism in Europe for CBSE Class 10 History: Key Notes", "subject": "History"},
    {"slug": "cbse10-nationalism-in-india", "title": "Nationalism in India for CBSE Class 10 History: Gandhi and Key Movements", "subject": "History"},
    {"slug": "cbse10-making-of-global-world", "title": "The Making of a Global World for CBSE Class 10: Complete Chapter Guide", "subject": "History"},
    {"slug": "cbse10-age-of-industrialisation", "title": "The Age of Industrialisation for CBSE Class 10: Key Concepts Explained", "subject": "History"},
    {"slug": "cbse10-print-culture-and-modern-world", "title": "Print Culture and the Modern World for CBSE Class 10: Chapter Summary", "subject": "History"},
    {"slug": "cbse10-resources-and-development", "title": "Resources and Development for CBSE Class 10 Geography: Complete Notes", "subject": "Geography"},
    {"slug": "cbse10-forest-and-wildlife-resources", "title": "Forest and Wildlife Resources for CBSE Class 10: Conservation Explained", "subject": "Geography"},
    {"slug": "cbse10-water-resources", "title": "Water Resources for CBSE Class 10 Geography: Dams and Rainwater Harvesting", "subject": "Geography"},
    {"slug": "cbse10-agriculture", "title": "Agriculture for CBSE Class 10 Geography: Cropping Patterns Explained", "subject": "Geography"},
    {"slug": "cbse10-minerals-and-energy-resources", "title": "Minerals and Energy Resources for CBSE Class 10: Complete Chapter Guide", "subject": "Geography"},
    {"slug": "cbse10-manufacturing-industries", "title": "Manufacturing Industries for CBSE Class 10 Geography: Key Notes", "subject": "Geography"},
    {"slug": "cbse10-lifelines-of-national-economy", "title": "Lifelines of National Economy for CBSE Class 10: Transport and Trade", "subject": "Geography"},
    {"slug": "cbse10-power-sharing", "title": "Power Sharing for CBSE Class 10 Civics: Belgium and Sri Lanka Case Studies", "subject": "Civics"},
    {"slug": "cbse10-federalism", "title": "Federalism for CBSE Class 10 Civics: Indian Federal System Explained", "subject": "Civics"},
    {"slug": "cbse10-political-parties", "title": "Political Parties for CBSE Class 10 Civics: Functions and Challenges", "subject": "Civics"},
    {"slug": "cbse10-outcomes-of-democracy", "title": "Outcomes of Democracy for CBSE Class 10 Civics: Complete Chapter Guide", "subject": "Civics"},
    {"slug": "cbse10-development", "title": "Development for CBSE Class 10 Economics: Income and Other Criteria", "subject": "Economics"},
    {"slug": "cbse10-sectors-of-the-indian-economy", "title": "Sectors of the Indian Economy for CBSE Class 10: Complete Chapter Guide", "subject": "Economics"},
    {"slug": "cbse10-money-and-credit", "title": "Money and Credit for CBSE Class 10 Economics: Key Concepts Explained", "subject": "Economics"},
    {"slug": "cbse10-globalisation-and-indian-economy", "title": "Globalisation and the Indian Economy for CBSE Class 10: Chapter Notes", "subject": "Economics"},
    {"slug": "cbse10-board-exam-strategy", "title": "CBSE Class 10 Board Exam Strategy: Last 90 Days Study Plan That Works", "subject": "Strategy"},
    {"slug": "cbse10-how-to-score-95-percent", "title": "How to Score 95%+ in CBSE Class 10 Boards: A Realistic Study Plan", "subject": "Strategy"},
]


def get_today_topic():
    day = datetime.now().timetuple().tm_yday
    return TOPICS[day % len(TOPICS)]


def generate_article_html(topic):
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    today = datetime.now().strftime("%B %d, %Y")
    slug = topic["slug"]
    title = topic["title"]
    subject = topic["subject"]

    prompt = (
        "Write a complete, standalone HTML article page for cbseclass10.com, "
        "a CBSE Class 10 board exam study resource site.\n\n"
        f"Topic: {title}\n"
        f"Subject: {subject}\n"
        f"Slug: {slug}\n"
        f"Date: {today}\n\n"
        "Requirements:\n"
        f"- Title tag: {title} | CBSEClass10\n"
        "- Add a compelling 140-155 char meta description\n"
        f"- Canonical URL: https://cbseclass10.com/{slug}.html\n"
        "- Include Google Fonts 'Outfit' link\n"
        "- Nav with links back to /\n"
        "- Article hero section with dark purple gradient background (#2E1065 to #5B21B6), subject tag badge, h1 title, date\n"
        "- Body: 800-1100 words, NCERT-grounded, board-exam-specific content for a CBSE Class 10 student\n"
        "- 3-4 H2 sections with specific NCERT chapter references and exam patterns\n"
        "- 1 highlight-box (background #F5F3FF, left border #7C3AED) with a key tip or common mistake\n"
        "- 1 CTA box linking to https://padhle.in mentioning Padhle Yoddha (Rs.2,000-3,000 mass batch for Class 9-10, daily live classes, study material) as the recommended coaching option\n"
        "- Footer mentioning Padhle Yoddha as the recommended affordable coaching\n"
        "- All inline styles as needed, purple theme (#5B21B6, #7C3AED)\n\n"
        "Return ONLY the complete HTML. No markdown fences, no commentary."
    )

    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=4096,
        messages=[{"role": "user", "content": prompt}],
    )

    html = message.content[0].text.strip()
    for fence in ["```html", "```"]:
        if html.startswith(fence):
            html = html[len(fence):]
    if html.endswith("```"):
        html = html[:-3]
    return html.strip()


def main():
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("ERROR: ANTHROPIC_API_KEY not set.")
        sys.exit(1)

    topic = get_today_topic()
    filename = f"{topic['slug']}.html"
    today_str = datetime.now().strftime("%Y-%m-%d")

    print(f"Topic: {topic['title']}")
    print(f"Output: {filename}")

    if os.path.exists(filename):
        print(f"{filename} already exists - skipping.")
        sys.exit(0)

    print("Calling Claude API...")
    html = generate_article_html(topic)
    html = add_byline(html, datetime.now().strftime("%B %d, %Y"))

    url = f"https://{DOMAIN}/{filename}"
    title = topic["title"]
    description = su.extract_description(html, title)

    tagged_html = su.publish_article(
        article_html=html, site_name=SITE_NAME, domain=DOMAIN,
        canonical_url=url, title=title, description=description,
        date_iso=today_str, category=topic["subject"],
    )

    with open(filename, "w", encoding="utf-8") as f:
        f.write(tagged_html)
    print(f"Saved {filename} ({len(tagged_html):,} bytes)")
    print("SEO tags injected, manifest/sitemap/homepage/archive rebuilt")
    print("Done!")


if __name__ == "__main__":
    main()
