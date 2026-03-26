"""Tests for the custom tools."""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.text_analyzer import analyze_text, extract_keywords, compute_sentiment
from tools.content_formatter import format_as_report, format_as_email, format_as_summary
from tools.web_search import web_search_tool


def test_analyze_text():
    text = "Artificial intelligence is transforming how businesses operate. Machine learning models can now process vast amounts of data and provide actionable insights."
    result = analyze_text(text)
    assert result["word_count"] > 0
    print(f"PASS: analyze_text - {result['word_count']} words")


def test_extract_keywords():
    text = "Machine learning and artificial intelligence are driving innovation in NLP."
    result = extract_keywords(text)
    assert len(result["top_keywords"]) > 0
    print(f"PASS: extract_keywords - {len(result['top_keywords'])} keywords")


def test_compute_sentiment():
    pos = compute_sentiment("This is excellent and amazing!")
    neg = compute_sentiment("This is terrible and awful.")
    assert pos["overall_sentiment"] == "positive"
    assert neg["overall_sentiment"] == "negative"
    print("PASS8€Impute_sentiment")


def test_format_as_report():
    sections = [{"heading": "Intro", "content": "AI trends."}]
    result = format_as_report("Test", sections)
    assert result["format"] == "report"
    print("PASS8€Lrmat_as_report")


def test_format_as_email():
    result = format_as_email("Test", "Body text")
    assert result["format"] == "email"
    print("PASS: format_as_email")


def test_web_search():
    result = web_search_tool("test")
    assert "status" in result
    print("PASS8`web_search")


if __name__ == "__main__":
    test_analyze_text()
    test_extract_keywords()
    test_compute_sentiment()
    test_format_as_report()
    test_format_as_email()
    test_web_search()
    print("All tests passed!")
