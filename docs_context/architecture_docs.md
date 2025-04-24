# Soul Engine

## Subsystems
1. **Embedding & Feature Extraction**

- Normalize text inputs
- Generate embeddings using local models (e.g., BGE, Instructor, MiniLM) or OpenRouter for prototyping
- Extract temporal and semantic features (topics, sentiment, focus areas)

**Output**:
- Vectorized knowledge base (e.g., using FAISS, Qdrant, Weaviate)
- Snapshot + delta tracking of focus, interests, behavioral traits

### PIEL - Progressive Identity Extraction Loop

#### Low friction high-leverage inputs to clarify unclear answers, probe missing dimentions (values, fears, etc) and adapt tone to match the user.

1. **Initial Seed Questions** → Hardcoded, high-yield prompts designed to generate dense identity signal
2.  **On-device Parsing & Heuristics**  → Use local logic, keyword mapping, light regex or small models (even [TF-IDF](https://www.capitalone.com/tech/machine-learning/understanding-tf-idf/)[^1] + sentence embeddings) to extract: potential core values, hints of fears, skills, etc.
3. **Coverage Detection** → Have we filled in most of the SoulProfile? If yes, proceed. If no…
4. **Singple API Call** → Send all answers in one batch to LLM/NLP to:
    - Fill missing fields
    - Validate extracted traits
    - Suggest (not ask) clarifying follow-up questions (if needed)
5. **Optional Second Pass (local)** → Use similarity matching, ontology reasoning, or prompt-engineered rule sets to relate traits to each other.

##### Why this approach?

- **80% of users** give shallow answers → You don't need the model to do 10 rounds with them.
- The high-context users already give you a lot in 1 go.
- You extract signal **before** sending to LLM, saving money.
- The LLM works like a final polisher, not the whole engine.

Every answer is:
- Embedded
- Compared with a small taxonomy map
- Stored in a structured format (that feeds Life Intelligence later)

[^1]: TF-IDF (Term Frequency-Inverse Document Frequency) is a statistical measure used to evaluate the importance of a word in a document relative to a collection of documents. It combines Term Frequency (TF), which measures how often a term appears in a document, and Inverse Document Frequency (IDF), which gauges a term's rarity across the document set. See [Capital One Tech](https://www.capitalone.com/tech/machine-learning/understanding-tf-idf/) for more details.
