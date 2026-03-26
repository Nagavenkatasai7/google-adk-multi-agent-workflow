"""Content formatting tools for the writer agent."""
from datetime import datetime


def format_as_report(
    title: str,
    sections: list[dict],
    author: str = "AI Research Team",
    include_toc: bool = True,
) -> dict:
    """Format content as a structured professional report.

    Takes raw content sections and formats them into a clean,
    professional report with optional table of contents.

    Args:
        title: The report title.
        sections: List of dicts with 'heading' and 'content' keys.
        author: Author name for the report header.
        include_toc: Whether to include a table of contents.

    Returns:
        dict: Formatted report with metadata.
    """
    date_str = datetime.now().strftime("%B %d, %Y")

    report_lines = [
        f"# {title}",
        f"**Author:** {author}",
        f"**Date:** {date_str}",
        "",
        "---",
        "",
    ]

    if include_toc and len(sections) > 1:
        report_lines.append("## Table of Contents")
        for i, section in enumerate(sections, 1):
            heading = section.get("heading", f"Section {i}")
            report_lines.append(f"{i}. {heading}")
        report_lines.extend(["", "---", ""])

    for i, section in enumerate(sections, 1):
        heading = section.get("heading", f"Section {i}")
        content = section.get("content", "")
        report_lines.append(f"## {i}. {heading}")
        report_lines.append("")
        report_lines.append(content)
        report_lines.append("")

    report_text = "\n".join(report_lines)

    return {
        "format": "report",
        "title": title,
        "author": author,
        "date": date_str,
        "num_sections": len(sections),
        "word_count": len(report_text.split()),
        "content": report_text,
    }


def format_as_email(
    subject: str,
    body: str,
    recipient: str = "Team",
    tone: str = "professional",
) -> dict:
    """Format content as a professional email.

    Takes raw content and formats it into a clean email structure
    with appropriate greeting, body, and sign-off.

    Args:
        subject: Email subject line.
        body: The main email body content.
        recipient: Name of the recipient or group.
        tone: Tone of the email ('professional', 'casual', 'formal').

    Returns:
        dict: Formatted email with all components.
    """
    greetings = {
        "professional": f"Hi {recipient},",
        "casual": f"Hey {recipient}!",
        "formal": f"Dear {recipient},",
    }
    signoffs = {
        "professional": "Best regards,",
        "casual": "Cheers,",
        "formal": "Sincerely,",
    }

    greeting = greetings.get(tone, greetings["professional"])
    signoff = signoffs.get(tone, signoffs["professional"])

    email_text = f"""Subject: {subject}

{greeting}

{body}

{signoff}
AI Research Team"""

    return {
        "format": "email",
        "subject": subject,
        "recipient": recipient,
        "tone": tone,
        "word_count": len(email_text.split()),
        "content": email_text,
    }


def format_as_summary(
    text: str,
    max_sentences: int = 5,
    style: str = "executive",
) -> dict:
    """Create a formatted summary of the given text.

    Extracts the most important information and presents it
    in a concise, structured format.

    Args:
        text: The text to summarize.
        max_sentences: Maximum number of sentences in summary.
        style: Summary style ('executive', 'bullet', 'narrative').

    Returns:
        dict: Formatted summary with metadata.
    """
    import re
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 20]

    # Simple extractive approach: pick sentences with most keywords
    selected = sentences[:max_sentences]

    if style == "bullet":
        summary_text = "\n".join(f"• {s}." for s in selected)
    elif style == "executive":
        summary_text = "**Executive Summary:**\n\n" + " ".join(f"{s}." for s in selected)
    else:
        summary_text = " ".join(f"{s}." for s in selected)

    return {
        "format": "summary",
        "style": style,
        "original_length": len(text.split()),
        "summary_length": len(summary_text.split()),
        "compression_ratio": round(len(summary_text.split()) / max(len(text.split()), 1), 2),
        "content": summary_text,
    }
