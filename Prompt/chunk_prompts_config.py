"""
================================================================================
📦 CHUNK CREATION PROMPTS CONFIGURATION
================================================================================

This module contains configurable prompts for Llama model to generate chunk
metadata during the chunk creation process (script 3).

Multiple variants available:
- default: Balanced quality and speed
- concise: Quick extraction for large datasets
- detailed: Maximum quality and depth
- multilingual: Language-aware processing
- validation: Quality check for generated chunks

Usage:
    from Prompt.chunk_prompts_config import get_chunk_prompt, CHUNK_SYSTEM_PROMPT
    
    prompt = get_chunk_prompt(text, variant="detailed", source_language="English")
    response = llama.generate(prompt, system_prompt=CHUNK_SYSTEM_PROMPT)
"""

# ============================================================================
# SYSTEM PROMPT FOR CHUNK CREATION
# ============================================================================

CHUNK_SYSTEM_PROMPT = """You are an expert AI assistant specialized in analyzing spiritual and philosophical texts. Your role is to extract structured metadata from text chunks to enable semantic search and RAG (Retrieval Augmented Generation).

Your responsibilities:
- Extract key concepts, themes, and ideas from the text
- Identify meaningful keywords for semantic search
- Select iconic quotes that capture the essence
- Generate natural questions users might ask about this content
- Provide clear, concise summaries
- Maintain spiritual and philosophical depth in your analysis

Output format: Always respond with valid JSON containing the requested metadata fields."""


# ============================================================================
# DEFAULT VARIANT - Balanced quality and speed
# ============================================================================

CHUNK_ANALYSIS_PROMPT = """Analyze the following text chunk and extract structured metadata for a spiritual AI chatbot RAG system.

TEXT TO ANALYZE:
{text}

Extract the following information and respond ONLY with a valid JSON object (no additional text):

{{
  "chunk_title": "Brief descriptive title (5-10 words)",
  "key_concepts": [
    "Concept 1 - clear and specific",
    "Concept 2 - practical and actionable",
    "Concept 3 - spiritual principle",
    "Concept 4 - deeper understanding",
    "Concept 5 - expected outcome"
  ],
  "keywords_primary": [
    "keyword1",
    "keyword2",
    "keyword3",
    "keyword4",
    "keyword5"
  ],
  "keywords_synonyms": {{
    "keyword1": ["synonym1", "synonym2", "synonym3"],
    "keyword2": ["variant1", "variant2"]
  }},
  "iconic_quotes": [
    "Memorable quote 1 from the text",
    "Key quote 2 that captures essence"
  ],
  "qa_pairs": [
    {{
      "question": "Practical question a user might ask about this content?",
      "answer": "COMPREHENSIVE answer (200-400 words) that thoroughly explains the concept, provides deep context, includes practical examples, offers step-by-step guidance, addresses common misconceptions, and links to related concepts. Take all the space needed to truly convey understanding.",
      "difficulty": "beginner/intermediate/advanced",
      "intent": ["understanding_concept", "practical_application"]
    }}
  ],
  "natural_questions": [
    "Question 1 a user might ask about this topic?",
    "Question 2 related to the concepts?",
    "Question 3 about practical application?"
  ],
  "summary": "2-3 sentence summary of the main ideas",
  "domain_metadata": {{}}
}}

CRITICAL INSTRUCTIONS FOR Q&A PAIRS:
- Generate VARIABLE number of Q&A pairs based on content complexity:
  * Simple content (1-2 concepts): Generate 2-3 Q&A pairs
  * Medium content (3-5 concepts): Generate 4-6 Q&A pairs  
  * Complex content (6+ concepts): Generate 6-10 Q&A pairs
- Each Q&A answer should be 200-400 words (comprehensive and thorough)
- Cover ALL major concepts with at least one Q&A each
- Include Q&A for:
  * Conceptual understanding (what/why)
  * Practical application (how to practice)
  * Troubleshooting common issues
  * Advanced/deeper insights
  * Integration with daily life
- Difficulty levels: distribute across beginner, intermediate, advanced
- Make answers COMPLETE - don't summarize, fully explain with examples

IMPORTANT:
- Respond ONLY with valid JSON (no markdown, no explanations)
- Extract 5-7 key concepts
- Provide 5-8 primary keywords
- Include 2-4 iconic quotes directly from the text
- Generate VARIABLE Q&A pairs (2-10 depending on complexity):
  * Each answer must be 200-400 words (comprehensive)
  * Cover every major concept with dedicated Q&A
  * Include beginner, intermediate, and advanced questions
  * Address practical application, troubleshooting, integration
- Generate 3-5 natural questions (short form)
- Keep summary concise but meaningful
- For qa_pairs: QUALITY over fixed quantity - create as many as needed to cover all concepts thoroughly
- For domain_metadata: Analyze the text and extract ONLY domain-specific metadata that is ACTUALLY present and relevant
  * For spiritual/esoteric content: chakra, mantra, element, color, body_location, meditation practices
  * For philosophical content: philosophical_school, key_thinkers, concepts, arguments
  * For historical content: time_period, locations, historical_figures, events
  * For scientific content: scientific_field, theories, experiments, researchers
  * Use empty object {{}} if no specific domain metadata is identifiable
  * NEVER force metadata that isn't clearly present in the text
  * Be flexible and adapt to the actual content type
- Themes should capture the spiritual/personal growth themes (e.g., grounding, self-love, empowerment, intuition)
- Practices should be specific exercises/meditations mentioned in the text"""


# ============================================================================
# CONCISE VARIANT - Quick extraction for large datasets
# ============================================================================

CHUNK_ANALYSIS_CONCISE = """Analyze this text and extract essential metadata. Respond ONLY with valid JSON:

TEXT:
{text}

JSON OUTPUT:
{{
  "chunk_title": "Short title",
  "key_concepts": ["concept1", "concept2", "concept3"],
  "keywords_primary": ["keyword1", "keyword2", "keyword3"],
  "iconic_quotes": ["quote1"],
  "natural_questions": ["question1", "question2"],
  "summary": "One sentence summary"
}}

Keep it minimal but accurate. JSON only, no extra text."""


# ============================================================================
# DETAILED VARIANT - Maximum quality and depth
# ============================================================================

CHUNK_ANALYSIS_DETAILED = """Perform a deep analysis of the following spiritual/philosophical text chunk. Extract comprehensive metadata for advanced RAG retrieval.

TEXT TO ANALYZE:
{text}

SOURCE CONTEXT:
- Language: {source_language}
- Expected depth: Maximum detail and nuance
- Purpose: Training data for spirituality AI chatbot

Extract and respond with ONLY a valid JSON object containing:

{{
  "chunk_title": "Descriptive title capturing the essence (8-15 words)",
  
  "key_concepts": [
    "Concept 1 - foundational principle explained clearly",
    "Concept 2 - practical application with specific details",
    "Concept 3 - spiritual/philosophical insight",
    "Concept 4 - interconnection with other concepts",
    "Concept 5 - deeper layer of understanding",
    "Concept 6 - transformative aspect",
    "Concept 7 - expected results or benefits"
  ],
  
  "keywords_primary": [
    "primary_keyword_1",
    "primary_keyword_2",
    "primary_keyword_3",
    "primary_keyword_4",
    "primary_keyword_5",
    "primary_keyword_6",
    "primary_keyword_7",
    "primary_keyword_8"
  ],
  
  "keywords_synonyms": {{
    "primary_keyword_1": ["synonym1", "synonym2", "synonym3", "synonym4"],
    "primary_keyword_2": ["variant1", "variant2", "variant3"],
    "primary_keyword_3": ["alternative1", "alternative2"]
  }},
  
  "keywords_relations": {{
    "keyword1": ["related_concept1", "related_concept2", "related_concept3"],
    "keyword2": ["connection1", "connection2"]
  }},
  
  "iconic_quotes": [
    "Powerful quote 1 that captures core teaching",
    "Memorable quote 2 with spiritual insight",
    "Impactful quote 3 that inspires transformation",
    "Key phrase 4 that synthesizes principles"
  ],
  
  "key_formulas": [
    "Formula 1 = Concept A + Concept B → Result",
    "Principle 2: Condition → Transformation",
    "Process 3: Input × Action = Output"
  ],
  
  "natural_questions": [
    "Deep question 1 about the core teaching?",
    "Practical question 2 about application?",
    "Philosophical question 3 about meaning?",
    "Transformative question 4 about personal growth?",
    "Integration question 5 about daily life?"
  ],
  
  "themes": [
    "primary_theme",
    "secondary_theme",
    "tertiary_theme"
  ],
  
  "difficulty_level": "beginner|intermediate|advanced",
  
  "tone": "instructional|contemplative|inspirational|practical",
  
  "prerequisites": [
    "Concept or knowledge needed to understand this",
    "Background understanding helpful"
  ],
  
  "natural_followup": [
    "Topic that naturally follows from this",
    "Related concept to explore next"
  ],
  
  "summary": "Comprehensive 3-5 sentence summary capturing the full depth and nuance of the text, including key teachings, practical applications, and transformative potential."
}}

CRITICAL REQUIREMENTS:
- Extract 7-10 key concepts with detailed descriptions
- Provide 6-10 primary keywords
- Include 3-5 synonyms for each main keyword
- Map semantic relationships between keywords
- Select 3-5 most powerful quotes from the text
- Create 3-5 key formulas/principles synthesizing the teachings
- Generate 5-7 diverse natural questions (deep, practical, philosophical)
- Identify 2-4 main themes
- Assess difficulty level and tone
- Note prerequisites and natural follow-up topics
- Write comprehensive summary (3-5 sentences)
- RESPOND ONLY WITH VALID JSON - no markdown, no explanations"""


# ============================================================================
# MULTILINGUAL VARIANT - Language-aware processing
# ============================================================================

CHUNK_ANALYSIS_MULTILINGUAL = """Analyze this text chunk with language-aware processing. The source language is: {source_language}

TEXT TO ANALYZE:
{text}

Extract metadata in ENGLISH (for consistent database), but preserve cultural and linguistic nuances from the original language.

Respond ONLY with valid JSON:

{{
  "chunk_title": "Title in English",
  "source_language": "{source_language}",
  "key_concepts": [
    "Concept 1 (with cultural context if relevant)",
    "Concept 2",
    "Concept 3",
    "Concept 4",
    "Concept 5"
  ],
  "keywords_primary": [
    "english_keyword_1",
    "english_keyword_2",
    "english_keyword_3",
    "english_keyword_4",
    "english_keyword_5"
  ],
  "keywords_original_language": [
    "original_term_1_if_significant",
    "original_term_2_if_untranslatable"
  ],
  "iconic_quotes": [
    "Quote 1 in English (preserve meaning)",
    "Quote 2 in English"
  ],
  "natural_questions": [
    "Question 1 in English?",
    "Question 2 in English?",
    "Question 3 in English?"
  ],
  "cultural_notes": "Brief note about cultural or linguistic context if relevant",
  "summary": "2-3 sentence summary in English"
}}

IMPORTANT:
- ALL extracted content must be in ENGLISH for database consistency
- Preserve cultural context and nuances in descriptions
- Include original language terms only if they're significant/untranslatable
- Respond ONLY with JSON (no markdown, no extra text)"""


# ============================================================================
# VALIDATION VARIANT - Quality check for generated chunks
# ============================================================================

CHUNK_VALIDATION_PROMPT = """Analyze this generated chunk and validate its quality for a spiritual AI RAG system.

CHUNK TO VALIDATE:
{text}

VALIDATION CRITERIA:
1. Completeness: All required fields present?
2. Accuracy: Metadata correctly extracted from source?
3. Clarity: Concepts and keywords clear and specific?
4. Relevance: Content appropriate for spiritual chatbot?
5. Quality: Quotes meaningful, questions natural, summary comprehensive?

Respond ONLY with valid JSON:

{{
  "is_valid": true/false,
  "completeness_score": 0-100,
  "accuracy_score": 0-100,
  "clarity_score": 0-100,
  "relevance_score": 0-100,
  "quality_score": 0-100,
  "overall_score": 0-100,
  "issues": [
    "Issue 1 description if any",
    "Issue 2 description if any"
  ],
  "suggestions": [
    "Suggestion 1 for improvement",
    "Suggestion 2 for improvement"
  ],
  "validation_summary": "Brief assessment of the chunk quality"
}}

Respond ONLY with JSON (no markdown, no extra text)."""


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_chunk_prompt(text: str, variant: str = "default", source_language: str = "English") -> str:
    """
    Get the appropriate chunk analysis prompt based on variant.
    
    Args:
        text: The text chunk to analyze
        variant: Prompt variant to use:
            - "default": Balanced quality and speed
            - "concise": Quick extraction
            - "detailed": Maximum quality
            - "multilingual": Language-aware
        source_language: Source language for multilingual variant (default: "English")
    
    Returns:
        Formatted prompt string ready for Llama model
    
    Raises:
        ValueError: If variant is not recognized
    """
    prompts = {
        "default": CHUNK_ANALYSIS_PROMPT,
        "concise": CHUNK_ANALYSIS_CONCISE,
        "detailed": CHUNK_ANALYSIS_DETAILED,
        "multilingual": CHUNK_ANALYSIS_MULTILINGUAL
    }
    
    if variant not in prompts:
        raise ValueError(
            f"Unknown variant '{variant}'. "
            f"Valid options: {', '.join(prompts.keys())}"
        )
    
    prompt_template = prompts[variant]
    
    # Format prompt with text and language
    if "{source_language}" in prompt_template:
        return prompt_template.format(text=text, source_language=source_language)
    else:
        return prompt_template.format(text=text)


def get_validation_prompt(chunk_text: str) -> str:
    """
    Get validation prompt for quality checking a generated chunk.
    
    Args:
        chunk_text: The generated chunk JSON to validate
    
    Returns:
        Formatted validation prompt
    """
    return CHUNK_VALIDATION_PROMPT.format(text=chunk_text)


def get_available_variants() -> list:
    """
    Get list of available prompt variants.
    
    Returns:
        List of variant names
    """
    return ["default", "concise", "detailed", "multilingual"]


def get_variant_description(variant: str) -> str:
    """
    Get description of a specific prompt variant.
    
    Args:
        variant: Variant name
    
    Returns:
        Human-readable description
    
    Raises:
        ValueError: If variant is not recognized
    """
    descriptions = {
        "default": "Balanced quality and speed - suitable for most use cases",
        "concise": "Quick extraction - minimal metadata for large datasets",
        "detailed": "Maximum quality - comprehensive metadata with depth",
        "multilingual": "Language-aware - preserves cultural context"
    }
    
    if variant not in descriptions:
        raise ValueError(
            f"Unknown variant '{variant}'. "
            f"Valid options: {', '.join(descriptions.keys())}"
        )
    
    return descriptions[variant]


# ============================================================================
# SEMANTIC CHUNKING - AI identifies natural breakpoints
# ============================================================================

SEMANTIC_CHUNKING_SYSTEM_PROMPT = """You are an expert at analyzing text structure and identifying natural semantic boundaries. You understand topic transitions, conceptual shifts, and logical flow in diverse content types."""

SEMANTIC_CHUNKING_PROMPT = """Analyze the following text and identify natural breakpoints where topics, concepts, or themes change significantly.

TEXT TO ANALYZE:
{text}

Your task:
1. Read the entire text carefully
2. Identify natural semantic boundaries where:
   - A new major topic/concept begins
   - There's a significant shift in focus or perspective
   - A complete idea/teaching ends and another begins
   - The narrative or argument transitions naturally
3. Consider optimal chunk size: aim for 400-1000 words per chunk, but PRIORITIZE semantic coherence over strict size
4. Each chunk should be self-contained and meaningful on its own

Respond ONLY with a JSON array of breakpoint positions (paragraph numbers, 0-indexed):

{{
  "breakpoints": [3, 7, 12, 18],
  "reasoning": [
    "Paragraph 3: Transition from introduction to first main concept",
    "Paragraph 7: Shift from theory to practical application",
    "Paragraph 12: New topic about meditation techniques begins",
    "Paragraph 18: Conclusion and integration section starts"
  ]
}}

IMPORTANT:
- Respond ONLY with valid JSON
- Breakpoints are paragraph indices (0-based)
- Include brief reasoning for each breakpoint
- If text is short (<500 words), return empty breakpoints: {{"breakpoints": [], "reasoning": ["Text is cohesive as single chunk"]}}
- If text is very long, don't create too many tiny chunks - aim for meaningful, substantial sections"""


# ============================================================================
# MODULE INFO
# ============================================================================

__all__ = [
    'CHUNK_SYSTEM_PROMPT',
    'CHUNK_ANALYSIS_PROMPT',
    'CHUNK_ANALYSIS_CONCISE',
    'CHUNK_ANALYSIS_DETAILED',
    'CHUNK_ANALYSIS_MULTILINGUAL',
    'CHUNK_VALIDATION_PROMPT',
    'SEMANTIC_CHUNKING_SYSTEM_PROMPT',
    'SEMANTIC_CHUNKING_PROMPT',
    'get_chunk_prompt',
    'get_validation_prompt',
    'get_available_variants',
    'get_variant_description'
]

__version__ = '1.0.0'
__author__ = 'Spirituality.AI Team'
