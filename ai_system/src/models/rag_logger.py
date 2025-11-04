"""
Sistema di logging per RAG Chatbot
Traccia: prompt, context, model, latency, tokens, risposta per ogni query
"""

import json
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict


@dataclass
class QueryLog:
    """Log di una singola query"""
    timestamp: str
    query: str
    model_used: str  # "groq" o "custom-pytorch"
    temperature: float
    max_tokens: int
    
    # Context RAG
    num_chunks_retrieved: int
    chunks_sources: List[str]  # [autore/libro/cap]
    retrieval_scores: List[float]
    
    # Response
    response: str
    latency_seconds: float
    
    # Token usage
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    
    # Metadata
    use_embeddings: bool
    search_method: str  # "hybrid", "semantic", "keyword"


class RAGLogger:
    """
    Logger persistente per tutte le query RAG
    Salva in JSON lines format per analisi
    """
    
    def __init__(self, log_dir: str = "logs"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # File log giornaliero
        today = datetime.now().strftime("%Y-%m-%d")
        self.log_file = self.log_dir / f"rag_queries_{today}.jsonl"
        
        # Stats in-memory
        self.session_queries = []
    
    def log_query(
        self,
        query: str,
        model_used: str,
        temperature: float,
        max_tokens: int,
        chunks_retrieved: List[Dict],
        response: str,
        latency: float,
        prompt_tokens: int,
        completion_tokens: int,
        use_embeddings: bool,
        search_method: str
    ):
        """Salva log di una query"""
        
        # Estrai sources dai chunks
        chunks_sources = [
            f"{c.get('autore', 'N/A')}/{c.get('libro', 'N/A')}/{c.get('capitolo', 'N/A').split('/')[-1]}"
            for c in chunks_retrieved
        ]
        
        # Estrai scores (converti a float Python standard per JSON)
        retrieval_scores = [float(c.get('score', 0.0)) for c in chunks_retrieved]
        
        # Crea log entry
        log_entry = QueryLog(
            timestamp=datetime.now().isoformat(),
            query=query,
            model_used=model_used,
            temperature=temperature,
            max_tokens=max_tokens,
            num_chunks_retrieved=len(chunks_retrieved),
            chunks_sources=chunks_sources,
            retrieval_scores=retrieval_scores,
            response=response,
            latency_seconds=round(latency, 3),
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=prompt_tokens + completion_tokens,
            use_embeddings=use_embeddings,
            search_method=search_method
        )
        
        # Salva su file (JSON lines)
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(asdict(log_entry), ensure_ascii=False) + '\n')
        
        # Aggiungi a sessione corrente
        self.session_queries.append(log_entry)
    
    def get_session_stats(self) -> Dict[str, Any]:
        """Statistiche sessione corrente"""
        if not self.session_queries:
            return {"total_queries": 0}
        
        total_latency = sum(q.latency_seconds for q in self.session_queries)
        total_tokens = sum(q.total_tokens for q in self.session_queries)
        
        models_used = {}
        for q in self.session_queries:
            models_used[q.model_used] = models_used.get(q.model_used, 0) + 1
        
        return {
            "total_queries": len(self.session_queries),
            "avg_latency": round(total_latency / len(self.session_queries), 3),
            "total_tokens": total_tokens,
            "models_used": models_used,
            "avg_chunks_per_query": round(
                sum(q.num_chunks_retrieved for q in self.session_queries) / len(self.session_queries), 1
            )
        }
    
    def print_stats(self):
        """Stampa stats sessione"""
        stats = self.get_session_stats()
        
        if stats["total_queries"] == 0:
            print("📊 Nessuna query registrata in questa sessione")
            return
        
        print("\n" + "="*60)
        print("📊 STATISTICHE SESSIONE")
        print("="*60)
        print(f"   Query totali: {stats['total_queries']}")
        print(f"   Latenza media: {stats['avg_latency']}s")
        print(f"   Token totali: {stats['total_tokens']}")
        print(f"   Chunks medi per query: {stats['avg_chunks_per_query']}")
        print(f"\n   Modelli usati:")
        for model, count in stats['models_used'].items():
            print(f"      • {model}: {count} query")
        print("="*60 + "\n")
    
    def load_daily_logs(self, date: Optional[str] = None) -> List[QueryLog]:
        """
        Carica log di un giorno specifico
        
        Args:
            date: "YYYY-MM-DD" o None per oggi
        
        Returns:
            Lista QueryLog
        """
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        
        log_file = self.log_dir / f"rag_queries_{date}.jsonl"
        
        if not log_file.exists():
            return []
        
        logs = []
        with open(log_file, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    data = json.loads(line)
                    logs.append(QueryLog(**data))
                except Exception as e:
                    print(f"⚠️  Errore parsing log: {e}")
        
        return logs
    
    def analyze_logs(self, date: Optional[str] = None):
        """Analisi avanzata log giornalieri"""
        logs = self.load_daily_logs(date)
        
        if not logs:
            print(f"📊 Nessun log disponibile per {date or 'oggi'}")
            return
        
        print(f"\n{'='*60}")
        print(f"📊 ANALISI LOG {date or 'OGGI'}")
        print(f"{'='*60}")
        
        # Stats generali
        avg_latency = sum(q.latency_seconds for q in logs) / len(logs)
        total_tokens = sum(q.total_tokens for q in logs)
        
        print(f"\n🔢 Statistiche Generali:")
        print(f"   Query totali: {len(logs)}")
        print(f"   Latenza media: {avg_latency:.3f}s")
        print(f"   Token totali: {total_tokens}")
        
        # Modelli
        models = {}
        for q in logs:
            models[q.model_used] = models.get(q.model_used, 0) + 1
        
        print(f"\n🤖 Modelli Usati:")
        for model, count in models.items():
            pct = (count / len(logs)) * 100
            print(f"   • {model}: {count} ({pct:.1f}%)")
        
        # Search methods
        methods = {}
        for q in logs:
            methods[q.search_method] = methods.get(q.search_method, 0) + 1
        
        print(f"\n🔍 Metodi di Ricerca:")
        for method, count in methods.items():
            pct = (count / len(logs)) * 100
            print(f"   • {method}: {count} ({pct:.1f}%)")
        
        # Top sources
        sources_count = {}
        for q in logs:
            for source in q.chunks_sources:
                sources_count[source] = sources_count.get(source, 0) + 1
        
        print(f"\n📚 Top 5 Fonti Più Usate:")
        for source, count in sorted(sources_count.items(), key=lambda x: x[1], reverse=True)[:5]:
            print(f"   • {source}: {count} chunk")
        
        print(f"\n{'='*60}\n")


if __name__ == "__main__":
    # Test logger
    print("🧪 Test RAGLogger\n")
    
    logger = RAGLogger()
    
    # Log fake query
    logger.log_query(
        query="Test question?",
        model_used="groq",
        temperature=0.7,
        max_tokens=500,
        chunks_retrieved=[
            {"autore": "Mathias de Stefano", "libro": "Pyramid Course", "capitolo": "cap01", "score": 0.95},
            {"autore": "Mathias de Stefano", "libro": "Pyramid Course", "capitolo": "cap02", "score": 0.87}
        ],
        response="Test answer",
        latency=1.234,
        prompt_tokens=100,
        completion_tokens=50,
        use_embeddings=True,
        search_method="hybrid"
    )
    
    # Print stats
    logger.print_stats()
    
    print("✅ Log salvato in:", logger.log_file)
