# Transcription Processing Instructions for Spiritual Teaching Videos

## Purpose
Convert raw video transcriptions (TXT files) from spiritual teaching series into professionally organized Markdown (MD) files with consistent structure, proper formatting, and complete preservation of all spiritual content.

## Important: Series and Speaker Information
- **Series Name, Speaker Name, Vibration, Statement, Chakra, and all daily metadata must be referenced and cross-checked against the GUIDE COURSE file.**
- Use the GUIDE COURSE file as the authoritative source for:
  - Series Name
  - Speaker Name
  - Vibration
  - Statement
  - Chakra
  - Week theme
  - Zodiac sign/cycle
  - Any other daily metadata
- Always use the exact spellings, wording, and capitalization from the GUIDE COURSE file throughout all processed files.

## Step 1: Pre-Processing and Cleaning

### Remove Non-Content Elements
- Delete filler words: "um," "uh," "hmm," "like" (when used as filler)
- Remove non-verbal cues: `[Music]`, `[Applause]`, `[Laughter]`, `foreign`
- Eliminate casual housekeeping: "good morning," "good afternoon," "see you tomorrow" (unless spiritually relevant)
- Remove YouTube/social media references unless directly tied to spiritual practice

### Text Cleanup
1. **Fix fragmented sentences**: Merge broken lines into complete sentences
2. **Add punctuation**: Periods, commas, question marks, exclamation points
3. **Capitalize properly**: First word of sentences, proper nouns, "I"
4. **Create paragraphs**: Group related sentences into logical paragraphs (3-5 sentences each)
5. **Preserve ALL spiritual content**: Never summarize or cut teachings, practices, or explanations

### Language Translation
- **If paragraphs are in Spanish**: Translate them to English while preserving meaning and spiritual terminology
- Keep spiritual terms authentic (e.g., chakra names, mantras, sacred concepts)

---

## Step 2: Content Analysis

### Identify Structural Elements
Analyze the transcript to locate these typical sections:
1. **Introduction**: Welcome, context, day/week information
2. **Core Teaching**: Main spiritual concepts and explanations
3. **Meditation/Alignment**: Guided practice (step-by-step instructions)
4. **Daily Elements**: Vibration, statement, code, chakra focus
5. **Exercise/Homework**: Practical tasks for the day
6. **Closing**: Final insights or farewell (if spiritual)

### Extract Key Information
- Day number
- Chakra focus (from GUIDE COURSE)
- Week theme (mental/emotional/physical, from GUIDE COURSE)
- Zodiac sign or cycle name (from GUIDE COURSE)
- Main topic or theme (from GUIDE COURSE)
- Daily vibration sound (from GUIDE COURSE)
- Daily statement (from GUIDE COURSE)
- Daily code description (from GUIDE COURSE)
- Practice elements (mantra, vibration, statement, from GUIDE COURSE)

---

## Step 3: Markdown Structure Template

### CRITICAL: Optimal Structure for RAG/Chunking Systems

**Why This Structure Matters:**
This specific organizational pattern is optimized for semantic search, vector embeddings, and RAG (Retrieval-Augmented Generation) systems. The structure ensures:

1. **Hierarchical Clarity**: Single main content container ("Core Teaching") with logical subsections allows chunking algorithms to identify semantic boundaries and maintain context across related concepts.

2. **Semantic Cohesion**: Grouping all teaching content under one H2 section prevents fragmentation. When RAG systems retrieve information, they can capture complete conceptual frameworks rather than isolated fragments.

3. **Predictable Section Flow**: Consistent placement of Overview → Core Teaching → Practice → Key Insights → Integration → Q&A trains better embeddings and allows retrieval systems to apply uniform strategies across all documents.

4. **Optimal Chunk Size**: H3 subsections within "Core Teaching" create natural chunking points at ideal sizes (3-6 paragraphs), balancing context preservation with retrieval precision.

5. **Context Preservation**: Related subsections under the same H2 parent maintain semantic relationships in vector space, improving retrieval accuracy for complex spiritual concepts.

**Do NOT deviate from this structure.** Fragmenting content across multiple H2 sections reduces chunking efficiency and retrieval accuracy.

---

### Template Structure

```markdown
---
title: "Day [X] - [Main Theme/Topic]"
author: [Speaker Name]
series: "[Series Name]"
day_number: [X]
source: "[Series Name]"
date_processed: YYYY-MM-DD
document_type: "transcript"
language: "en"

keywords:
  - [keyword 1]
  - [keyword 2]
  - [keyword 3 - 20 keywords total]

practice_elements:
  vibration: "[Sound]"
  statement: "[Daily Statement]"
  chakra: "[Chakra Name]"
  code: "[Code description]"

---

# Day [X] - [Main Theme/Topic]

**Author:** [Speaker Name]  
**Series:** [Series Name]  
**Source:** [Series Name]  

## Daily Practice Elements

- **Chakra Focus:** [Chakra Name]
- **Week Theme:** [Mental/Emotional/Physical Week of Zodiac Sign]
- **Main Topic:** [Topic]
- **Vibration:** `[Sound]`
- **Statement:** `[Daily Statement]`
- **Code:** [Full code description]

---

## Overview

[2-4 paragraphs: Context of the day, connection to series structure, any introductory teachings or guidance for new participants]

---

## Core Teaching

[ALL conceptual/teaching content goes in this single H2 section, organized into logical H3 subsections]

### [Subsection 1 - Main Concept]

[Complete explanation with ALL details preserved. 3-6 paragraphs per subsection.]

### [Subsection 2 - Related Concept]

[Continue with full content, no summarizing]

### [Subsection 3 - Supporting Concept]

[Each subsection should flow logically from the previous one]

### [Continue with additional subsections as needed - typically 5-10 total]

[Historical context, etymology, examples, metaphors - ALL go under "Core Teaching" as H3 subsections]

---

## Practice

[If meditation or alignment practice is present]

### Preparation

[Setup instructions, posture, breathing]

### Main Practice

[COMPLETE step-by-step instructions - every single step preserved]

### Closing

[Grounding, integration, final steps]

---

## Key Insights

[Extract 8-15 direct quotes or key teachings as bullet points - NO bold formatting on these]

- "Quote 1 - impactful phrase from the teaching"
- "Quote 2"
- [Continue...]

---

## Integration

### Daily Exercise

[Homework or practical task for the day]

### Applying This Teaching

[How to use this in daily life, next steps, connections to other teachings]

---

## Q&A

[Create 5-8 Q&A pairs by extracting rhetorical questions or common concerns addressed in the transcript]

### Q: [Question extracted or inferred from content]?

[Answer from the transcript content, properly formatted]

### Q: [Another question]?

[Answer]

[Continue for 5-8 pairs]

---



## Step 4: Writing Guidelines

### Core Teaching Section
- **Use ONLY ONE H2 section titled "Core Teaching"** - do NOT create multiple H2 sections like "Etymology," "Historical Context," "Modern Application," etc.
- **All teaching content must be organized as H3 subsections under "Core Teaching"**
- **Break into logical subsections** based on topic shifts using H3 headers (###)
- **Preserve 100% of content** - reorganize but don't cut
- **Add paragraph breaks** every 3-5 sentences
- **Minimize bold formatting** - use sparingly only for critical terms on first mention
- **Maintain conversational tone** of original speaker
- **Typical structure**: 5-10 H3 subsections covering etymology, history, examples, metaphors, applications - ALL under the single "Core Teaching" H2

### Practice Section
- **Keep subsection names simple**: "Preparation," "Main Practice," "Closing" (not overly specific titles)
- **Number steps** if sequential (1, 2, 3...) within the practice flow
- **Use clear action verbs**: "Close your eyes," "Breathe in," "Recognize"
- **Preserve exact meditation language** including repetitions
- **Keep mantras/statements** exactly as spoken
- **Include all sensory details** (colors, feelings, visualizations)
- **Minimize bold formatting** in practice instructions

### Q&A Generation Rules
1. Look for rhetorical questions in the transcript
2. Identify common objections or concerns addressed
3. Extract "What if..." or "How do..." questions
4. Create questions from explanatory sections
5. Ensure answers come ONLY from transcript content
6. Never invent or add outside information

### Keywords Selection
- Extract 10-20 keywords naturally from content
- Include: main topic, chakra name, spiritual concepts, practices
- Use both single words and short phrases
- Prioritize terms someone might search for
- Include names, locations, dates if significant

### Key Insights Formatting
- **Do NOT use bold formatting** in the Key Insights bullet points
- Extract 8-15 direct quotes or impactful phrases
- Present as simple bullet list without quotation marks unless part of the original quote
- Keep insights concise (1-2 lines each)

---

## Step 5: Quality Checklist

Before finalizing, verify:

- [ ] All filler words removed
- [ ] Complete sentences with proper punctuation
- [ ] ALL spiritual content preserved (90-100% of original)
- [ ] Spanish sections translated to English
- [ ] Consistent paragraph structure (3-5 sentences)
- [ ] All metadata fields filled correctly and cross-checked with GUIDE COURSE file
- [ ] Vibration, statement, author, series, chakra, and other daily metadata match GUIDE COURSE exactly
- [ ] Keywords list has 10-20 items
- [ ] Practice section has complete step-by-step
- [ ] Q&A has 5-8 relevant pairs
- [ ] No invented content - only reorganized original
- [ ] Markdown formatting correct (headers, bold, lists)
- [ ] Code block properly formatted if present
- [ ] **Optimal file length: 300-500 lines** (excluding edge cases for particularly complex or simple days)

---

## Special Considerations

### Handling Incomplete Transcriptions
- If text is heavily fragmented, use context to complete thoughts
- Mark unclear sections with `[unclear]` if meaning cannot be determined
- Never guess at spiritual terms - keep original if uncertain

### Preserving Speaker's Voice
- Keep conversational phrases like "you know," "I mean" if they add authenticity
- Maintain personal examples and stories completely
- Don't formalize too much - balance clarity with authenticity

### Cultural/Spiritual Terms
- Keep original names: Atlantean terms, constellation names, spiritual concepts
- Add brief clarification in parentheses if needed: "Hollac (first cycle in Atlantean)"
- Never translate mantras, vibrations, or sacred sounds

---

## Output Format

- **Output Directory:** `d:\GitHub_puba\spitituality_ai_GPT\Fonti\Autori\Mathias de Stefano\Processati\MD\`
- **Filename Pattern:** `Day_[XXX]_Transcript.md` (use original day number with leading zeros if needed, e.g., Day_001, Day_015, Day_144)
- **File Handling:**
  - **First, check if the file already exists** in the MD directory
  - **If file exists (even if empty):** Overwrite it with the processed content
  - **If file does not exist:** Create a new file with the proper filename
- **Encoding:** UTF-8
- **Line endings:** LF (Unix style)
- **Validation:**
  - Ensure YAML frontmatter is valid
  - Check that all markdown renders correctly
  - Verify file was saved to correct location

---

## Example Transformation

**Before (Raw TXT):**
```
um so frustration we are surrounded by frustration today
in our lives because we are constantly expecting for things
to happen and they don't happen
```

**After (Cleaned MD):**
```markdown
## Core Teaching

### The Nature of Frustration

We are surrounded by frustration today in our lives because we are constantly expecting things to happen, and they don't happen. Frustration comes from the word "fraus," which also originates the word "fraud."
```

---

**Following these instructions will produce consistent, high-quality markdown files optimized for RAG embeddings while preserving the complete spiritual teachings.**
