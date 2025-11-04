"""
Test rapido backend API
Verifica connessione e risposta del chatbot
"""

import requests
import json

API_URL = "http://localhost:5000"

def test_health():
    """Test health check"""
    print("🔍 Testing health endpoint...")
    try:
        response = requests.get(f"{API_URL}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check OK")
            print(f"   Status: {data['status']}")
            print(f"   Model loaded: {data['model_loaded']}")
            return True
        else:
            print(f"❌ Health check failed: HTTP {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed. Backend non avviato?")
        print("   Esegui: python backend_api/app.py")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_chat():
    """Test chat endpoint"""
    print("\n💬 Testing chat endpoint...")
    
    test_message = "Cosa sono i chakra?"
    
    try:
        response = requests.post(
            f"{API_URL}/chat",
            json={"message": test_message},
            timeout=60
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Chat response OK")
            print(f"   User: {test_message}")
            print(f"   Bot: {data['response'][:100]}...")
            print(f"   Status: {data['status']}")
            return True
        else:
            error = response.json()
            print(f"❌ Chat failed: {error.get('error', 'Unknown error')}")
            return False
            
    except requests.exceptions.Timeout:
        print("⏰ Timeout: Il modello impiega troppo tempo")
        print("   Questo è normale la prima volta (caricamento modello)")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_stats():
    """Test stats endpoint"""
    print("\n📊 Testing stats endpoint...")
    try:
        response = requests.get(f"{API_URL}/stats", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Stats OK")
            print(f"   Model loaded: {data['model_loaded']}")
            print(f"   Conversation turns: {data['conversation_turns']}")
            print(f"   Endpoints: {len(data['endpoints'])}")
            return True
        else:
            print(f"❌ Stats failed: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("\n" + "="*70)
    print("🧪 SPIRITUALITY AI - Backend API Test")
    print("="*70 + "\n")
    
    # Test sequenziale
    results = []
    
    # 1. Health check
    results.append(("Health", test_health()))
    
    if results[0][1]:  # Solo se health passa
        # 2. Stats
        results.append(("Stats", test_stats()))
        
        # 3. Chat (opzionale, richiede modello caricato)
        print("\n⚠️  Il test chat può richiedere tempo (caricamento modello)")
        user_input = input("Vuoi testare /chat? (y/n): ").strip().lower()
        if user_input == 'y':
            results.append(("Chat", test_chat()))
    
    # Riepilogo
    print("\n" + "="*70)
    print("📋 RISULTATI")
    print("="*70)
    for name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"   {name:<15} {status}")
    
    print("\n" + "="*70 + "\n")
    
    # Conclusione
    if all(r[1] for r in results):
        print("🎉 Tutti i test passati! Backend funzionante.")
        print("💡 Ora apri UI_experience/index.html nel browser")
    else:
        print("⚠️  Alcuni test falliti. Controlla errori sopra.")
