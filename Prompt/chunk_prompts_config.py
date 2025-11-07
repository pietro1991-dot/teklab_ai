"""
================================================================================
📦 CHUNK CREATION PROMPTS CONFIGURATION - TEKLAB AI
================================================================================

This module contains configurable prompts for Llama model to generate chunk
metadata for Teklab industrial products (liquid level sensors and controllers).

Multiple variants available:
- default: Balanced quality and speed for technical documentation
- concise: Quick extraction for product catalogs
- detailed: Maximum quality for technical specifications
- multilingual: Multi-language product documentation
- validation: Quality check for generated chunks

Usage:
    from Prompt.chunk_prompts_config import get_chunk_prompt, CHUNK_SYSTEM_PROMPT
    
    prompt = get_chunk_prompt(text, variant="detailed", source_language="English")
    response = llama.generate(prompt, system_prompt=CHUNK_SYSTEM_PROMPT)
"""

# ============================================================================
# SYSTEM PROMPT FOR CHUNK CREATION - TEKLAB PRODUCTS
# ============================================================================

CHUNK_SYSTEM_PROMPT = """You are an expert TECHNICAL SALES ASSISTANT for Teklab, a leading manufacturer of liquid level sensors and controllers for industrial refrigeration and air conditioning applications.

Your role is to extract structured metadata from technical product documentation to enable semantic search and RAG (Retrieval Augmented Generation) for a B2B chatbot.

Your responsibilities:
- Extract product specifications, technical parameters, and application details
- Identify industry-standard keywords and technical terminology
- Select key technical quotes that define product capabilities
- Generate practical questions engineers and buyers might ask
- Provide clear, accurate summaries of technical content
- Maintain technical accuracy and precision in all metadata

Focus areas:
- Product models: TK1+, TK3+, TK4, LC-PS, LC-PH, LC-XP, LC-XT, K25, Rotalock
- Technical specs: Pressure ranges, temperature limits, refrigerant compatibility
- Features: MODBUS, ATEX certification, accuracy, response time, IP rating
- Applications: Compressors, evaporators, refrigeration systems, HVAC

Output format: Always respond with valid JSON containing the requested metadata fields."""


# ============================================================================
# DEFAULT VARIANT - Balanced quality and speed for TEKLAB PRODUCTS
# ============================================================================

CHUNK_ANALYSIS_PROMPT = """Analyze the following technical product documentation from Teklab and extract structured metadata for a B2B RAG chatbot system.

TECHNICAL TEXT TO ANALYZE:
{text}

Extract the following information and respond ONLY with a valid JSON object (no additional text):

{{
  "chunk_title": "Product/topic title (e.g., 'TK3+ 130bar CO2 Oil Level Controller')",
  "key_concepts": [
    "Primary product feature or specification",
    "Key technical parameter or capability",
    "Main application or use case",
    "Important compatibility or standard",
    "Critical performance characteristic"
  ],
  "keywords_primary": [
    "product_model (e.g., TK3+, LC-PS)",
    "pressure_range (e.g., 130bar, 0-600bar)",
    "temperature (e.g., -40°C, +125°C)",
    "feature (e.g., MODBUS, ATEX)",
    "application (e.g., compressor, refrigeration)"
  ],
  "keywords_synonyms": {{
    "TK3+": ["TK3 plus", "TK3-plus", "TK 3+"],
    "MODBUS": ["Modbus RTU", "Modbus protocol"],
    "oil level": ["oil management", "lubrication control"]
  }},
  "iconic_quotes": [
    "Key technical specification or feature from the text",
    "Important application note or compatibility detail"
  ],
  "qa_pairs": [
    {{
      "question": "Technical question engineers/buyers might ask (e.g., 'What pressure range does TK3+ 130bar support?')",
      "answer": "COMPREHENSIVE technical answer (200-400 words) that explains specifications, provides application context, includes compatibility details, offers selection guidance, addresses common technical concerns, and references relevant standards or certifications. Be thorough and precise.",
      "difficulty": "beginner/intermediate/advanced",
      "intent": ["product_selection", "technical_specification", "application_design", "troubleshooting"]
    }}
  ],
  "natural_questions": [
    "What is the maximum pressure for [product]?",
    "Which refrigerants are compatible with [model]?",
    "How do I select between TK3+ and TK4?"
  ],
  "summary": "2-3 sentence technical summary of the product/feature",
  "domain_metadata": {{
    "product_family": "TK Series / LC Series / K25 / Rotalock / ATEX",
    "pressure_class": "46bar / 80bar / 130bar / custom",
    "refrigerants": ["R134a", "R404A", "R410A", "CO2", "ammonia"],
    "certifications": ["ATEX", "CE", "UL"],
    "communication": ["MODBUS RTU", "analog 4-20mA", "relay output"],
    "application_type": ["compressor", "evaporator", "separator", "receiver"]
  }}
}}

CRITICAL INSTRUCTIONS FOR TEKLAB TECHNICAL Q&A:
- Generate VARIABLE number of Q&A pairs based on technical complexity:
  * Simple products (basic sensors): 2-3 Q&A pairs
  * Medium products (standard controllers): 4-6 Q&A pairs  
  * Complex products (advanced systems): 6-10 Q&A pairs
- Each Q&A answer should be 200-400 words (comprehensive technical detail)
- Cover ALL major technical aspects with at least one Q&A each
- Include Q&A for:
  * Product specifications (pressure, temperature, accuracy)
  * Application selection (which product for which use case)
  * Installation and wiring (technical setup)
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
- For domain_metadata: Analyze the text and extract ONLY technical metadata that is ACTUALLY present and relevant
  * For Teklab products: pressure_class, refrigerants, certifications, communication protocols, applications
  * For technical specifications: operating ranges, accuracy, response time, materials, standards
  * For installation: mounting, wiring, setup requirements, compatibility
  * Use empty object {{}} if no specific domain metadata is identifiable
  * NEVER force metadata that isn't clearly present in the text
  * Be flexible and adapt to the actual content type
- Applications should capture the industrial use cases (e.g., compressor lubrication, refrigerant level, HVAC systems)
- Features should be specific technical capabilities mentioned in the text"""


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
# DETAILED VARIANT - Maximum quality and depth for TEKLAB PRODUCTS
# ============================================================================

CHUNK_ANALYSIS_DETAILED = """Perform a deep technical analysis of the following Teklab product documentation. Extract comprehensive metadata for advanced B2B RAG retrieval.

TEXT TO ANALYZE:
{text}

SOURCE CONTEXT:
- Language: {source_language}
- Expected depth: Maximum technical detail and precision
- Purpose: Training data for Teklab B2B technical chatbot

Extract and respond with ONLY a valid JSON object containing:

{{
  "chunk_title": "Descriptive product/feature title (8-15 words)",
  
  "key_concepts": [
    "Concept 1 - foundational product specification explained clearly",
    "Concept 2 - practical application with specific installation details",
    "Concept 3 - technical feature or capability",
    "Concept 4 - interconnection with other products or systems",
    "Concept 5 - deeper layer of technical understanding",
    "Concept 6 - competitive advantage or unique aspect",
    "Concept 7 - expected performance or benefits"
  ],
  
  "keywords_primary": [
    "product_model (e.g., TK3+, LC-PS)",
    "pressure_range (e.g., 130bar, 46bar)",
    "temperature_range (e.g., -40°C, +125°C)",
    "communication_protocol (e.g., MODBUS)",
    "certification (e.g., ATEX, CE)",
    "application (e.g., compressor, evaporator)",
    "refrigerant (e.g., R134a, CO2)",
    "feature (e.g., digital output, analog 4-20mA)"
  ],
  
  "keywords_synonyms": {{
    "TK3+": ["TK3 plus", "TK3-plus", "TK 3+", "Teklab TK3+"],
    "MODBUS": ["Modbus RTU", "Modbus protocol", "ModBus communication"],
    "oil level": ["oil management", "lubrication control", "oil regulation"]
  }},
  
  "keywords_relations": {{
    "TK3+": ["oil level regulator", "compressor protection", "130bar capability"],
    "MODBUS": ["digital communication", "BMS integration", "remote monitoring"]
  }},
  
  "iconic_quotes": [
    "Key technical specification that defines product capability",
    "Important compatibility or certification detail",
    "Critical performance metric or accuracy statement",
    "Unique feature or competitive advantage statement"
  ],
  
  "key_formulas": [
    "Operating Range = -40°C to +125°C",
    "Pressure Capability: 46bar / 80bar / 130bar variants",
    "Accuracy: ±X% or ±X mm at specified conditions"
  ],
  
  "natural_questions": [
    "Technical question 1 about product specifications?",
    "Application question 2 about installation or setup?",
    "Selection question 3 about choosing right model?",
    "Compatibility question 4 about system integration?",
    "Performance question 5 about accuracy or reliability?"
  ],
  
  "themes": [
    "product_category (Oil_Level_Regulators, Level_Switches, Sensors)",
    "application_area (refrigeration, HVAC, industrial)",
    "technical_focus (pressure, temperature, communication)"
  ],
  
  "difficulty_level": "beginner|intermediate|advanced",
  
  "tone": "technical|instructional|specification|application-focused",
  
  "prerequisites": [
    "Technical knowledge needed to understand this product",
    "System or application context required"
  ],
  
  "natural_followup": [
    "Related product that naturally follows from this",
    "Related concept to explore next"
  ],
  
  "summary": "Comprehensive 3-5 sentence summary capturing the full depth and nuance of the text, including key teachings, practical applications, and transformative potential."
}}

CRITICAL REQUIREMENTS:
- Extract 7-10 key concepts with detailed descriptions
- Provide 6-10 primary keywords
- Include 3-5 synonyms for each main keyword
- Map semantic relationships between keywords
- Select 3-5 most powerful technical quotes from the text
- Create 3-5 key specifications/parameters defining the product
- Generate 5-7 diverse natural questions (technical, practical, application-focused)
- Identify 2-4 main themes
- Assess difficulty level and tone
- Note prerequisites and natural follow-up topics
- Write comprehensive technical summary (3-5 sentences)
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
# VALIDATION VARIANT - Quality check for generated TEKLAB chunks
# ============================================================================

CHUNK_VALIDATION_PROMPT = """Analyze this generated chunk and validate its quality for a Teklab B2B technical RAG system.

CHUNK TO VALIDATE:
{text}

VALIDATION CRITERIA:
1. Completeness: All required technical fields present (product specs, features, compatibility)?
2. Accuracy: Technical metadata correctly extracted from product documentation?
3. Clarity: Product models, specifications, and features clear and precise?
4. Relevance: Content appropriate for B2B technical chatbot (industrial buyers, engineers)?
5. Quality: Technical quotes meaningful, questions practical, summary comprehensive?

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
    "Issue 1 description if any (e.g., missing pressure specifications)",
    "Issue 2 description if any (e.g., unclear product model reference)"
  ],
  "suggestions": [
    "Suggestion 1 for improvement (e.g., add refrigerant compatibility)",
    "Suggestion 2 for improvement (e.g., clarify MODBUS protocol version)"
  ],
  "validation_summary": "Brief technical assessment of the chunk quality"
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
# SEMANTIC CHUNKING - AI identifies natural breakpoints for TEKLAB PRODUCTS
# ============================================================================

SEMANTIC_CHUNKING_SYSTEM_PROMPT = """You are an expert at analyzing technical product documentation and identifying natural semantic boundaries. You understand product families, specification sections, feature descriptions, and technical flow in industrial B2B catalogs."""

SEMANTIC_CHUNKING_PROMPT = """Analyze the following technical product documentation and identify natural breakpoints where products, specifications, or features change significantly.

TEXT TO ANALYZE:
{text}

Your task:
1. Read the entire technical documentation carefully
2. Identify natural semantic boundaries where:
   - A new product model begins (e.g., TK3+ → TK4)
   - A new pressure class section starts (e.g., 46bar → 80bar → 130bar)
   - Technical specifications change to different category (pressure → temperature → communication)
   - Product family changes (Oil Level Regulators → Level Switches → Sensors)
   - Application context shifts (compressor → evaporator → refrigeration system)
   - A complete feature description ends and another begins
3. Consider optimal chunk size: aim for 400-1000 words per chunk, but PRIORITIZE semantic coherence over strict size
4. Each chunk should be self-contained and meaningful for B2B technical search

Respond ONLY with a JSON array of breakpoint positions (paragraph numbers, 0-indexed):

{{
  "breakpoints": [3, 7, 12, 18],
  "reasoning": [
    "Paragraph 3: Transition from TK3+ specifications to TK4 product line",
    "Paragraph 7: Shift from pressure specs to communication protocols (MODBUS)",
    "Paragraph 12: New product family LC Series level switches begins",
    "Paragraph 18: Application section for compressor integration starts"
  ]
}}

IMPORTANT:
- Respond ONLY with valid JSON
- Breakpoints are paragraph indices (0-based)
- Include brief technical reasoning for each breakpoint
- If text is short (<500 words), return empty breakpoints: {{"breakpoints": [], "reasoning": ["Product description is cohesive as single chunk"]}}
- If text is very long, don't create too many tiny chunks - aim for meaningful product/feature sections
- Prioritize keeping product specifications together (don't split TK3+ 130bar specs across chunks)"""


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

__version__ = '2.0.0'
__author__ = 'Teklab AI Team'
