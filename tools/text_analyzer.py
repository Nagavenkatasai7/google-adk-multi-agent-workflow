"""Text analysis tools for the analysis agent."""
import re
from collections import Counter
from typing import Optional


def analyze_text(text: str) -> dict:
    """Analyze text and return statistics and metrics.

    Computes word count, sentence count, average sentence length,
    reading level estimate, and key phrases.

    Args:
        text: The text to analyze.

    Returns:
        dict: Analysis results including word count, sentence count,
              readability metrics, and key statistics.
    """
    words = text.split()
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]

    word_count = len(words)
    sentence_count = len(sentences)
    paragraph_count = len(paragraphs)
    avg_sentence_length = word_count / max(sentence_count, 1)

    # Simple readability estimate (Flesch-Kincaid approximation)
    syllable_count = sum(_count_syllables(w) for w in words)
    avg_syllables = syllable_count / max(word_count, 1)

    # Flesch Reading Ease (simplified)
    reading_ease = 206.835 - (1.015 * avg_sentence_length) - (84.6 * avg_syllables)
    reading_ease = max(0, min(100, reading_ease))

    return {
        "word_count": word_count,
        "sentence_count": sentence_count,
        "paragraph_count": paragraph_count,
        "avg_sentence_length": round(avg_sentence_length, 1),
        "avg_syllables_per_word": round(avg_syllables, 2),
        "reading_ease_score": round(reading_ease, 1),
        "reading_level": _get_reading_level(reading_ease),
        "estimated_read_time_minutes": round(word_count / 200, 1),
    }


def extract_keywords(text: str, top_n: int = 10) -> dict:
    """Extract the most important keywords from text.

    Uses frequency analysis with stopword filtering to identify
    the most relevant terms in the text.

    Args:
        text: The text to extract keywords from.
        top_n: Number of top keywords to return (default: 10).

    Returns:
        dict: Top keywords with their frequency counts.
    """
    stopwords = {
        "the", "a", "an", "is", "are", "was", "were", "be", "been",
        "being", "have", "has", "had", "do", "does", "did", "will",
        "would", "could", "should", "may", "might", "shall", "can",
        "to", "of", "in", "for", "on", "with", "at", "by", "from",
        "as", "into", "through", "during", "before", "after", "above",
        "below", "between", "out", "off", "over", "under", "again",
        "further", "then", "once", "here", "there", "when", "where",
        "why", "how", "all", "each", "every", "both", "few", "more",
        "most", "other", "some", "such", "no", "nor", "not", "only",
        "own", "same", "so", "than", "too", "very", "just", "because",
        "but", "and", "or", "if", "while", "about", "it", "its",
        "this", "that", "these", "those", "i", "me", "my", "we",
        "our", "you", "your", "he", "him", "his", "she", "her",
        "they", "them", "their", "what", "which", "who", "whom",
    }

    words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
    filtered = [w for w in words if w not in stopwords]
    counts = Counter(filtered)

    keywords = [
        {"keyword": word, "count": count}
        for word, count in counts.most_common(top_n)
    ]

    return {
        "total_unique_words": len(set(filtered)),
        "top_keywords": keywords,
    }


def compute_sentiment(text: str) -> dict:
    """Compute a basic sentiment analysis of the text.

    Uses a lexicon-based approach to estimate positive, negative,
    and neutral sentiment of the input text.

    Args:
        text: The text to analyze sentiment for.

    Returns:
        dict: Sentiment scores and overall classification.
    """
    positive_words = {
        "good", "great", "excellent", "amazing", "wonderful", "fantastic",
        "positive", "success", "successful", "benefit", "improve", "growth",
        "innovative", "efficient", "effective", "advantage", "opportunity",
        "strong", "powerful", "breakthrough", "progress", "gain", "profit",
        "best", "better", "outstanding", "remarkable", "impressive", "superior",
    }
    negative_words = {
        "bad", "poor", "terrible", "awful", "horrible", "negative",
        "failure", "fail", "loss", "decline", "decrease", "risk",
        "problem", "issue", "challenge", "threat", "weakness", "danger",
        "worse", "worst", "inferior", "disappointing", "concerning",
        "costly", "expensive", "difficult", "complex", "slow", "limited",
    }

    words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
    total = len(words) if words else 1

    pos_count = sum(1 for w in words if w in positive_words)
    neg_count = sum(1 for w in words if w in negative_words)
    neu_count = total - pos_count - neg_count

    pos_score = round(pos_count / total, 3)
    neg_score = round(neg_count / total, 3)
    neu_score = round(neu_count / total, 3)

    if pos_score > neg_score * 1.5:
        overall = "positive"
    elif neg_score > pos_score * 1.5:
        overall = "negative"
    else:
        overall = "neutral"

    return {
        "positive_score": pos_score,
        "negative_score": neg_score,
        "neutral_score": neu_score,
        "overall_sentiment": overall,
        "positive_word_count": pos_count,
        "negative_word_count": neg_count,
    }


def _count_syllables(word: str) -> int:
    """Estimate syllable count for a word."""
    word = word.lower().strip()
    if len(word) <= 3:
        return 1
    vowels = "aeiouy"
    count = 0
    prev_vowel = False
    for char in word:
        is_vowel = char in vowels
        if is_vowel and not prev_vowel:
            count += 1
        prev_vowel = is_vowel
    if word.endswith("e"):
        count -= 1
    return max(1, count)


def _get_reading_level(score: float) -> str:
    """Convert Flesch Reading Ease score to reading level."""
    if score >= 90:
        return "Very Easy (5th grade)"
    elif score >= 80:
        return "Easy (6th grade)"
    elif score >= 70:
        return "Fairly Easy (7th grade)"
    elif score >= 60:
        return "Standard (8th-9th grade)"
    elif score >= 50:
        return "Fairly Difficult (10th-12th grade)"
    elif score >= 30:
        return "Difficult (College level)"
    else:
        return "Very Difficult (Graduate level)"
