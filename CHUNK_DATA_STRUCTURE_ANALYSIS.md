================================================================================
📊 TEKLAB RAG CHUNK DATA STRUCTURE - COMPLETE ANALYSIS & SPECIFICATION
================================================================================

Document Version: 1.0
Created: November 7, 2025
Purpose: Define exact data structure for RAG chunks based on current Teklab sources

================================================================================
🎯 OBIETTIVO PRINCIPALE
================================================================================

Creare chunk JSON strutturati che:
1. **Mappano esattamente la struttura INPUT delle fonti Teklab**
2. **Contengono TUTTI i dati necessari per il RAG bot** (self-contained)
3. **Organizzano metadata tecnici per ricerca semantica ottimale**
4. **Supportano conversazioni multilingua** (EN/IT/ES/DE)
5. **Permettono retrieval preciso** tramite keywords, specifiche tecniche, applicazioni

================================================================================
📁 STRUTTURA INPUT/OUTPUT - MAPPING DIRETTO
================================================================================

INPUT SOURCES:
```
Fonti/Teklab/input/
├── Dal Catalogo/
│   ├── Oil Level Regulators/          → Output: chunks/oil_level_regulators/
│   │   ├── Tk3+ 46bar.txt
│   │   ├── Tk3+ 80bar.txt
│   │   ├── Tk3+ 130bar.txt
│   │   ├── tk4 46bar.txt
│   │   ├── tk4 80 bar.txt
│   │   ├── tk4 130bar.txt
│   │   ├── Tk4 mb 46bar.txt
│   │   ├── Tk4 mb 80bar.txt
│   │   └── Tk4 mb 130bar.txt
│   │
│   ├── Level Switches/                → Output: chunks/level_switches/
│   │   ├── Tk1+.txt
│   │   ├── LC PS.txt
│   │   ├── LC PH.txt
│   │   ├── LC XT-XP.txt
│   │   └── Rotalock.txt
│   │
│   ├── Sensors/                       → Output: chunks/sensors/
│   │   ├── K25.txt
│   │   ├── K11.txt
│   │   └── Atex.txt
│   │
│   ├── Adapters/                      → Output: chunks/adapters/
│   │   └── Adapters.txt
│   │
│   └── Fie_PDF/                       → Output: chunks/general/
│       ├── FULL Teklab Catalogue.txt
│       └── FULL Teklab Catalogue.html
│
└── Generali/                          → Output: chunks/support/ + chunks/applications/
    ├── Spiegazione Prodotti.txt       → chunks/support/product_overview.json
    ├── Presentazione Teklab.txt       → chunks/general/company_intro.json
    ├── Compressori con Prodotti teklab.txt → chunks/applications/compressor_integration.json
    └── TK_Series_Overview.txt         → chunks/support/tk_series_guide.json
```

OUTPUT STRUCTURE (mantiene gerarchia input):
```
Fonti/Teklab/input/Dal Catalogo/Processati/
├── .checkpoints/                      ← Sistema checkpoint (non modificare)
│   └── file_*_checkpoint.json
│
├── chunks/                            ← TUTTI I CHUNK (self-contained)
│   ├── oil_level_regulators/          ← Da "Oil Level Regulators/"
│   │   ├── tk3_plus_46bar_v001.json
│   │   ├── tk3_plus_46bar_v002.json   (chunk multipli per file lungo)
│   │   ├── tk3_plus_80bar_v001.json
│   │   ├── tk3_plus_130bar_v001.json
│   │   ├── tk4_46bar_v001.json
│   │   ├── tk4_80bar_v001.json
│   │   ├── tk4_130bar_v001.json
│   │   ├── tk4mb_46bar_v001.json
│   │   ├── tk4mb_80bar_v001.json
│   │   └── tk4mb_130bar_v001.json
│   │
│   ├── level_switches/                ← Da "Level Switches/"
│   │   ├── tk1_plus_v001.json
│   │   ├── lc_ps_v001.json
│   │   ├── lc_ph_v001.json
│   │   ├── lc_xt_v001.json
│   │   ├── lc_xp_v001.json
│   │   └── rotalock_connection_v001.json
│   │
│   ├── sensors/                       ← Da "Sensors/"
│   │   ├── k25_analog_sensor_v001.json
│   │   ├── k11_sensor_v001.json
│   │   ├── atex_metallic_ir_v001.json
│   │   └── atex_plastic_ir_v001.json
│   │
│   ├── adapters/                      ← Da "Adapters/"
│   │   ├── rotalock_adapters_v001.json
│   │   ├── flange_adapters_v001.json
│   │   └── threaded_adapters_v001.json
│   │
│   ├── applications/                  ← Da "Generali/" (use cases)
│   │   ├── compressor_oil_management_v001.json
│   │   ├── refrigeration_systems_v001.json
│   │   ├── co2_transcritical_v001.json
│   │   └── high_pressure_applications_v001.json
│   │
│   ├── support/                       ← Da "Generali/" (guides/FAQ)
│   │   ├── product_selection_guide_v001.json
│   │   ├── pressure_rating_selection_v001.json
│   │   ├── tk_series_comparison_v001.json
│   │   └── troubleshooting_common_issues_v001.json
│   │
│   └── general/                       ← Da "Fie_PDF/" + presentazioni
│       ├── teklab_company_overview_v001.json
│       ├── technology_overview_v001.json
│       └── catalog_index_v001.json
│
├── summaries/                         ← Summary per file originale (aggregati)
│   ├── Tk3+_46bar_txt_summary.json
│   ├── Tk3+_80bar_txt_summary.json
│   ├── LC_PS_txt_summary.json
│   └── ...
│
├── metadata/                          ← Metadata aggregati cross-cutting
│   ├── products_metadata.json         (tutti i prodotti con specs)
│   ├── technology_metadata.json       (tecnologie comuni)
│   └── applications_metadata.json     (scenari applicativi)
│
├── keywords/                          ← Keywords consolidate
│   └── teklab_keywords.json
│
└── qa_pairs/                          ← Q&A addizionali estratte
    └── teklab_qa_pairs.json
```

================================================================================
📦 STRUTTURA DATI CHUNK - FORMATO JSON COMPLETO
================================================================================

Ogni chunk è un file JSON **SELF-CONTAINED** con questa struttura:

```json
{
  "id": "teklab_chunk_{file_index:03d}_{chunk_num:03d}_{product_model}_{pressure_version}",
  "original_text": "Testo completo originale estratto dal file sorgente...",
  
  "messages": [
    {
      "role": "system",
      "content": "SYSTEM PROMPT COMPLETO da Prompt/prompts_config.py (IDENTICO in tutti i chunk)"
    },
    {
      "role": "user",
      "content": "Domanda tecnica contestualizzata con specs chiave dal documento"
    },
    {
      "role": "assistant",
      "content": "Risposta tecnica dettagliata 200-400 parole con specifiche precise"
    }
  ],
  
  "metadata": {
    // === IDENTIFICAZIONE CHUNK ===
    "chunk_id": "teklab_chunk_003_001_tk3_plus_46bar",
    "file_index": 3,
    "file_source": "Tk3+ 46bar.txt",
    "source_folder": "Oil Level Regulators",        // Traccia folder di provenienza
    "chunk_number": 1,
    "chunk_title": "TK3+ @46bar Oil Level Regulator - Main Features",
    "manufacturer": "Teklab S.r.l.",
    "document_type": "Product Technical Datasheet",
    "language": "en",                               // "en"|"it"|"es"|"de"
    "creation_date": "2025-11-07",
    "version": "1.0",
    
    // === CATEGORIZZAZIONE PRODOTTO ===
    "product_category": "Oil Level Regulators",     // Main category
    "product_family": "TK Series",                  // TK Series | LC Series | K Series
    "product_model": "TK3+",                        // Specific model
    "pressure_version": "46bar",                    // 46bar | 80bar | 130bar
    "product_variants": [                           // Varianti disponibili
      "TK3P-A50AB11-01 (24VAC, 1m cable gland)",
      "TK3P-A50AB11-02 (24VAC, 3m cable gland)",
      "TK3P-B50AB11-01 (230VAC, 1m cable gland)",
      "TK3P-A50AB31-01 (24VAC, 3m connector)"
    ],
    
    // === SPECIFICHE TECNICHE (CRITICAL per RAG) ===
    "technical_specs": {
      "pressure": {
        "max_working_pressure": "46 bar",
        "max_operating_pressure_differential": "26 bar",
        "test_pressure": "70 bar"
      },
      "temperature": {
        "operating_range_medium": "-40°C to +85°C",
        "operating_range_ambient": "-40°C to +60°C",
        "storage_range": "-40°C to +85°C"
      },
      "electrical": {
        "supply_voltage": ["24 VAC ±10%", "230 VAC ±10%"],
        "supply_current": "20 VA",
        "frequency": "50/60 Hz",
        "relay_output": "230 VAC @2A (NO/NC, potential-free)",
        "solenoid_valve_output": "Integrated"
      },
      "connections": {
        "oil_return_line": "7/16-20 UNF male",
        "electrical": ["Cable glands (1m/3m)", "EN175301-803 Connector (3m/6m)"],
        "mounting": ["3/4/6 holes flange", "Various compressor adapters"]
      },
      "materials": {
        "body": "Nickel-plated steel",
        "sensor_dome": "Fused glass",
        "electronics_housing": "PA glass fiber reinforced"
      },
      "protection": {
        "ip_rating": "IP65",
        "standards": ["2014/30/UE (EMC)", "2014/35/UE (LVD)"]
      },
      "dimensions": {
        "height": "Compact design",
        "mounting_type": "Left/Right reversible"
      }
    },
    
    // === REFRIGERANTI E APPLICAZIONI ===
    "refrigerants_compatible": [
      "R134a", "R404A", "R407C", "R410A", "R507", "CO2 (R744)",
      "NH3 (Ammonia)", "HFO refrigerants"
    ],
    "applications": [
      "Compressor oil level management",
      "High pressure oil return line systems",
      "Multi-compressor racks (3+ compressors)",
      "CO2 transcritical refrigeration",
      "Industrial refrigeration plants",
      "HVAC&R systems"
    ],
    "target_industries": [
      "Industrial refrigeration",
      "Commercial refrigeration",
      "HVAC&R",
      "Food processing",
      "Cold storage facilities"
    ],
    
    // === KEY FEATURES (per sales/marketing) ===
    "key_features": [
      "No mechanical moving parts (high reliability)",
      "Electro-optic infrared sensor technology",
      "Integrated sight glass + electronic LEDs",
      "Left/Right mounting flexibility (same unit)",
      "Direct sight-glass replacement (3/4/6 holes flange)",
      "Easy maintenance (coil & sensor replaceable without depressurizing)",
      "Integrated solenoid valve for oil filling",
      "230 VAC @2A alarm relay (direct security chain connection)",
      "Optional integrated filter",
      "Compact dimensions"
    ],
    
    "competitive_advantages": [
      "vs Float switches: No mechanical parts to fail or stick",
      "vs Capacitive sensors: No calibration needed, instant response",
      "Reduced circuit junctions = less leakage risk",
      "Simplified installation (cost & time savings)",
      "Lower warehouse complexity (one unit for left/right mounting)"
    ],
    
    // === KEYWORDS per RETRIEVAL ===
    "keywords_primary": [
      "TK3+ 46bar",
      "oil level regulator",
      "electro-optic sensor",
      "compressor oil control",
      "high pressure oil return",
      "refrigeration oil management",
      "CO2 compatible"
    ],
    
    "keywords_synonyms": {
      "oil level regulator": ["oil level controller", "oil management system", "crankcase level control"],
      "electro-optic": ["infrared sensor", "IR detection", "optical sensor"],
      "compressor": ["reciprocating compressor", "screw compressor", "scroll compressor"]
    },
    
    "keywords_technical": [
      "46 bar working pressure",
      "26 bar pressure differential",
      "7/16-20 UNF connection",
      "IP65 protection",
      "230 VAC relay output",
      "fused glass technology",
      "solenoid valve integrated"
    ],
    
    "keywords_relations": {
      "related_products": ["TK3+ 80bar", "TK3+ 130bar", "TK4 46bar", "TK4MB 46bar"],
      "alternative_solutions": ["TK1+ level switch", "LC-PS level switch"],
      "compatible_accessories": ["Rotalock adapters", "3/4/6 holes flange", "M20x1.5 adapter"]
    },
    
    // === CONTENUTO EDUCATIVO ===
    "key_concepts": [
      "Electro-optic infrared oil level detection principle",
      "Advantages of no moving parts in harsh environments",
      "High pressure oil return line system configuration",
      "Multi-compressor rack oil management strategies",
      "Fused glass sensor technology for chemical compatibility"
    ],
    
    "iconic_quotes": [
      "Extremely compact dimensions with left/right mounting possibility",
      "High reliability ensured by absence of mechanical moving parts",
      "Direct sight glass replacement with 3/4/6 holes flange connection",
      "Reduction of circuit junctions = less leakage risk"
    ],
    
    // === Q&A PAIRS (training data) ===
    "qa_pairs": [
      {
        "question": "What is the maximum working pressure of TK3+ @46bar?",
        "answer": "The TK3+ @46bar has a maximum working pressure (MWP) of 46 bar and a maximum operating pressure differential (MOPD) of 26 bar. It's suitable for standard refrigeration systems with R134a, R404A, R407C, and similar refrigerants operating within these pressure ranges.",
        "difficulty": "basic",
        "intent": ["technical_specification", "product_selection"]
      },
      {
        "question": "Can TK3+ be mounted on both left and right sides?",
        "answer": "Yes, TK3+ features a unique reversible design allowing left/right mounting with the same unit. This reduces inventory complexity and installation time, as you only need one product version for both mounting configurations. The sight glass and LEDs can be checked from whichever side is more accessible.",
        "difficulty": "intermediate",
        "intent": ["installation", "product_features"]
      },
      {
        "question": "How does TK3+ compare to traditional float-based oil level regulators?",
        "answer": "TK3+ uses electro-optic infrared technology instead of mechanical floats, offering several advantages: (1) No moving parts to fail or stick, (2) Instant response with no hysteresis, (3) No calibration required, (4) Better reliability in harsh conditions, (5) Resistant to vibrations and oil foaming. The fused glass sensor dome ensures chemical compatibility with all refrigerants without degradation over time.",
        "difficulty": "advanced",
        "intent": ["product_comparison", "technology_explanation"]
      }
    ],
    
    "natural_questions": [
      "What pressure rating do I need for R404A system?",
      "How to install TK3+ on Bitzer compressor?",
      "Can TK3+ work with CO2 refrigerant?",
      "What's the difference between TK3+ and TK4?",
      "Do I need to calibrate the oil level sensor?"
    ],
    
    "follow_up_questions": [
      "Which compressor adapter do you need?",
      "What is your refrigerant type?",
      "Do you need Modbus connectivity?",
      "Is ATEX certification required for your application?",
      "How many compressors in your rack system?"
    ],
    
    // === INSTALLATION & CONFIGURATION ===
    "installation_notes": [
      "Direct replacement for 3/4/6 holes sight-glass flanges",
      "Ensure correct adapter for your compressor brand/model",
      "Check oil return line pressure differential (max 26 bar)",
      "Verify power supply matches unit specification (24V or 230V)",
      "Optional filter can be integrated in series with solenoid valve",
      "Sensor and coil are field-replaceable without depressurizing"
    ],
    
    "configuration_tips": [
      "Adjust filling timer based on oil return line length",
      "Set alarm delay to avoid false alarms during transients",
      "Connect alarm relay to compressor security chain",
      "Test sight glass visibility before final installation",
      "Verify LED indication matches actual oil level"
    ],
    
    // === TROUBLESHOOTING ===
    "common_issues": [
      {
        "issue": "Alarm triggered immediately after startup",
        "cause": "Oil level below sensor due to system migration",
        "solution": "Verify oil charge, check for leaks, adjust filling timer if needed"
      },
      {
        "issue": "Solenoid valve not opening",
        "cause": "Pressure differential too high or electrical issue",
        "solution": "Check MOPD (max 26 bar), verify power supply, test coil resistance"
      },
      {
        "issue": "LED blinking but sight glass shows oil present",
        "cause": "Sensor calibration or contamination on glass dome",
        "solution": "Clean sensor dome, replace sensor if issue persists (no calibration needed)"
      }
    ],
    
    "troubleshooting_hints": [
      "Always check pressure differential before diagnosing valve issues",
      "Clean sight glass and sensor dome during annual maintenance",
      "Verify refrigerant compatibility if sensor behaves erratically",
      "Check alarm delay settings if false alarms occur"
    ],
    
    // === METADATA PER RAG RETRIEVAL ===
    "prerequisites": [
      "Understanding of refrigeration oil management principles",
      "Knowledge of compressor crankcase lubrication requirements",
      "Familiarity with high pressure oil return line systems"
    ],
    
    "related_topics": [
      "Oil separator sizing and efficiency",
      "Multi-compressor rack configuration",
      "CO2 transcritical system oil management",
      "Compressor protection strategies"
    ],
    
    "difficulty_level": "intermediate",           // basic | intermediate | advanced
    "content_type": "product_specification",      // product_specification | application_guide | troubleshooting | comparison
    "question_type": "technical",                 // technical | application | installation | troubleshooting
    "user_intent": [                              // Array per multi-intent
      "product_selection",
      "technical_specification",
      "application_design"
    ],
    
    "importance": 0.95,                           // 0.0-1.0 (per ranking)
    "relevance": 9,                               // 1-10 (per filtering)
    
    // === SUMMARY ===
    "summary": "TK3+ @46bar is a compact, highly reliable oil level regulator using electro-optic infrared technology for compressor oil management. Key advantages include no mechanical parts, reversible left/right mounting, integrated solenoid valve and alarm relay, direct sight-glass replacement capability, and compatibility with all common refrigerants including CO2. Suitable for industrial refrigeration systems with working pressures up to 46 bar and pressure differentials up to 26 bar."
  }
}
```

================================================================================
🔍 ANALISI DATI DALLE FONTI TEKLAB - COSA ESTRARRE
================================================================================

### 1️⃣ DA FILE "Oil Level Regulators/" (TK3+, TK4, TK4MB)

**DATI TECNICI da estrarre:**
- Modello esatto (TK3+, TK4, TK4MB)
- Versione pressione (46bar, 80bar, 130bar)
- Varianti disponibili (codici prodotto)
- Specifiche elettriche (voltage, current, VA)
- Specifiche pressione (MWP, MOPD, test pressure)
- Temperature operative (medium, ambient, storage)
- Connessioni (oil line, electrical, mounting)
- Output (relay specs, solenoid valve specs)
- Materiali (body, sensor dome, housing)
- Protezioni (IP rating, standards)
- Dimensioni e peso

**CARATTERISTICHE DISTINTIVE:**
- TK3+: Base model, compact, no connectivity
- TK4: Adds NFC connectivity for field customization
- TK4MB: Adds Modbus RTU + NFC for remote monitoring

**APPLICAZIONI:**
- Multi-compressor racks
- High pressure oil return lines
- CO2 transcritical systems
- Industrial refrigeration

**VANTAGGI COMPETITIVI:**
- No moving parts vs float switches
- Left/right mounting flexibility
- Direct sight-glass replacement
- Easy maintenance without depressurizing
- Integrated filtering option

### 2️⃣ DA FILE "Level Switches/" (TK1+, LC-PS, LC-PH, LC-XP, LC-XT, Rotalock)

**DATI TECNICI da estrarre:**
- Modello (TK1+, LC-PS, LC-PH, LC-XT, LC-XP)
- Pressione max (46bar, 80bar, 120bar)
- Alimentazione (24VAC, 115VAC, 230VAC, 24VDC)
- Output type (NO/NC, voltage/current limits)
- Connessioni (M20x1.5, 1-1/8 UNEF, 1/2 NPT)
- Delays (customizable timing)
- Temperature range
- IP rating
- Materiali

**DIFFERENZE MODELLI:**
- TK1+: Simple level switch, alarm only (no valve)
- LC-PS: Up to 46 bar, 230V/115V/24V options
- LC-PH: Up to 120 bar (high pressure)
- LC-XT: Standard version
- LC-XP: Extended pressure version (120 bar)
- Rotalock: Connection type for direct compressor mounting

**APPLICAZIONI:**
- Single compressor monitoring
- Tank level monitoring
- Low/high level alarms
- Backup protection

### 3️⃣ DA FILE "Sensors/" (K25, K11, ATEX)

**DATI TECNICI da estrarre:**
- Modello (K25, K11, ATEX metallic/plastic)
- Pressione max (150 bar for K25 - CO2 systems)
- Output types:
  - K25: Digital level + Analog temperature (4-20mA)
  - K11: Digital level only
  - ATEX: Explosion-proof versions
- Alimentazione (24VDC typically)
- Certificazioni (ATEX, CE)
- Temperature range (-40°C to +125°C)
- Ripetibilità (±2mm)

**APPLICAZIONI SPECIFICHE:**
- K25: CO2 transcritical/subcritical systems (up to 150 bar)
- ATEX: Explosive atmospheres (zone 1, zone 2)
- K11: Standard industrial applications

**CARATTERISTICHE UNICHE:**
- K25: Dual output (level + temperature)
- ATEX: Intrinsically safe design
- High pressure resistance

### 4️⃣ DA FILE "Adapters/"

**DATI da estrarre:**
- Tipi di connessioni:
  - Rotalock (various sizes)
  - 3/4/6 holes flange
  - M20x1.5
  - 1-1/8 UNEF
  - 3/4 NPT, 1/2 NPT
  - SAE connections
- Compatibilità compressori:
  - Bitzer (specific models)
  - Bock (specific models)
  - Copeland (specific models)
  - Dorin, Frascold, Grasso, etc.
- Materiali e pressioni supportate
- Note installazione

### 5️⃣ DA FILE "Generali/"

**Dati da estrarre:**

**Da "Spiegazione Prodotti.txt":**
- Panoramica famiglie prodotti
- Confronto TK3+ vs TK4 vs TK4MB
- Differenze versioni pressione
- Principi funzionamento generale
- Vantaggi tecnologia elettro-ottica

**Da "Presentazione Teklab.txt":**
- Storia azienda
- Missione e valori
- Certificazioni qualità
- Presenza geografica

**Da "Compressori con Prodotti teklab.txt":**
- Mapping compressori → prodotti compatibili
- Tabelle compatibilità
- Guide selezione

**Da "TK_Series_Overview.txt":**
- Albero decisionale selezione prodotto
- Tabelle comparative features
- Scenari applicativi

================================================================================
📋 REGOLE CREAZIONE CONTENT (User/Assistant messages)
================================================================================

### USER MESSAGE - Struttura tipo:

```
Technical documentation context (Teklab industrial products):

[{Product_Family}] - {Model} @{Pressure} {Product_Type}
Key Specifications: {Top 5 specs estratte dal documento}
📌 Important Details: {Quotes iconiche dal testo originale}

Complete technical text:
{Original_text estratto dal documento}

---

Question: {Domanda tecnica realistica come la farebbe un cliente}

Respond as an expert Teklab technical sales assistant:
- Provide accurate technical specifications
- Explain product features and applications clearly
- Give installation and configuration guidance
- Focus on PRACTICAL IMPLEMENTATION and compatibility
- Cite pressure ranges, temperatures, certifications when relevant
```

### ASSISTANT MESSAGE - Struttura tipo (200-400 parole):

```
[Direct Product Recommendation]
For your [application context], I recommend the [Product Model] @[Pressure] 
because [main technical reason].

[Technical Justification]
This model features:
- [Key spec 1 with exact values]
- [Key spec 2 with exact values]
- [Key spec 3 with exact values]

[Application Benefits]
In your specific case:
- [Benefit 1 for the application]
- [Benefit 2 compared to alternatives]
- [Benefit 3 for installation/maintenance]

[Installation/Configuration Notes]
For optimal installation:
- [Practical tip 1]
- [Practical tip 2]
- [Adapter/connection requirement if applicable]

[Follow-up Considerations]
You should also consider:
- [Alternative if pressure/temp outside range]
- [Complementary product or accessory]
- [Clarifying question if info missing]
```

**CRITICAL RULES:**
❌ NO vague language: "maybe", "could work", "might be suitable"
✅ PRECISE specs: "46 bar MWP", "26 bar MOPD", "-40°C to +85°C"
✅ CITE standards: "IP65", "CE 2014/30/UE", "ATEX Zone 1"
✅ PRACTICAL details: adapter types, wiring, delays, mounting

================================================================================
🔄 FILE AGGREGATI (SECONDARY) - Dopo chunk creation
================================================================================

### 1️⃣ summaries/{filename}_summary.json

Per ogni file sorgente, uno summary con:
- Total chunks created
- Main topics covered
- Key products described
- Technical specs ranges (min/max pressure, temp, etc.)
- Cross-references to chunks

### 2️⃣ metadata/products_metadata.json

Tabella prodotti consolidata:
```json
{
  "products": [
    {
      "model": "TK3+",
      "family": "Oil Level Regulators",
      "pressure_versions": ["46bar", "80bar", "130bar"],
      "key_features": [...],
      "applications": [...],
      "related_chunks": ["chunk_003_*", "chunk_011_*", "chunk_012_*"]
    },
    ...
  ]
}
```

### 3️⃣ metadata/technology_metadata.json

Tecnologie comuni:
- Electro-optic infrared principle
- Fused glass sensor technology
- NFC connectivity (TK4)
- Modbus RTU (TK4MB)
- Solenoid valve integration

### 4️⃣ keywords/teklab_keywords.json

Keyword mapping globale:
```json
{
  "primary_keywords": {
    "oil level regulator": {
      "frequency": 45,
      "chunks": ["chunk_003_*", "chunk_011_*", ...],
      "synonyms": ["oil level controller", "crankcase level control"]
    },
    ...
  },
  "technical_terms": {
    "46 bar": {
      "products": ["TK3+ 46bar", "TK4 46bar", "LC-PS"],
      "chunks": [...]
    },
    ...
  }
}
```

### 5️⃣ qa_pairs/teklab_qa_pairs.json

Q&A addizionali estratte da chunks per training:
```json
{
  "qa_pairs": [
    {
      "question": "...",
      "answer": "...",
      "source_chunks": ["chunk_003_001", ...],
      "products": ["TK3+ 46bar"],
      "difficulty": "intermediate"
    },
    ...
  ]
}
```

================================================================================
🎯 PRIORITÀ DATI PER RAG RETRIEVAL
================================================================================

**CRITICAL per retrieval accuracy:**
1. ✅ **technical_specs** → exact matching (pressure, temp, voltage)
2. ✅ **keywords_primary** → semantic search primary
3. ✅ **product_model + pressure_version** → filtering
4. ✅ **refrigerants_compatible** → application matching
5. ✅ **applications** → use case matching
6. ✅ **qa_pairs** → natural language matching

**IMPORTANT per context enrichment:**
7. ✅ **key_features** → product differentiation
8. ✅ **competitive_advantages** → sales arguments
9. ✅ **installation_notes** → practical guidance
10. ✅ **troubleshooting_hints** → support

**NICE TO HAVE per completeness:**
11. ⭕ **iconic_quotes** → exact text retrieval
12. ⭕ **related_topics** → exploration
13. ⭕ **prerequisites** → educational context

================================================================================
✅ VALIDATION CHECKLIST
================================================================================

Prima di considerare un chunk "completo", verificare:

- [ ] File mapping: Input folder → Output folder corretto
- [ ] ID univoco: teklab_chunk_{file_idx:03d}_{chunk_num:03d}_{model}
- [ ] System prompt: Identico in tutti i chunk (da prompts_config.py)
- [ ] Language field: Presente e corretto ("en"|"it"|"es"|"de")
- [ ] Technical specs: TUTTI i valori numerici presenti (pressure, temp, voltage)
- [ ] Refrigerants: Lista completa compatibilità
- [ ] Keywords: Primary (5-10) + synonyms + technical terms
- [ ] Q&A pairs: Almeno 2-3 per chunk, vari livelli difficoltà
- [ ] Applications: Scenari realistici di utilizzo
- [ ] Installation notes: Dettagli pratici montaggio
- [ ] Summary: 2-3 frasi che riassumono contenuto chunk
- [ ] Original text: Estratto completo senza troncamenti

================================================================================
📊 METRICHE QUALITÀ CHUNK
================================================================================

**Target metrics per chunk di qualità:**
- User message: 150-300 parole
- Assistant message: 200-400 parole
- Keywords primary: 5-10
- Keywords synonyms: 3-5 per primary keyword
- Q&A pairs: 2-4 per chunk
- Technical specs: Completezza 100% per prodotto
- Applications: 3-6 scenari
- Installation notes: 4-8 tips pratici

================================================================================
🔄 WORKFLOW GENERAZIONE CHUNK
================================================================================

1. **Input file selection** → Seleziona categoria (Oil Level Regulators, Level Switches, etc.)
2. **File parsing** → Estrai testo completo + identifica breakpoint semantici
3. **Semantic chunking** → Split in sezioni logiche (max 800 parole)
4. **Metadata extraction** → LLM genera metadata da section text
5. **Q&A generation** → LLM genera domande realistiche + risposte
6. **Validation** → Verifica completezza campi required
7. **Save chunk** → JSON in folder output corretto
8. **Update checkpoint** → Salva progresso per resume
9. **Generate summary** → Dopo tutti i chunk del file
10. **Update aggregates** → Metadata, keywords, qa_pairs globali

================================================================================
📝 NOTE IMPLEMENTAZIONE
================================================================================

**Per lo script Python:**
1. Mantenere mapping esatto: Input folder → Output subfolder
2. Checkpoint system per resume dopo interruzioni
3. Validazione JSON schema prima di save
4. Logging dettagliato per debug
5. Gestione errori LLM (retry logic)
6. Progress bar per visibilità stato

**Per il RAG system:**
1. Indexing su keywords_primary + technical_specs
2. Semantic embeddings su messages[user] + messages[assistant]
3. Filtering pre-retrieval: product_model, pressure_version, language
4. Ranking post-retrieval: importance score + relevance score
5. Context window: 3-5 chunk retrieved per query

================================================================================
END OF DOCUMENT
================================================================================
