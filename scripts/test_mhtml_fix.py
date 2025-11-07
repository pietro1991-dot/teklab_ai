"""
Test estrazione HTML da MHTML - Verifica fix
"""
import re
import quopri
from pathlib import Path
from bs4 import BeautifulSoup

def extract_html_from_mhtml(mhtml_content: str) -> str:
    """Estrae HTML puro da MHTML"""
    try:
        # Split per boundary principale
        parts = re.split(r'------MultipartBoundary--[a-zA-Z0-9-]+----', mhtml_content)
        
        for part in parts:
            # Cerca parte con Content-Type: text/html
            if 'Content-Type: text/html' in part:
                # Rimuovi header MIME fino a doppio newline
                lines = part.split('\n')
                
                # Trova dove finiscono gli header
                html_start = 0
                for i, line in enumerate(lines):
                    if line.strip() == '' and i > 0:
                        html_start = i + 1
                        break
                
                # Estrai HTML puro
                html_content = '\n'.join(lines[html_start:])
                
                # Decodifica Quoted-Printable se presente
                if '=' in html_content and re.search(r'=[0-9A-F]{2}', html_content):
                    try:
                        html_bytes = html_content.encode('latin-1')
                        decoded_bytes = quopri.decodestring(html_bytes)
                        html_content = decoded_bytes.decode('utf-8', errors='ignore')
                    except Exception:
                        pass
                
                # Verifica che sia HTML valido
                if '<html' in html_content.lower() or '<body' in html_content.lower():
                    return html_content
        
        return mhtml_content
        
    except Exception as e:
        print(f"⚠️  Errore: {e}")
        return mhtml_content

def test_mhtml_extraction():
    """Testa estrazione su file K25"""
    print("\n" + "="*60)
    print("TEST ESTRAZIONE HTML DA MHTML")
    print("="*60)
    
    # File di test
    test_file = Path("Fonti/Autori/Teklab/K25 4-20 mA Level Switch - Teklab.eu.mhtml")
    
    if not test_file.exists():
        print(f"❌ File non trovato: {test_file}")
        return
    
    print(f"\n📄 File test: {test_file.name}")
    
    # Leggi contenuto grezzo
    with open(test_file, 'r', encoding='utf-8') as f:
        raw_mhtml = f.read()
    
    print(f"📊 Dimensione MHTML grezzo: {len(raw_mhtml):,} chars")
    
    # Preview grezzo (primi 500 chars)
    print("\n🔍 PREVIEW MHTML GREZZO (primi 500 chars):")
    print("-" * 60)
    print(raw_mhtml[:500])
    print("-" * 60)
    
    # Estrai HTML
    html_content = extract_html_from_mhtml(raw_mhtml)
    
    print(f"\n📊 Dimensione HTML estratto: {len(html_content):,} chars")
    
    # Preview HTML estratto
    print("\n🔍 PREVIEW HTML ESTRATTO (primi 500 chars):")
    print("-" * 60)
    print(html_content[:500])
    print("-" * 60)
    
    # Pulisci con BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Rimuovi elementi non necessari
    for tag in soup(['script', 'style', 'nav', 'header', 'footer', 'iframe']):
        tag.decompose()
    
    # Estrai testo
    text = soup.get_text()
    text = re.sub(r'\s+', ' ', text).strip()
    
    print(f"\n📊 Dimensione TESTO PULITO: {len(text):,} chars")
    
    # Preview testo pulito
    print("\n🔍 PREVIEW TESTO PULITO (primi 500 chars):")
    print("-" * 60)
    print(text[:500])
    print("-" * 60)
    
    # Verifica
    issues = []
    
    if 'From: <Saved by Blink>' in text:
        issues.append("❌ Header MHTML ancora presente")
    
    if 'MultipartBoundary' in text:
        issues.append("❌ Boundary MHTML ancora presente")
    
    keywords = ['k25', 'teklab', 'level', 'switch', 'sensor']
    found = [kw for kw in keywords if kw.lower() in text.lower()]
    
    if found:
        print(f"\n✅ Keywords trovate: {', '.join(found)}")
    else:
        issues.append("❌ Nessuna keyword Teklab trovata")
    
    if issues:
        print("\n⚠️  PROBLEMI:")
        for issue in issues:
            print(f"   {issue}")
    else:
        print("\n✅ ESTRAZIONE COMPLETATA CON SUCCESSO!")
    
    print("\n" + "="*60)

if __name__ == "__main__":
    test_mhtml_extraction()
