#!/usr/bin/env python3
"""
Script per configurare automaticamente HuggingFace con il token dal file .env
"""
import os
import subprocess
import sys
from pathlib import Path

def load_env_file():
    """Carica variabili dal file .env"""
    env_path = Path(__file__).parent / ".env"
    
    if not env_path.exists():
        print("❌ File .env non trovato!")
        print("   Crea il file .env con il token HuggingFace")
        return None
    
    env_vars = {}
    try:
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    env_vars[key.strip()] = value.strip()
        
        return env_vars
    except Exception as e:
        print(f"❌ Errore lettura .env: {e}")
        return None

def login_huggingface(token):
    """Esegue il login di HuggingFace con il token"""
    print("🔑 Configurando HuggingFace login...")
    
    try:
        # Metodo 1: Usa huggingface-hub programmaticamente
        try:
            from huggingface_hub import login
            login(token=token)
            print("✅ Login HuggingFace completato (programmatico)!")
            return True
        except ImportError:
            pass
        
        # Metodo 2: Usa command line
        result = subprocess.run(
            ["huggingface-cli", "login", "--token", token],
            capture_output=True,
            text=True,
            check=False
        )
        
        if result.returncode == 0:
            print("✅ Login HuggingFace completato (CLI)!")
            return True
        else:
            print(f"❌ Errore login CLI: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Errore durante login: {e}")
        return False

def verify_login():
    """Verifica che il login sia andato a buon fine"""
    try:
        from huggingface_hub import whoami
        user_info = whoami()
        print(f"👤 Utente HuggingFace: {user_info['name']}")
        return True
    except Exception as e:
        print(f"⚠️  Impossibile verificare utente: {e}")
        return False

def main():
    print("\n" + "="*60)
    print("🔑 CONFIGURAZIONE HUGGINGFACE LOGIN")
    print("="*60 + "\n")
    
    # Carica token dal .env
    env_vars = load_env_file()
    if not env_vars:
        return 1
    
    token = env_vars.get('HF_TOKEN')
    if not token:
        print("❌ HF_TOKEN non trovato nel file .env")
        return 1
    
    print(f"📋 Token trovato: {token[:8]}...{token[-8:]}")
    
    # Esegui login
    if login_huggingface(token):
        print("\n🧪 Verifica login...")
        verify_login()
        
        print("\n✅ Configurazione completata!")
        print("   Ora puoi scaricare modelli Llama privati")
        return 0
    else:
        print("\n❌ Login fallito")
        return 1

if __name__ == "__main__":
    exit(main())