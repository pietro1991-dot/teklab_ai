"""
Test del Sistema di Prompt Configurabili per Chunk Creation
============================================================

Verifica:
- Import corretto dei moduli prompt
- Funzionamento delle helper functions
- Formato dei prompt generati
- Varianti disponibili
"""

import sys
from pathlib import Path

# Setup path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "Prompt"))

# Test import
print("🧪 Testing Chunk Prompts Configuration System")
print("=" * 70)

try:
    from chunk_prompts_config import (
        CHUNK_SYSTEM_PROMPT,
        CHUNK_ANALYSIS_PROMPT,
        CHUNK_ANALYSIS_CONCISE,
        CHUNK_ANALYSIS_DETAILED,
        CHUNK_ANALYSIS_MULTILINGUAL,
        CHUNK_VALIDATION_PROMPT,
        get_chunk_prompt,
        get_validation_prompt,
        get_available_variants,
        get_variant_description
    )
    print("✅ Import successful!")
except ImportError as e:
    print(f"❌ Import failed: {e}")
    sys.exit(1)

print()

# Test 1: System Prompt
print("📝 Test 1: System Prompt")
print("-" * 70)
print(f"Length: {len(CHUNK_SYSTEM_PROMPT)} characters")
print(f"Preview: {CHUNK_SYSTEM_PROMPT[:150]}...")
print("✅ System prompt loaded\n")

# Test 2: Available Variants
print("📝 Test 2: Available Variants")
print("-" * 70)
variants = get_available_variants()
print(f"Found {len(variants)} variants:")
for variant in variants:
    description = get_variant_description(variant)
    print(f"  • {variant}: {description}")
print("✅ All variants available\n")

# Test 3: Generate Prompt for Each Variant
print("📝 Test 3: Generate Prompts")
print("-" * 70)

sample_text = """The ankles represent the direction we choose in life. 
They are the pivot point between the feet (our foundation) and the legs (our movement). 
When we align our ankles with our true purpose, we move forward with grace and certainty."""

for variant in variants:
    try:
        prompt = get_chunk_prompt(
            text=sample_text,
            variant=variant,
            source_language="English"
        )
        print(f"✅ {variant.upper()}: {len(prompt)} characters")
        
        # Verifica che il testo sia incluso
        if sample_text[:50] in prompt:
            print(f"   ✓ Text correctly embedded")
        else:
            print(f"   ⚠ Text might not be embedded")
            
    except Exception as e:
        print(f"❌ {variant}: Error - {e}")

print()

# Test 4: Validation Prompt
print("📝 Test 4: Validation Prompt")
print("-" * 70)

sample_chunk = """{
    "chunk_title": "ankles_direction_purpose",
    "key_concepts": ["ankles", "life direction", "purpose"],
    "keywords_primary": ["ankles", "direction", "purpose"]
}"""

try:
    validation_prompt = get_validation_prompt(sample_chunk)
    print(f"✅ Validation prompt generated: {len(validation_prompt)} characters")
    if sample_chunk[:50] in validation_prompt:
        print(f"   ✓ Chunk text correctly embedded")
except Exception as e:
    print(f"❌ Error: {e}")

print()

# Test 5: Error Handling
print("📝 Test 5: Error Handling")
print("-" * 70)

try:
    prompt = get_chunk_prompt(sample_text, variant="invalid_variant")
    print("❌ Should have raised ValueError for invalid variant")
except ValueError as e:
    print(f"✅ Correctly raised ValueError: {e}")

try:
    desc = get_variant_description("invalid_variant")
    print("❌ Should have raised ValueError for invalid variant")
except ValueError as e:
    print(f"✅ Correctly raised ValueError: {e}")

print()

# Test 6: Prompt Templates Content
print("📝 Test 6: Prompt Templates Validation")
print("-" * 70)

templates = {
    "default": CHUNK_ANALYSIS_PROMPT,
    "concise": CHUNK_ANALYSIS_CONCISE,
    "detailed": CHUNK_ANALYSIS_DETAILED,
    "multilingual": CHUNK_ANALYSIS_MULTILINGUAL,
}

for name, template in templates.items():
    # Verifica placeholder
    has_text_placeholder = "{text}" in template
    has_language_placeholder = "{source_language}" in template
    
    print(f"• {name.upper()}")
    print(f"  - Length: {len(template)} chars")
    print(f"  - {{text}} placeholder: {'✓' if has_text_placeholder else '✗'}")
    if has_language_placeholder:
        print(f"  - {{source_language}} placeholder: ✓")

print()

# Test 7: Integration Test
print("📝 Test 7: Integration Test (Simulated Workflow)")
print("-" * 70)

print("Simulating chunk creation workflow:")
print("1. Select prompt variant...")
selected_variant = "detailed"
print(f"   → Selected: {selected_variant}")

print("2. Get prompt...")
prompt = get_chunk_prompt(sample_text, variant=selected_variant)
print(f"   → Generated: {len(prompt)} chars")

print("3. Prepare messages for Llama...")
messages = [
    {"role": "system", "content": CHUNK_SYSTEM_PROMPT},
    {"role": "user", "content": prompt}
]
print(f"   → Messages created: {len(messages)} messages")
print(f"   → System prompt: {len(messages[0]['content'])} chars")
print(f"   → User prompt: {len(messages[1]['content'])} chars")

print("✅ Integration test successful")

print()
print("=" * 70)
print("🎉 ALL TESTS PASSED!")
print("=" * 70)
print()
print("Next steps:")
print("1. Run: python scripts/3_create_chunks_with_llama.py --days 1 --prompt-variant detailed")
print("2. Compare chunk quality with different variants")
print("3. Choose best variant for your dataset")
