"""
Script per aggiungere keywords ai chunk Marketing
Aggiunge keywords_primary, keywords_synonyms, keywords_relations
"""

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
MARKETING_PATH = PROJECT_ROOT / "Fonti" / "Teklab" / "input" / "Dal Catalogo" / "Processati" / "chunks" / "Marketing"

# Mapping keywords per prodotto
PRODUCT_KEYWORDS = {
    "LC-PS": {
        "keywords_primary": [
            "product_model (LC-PS)",
            "pressure_range (46 bar)",
            "competitor (Danfoss AKS 38, Alco FS-C, Sporlan OLS-C, Emerson ELS)",
            "feature (capacitive sensor, digital output, PNP/NPN)",
            "application (level switch, oil level control, HFC/HFO refrigeration)"
        ],
        "keywords_synonyms": {
            "LC-PS": ["level switch", "interruttore di livello", "sensore livello"],
            "Danfoss AKS 38": ["AKS38", "Danfoss level switch"],
            "Alco FS-C": ["Alco FS-J", "Alco float switch"],
            "capacitive": ["capacitivo", "electronic sensor", "sensore elettronico"],
            "retrofit": ["sostituzione", "replacement", "upgrade"]
        },
        "keywords_relations": {
            "LC-PS_replaces": ["Danfoss AKS 38", "Alco FS-C", "Alco FS-J", "Sporlan OLS-C"],
            "technology_advantage": ["electronic vs mechanical", "no moving parts", "capacitive technology"],
            "compatibility": ["PLC universal", "12-24V DC", "2-wire connection"],
            "installation": ["1/4 inch SAE", "M10x1 thread", "easy retrofit"]
        }
    },
    "LC-PH": {
        "keywords_primary": [
            "product_model (LC-PH)",
            "pressure_range (120 bar)",
            "competitor (Danfoss AKS 4100, HBControls HL-CO2, Emerson PSL)",
            "feature (M12 connector, high pressure, CO2 transcritical)",
            "application (CO2 refrigeration, transcritical systems, 316L stainless steel)"
        ],
        "keywords_synonyms": {
            "LC-PH": ["high pressure level switch", "CO2 level sensor"],
            "CO2": ["R744", "carbon dioxide", "transcritical"],
            "M12": ["M12 connector", "IP67", "industrial connector"],
            "120 bar": ["high pressure", "alta pressione"]
        },
        "keywords_relations": {
            "LC-PH_replaces": ["Danfoss AKS 4100", "HBControls HL-CO2", "Emerson PSL"],
            "applications": ["CO2 transcritical", "supermarket refrigeration", "cold storage"],
            "certifications": ["EN 12263", "316L stainless steel", "R744 approved"],
            "connectivity": ["cable + M12 dual option", "plug-and-play"]
        }
    },
    "LC-XT": {
        "keywords_primary": [
            "product_model (LC-XT)",
            "pressure_range (46 bar)",
            "competitor (Danfoss AKS 38 + adapter)",
            "feature (DIN 43650-A connector, plug-and-play, quick maintenance)",
            "application (modular chillers, fast replacement, MTTR reduction)"
        ],
        "keywords_synonyms": {
            "LC-XT": ["DIN connector level switch"],
            "DIN 43650-A": ["DIN connector", "industrial connector"],
            "MTTR": ["Mean Time To Repair", "maintenance time"],
            "plug-and-play": ["quick connect", "rapid installation"]
        },
        "keywords_relations": {
            "advantages_vs_competitors": ["integrated DIN", "no external adapter", "5 min vs 20 min installation"],
            "applications": ["modular equipment", "chiller systems", "quick maintenance"],
            "installation": ["DIN female cable compatible", "2 minute replacement"]
        }
    },
    "LC-XP": {
        "keywords_primary": [
            "product_model (LC-XP)",
            "pressure_range (120 bar)",
            "competitor (Danfoss AKS 4100 M12)",
            "feature (DIN connector 120 bar, unique market product, CO2 transcritical)",
            "application (CO2 high pressure, EU market standard, DIN preference)"
        ],
        "keywords_synonyms": {
            "LC-XP": ["high pressure DIN level switch"],
            "DIN vs M12": ["EU standard", "connector comparison"],
            "unique product": ["market innovation", "only DIN 120bar"]
        },
        "keywords_relations": {
            "market_positioning": ["ONLY DIN 120bar globally", "uncovered niche"],
            "advantages": ["DIN cables 50% cheaper", "EU market familiarity", "higher stock availability"],
            "applications": ["CO2 transcritical EU", "DIN standardization"]
        }
    },
    "TK1+": {
        "keywords_primary": [
            "product_model (TK1+)",
            "pressure_range (100 bar)",
            "competitor (Danfoss OLS-H, Emerson OLS, Alco FS-J)",
            "feature (sight-glass retrofit, relay NO/NC, drop-in replacement)",
            "application (compressor sight-glass upgrade, automatic monitoring)"
        ],
        "keywords_synonyms": {
            "TK1+": ["sight-glass replacement", "oil level switch"],
            "sight-glass": ["visual indicator", "vetro indicatore"],
            "drop-in": ["direct replacement", "retrofit diretto"],
            "relay": ["NO/NC", "alarm contact", "SPDT"]
        },
        "keywords_relations": {
            "replaces": ["sight-glass visual indicator", "manual inspection"],
            "advantages": ["100 bar vs 90 bar Danfoss", "24/7 automatic monitoring", "optical electronic"],
            "installation": ["M18x1.5 thread", "3/4 inch UNF-16", "10-15 min installation"],
            "compatibility": ["Bitzer compressors", "Copeland", "Frascold", "Dorin"]
        }
    },
    "Rotalock": {
        "keywords_primary": [
            "product_model (Rotalock Switch)",
            "pressure_range (46 bar)",
            "competitor (NONE - unique product)",
            "feature (direct Rotalock mount, no adapters, zero additional leak points)",
            "application (liquid receivers, Rotalock valves, retrofit without shutdown)"
        ],
        "keywords_synonyms": {
            "Rotalock": ["Rotalock valve", "valvola Rotalock"],
            "unique product": ["market innovation", "exclusive Teklab"],
            "no adapters": ["direct mount", "native installation"]
        },
        "keywords_relations": {
            "market_positioning": ["ONLY Rotalock-native globally", "absolute competitive advantage"],
            "savings": ["90-150€ labor", "35€ materials", "immediate ROI"],
            "advantages": ["5 min vs 45 min installation", "50% fewer leak points", "no Rotalock-NPT adapter"],
            "compatibility": ["Sporlan valves", "Castel", "Parker", "Danfoss EVRA"]
        }
    },
    "TK3+": {
        "keywords_primary": [
            "product_model (TK3+)",
            "pressure_range (46/80/130 bar)",
            "competitor (Danfoss AKS/ORV, Emerson OLR, Alco OLR)",
            "feature (3 pressure versions, optical sensor, integrated valve, standalone)",
            "application (oil level regulation, HFC/ammonia/CO2, compressor protection)"
        ],
        "keywords_synonyms": {
            "TK3+": ["oil level regulator", "OLR", "regolatore livello olio"],
            "optical sensor": ["electro-optic", "ottico capacitivo"],
            "standalone": ["autonomous", "self-contained"]
        },
        "keywords_relations": {
            "pressure_versions": ["46 bar HFC/HFO", "80 bar ammonia R717", "130 bar CO2 transcritical"],
            "advantages": ["optical vs float", "no moving parts", "2x durability"],
            "applications": ["compressor lubrication", "rack systems", "long piping systems"]
        }
    },
    "TK4": {
        "keywords_primary": [
            "product_model (TK4)",
            "pressure_range (46/80/130 bar)",
            "competitor (Danfoss AKS 4100 BLE)",
            "feature (NFC wireless, smartphone config, first in market, diagnostic history)",
            "application (rapid commissioning, field maintenance, multi-compressor projects)"
        ],
        "keywords_synonyms": {
            "TK4": ["NFC oil regulator", "wireless OLR"],
            "NFC": ["Near Field Communication", "tap-and-go", "contactless"],
            "wireless config": ["smartphone setup", "app configuration"]
        },
        "keywords_relations": {
            "innovation": ["FIRST NFC oil regulator globally", "market exclusive"],
            "advantages": ["30 sec vs 10 min config", "no panel opening", "diagnostic history"],
            "NFC_vs_BLE": ["<5cm range vs 10m", "no pairing vs pairing required", "higher security"],
            "ROI": ["95% time saving", "10 devices = 1.5h labor saved"]
        }
    },
    "TK4MB": {
        "keywords_primary": [
            "product_model (TK4MB)",
            "pressure_range (46/80/130 bar)",
            "competitor (Danfoss AKS 4100 IoT, Carel LEV-BUS, Honeywell BACnet)",
            "feature (triple interface, Relay + NFC + Modbus RTU, Industry 4.0)",
            "application (centralized supervision, PLC/SCADA integration, predictive maintenance)"
        ],
        "keywords_synonyms": {
            "TK4MB": ["Modbus oil regulator", "Industry 4.0 OLR"],
            "Modbus RTU": ["RS485", "fieldbus", "serial communication"],
            "triple interface": ["multi-level control", "flexible architecture"]
        },
        "keywords_relations": {
            "interfaces": ["relay standalone", "NFC local config", "Modbus centralized"],
            "compatibility": ["Siemens PLC", "Allen-Bradley", "Schneider", "Omron", "WinCC SCADA"],
            "Modbus_RTU_advantages": ["2-wire RS485", "1200m range", "robust industrial", "no Ethernet cost"],
            "applications": ["supermarket chains", "industrial plants", "BMS integration"]
        }
    },
    "K11": {
        "keywords_primary": [
            "product_model (K11)",
            "pressure_range (60 bar)",
            "competitor (Danfoss AKS 33, Alco ELS, Sporlan ELS-C)",
            "feature (configurable output NPN/PNP/AC, 3-in-1, universal PLC)",
            "application (industrial refrigeration, HVAC, SKU reduction)"
        ],
        "keywords_synonyms": {
            "K11": ["universal level sensor", "configurable sensor"],
            "configurable output": ["DIP switch", "NPN/PNP/AC selectable"],
            "3-in-1": ["universal", "multi-output"]
        },
        "keywords_relations": {
            "innovation": ["output configurability", "1 SKU vs 3", "66% SKU reduction"],
            "outputs": ["NPN sink", "PNP source", "AC relay"],
            "advantages": ["universal PLC compatibility", "eliminate order errors", "stock flexibility"],
            "installation": ["M18x1 thread", "2 min DIP switch config"]
        }
    },
    "K25": {
        "keywords_primary": [
            "product_model (K25)",
            "pressure_range (150 bar)",
            "competitor (Danfoss AKS 4100 + AKS T, 2 separate sensors)",
            "feature (2-in-1 level + temperature, NPN + 4-20mA, CO2 transcritical)",
            "application (CO2 systems, dual measurement, gas discharge monitoring)"
        ],
        "keywords_synonyms": {
            "K25": ["2-in-1 sensor", "level + temperature combo"],
            "2-in-1": ["integrated dual sensor", "combo sensor"],
            "4-20mA": ["analog output", "current loop", "industrial standard"]
        },
        "keywords_relations": {
            "innovation": ["ONLY 2-in-1 CO2 sensor globally", "unique market product"],
            "savings": ["1 installation vs 2", "1 leak point vs 2", "50% labor saving", "200-300€ hardware"],
            "4-20mA_advantages": ["no PT1000 converter", "noise immunity", "1000m cabling"],
            "applications": ["CO2 transcritical", "temperature -50 to +150°C", "±0.5°C precision"]
        }
    },
    "ATEX": {
        "keywords_primary": [
            "product_model (ATEX Sensor)",
            "pressure_range (20 bar)",
            "competitor (Danfoss AKS 38 ATEX, Honeywell Smart ATEX)",
            "feature (ATEX Ex ia IIC T4, intrinsic safety, explosive atmospheres)",
            "application (R290 propane, R600a isobutane, Zone 0/1/2, petrochemical)"
        ],
        "keywords_synonyms": {
            "ATEX": ["explosive atmosphere", "intrinsic safety", "Ex ia"],
            "R290": ["propane", "flammable refrigerant"],
            "R600a": ["isobutane", "hydrocarbon refrigerant"],
            "Zone 0/1/2": ["hazardous area classification"]
        },
        "keywords_relations": {
            "certifications": ["ATEX Ex ia IIC T4", "EN 60079-0", "EN 60079-11"],
            "mandatory_for": ["Group A3 refrigerants", "R290", "R600a", "hydrogen"],
            "installation": ["Zener barrier required", "intrinsic safety loop", "Open Collector output"],
            "applications": ["commercial refrigeration R290", "domestic appliances", "petrochemical"]
        }
    }
}

# Keywords per innovazioni uniche
INNOVATION_KEYWORDS = {
    "Rotalock_Innovation": {
        "keywords_primary": [
            "innovation (Rotalock native mount)",
            "unique_product (only globally)",
            "savings (75-105€ per installation)",
            "feature (zero adapters, direct installation, 5 min setup)",
            "application (Rotalock valves, liquid receivers, quick retrofit)"
        ],
        "keywords_synonyms": {
            "Rotalock innovation": ["market first", "exclusive Teklab", "uncovered niche"],
            "no adapters": ["direct mount", "native connection", "plug-and-play"],
            "ROI": ["immediate payback", "first installation savings"]
        },
        "keywords_relations": {
            "problem_solved": ["adapter elimination", "leak point reduction", "installation time"],
            "valve_compatibility": ["Sporlan", "Castel", "Parker", "Danfoss EVRA"],
            "savings_breakdown": ["40 min labor (40-70€)", "adapter 30€", "gaskets 5€"]
        }
    },
    "K25_Innovation": {
        "keywords_primary": [
            "innovation (2-in-1 level + temperature)",
            "unique_product (only CO2 combo globally)",
            "savings (50% installation, 200-300€ hardware)",
            "feature (NPN + 4-20mA, single calibration, one leak point)",
            "application (CO2 transcritical, dual sensing, gas discharge)"
        ],
        "keywords_synonyms": {
            "2-in-1": ["dual sensor", "integrated combo", "two-in-one"],
            "revolutionary": ["market first", "game changer", "innovation exclusive"]
        },
        "keywords_relations": {
            "vs_competitors": ["1 sensor vs 2 Danfoss", "1 installation vs 2", "1 hole vs 2"],
            "4-20mA_benefits": ["no PT1000 converter", "universal PLC", "long cabling", "noise immunity"],
            "ROI": ["immediate payback", "30-60€ labor", "200-300€ hardware", "50% leak risk"]
        }
    },
    "K11_Innovation": {
        "keywords_primary": [
            "innovation (configurable output 3-in-1)",
            "unique_feature (NPN/PNP/AC selectable)",
            "savings (66% SKU reduction)",
            "feature (DIP switch config, universal PLC, 2 min setup)",
            "application (stock optimization, order error elimination, retrofit flexibility)"
        ],
        "keywords_synonyms": {
            "configurable": ["selectable", "programmable", "universal"],
            "3-in-1": ["triple output", "multi-mode"]
        },
        "keywords_relations": {
            "vs_competitors": ["1 SKU vs 3 Danfoss", "eliminates version selection"],
            "outputs": ["NPN sink", "PNP source", "AC relay"],
            "business_benefits": ["stock reduction", "capital savings", "flexibility"]
        }
    },
    "TK4_Innovation": {
        "keywords_primary": [
            "innovation (NFC wireless config)",
            "unique_product (first NFC oil regulator globally)",
            "savings (95% time, 30 sec vs 10 min)",
            "feature (smartphone app, diagnostic history, no panel opening)",
            "application (rapid commissioning, field maintenance, multi-site)"
        ],
        "keywords_synonyms": {
            "NFC": ["Near Field Communication", "wireless", "contactless"],
            "first globally": ["market pioneer", "innovation leader"]
        },
        "keywords_relations": {
            "vs_BLE": ["tap-and-go vs pairing", "<5cm vs 10m range", "higher security"],
            "time_savings": ["30 sec config", "no panel access", "instant diagnostics"],
            "ROI_example": ["10 devices = 95 min saved = 1.5h labor (90-150€)"]
        }
    },
    "LCXP_Innovation": {
        "keywords_primary": [
            "innovation (only DIN 120 bar globally)",
            "unique_product (uncovered niche)",
            "feature (DIN 43650-A high pressure, EU market standard)",
            "application (CO2 transcritical, DIN preference, cable economics)"
        ],
        "keywords_synonyms": {
            "only DIN 120bar": ["unique globally", "market first"],
            "DIN vs M12": ["connector comparison", "EU standard"]
        },
        "keywords_relations": {
            "market_gap": ["all competitors use M12", "Teklab filled niche"],
            "DIN_advantages": ["50% cheaper cables", "higher EU stock", "technician familiarity"],
            "applications": ["EU CO2 market", "DIN standardization projects"]
        }
    },
    "TK4MB_Innovation": {
        "keywords_primary": [
            "innovation (triple interface Relay + NFC + Modbus)",
            "unique_combination (no competitor equivalent)",
            "feature (flexible architecture, local + centralized control)",
            "application (Industry 4.0, scalable deployment, hybrid systems)"
        ],
        "keywords_synonyms": {
            "triple interface": ["multi-level", "hybrid control"],
            "flexible architecture": ["scalable", "adaptable deployment"]
        },
        "keywords_relations": {
            "interfaces": ["standalone relay", "local NFC", "centralized Modbus"],
            "deployment_flexibility": ["start standalone", "add supervision later", "no rewiring"],
            "Modbus_RTU_choice": ["robust RS485", "economical vs TCP", "industrial standard"]
        }
    }
}

def add_keywords_to_file(file_path):
    """Aggiunge keywords a un singolo file JSON"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Determina quale set di keywords usare
        teklab_product = data['metadata'].get('teklab_product', '')
        chunk_title = data['metadata'].get('chunk_title', '')
        
        keywords = None
        
        # Cerca keywords per prodotto
        if teklab_product in PRODUCT_KEYWORDS:
            keywords = PRODUCT_KEYWORDS[teklab_product]
        # Cerca keywords per innovazione
        elif "Innovation" in chunk_title or "innovation" in file_path.stem:
            for key, kw in INNOVATION_KEYWORDS.items():
                if key.replace('_Innovation', '') in chunk_title or key.replace('_Innovation', '') in file_path.stem:
                    keywords = kw
                    break
        
        if keywords:
            # Aggiungi keywords se non esistono
            if 'keywords_primary' not in data['metadata']:
                data['metadata']['keywords_primary'] = keywords['keywords_primary']
            if 'keywords_synonyms' not in data['metadata']:
                data['metadata']['keywords_synonyms'] = keywords['keywords_synonyms']
            if 'keywords_relations' not in data['metadata']:
                data['metadata']['keywords_relations'] = keywords['keywords_relations']
            
            # Salva file
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            
            return True, f"✅ {file_path.name}"
        else:
            return False, f"⚠️  {file_path.name} - Nessun mapping keywords trovato"
            
    except Exception as e:
        return False, f"❌ {file_path.name} - Errore: {e}"

def main():
    print("🔧 Aggiunta keywords ai chunk Marketing...\n")
    
    if not MARKETING_PATH.exists():
        print(f"❌ Cartella Marketing non trovata: {MARKETING_PATH}")
        return
    
    # Processa Competitor_Analysis
    comp_analysis_path = MARKETING_PATH / "Competitor_Analysis"
    value_prop_path = MARKETING_PATH / "Value_Proposition"
    
    total_processed = 0
    total_success = 0
    
    for folder in [comp_analysis_path, value_prop_path]:
        if not folder.exists():
            continue
            
        print(f"📁 Processando: {folder.name}/\n")
        
        json_files = list(folder.glob("*.json"))
        for json_file in json_files:
            success, message = add_keywords_to_file(json_file)
            print(f"   {message}")
            total_processed += 1
            if success:
                total_success += 1
        
        print()
    
    print("="*60)
    print(f"✅ Completato! {total_success}/{total_processed} file aggiornati con keywords")
    print("="*60)

if __name__ == "__main__":
    main()
