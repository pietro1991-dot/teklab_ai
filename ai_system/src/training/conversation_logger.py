"""
Conversation Logger per Spirituality AI
Registra tutte le conversazioni con dettagli completi per training futuro
"""

import json
import os
import uuid
import hashlib
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Any


class ConversationLogger:
    """Logger per salvare conversazioni complete con metadata RAG"""
    
    def __init__(self, output_dir: str = "ai_system/training_data/conversations"):
        """
        Inizializza logger conversazioni
        
        Args:
            output_dir: Directory base per salvare conversazioni
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Crea cartella per oggi
        self.today = datetime.now().strftime("%Y-%m-%d")
        self.today_dir = self.output_dir / self.today
        self.today_dir.mkdir(exist_ok=True)
        
        # File aggregato giornaliero
        self.daily_log = self.today_dir / "daily_aggregate.jsonl"
        
        print(f"📝 Conversation Logger inizializzato: {self.today_dir}")
    
    def generate_user_hash(self, user_identifier: str) -> str:
        """
        Genera hash anonimo per user ID (privacy)
        
        Args:
            user_identifier: ID utente originale
            
        Returns:
            Hash SHA256 troncato (16 caratteri)
        """
        return hashlib.sha256(user_identifier.encode()).hexdigest()[:16]
    
    def log_conversation(
        self,
        query: str,
        response: str,
        chunks_used: List[Dict],
        model_used: str,
        language: str = "en",
        user_id: str = "anonymous",
        session_id: Optional[str] = None,
        conversation_turn: int = 1,
        has_image: bool = False,
        image_path: Optional[str] = None,
        memory_context: Optional[List[Dict]] = None,
        tokens_input: int = 0,
        tokens_output: int = 0,
        generation_time_ms: int = 0,
        cost_usd: float = 0.0,
        search_type: str = "semantic",
        embeddings_used: bool = True,
        additional_metadata: Optional[Dict] = None
    ) -> str:
        """
        Registra conversazione completa con tutti i dettagli
        
        Args:
            query: Domanda utente
            response: Risposta bot
            chunks_used: Lista chunks RAG utilizzati
            model_used: Modello API usato (gpt-4o-mini, llama-3.1-8b, etc.)
            language: Lingua conversazione (it/en/es)
            user_id: ID utente (verrà hashato)
            session_id: ID sessione conversazione
            conversation_turn: Numero turno nella sessione
            has_image: Se query include immagine
            image_path: Path immagine se presente
            memory_context: Scambi precedenti in memoria
            tokens_input: Token input stimati
            tokens_output: Token output stimati
            generation_time_ms: Tempo generazione risposta (ms)
            cost_usd: Costo stimato conversazione
            search_type: Tipo ricerca (semantic/keyword/hybrid)
            embeddings_used: Se embeddings sono stati usati
            additional_metadata: Metadata aggiuntivi opzionali
            
        Returns:
            conversation_id generato
        """
        # Genera IDs
        conversation_id = str(uuid.uuid4())
        user_hash = self.generate_user_hash(user_id)
        
        if not session_id:
            session_id = str(uuid.uuid4())
        
        # Processa chunks per info compatte + complete
        chunks_info = []
        for chunk in chunks_used:
            # Estrai metadata chunk
            chunk_meta = chunk.get("metadata", {})
            
            # Info base chunk
            chunk_info = {
                "chunk_id": chunk.get("id") or chunk.get("chunk_id") or "unknown",
                "author": chunk_meta.get("author") or chunk.get("autore", "unknown"),
                "work": chunk_meta.get("work") or chunk.get("libro", "unknown"),
                "day": chunk_meta.get("day") or chunk_meta.get("file_number", 0),
                "chapter": chunk_meta.get("chapter") or chunk.get("capitolo", ""),
                "relevance_score": chunk.get("score", 0.0),
                "language": chunk_meta.get("language", "en"),
                "content_preview": self._extract_preview(chunk, max_length=150),
                "full_chunk": chunk  # Chunk completo per training
            }
            
            chunks_info.append(chunk_info)
        
        # Context memoria
        memory_summary = {
            "turns_used": len(memory_context) if memory_context else 0,
            "context": memory_context if memory_context else []
        }
        
        # Costruisci log entry completo
        log_entry = {
            # Identificazione
            "conversation_id": conversation_id,
            "user_id": user_hash,
            "session_id": session_id,
            "timestamp": datetime.now().isoformat(),
            "date": self.today,
            
            # Lingua e modello
            "language": language,
            "model_used": model_used,
            
            # Query utente
            "query": {
                "text": query,
                "length_chars": len(query),
                "length_words": len(query.split()),
                "has_image": has_image,
                "image_path": image_path,
                "detected_intent": self._detect_intent(query),
                "detected_topic": self._detect_topic(query)
            },
            
            # RAG retrieval
            "rag_retrieval": {
                "search_type": search_type,
                "embeddings_used": embeddings_used,
                "chunks_retrieved": chunks_info,
                "num_chunks_used": len(chunks_used),
                "context_length_tokens": tokens_input,
                "sources_used": self._extract_sources(chunks_info)
            },
            
            # Risposta generata
            "response": {
                "text": response,
                "length_chars": len(response),
                "length_words": len(response.split()),
                "length_tokens": tokens_output,
                "generation_time_ms": generation_time_ms,
                "cost_usd": round(cost_usd, 6)
            },
            
            # Metadata conversazione
            "conversation_metadata": {
                "conversation_turn": conversation_turn,
                "memory_context": memory_summary,
                "user_feedback": None,  # Placeholder per feedback futuro
                "user_rating": None,
                "follow_up_question": None,
                "session_duration_turns": conversation_turn
            },
            
            # Metriche tecniche
            "technical_metrics": {
                "tokens_input": tokens_input,
                "tokens_output": tokens_output,
                "tokens_total": tokens_input + tokens_output,
                "api_latency_ms": generation_time_ms,
                "cost_per_token": round(cost_usd / max(tokens_output, 1), 8),
                "chunks_per_token": round(len(chunks_used) / max(tokens_output, 1), 4)
            },
            
            # Metadata aggiuntivi
            "additional_metadata": additional_metadata or {}
        }
        
        # Salva file individuale JSON (formato leggibile)
        filename = f"{conversation_id}.json"
        filepath = self.today_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(log_entry, f, indent=2, ensure_ascii=False)
        
        # Aggiungi a log aggregato giornaliero (formato JSONL per processing)
        with open(self.daily_log, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
        
        return conversation_id
    
    def add_feedback(
        self,
        conversation_id: str,
        rating: Optional[int] = None,
        feedback: Optional[str] = None,
        follow_up: Optional[str] = None
    ) -> bool:
        """
        Aggiungi feedback utente a conversazione esistente
        
        Args:
            conversation_id: ID conversazione da aggiornare
            rating: Rating 1-5 stelle
            feedback: Feedback testuale utente
            follow_up: Domanda follow-up utente
            
        Returns:
            True se aggiornamento riuscito, False altrimenti
        """
        # Cerca file conversazione (potrebbe essere in date diverse)
        for date_dir in sorted(self.output_dir.iterdir(), reverse=True):
            if not date_dir.is_dir():
                continue
            
            conv_file = date_dir / f"{conversation_id}.json"
            if conv_file.exists():
                try:
                    # Leggi conversazione esistente
                    with open(conv_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    # Aggiorna metadata
                    data["conversation_metadata"]["user_rating"] = rating
                    data["conversation_metadata"]["user_feedback"] = feedback
                    data["conversation_metadata"]["follow_up_question"] = follow_up
                    data["conversation_metadata"]["feedback_timestamp"] = datetime.now().isoformat()
                    
                    # Salva aggiornamento
                    with open(conv_file, 'w', encoding='utf-8') as f:
                        json.dump(data, f, indent=2, ensure_ascii=False)
                    
                    print(f"✅ Feedback aggiunto a conversazione {conversation_id[:8]}...")
                    return True
                
                except Exception as e:
                    print(f"❌ Errore aggiunta feedback: {e}")
                    return False
        
        print(f"⚠️  Conversazione {conversation_id[:8]}... non trovata")
        return False
    
    def get_daily_statistics(self, date: Optional[str] = None) -> Dict[str, Any]:
        """
        Ottieni statistiche conversazioni per data specifica
        
        Args:
            date: Data formato YYYY-MM-DD (default: oggi)
            
        Returns:
            Dict con statistiche aggregate
        """
        target_date = date or self.today
        target_dir = self.output_dir / target_date
        
        if not target_dir.exists():
            return {"error": f"No data for {target_date}"}
        
        # Conta file conversazioni
        conv_files = list(target_dir.glob("*.json"))
        conv_files = [f for f in conv_files if f.name != "daily_aggregate.jsonl"]
        
        stats = {
            "date": target_date,
            "total_conversations": len(conv_files),
            "by_language": {},
            "by_model": {},
            "by_topic": {},
            "total_tokens": 0,
            "total_cost_usd": 0.0,
            "avg_response_time_ms": 0,
            "avg_chunks_used": 0,
            "with_feedback": 0
        }
        
        # Analizza ogni conversazione
        total_response_time = 0
        total_chunks = 0
        
        for conv_file in conv_files:
            try:
                with open(conv_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Lingua
                lang = data.get("language", "unknown")
                stats["by_language"][lang] = stats["by_language"].get(lang, 0) + 1
                
                # Modello
                model = data.get("model_used", "unknown")
                stats["by_model"][model] = stats["by_model"].get(model, 0) + 1
                
                # Topic
                topic = data.get("query", {}).get("detected_topic", "unknown")
                stats["by_topic"][topic] = stats["by_topic"][topic].get(topic, 0) + 1
                
                # Metriche
                stats["total_tokens"] += data.get("technical_metrics", {}).get("tokens_total", 0)
                stats["total_cost_usd"] += data.get("response", {}).get("cost_usd", 0.0)
                total_response_time += data.get("response", {}).get("generation_time_ms", 0)
                total_chunks += data.get("rag_retrieval", {}).get("num_chunks_used", 0)
                
                # Feedback
                if data.get("conversation_metadata", {}).get("user_rating"):
                    stats["with_feedback"] += 1
                
            except Exception as e:
                print(f"⚠️  Errore lettura {conv_file.name}: {e}")
                continue
        
        # Calcola medie
        if stats["total_conversations"] > 0:
            stats["avg_response_time_ms"] = round(total_response_time / stats["total_conversations"], 2)
            stats["avg_chunks_used"] = round(total_chunks / stats["total_conversations"], 2)
            stats["avg_cost_per_conversation"] = round(stats["total_cost_usd"] / stats["total_conversations"], 6)
        
        return stats
    
    def _extract_preview(self, chunk: Dict, max_length: int = 150) -> str:
        """Estrai preview testuale dal chunk"""
        # Formato messages
        if "messages" in chunk:
            for msg in chunk["messages"]:
                if msg.get("role") == "assistant":
                    content = msg.get("content", "")
                    return content[:max_length] + "..." if len(content) > max_length else content
        
        # Formato vecchio
        if "risposta" in chunk:
            content = chunk["risposta"]
            return content[:max_length] + "..." if len(content) > max_length else content
        
        # Fallback
        return "N/A"
    
    def _extract_sources(self, chunks_info: List[Dict]) -> List[str]:
        """Estrai lista fonti uniche dai chunks"""
        sources = set()
        for chunk in chunks_info:
            author = chunk.get("author", "Unknown")
            work = chunk.get("work", "Unknown")
            if author != "unknown" and work != "unknown":
                sources.add(f"{author} - {work}")
        return sorted(list(sources))
    
    def _detect_intent(self, query: str) -> str:
        """Rileva intent base della query"""
        query_lower = query.lower()
        
        if any(w in query_lower for w in ["come", "how", "cómo"]):
            return "how_to"
        elif any(w in query_lower for w in ["cos'è", "cosa è", "what is", "qué es"]):
            return "definition"
        elif any(w in query_lower for w in ["perché", "why", "por qué"]):
            return "explanation"
        elif any(w in query_lower for w in ["quando", "when", "cuándo"]):
            return "timing"
        elif any(w in query_lower for w in ["dove", "where", "dónde"]):
            return "location"
        else:
            return "general_question"
    
    def _detect_topic(self, query: str) -> str:
        """Rileva topic principale della query"""
        query_lower = query.lower()
        
        topics = {
            "chakra": ["chakra", "energy center", "centro energetico"],
            "meditation": ["meditazione", "meditation", "meditación", "meditar"],
            "spirituality": ["spirituale", "spiritual", "espiritual", "anima", "soul", "alma"],
            "healing": ["guarigione", "healing", "sanación", "curare", "heal"],
            "consciousness": ["coscienza", "consciousness", "conciencia", "consapevolezza", "awareness"],
            "energy": ["energia", "energy", "energía"],
            "practice": ["pratica", "practice", "práctica", "esercizio", "exercise"]
        }
        
        for topic, keywords in topics.items():
            if any(kw in query_lower for kw in keywords):
                return topic
        
        return "general"
