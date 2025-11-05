"""
DEBUG COMPLETO SISTEMA TEKLAB RAG
Verifica tutti i componenti critici prima del deployment produzione
"""

import pickle
import os
from pathlib import Path

# ANSI colors per output
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"

def check_embeddings_cache():
    """Verifica integrità embeddings_cache.pkl"""
    print(f"\n{BLUE}{'='*70}{RESET}")
    print(f"{BLUE}1. VERIFICA EMBEDDINGS CACHE{RESET}")
    print(f"{BLUE}{'='*70}{RESET}\n")
    
    cache_path = Path("ai_system/Embedding/embeddings_cache.pkl")
    
    if not cache_path.exists():
        print(f"{RED}❌ ERRORE: embeddings_cache.pkl NON TROVATO!{RESET}")
        return False
    
    print(f"{GREEN}✅ File trovato:{RESET} {cache_path} ({cache_path.stat().st_size / 1024:.1f} KB)")
    
    try:
        with open(cache_path, 'rb') as f:
            cache = pickle.load(f)
        
        chunks_data = cache.get('chunks_data', {})
        qa_data = cache.get('qa_data', {})
        embeddings = cache.get('embeddings', {})
        
        print(f"\n{YELLOW}📊 STATISTICHE CACHE:{RESET}")
        print(f"   Chunks: {len(chunks_data)}")
        print(f"   Q&A pairs: {len(qa_data)}")
        print(f"   Embeddings totali: {len(embeddings)}")
        
        # Verifica chunks senza product_model
        unknown_chunks = []
        chunks_with_messages = 0
        chunks_with_assistant = 0
        
        print(f"\n{YELLOW}🔍 ANALISI CHUNKS:{RESET}")
        
        for chunk_id, chunk_data in chunks_data.items():
            metadata = chunk_data.get('metadata', {})
            product_model = metadata.get('product_model', 'Unknown')
            
            if product_model == 'Unknown':
                unknown_chunks.append(chunk_id)
            
            # Verifica struttura messages
            messages = chunk_data.get('messages', [])
            if messages:
                chunks_with_messages += 1
                if len(messages) > 2:
                    chunks_with_assistant += 1
        
        print(f"   Chunks con messages: {chunks_with_messages}/{len(chunks_data)}")
        print(f"   Chunks con messages[2] (assistant): {chunks_with_assistant}/{len(chunks_data)}")
        
        if unknown_chunks:
            print(f"\n{RED}❌ CHUNK SENZA product_model ({len(unknown_chunks)}):{RESET}")
            for chunk_id in unknown_chunks[:5]:  # Mostra primi 5
                print(f"      - {chunk_id}")
            if len(unknown_chunks) > 5:
                print(f"      ... e altri {len(unknown_chunks) - 5}")
            return False
        else:
            print(f"{GREEN}✅ TUTTI i chunks hanno product_model{RESET}")
        
        # Mostra sample chunk structure
        print(f"\n{YELLOW}📝 SAMPLE CHUNK STRUCTURE:{RESET}")
        sample_id = list(chunks_data.keys())[0]
        sample_chunk = chunks_data[sample_id]
        
        print(f"   Chunk ID: {sample_id}")
        print(f"   Category: {sample_chunk.get('category', 'N/A')}")
        print(f"   Metadata product_model: {sample_chunk.get('metadata', {}).get('product_model', 'N/A')}")
        print(f"   Messages count: {len(sample_chunk.get('messages', []))}")
        
        if sample_chunk.get('messages'):
            for i, msg in enumerate(sample_chunk['messages']):
                role = msg.get('role', 'unknown')
                content_len = len(msg.get('content', ''))
                print(f"      messages[{i}] role={role}, length={content_len} chars")
        
        return True
        
    except Exception as e:
        print(f"{RED}❌ ERRORE caricamento cache: {e}{RESET}")
        return False


def check_chatbot_config():
    """Verifica configurazione 6_chatbot_ollama.py"""
    print(f"\n{BLUE}{'='*70}{RESET}")
    print(f"{BLUE}2. VERIFICA CHATBOT CONFIGURATION{RESET}")
    print(f"{BLUE}{'='*70}{RESET}\n")
    
    chatbot_path = Path("scripts/6_chatbot_ollama.py")
    
    if not chatbot_path.exists():
        print(f"{RED}❌ ERRORE: 6_chatbot_ollama.py NON TROVATO!{RESET}")
        return False
    
    with open(chatbot_path, 'r', encoding='utf-8') as f:
        code = f.read()
    
    checks = {
        "device='cpu'": "Embeddings su CPU",
        "min_similarity=0.28": "Threshold similarity 0.28",
        "top_k=5": "Top-k chunks = 5",
        "max_context_length = 4000": "Context limit 4000 chars",
        "TEKLAB TECHNICAL SALES ASSISTANT": "Prompt Teklab brand",
        "chunk_data['messages'][2].get('content'": "Text extraction messages[2]"
    }
    
    print(f"{YELLOW}🔍 PARAMETRI CRITICI:{RESET}")
    
    all_ok = True
    for pattern, description in checks.items():
        if pattern in code:
            print(f"{GREEN}✅ {description}{RESET}")
        else:
            print(f"{RED}❌ MANCANTE: {description}{RESET}")
            all_ok = False
    
    # Check filter order (CRITICAL bug fix)
    if "filtered = [(item_id, score, item_type) for item_id, score, item_type in similarities if score >= min_similarity]" in code:
        print(f"{GREEN}✅ Filter order: BEFORE top_k (correct){RESET}")
    else:
        print(f"{RED}❌ Filter order: potenziale bug!{RESET}")
        all_ok = False
    
    return all_ok


def check_backend_api_config():
    """Verifica configurazione backend_api/app.py"""
    print(f"\n{BLUE}{'='*70}{RESET}")
    print(f"{BLUE}3. VERIFICA BACKEND API CONFIGURATION{RESET}")
    print(f"{BLUE}{'='*70}{RESET}\n")
    
    backend_path = Path("backend_api/app.py")
    
    if not backend_path.exists():
        print(f"{RED}❌ ERRORE: backend_api/app.py NON TROVATO!{RESET}")
        return False
    
    with open(backend_path, 'r', encoding='utf-8') as f:
        code = f.read()
    
    checks = {
        "device='cpu'": "Embeddings su CPU",
        "sim >= 0.25": "Threshold similarity (backend può usare 0.25-0.28)",
        "max_context_length = 4000": "Context limit 4000 chars",
        "TEKLAB TECHNICAL SALES ASSISTANT": "Prompt Teklab brand (identico chatbot)",
        "messages[2].get('content'": "Text extraction messages[2]"
    }
    
    print(f"{YELLOW}🔍 PARAMETRI CRITICI:{RESET}")
    
    all_ok = True
    for pattern, description in checks.items():
        if pattern in code:
            print(f"{GREEN}✅ {description}{RESET}")
        else:
            print(f"{RED}❌ MANCANTE: {description}{RESET}")
            all_ok = False
    
    # Verifica top_k nel get_relevant_chunks
    if "top_k=3" in code or "top_k=5" in code:
        print(f"{GREEN}✅ top_k configurato{RESET}")
    else:
        print(f"{YELLOW}⚠️  top_k non trovato - verificare manualmente{RESET}")
    
    return all_ok


def check_prompt_consistency():
    """Verifica consistency tra chatbot e backend prompts"""
    print(f"\n{BLUE}{'='*70}{RESET}")
    print(f"{BLUE}4. VERIFICA PROMPT CONSISTENCY{RESET}")
    print(f"{BLUE}{'='*70}{RESET}\n")
    
    chatbot_path = Path("scripts/6_chatbot_ollama.py")
    backend_path = Path("backend_api/app.py")
    
    with open(chatbot_path, 'r', encoding='utf-8') as f:
        chatbot_code = f.read()
    
    with open(backend_path, 'r', encoding='utf-8') as f:
        backend_code = f.read()
    
    # Extract prompt signatures
    chatbot_has_teklab = "TEKLAB TECHNICAL SALES ASSISTANT" in chatbot_code
    backend_has_teklab = "TEKLAB TECHNICAL SALES ASSISTANT" in backend_code
    
    chatbot_has_guidelines = "RESPONSE GUIDELINES" in chatbot_code
    backend_has_guidelines = "RESPONSE GUIDELINES" in backend_code
    
    print(f"{YELLOW}🔍 PROMPT STRUCTURE:{RESET}")
    
    if chatbot_has_teklab and backend_has_teklab:
        print(f"{GREEN}✅ Entrambi usano 'TEKLAB TECHNICAL SALES ASSISTANT'{RESET}")
    else:
        print(f"{RED}❌ Prompt diversi tra chatbot e backend!{RESET}")
        print(f"   Chatbot: {'✅' if chatbot_has_teklab else '❌'}")
        print(f"   Backend: {'✅' if backend_has_teklab else '❌'}")
        return False
    
    if chatbot_has_guidelines and backend_has_guidelines:
        print(f"{GREEN}✅ Entrambi usano 'RESPONSE GUIDELINES'{RESET}")
    else:
        print(f"{YELLOW}⚠️  Guidelines diverse (accettabile se funzionalmente equivalenti){RESET}")
    
    return True


def check_system_prompt():
    """Verifica system prompt in prompts_config.py"""
    print(f"\n{BLUE}{'='*70}{RESET}")
    print(f"{BLUE}5. VERIFICA SYSTEM PROMPT{RESET}")
    print(f"{BLUE}{'='*70}{RESET}\n")
    
    prompt_path = Path("Prompt/prompts_config.py")
    
    if not prompt_path.exists():
        print(f"{RED}❌ ERRORE: Prompt/prompts_config.py NON TROVATO!{RESET}")
        return False
    
    with open(prompt_path, 'r', encoding='utf-8') as f:
        code = f.read()
    
    checks = {
        "TECHNICAL SALES ASSISTANT": "Ruolo sales assistant",
        "LANGUAGE RULES": "Regole multilingua",
        "SAME LANGUAGE as user": "Match lingua cliente",
        "Italian/English/Spanish/German": "Supporto multilingua"
    }
    
    print(f"{YELLOW}🔍 SYSTEM PROMPT FEATURES:{RESET}")
    
    all_ok = True
    for pattern, description in checks.items():
        if pattern in code:
            print(f"{GREEN}✅ {description}{RESET}")
        else:
            print(f"{YELLOW}⚠️  {description} - verificare manualmente{RESET}")
    
    return True


def run_all_checks():
    """Esegui tutti i check"""
    print(f"\n{BLUE}{'#'*70}{RESET}")
    print(f"{BLUE}#  DEBUG COMPLETO SISTEMA TEKLAB RAG - PRODUZIONE{RESET}")
    print(f"{BLUE}{'#'*70}{RESET}")
    
    results = {
        "Embeddings Cache": check_embeddings_cache(),
        "Chatbot Config": check_chatbot_config(),
        "Backend API Config": check_backend_api_config(),
        "Prompt Consistency": check_prompt_consistency(),
        "System Prompt": check_system_prompt()
    }
    
    print(f"\n{BLUE}{'='*70}{RESET}")
    print(f"{BLUE}RIEPILOGO FINALE{RESET}")
    print(f"{BLUE}{'='*70}{RESET}\n")
    
    all_passed = True
    for check_name, passed in results.items():
        status = f"{GREEN}✅ PASS{RESET}" if passed else f"{RED}❌ FAIL{RESET}"
        print(f"{status}  {check_name}")
        if not passed:
            all_passed = False
    
    print()
    
    if all_passed:
        print(f"{GREEN}{'='*70}{RESET}")
        print(f"{GREEN}🎉 TUTTI I CHECK SUPERATI - SISTEMA PRONTO PER PRODUZIONE{RESET}")
        print(f"{GREEN}{'='*70}{RESET}\n")
        
        print(f"{YELLOW}📋 PROSSIMI STEP:{RESET}")
        print(f"   1. Test chatbot: python scripts/6_chatbot_ollama.py")
        print(f"   2. Query test: 'Quale TK3+ per CO2 transcritical 100 bar?'")
        print(f"   3. Query test: 'Difference between TK3+ 80bar and 130bar?'")
        print(f"   4. Query test: 'LC-XP vs LC-XT per PLC integration?'")
        print(f"   5. Verifica retrieval: 3-5 chunks, similarity >0.28")
        print(f"   6. Verifica risposte: specs corretti, nessun hallucination")
        print(f"   7. Start backend: python backend_api/app.py")
        print(f"   8. Test UI: UI_experience/index.html\n")
    else:
        print(f"{RED}{'='*70}{RESET}")
        print(f"{RED}❌ ALCUNI CHECK FALLITI - VERIFICARE ERRORI SOPRA{RESET}")
        print(f"{RED}{'='*70}{RESET}\n")
    
    return all_passed


if __name__ == "__main__":
    run_all_checks()
