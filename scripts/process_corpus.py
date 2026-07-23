import json
import re
import os
import mishkal.tashkeel

DIALECT_MAPPING = {
    r'\bعايز\b': 'أريد',
    r'\bبدي\b': 'أريد',
    r'\bشلونك\b': 'كيف حالك',
    r'\bإيه\b': 'ماذا',
    r'\bشو\b': 'ماذا',
    r'\bليش\b': 'لماذا',
    r'\bمشان\b': 'من أجل',
    r'\bعشان\b': 'من أجل',
    r'\bكتير\b': 'كثيرا',
    r'\bوايد\b': 'كثيرا',
    r'\bأوي\b': 'جدا',
    r'\bحلو\b': 'جميل',
    r'\bفين\b': 'أين',
    r'\bوين\b': 'أين',
    r'\bإزاي\b': 'كيف',
    r'\bكيف\b': 'كيف',
    r'\bامتى\b': 'متى',
}

def apply_dialect_mapping(text):
    for pattern, replacement in DIALECT_MAPPING.items():
        text = re.sub(pattern, replacement, text)
    return text

def audit_word_limit(text, limit=5):
    # This just splits sentences into segments of 5 words
    words = text.split()
    if len(words) > limit:
        # A simple audit: keep only the first `limit` words.
        # Alternatively, split into multiple short sentences, but the requirement is just "audit sentences against a 5-word limit".
        return " ".join(words[:limit])
    return text

def add_baseline_tashkeel(text):
    voweler = mishkal.tashkeel.TashkeelClass()
    return voweler.tashkeel(text)

def process_story(story):
    processed_story = []
    for sentence in story:
        sentence = apply_dialect_mapping(sentence)
        sentence = audit_word_limit(sentence, limit=5)
        sentence = add_baseline_tashkeel(sentence)
        processed_story.append(sentence)
    return processed_story

def main():
    mock_stories = [
        {"id": 1, "title": "القطة", "content": ["أنا عايز العب", "القطة حلو أوي"]},
        {"id": 2, "title": "الكلب", "content": ["بدي أكل", "الكلب يلعب كتير"]},
        {"id": 3, "title": "العصفور", "content": ["شلونك يا عصفور", "العصفور يطير"]},
        {"id": 4, "title": "السمكة", "content": ["فين السمكة", "السمكة في الماء"]},
        {"id": 5, "title": "الشجرة", "content": ["الشجرة حلوة", "أنا أحب الشجرة"]},
        {"id": 6, "title": "الشمس", "content": ["الشمس تشرق", "الجو حلو"]},
        {"id": 7, "title": "القمر", "content": ["القمر ينير", "الليل جميل"]},
        {"id": 8, "title": "البحر", "content": ["البحر كبير أوي", "أنا عايز أسبح"]},
        {"id": 9, "title": "الجبل", "content": ["الجبل عالي", "أنا أصعد الجبل"]},
        {"id": 10, "title": "الزهرة", "content": ["الزهرة حلوة", "الزهرة حمراء"]}
    ]

    os.makedirs('public/assets/stories', exist_ok=True)

    for story in mock_stories:
        processed_content = process_story(story['content'])
        processed_story = {
            "id": story['id'],
            "title": story['title'],
            "content": processed_content
        }
        
        with open(f"public/assets/stories/story_{story['id']}.json", "w", encoding="utf-8") as f:
            json.dump(processed_story, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    main()
