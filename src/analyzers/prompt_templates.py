"""Prompt templates for Claude AI analysis."""


DETAILED_ANALYSIS_PROMPT = """You are a professional research analyst. Analyze the following collected data about "{topic}" and provide a comprehensive research analysis.

# Collected Data

{data_summary}

# Your Task

Analyze this data and provide:

1. **Executive Summary** (3-5 sentences)
   - Synthesize the most important findings
   - Highlight key trends and patterns

2. **Key Insights** (3-5 major insights)
   - For each insight, provide:
     - What was discovered
     - Supporting evidence from the data
     - Why it matters

3. **Detailed Analysis by Theme**
   - Identify 3-5 main themes/categories in the data
   - For each theme:
     - Summarize the main points
     - List key sources and their contributions
     - Analyze the significance

4. **Opinion Analysis**
   - Mainstream opinions: What do most sources agree on?
   - Contrasting opinions: What disagreements or alternative viewpoints exist?
   - Identify any notable gaps or missing perspectives

5. **Conclusion and Recommendations**
   - Overall conclusions based on the analysis
   - Suggested next steps or areas for further research

# Guidelines

- Be objective and evidence-based
- Cite specific sources when making claims
- Identify patterns and trends across multiple sources
- Note any contradictions or inconsistencies
- Focus on actionable insights
- Use clear, professional language
- Avoid speculation without evidence

Please provide your analysis in a structured format that can be easily converted to Markdown."""


QUICK_ANALYSIS_PROMPT = """You are a research analyst. Provide a quick analysis of the following data about "{topic}".

# Collected Data

{data_summary}

# Your Task

Provide a concise analysis including:

1. **Executive Summary** (2-3 sentences)
   - Main takeaway from the data

2. **Top 3 Key Findings**
   - Brief bullet points with supporting evidence

3. **Main Trend**
   - What's the dominant pattern or theme?

4. **Notable Points**
   - Any surprising or important information

Keep your analysis focused and actionable. Cite specific sources when relevant."""


def get_analysis_prompt(topic: str, data_items: list, depth: str = "detailed") -> str:
    """
    Generate analysis prompt based on collected data.

    Args:
        topic: Research topic
        data_items: List of collected data items
        depth: Analysis depth (quick or detailed)

    Returns:
        Formatted prompt string
    """
    # Format data summary
    data_summary = _format_data_summary(data_items)

    # Select appropriate prompt template
    template = DETAILED_ANALYSIS_PROMPT if depth == "detailed" else QUICK_ANALYSIS_PROMPT

    return template.format(topic=topic, data_summary=data_summary)


def _format_data_summary(data_items: list) -> str:
    """
    Format collected data items into a readable summary.

    Args:
        data_items: List of data items from collectors

    Returns:
        Formatted data summary string
    """
    if not data_items:
        return "No data collected."

    # Group by source
    x_items = [item for item in data_items if item.get("source") == "x"]
    web_items = [item for item in data_items if item.get("source") == "web"]

    summary_parts = []

    # Format X data
    if x_items:
        summary_parts.append(f"## X (Twitter) Posts ({len(x_items)} items)\n")
        for i, item in enumerate(x_items[:50], 1):  # Limit to first 50 to avoid token limit
            author = item.get("author", "Unknown")
            content = item.get("content", "")[:300]  # Truncate long content
            date = item.get("date", "")
            likes = item.get("engagement", {}).get("likes", 0)

            summary_parts.append(
                f"{i}. **@{author}** ({date})\n"
                f"   {content}\n"
                f"   [Likes: {likes}]\n"
            )

    # Format Web data
    if web_items:
        summary_parts.append(f"\n## Web Results ({len(web_items)} items)\n")
        for i, item in enumerate(web_items[:50], 1):  # Limit to first 50
            title = item.get("title", "Untitled")
            content = item.get("content", "")[:300]  # Truncate
            author = item.get("author", "Unknown")
            url = item.get("url", "")

            summary_parts.append(
                f"{i}. **{title}**\n"
                f"   Source: {author}\n"
                f"   {content}\n"
                f"   URL: {url}\n"
            )

    return "\n".join(summary_parts)
