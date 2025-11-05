"""
Test Multi-User Queue System
Simula 5 utenti concorrenti che inviano richieste
"""
import requests
import threading
import time
from datetime import datetime

BACKEND_URL = "http://localhost:5000"

def simulate_user(user_id, query, delay=0):
    """Simula un singolo utente che fa una richiesta"""
    time.sleep(delay)
    
    print(f"\n[User {user_id}] 🔵 Sending query at {datetime.now().strftime('%H:%M:%S')}")
    print(f"[User {user_id}] Query: {query}")
    
    try:
        response = requests.post(
            f"{BACKEND_URL}/chat/stream",
            json={"message": query},
            stream=True,
            timeout=300  # 5 min max
        )
        
        start_time = time.time()
        queue_time = None
        processing_started = False
        tokens_received = 0
        
        for line in response.iter_lines():
            if line:
                try:
                    # Parse SSE format: "data: {...}"
                    if line.startswith(b'data: '):
                        import json
                        data = json.loads(line[6:])
                        
                        event_type = data.get('type')
                        
                        if event_type == 'queue':
                            position = data.get('position')
                            message = data.get('message')
                            if queue_time is None:
                                queue_time = time.time() - start_time
                            print(f"[User {user_id}] ⏳ {message} (t={time.time()-start_time:.1f}s)")
                        
                        elif event_type == 'sources':
                            if not processing_started:
                                processing_started = True
                                processing_start_time = time.time() - start_time
                                print(f"[User {user_id}] 🟢 Processing started (waited {processing_start_time:.1f}s)")
                            
                            sources = data.get('sources', [])
                            print(f"[User {user_id}] 📚 Received {len(sources)} sources")
                        
                        elif event_type == 'token':
                            tokens_received += 1
                            if tokens_received == 1:
                                print(f"[User {user_id}] ✍️  First token arrived (t={time.time()-start_time:.1f}s)")
                        
                        elif event_type == 'done':
                            total_time = time.time() - start_time
                            print(f"[User {user_id}] ✅ COMPLETED in {total_time:.1f}s ({tokens_received} tokens)")
                            break
                        
                        elif event_type == 'error':
                            error_msg = data.get('error')
                            print(f"[User {user_id}] ❌ ERROR: {error_msg}")
                            break
                
                except json.JSONDecodeError:
                    pass
        
    except requests.exceptions.Timeout:
        print(f"[User {user_id}] ⏱️  TIMEOUT after 5 minutes")
    except Exception as e:
        print(f"[User {user_id}] ❌ ERROR: {e}")

def check_queue_status():
    """Monitor queue status ogni 2 secondi"""
    while True:
        try:
            response = requests.get(f"{BACKEND_URL}/queue/status", timeout=2)
            if response.ok:
                data = response.json()
                queue_len = data['queue_length']
                active = data['active_requests']
                total = data['total_processed']
                
                if queue_len > 0 or active > 0:
                    print(f"\n📊 QUEUE STATUS: {queue_len} waiting | {active} processing | {total} total processed")
        except:
            pass
        
        time.sleep(2)

def test_single_user():
    """Test con singolo utente - nessuna coda"""
    print("\n" + "="*80)
    print("TEST 1: SINGLE USER (no queue expected)")
    print("="*80)
    
    simulate_user(1, "What is the TK1+ sensor?")
    
    print("\n✅ Test 1 completed\n")

def test_concurrent_users(num_users=5):
    """Test con più utenti concorrenti"""
    print("\n" + "="*80)
    print(f"TEST 2: {num_users} CONCURRENT USERS (queue expected)")
    print("="*80)
    
    queries = [
        "Tell me about TK1+ oil level controller",
        "What is the difference between TK3+ and TK4?",
        "Explain LC-XP level switch features",
        "ATEX certification for hazardous areas?",
        "MODBUS communication protocol details"
    ]
    
    threads = []
    
    # Start queue monitor in background
    monitor_thread = threading.Thread(target=check_queue_status, daemon=True)
    monitor_thread.start()
    
    # Launch users con delay 2s tra uno e l'altro
    for i in range(min(num_users, len(queries))):
        thread = threading.Thread(
            target=simulate_user,
            args=(i+1, queries[i], i * 2)  # delay crescente
        )
        threads.append(thread)
        thread.start()
    
    # Wait for all users to complete
    for thread in threads:
        thread.join()
    
    print("\n✅ Test 2 completed\n")

def test_health_check():
    """Verifica che backend sia online"""
    print("\n" + "="*80)
    print("HEALTH CHECK")
    print("="*80)
    
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=5)
        if response.ok:
            data = response.json()
            print(f"✅ Backend online: {data['service']}")
            print(f"   Model: {data['model']}")
            print(f"   Timestamp: {data['timestamp']}")
            return True
        else:
            print(f"❌ Backend error: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Backend offline: {e}")
        print("\nAssicurati che il backend sia avviato:")
        print("  cd backend_api")
        print("  python app.py")
        return False

if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════════════════════════╗
║  TEKLAB AI - Multi-User Queue System Test                   ║
║  Test streaming + queue con utenti concorrenti              ║
╚══════════════════════════════════════════════════════════════╝
""")
    
    # Verifica backend online
    if not test_health_check():
        exit(1)
    
    print("\n⏳ Starting tests in 3 seconds...\n")
    time.sleep(3)
    
    # Test 1: Single user (baseline)
    test_single_user()
    
    time.sleep(5)
    
    # Test 2: 5 concurrent users
    test_concurrent_users(num_users=5)
    
    print("\n" + "="*80)
    print("ALL TESTS COMPLETED")
    print("="*80)
    print("\nVerifica:")
    print("1. User 1 non dovrebbe vedere 'In coda' (immediate processing)")
    print("2. User 2-5 dovrebbero vedere 'In coda: posizione X'")
    print("3. Ordine FIFO: User 1 finisce per primo, poi User 2, etc.")
    print("4. Nessun timeout (tutti completano)")
    print("5. Total time ≈ 5 users × 35s = ~3 minuti")
