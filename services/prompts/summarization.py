"""
Prompt templates for document and text summarization tasks
"""

DOCUMENT_SUMMARY_PROMPT = """
You are a skilled document analyst. Please provide a concise, informative summary of the following document.

Instructions:
- Focus on the main purpose and key points
- Identify the document type if possible (report, specification, guide, etc.)
- Highlight important findings, decisions, or recommendations
- Keep the summary to 2-3 paragraphs maximum
- Use clear, professional language
- Format your response using STRICT CommonMark markdown only:
  * Headers: "## Header" (space after ##, NEVER ##Header)
  * Bullet points: "- Item" (dash space only, NEVER "• -" or "• " or "●")
  * Bold text: "**text**" (double asterisks only)
  * Code: "`code`" (backticks only)
  * NO Unicode bullets (•, ●, ◦) - use ASCII dash (-) only
  * NO mixed bullet syntax like "• -" - this breaks rendering
  * Follow CommonMark specification exactly

Document content:
{content}

Please provide a comprehensive summary in markdown format:
"""

TEXT_FILE_SUMMARY_PROMPT = """
You are analyzing a text file. Please provide a clear, structured summary of its contents.

Instructions:
- Identify the file type/purpose if evident (code, configuration, documentation, etc.)
- Summarize the main content and structure
- Note any important technical details or patterns
- Keep the summary concise but informative
- Format your response using STANDARD markdown only:
  * Headers: "## Header" (space after ##)
  * Bullet points: "- Item" (dash space, NOT "• -")
  * Code blocks: "```language" and "```"
  * Follow CommonMark specification exactly

Text content:
{content}

Please provide a structured summary in markdown format:
"""

KEY_FINDINGS_PROMPT = """
You are extracting key findings from a document. Please identify and list the most important points, findings, or conclusions.

Instructions:
- Focus on actionable insights and important facts
- List findings as clear, concise bullet points using markdown formatting
- Prioritize findings by importance
- Include specific details when relevant
- Maximum 8-10 findings
- Use STRICT CommonMark bullet points with **bold** emphasis for key terms:
  * "- Item" (dash space only, NEVER "• -" or "• " or "●")
  * "## Header" (space after ##, NEVER ##Header)
  * NO Unicode bullets (•, ●, ◦) - use ASCII dash (-) only
  * NO mixed bullet syntax like "• -" - this breaks rendering
- Group related findings under subheadings if appropriate

Document content:
{content}

Key findings (in markdown format):
"""

SUMMARY_BY_FILE_TYPE = {
    "pdf": DOCUMENT_SUMMARY_PROMPT,
    "txt": TEXT_FILE_SUMMARY_PROMPT,
    "md": TEXT_FILE_SUMMARY_PROMPT,
    "csv": """
You are analyzing a CSV file. Please provide a summary of its structure and content.

Instructions:
- Identify the number of columns and rows
- Describe the data types and patterns
- Note any interesting trends or outliers
- Mention data quality issues if evident
- Keep the summary focused on data characteristics
- Format your response using markdown with headers, bullet points, and tables where appropriate

CSV content (first 3000 characters):
{content}

Please provide a data summary in markdown format:
""",
    "json": """
You are analyzing a JSON file. Please provide a summary of its structure and content.

Instructions:
- Describe the overall structure and key objects
- Identify main data types and patterns
- Note any important configuration or data values
- Mention the apparent purpose of the JSON
- Keep the summary technical but accessible
- Format your response using markdown with headers, code blocks, and bullet points

JSON content:
{content}

Please provide a structural summary in markdown format:
""",
}


def get_summary_prompt(file_extension: str = None) -> str:
    """Get appropriate summary prompt based on file type."""
    if file_extension and file_extension.lower() in SUMMARY_BY_FILE_TYPE:
        return SUMMARY_BY_FILE_TYPE[file_extension.lower()]
    return DOCUMENT_SUMMARY_PROMPT


def get_key_findings_prompt() -> str:
    """Get the key findings extraction prompt."""
    return KEY_FINDINGS_PROMPT


# JSON Mode Prompts - Structured Output
JSON_SUMMARY_PROMPT = """
You are analyzing a document and must provide a structured summary in JSON format.

CRITICAL FORMATTING RULES:
- Return ONLY valid JSON - no additional text, explanations, or markdown
- Use proper ASCII markdown syntax in your content:
  * For bullet points: Use "- " (dash + space) NEVER "•", "●", or "• -"
  * For headers: Use "## " (hash + space) NEVER "##" without space
  * NO Unicode bullet characters (•, ●, ◦) anywhere in the content
- All text content should be clean and readable

IMPORTANT: key_findings and points MUST be arrays of strings, NOT single strings!

Required JSON structure:
{{
  "title": "Document title or main topic",
  "document_type": "Type of document (report, specification, guide, etc.)",
  "key_findings": [
    "Important finding 1",
    "Important finding 2",
    "Important finding 3"
  ],
  "sections": [
    {{
      "heading": "Section Name",
      "points": [
        "Point 1 about this section",
        "Point 2 about this section"
      ]
    }}
  ]
}}

EXAMPLES OF CORRECT vs INCORRECT:
✓ CORRECT: "key_findings": ["Finding 1", "Finding 2", "Finding 3"]
✗ INCORRECT: "key_findings": "• Finding 1 • Finding 2 • Finding 3"

The content below may be only the first part of a longer document. Do not state or
imply the document's total length, size, page count or number of sections, and do not
describe what you were given as the whole document.

Document content:
{content}

Return only the JSON response:
"""


def get_json_summary_prompt() -> str:
    """Get the JSON mode summary prompt."""
    return JSON_SUMMARY_PROMPT
