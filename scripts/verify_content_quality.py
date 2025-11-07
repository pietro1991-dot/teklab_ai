"""
Step 4: Verifica qualità contenuto estratto da BeautifulSoup
"""
import json
from pathlib import Path

def check_content_quality():
    """Verifica sample di contenuto estratto"""
    print("\n" + "="*60)
    print("STEP 4: VERIFICA QUALITÀ CONTENUTO ESTRATTO")
    print("="*60)
    
    base_path = Path(__file__).parent.parent / "organized_sources"
    
    # Carica organized_data (ATTENZIONE: file molto grande)
    print("\n📂 Caricamento organized_data.json (154 MB)...")
    with open(base_path / "organized_data.json", 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print("✅ Dati caricati!\n")
    
    # Analizza sample da diverse categorie
    samples = []
    
    # 1. TK3+ da products
    if 'TK Series - TK3+' in data['products']:
        tk3_files = data['products']['TK Series - TK3+']
        if tk3_files:
            samples.append(('PRODUCTS - TK3+', tk3_files[0]))
    
    # 2. K25 da products
    if 'K25 Series' in data['products']:
        k25_files = data['products']['K25 Series']
        if k25_files:
            samples.append(('PRODUCTS - K25', k25_files[0]))
    
    # 3. Electro Optical da products
    if 'Electro Optical Sensors' in data['products']:
        eo_files = data['products']['Electro Optical Sensors']
        if eo_files:
            samples.append(('PRODUCTS - Electro Optical', eo_files[0]))
    
    # 4. Adapters da support
    if 'Adapters and Accessories' in data['support']:
        adapter_files = data['support']['Adapters and Accessories']
        if adapter_files:
            samples.append(('SUPPORT - Adapters', adapter_files[0]))
    
    # 5. FAQs da support
    if 'FAQs and Troubleshooting' in data['support']:
        faq_files = data['support']['FAQs and Troubleshooting']
        if faq_files:
            samples.append(('SUPPORT - FAQs', faq_files[0]))
    
    # Analizza ogni sample
    for category, file_data in samples:
        print("\n" + "-"*60)
        print(f"📄 {category}")
        print("-"*60)
        print(f"File: {file_data['file_name']}")
        print(f"Dimensione: {file_data['content_length']:,} caratteri")
        
        content = file_data['content']
        
        # Prendi primi 500 caratteri
        preview = content[:500]
        
        print("\n🔍 PREVIEW CONTENUTO (primi 500 chars):")
        print("-" * 60)
        print(preview)
        print("-" * 60)
        
        # Verifica qualità
        issues = []
        
        # 1. Check HTML residuo
        if '<' in preview and '>' in preview:
            html_tags = preview.count('<')
            issues.append(f"⚠️  Possibili tag HTML residui: {html_tags} occorrenze di '<'")
        
        # 2. Check caratteri strani
        if '&nbsp;' in preview or '&amp;' in preview:
            issues.append("⚠️  Entità HTML non decodificate (&nbsp;, &amp;, ecc.)")
        
        # 3. Check spazi multipli eccessivi
        if '    ' in preview:  # 4+ spazi consecutivi
            issues.append("⚠️  Spazi multipli non normalizzati")
        
        # 4. Check contenuto sensato
        words = preview.split()
        if len(words) < 10:
            issues.append("❌ Contenuto troppo breve o vuoto")
        
        # 5. Check keywords Teklab presenti
        keywords = ['teklab', 'tk', 'lc', 'sensor', 'level', 'switch', 'oil']
        found_keywords = [kw for kw in keywords if kw in preview.lower()]
        
        if found_keywords:
            print(f"\n✅ Keywords trovate: {', '.join(found_keywords)}")
        else:
            issues.append("⚠️  Nessuna keyword Teklab trovata nei primi 500 chars")
        
        # Report issues
        if issues:
            print("\n⚠️  PROBLEMI RILEVATI:")
            for issue in issues:
                print(f"   {issue}")
        else:
            print("\n✅ CONTENUTO PULITO - Nessun problema rilevato")
        
        # Statistiche
        print(f"\n📊 STATISTICHE:")
        print(f"   • Parole totali: {len(content.split()):,}")
        print(f"   • Caratteri totali: {len(content):,}")
        print(f"   • Media lunghezza parola: {len(content) / max(1, len(content.split())):.1f} chars")
    
    print("\n" + "="*60)
    print("✅ VERIFICA CONTENUTO COMPLETATA")
    print("="*60)

if __name__ == "__main__":
    check_content_quality()
