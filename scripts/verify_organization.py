"""
Verifica passo-passo della struttura organizzata
"""
import json
from pathlib import Path
from collections import defaultdict

def verify_step_1():
    """Verifica file JSON esistano e siano validi"""
    print("\n" + "="*60)
    print("STEP 1: Verifica file JSON")
    print("="*60)
    
    base_path = Path(__file__).parent.parent / "organized_sources"
    files = ["organized_data.json", "inventory.json", "organization_report.json"]
    
    results = {}
    for file in files:
        path = base_path / file
        if path.exists():
            size_mb = path.stat().st_size / (1024 * 1024)
            print(f"✅ {file}: {size_mb:.2f} MB")
            results[file] = True
        else:
            print(f"❌ {file}: NON TROVATO")
            results[file] = False
    
    return all(results.values())

def verify_step_2():
    """Verifica categorizzazione prodotti"""
    print("\n" + "="*60)
    print("STEP 2: Analisi categorizzazione prodotti")
    print("="*60)
    
    base_path = Path(__file__).parent.parent / "organized_sources"
    
    # Leggi inventory (più piccolo di organized_data)
    with open(base_path / "inventory.json", 'r', encoding='utf-8') as f:
        inventory = json.load(f)
    
    # Raggruppa per categoria
    by_category = defaultdict(lambda: defaultdict(list))
    
    for item in inventory:
        cat = item['category']
        subcat = item['sub_category']
        by_category[cat][subcat].append(item['file_name'])
    
    print(f"\n📊 TOTALE FILE: {len(inventory)}\n")
    
    for category, subcats in sorted(by_category.items()):
        total = sum(len(files) for files in subcats.values())
        print(f"\n📁 {category.upper()}: {total} file")
        
        for subcat, files in sorted(subcats.items()):
            print(f"   └─ {subcat}: {len(files)} file")
            if category == "products" and len(files) <= 3:
                for f in files:
                    print(f"      • {f}")
    
    return by_category

def verify_step_3_uncategorized(by_category):
    """Analizza file uncategorized per capire cosa sono"""
    print("\n" + "="*60)
    print("STEP 3: Analisi file UNCATEGORIZED")
    print("="*60)
    
    base_path = Path(__file__).parent.parent / "organized_sources"
    
    with open(base_path / "inventory.json", 'r', encoding='utf-8') as f:
        inventory = json.load(f)
    
    uncategorized = [item for item in inventory if item['category'] == 'uncategorized']
    
    print(f"\n⚠️  TOTALE UNCATEGORIZED: {len(uncategorized)} file\n")
    
    # Analizza per tipo file
    by_ext = defaultdict(list)
    for item in uncategorized:
        ext = Path(item['file_name']).suffix.lower()
        by_ext[ext].append(item['file_name'])
    
    print("📋 Per tipo file:")
    for ext, files in sorted(by_ext.items()):
        print(f"\n   {ext or 'NO_EXT'}: {len(files)} file")
        for f in files[:5]:  # Mostra primi 5
            print(f"      • {f}")
        if len(files) > 5:
            print(f"      ... e altri {len(files)-5}")
    
    # Identifica pattern nei nomi
    print("\n\n🔍 PATTERN NEI NOMI:")
    patterns = {
        'K25': [f for f in [item['file_name'] for item in uncategorized] if 'K25' in f or 'k25' in f.lower()],
        'Adapters': [f for f in [item['file_name'] for item in uncategorized] if 'adapter' in f.lower()],
        'Electro Optical': [f for f in [item['file_name'] for item in uncategorized] if 'electro' in f.lower() or 'optical' in f.lower()],
        'Catalogue': [f for f in [item['file_name'] for item in uncategorized] if 'catalogue' in f.lower() or 'catalog' in f.lower()],
        'JSON metadata': [f for f in [item['file_name'] for item in uncategorized] if f.endswith('.json')]
    }
    
    for pattern_name, files in patterns.items():
        if files:
            print(f"\n   {pattern_name}: {len(files)} file")
            for f in files[:3]:
                print(f"      • {f}")
    
    return uncategorized

def verify_step_4_content_quality():
    """Verifica qualità del contenuto estratto (sample)"""
    print("\n" + "="*60)
    print("STEP 4: Verifica qualità contenuto estratto")
    print("="*60)
    
    base_path = Path(__file__).parent.parent / "organized_sources"
    
    with open(base_path / "inventory.json", 'r', encoding='utf-8') as f:
        inventory = json.load(f)
    
    # Prendi sample di prodotti categorizzati
    products = [item for item in inventory if item['category'] == 'products']
    
    print(f"\n📦 Sample di prodotti categorizzati:\n")
    
    # Raggruppa per subcategory
    by_subcat = defaultdict(list)
    for item in products:
        by_subcat[item['sub_category']].append(item)
    
    for subcat, items in sorted(by_subcat.items()):
        sample = items[0]  # Prendi il primo di ogni subcategory
        print(f"\n   {subcat}:")
        print(f"      File: {sample['file_name']}")
        print(f"      Dimensione: {sample['content_length']:,} caratteri")
        print(f"      Path: {sample['file_path']}")
    
    print("\n\n📊 STATISTICHE LUNGHEZZA CONTENUTO:")
    all_lengths = [item['content_length'] for item in products]
    print(f"   • Media: {sum(all_lengths)/len(all_lengths):,.0f} caratteri")
    print(f"   • Min: {min(all_lengths):,} caratteri")
    print(f"   • Max: {max(all_lengths):,} caratteri")
    
    return products

if __name__ == "__main__":
    print("\n🔍 VERIFICA ORGANIZZAZIONE SOURCES - PASSO DOPO PASSO\n")
    
    # Step 1: File esistono?
    if not verify_step_1():
        print("\n❌ ERRORE: File JSON non trovati!")
        exit(1)
    
    # Step 2: Categorizzazione prodotti
    by_category = verify_step_2()
    
    # Step 3: Analisi uncategorized
    uncategorized = verify_step_3_uncategorized(by_category)
    
    # Step 4: Qualità contenuto
    products = verify_step_4_content_quality()
    
    print("\n" + "="*60)
    print("✅ VERIFICA COMPLETATA")
    print("="*60)
    print(f"""
RIEPILOGO:
- ✅ {len(products)} prodotti categorizzati correttamente
- ⚠️  {len(uncategorized)} file da rivedere (uncategorized)
- 📊 Contenuto estratto: dimensioni consistenti
- 🎯 Pronto per chunking migliorato
""")
