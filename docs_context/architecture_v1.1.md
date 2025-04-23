# LifeOS: Technical Architecture & Module Overview (v2)

---

## 🧠 Conceptual Architecture

```
          ┌────────────────────────┐
          │     User Input         │
          └────────┬───────────────┘
                   ▼
       ┌─────────────────────────────┐
       │      Soul Engine            │ ◄────────────┐
       │  (User Identity Model)      │              │
       └─────┬────────────┬──────────┘              │
             ▼            ▼                         │
   [ Primary Node ]   [ Supporting Nodes ]          │
    (Core values,     (Fears, skills, goals...)     │
     philosophy,                                    │
     worldview)                                     │
             │                                      │
             ▼                                      │
       ┌─────────────┐            ┌─────────────────▼────────────┐
       │ Soul Profile│───────────▶ Life Intelligence Engine      │
       │  (object)   │            │ (Navigable Decision Graph)   │
       └─────────────┘            └──────────────────────────────┘
                                        ▲            │
                                        │            ▼
                            ┌───────────┴───────┐┌────────────┐
                            │ Action Nodes      ││ Data Layer │
                            │ Suggestions,      ││ (Optional) │
                            │ Transitions, etc. │└────────────┘
                            └───────────────────┘

```

---

## 🧩 Core Modules (v2)

### 1. `SoulEngine`
#### Purpose:
Extract a structured identity graph from minimal user input.

#### Components:
- `SoulNode`: Represents one facet of the user identity (value, goal, fear, etc.)
- `SoulProfile`: Master object containing the identity graph
- `SoulParser`: Extracts and categorizes input into node types
- `SoulEvolver`: Updates the profile as new input comes in or decisions are made

#### Sample Types:
```python
SoulNode(type="core_value", label="freedom")
SoulNode(type="philosophy", label="data ownership")
SoulNode(type="interest", label="cybersecurity")
SoulNode(type="goal", label="financial autonomy")
```

#### Output:
- Identity Graph (non-navigable, but queryable)
- `SoulProfile` object used by LifeGraph

---

### 1.1 `Embedding Layer`
#### Purpose:
To Build a Local Knowledge Graph Engine Backed by Embeddings + Ontologies. Instead of hardcoding rules, we use a hybrid system. 

#### Components:
- `Static Ontology Layer`:  A extremely curated JSON/YAML file, with example provided below. 
- `Local Embedding Similarity (Core Strategy)`: We use sentence-transformers to embed all traits. Then:
    - Compute cosine similarity between all node pairs.
    - Build edges based on high similarity + contextual tags (e.g., both from "skills" or one from "fear", one from "value").
    - This gives semantic edges without needing the LLM again.
- `Relationship Templates`: For readability and control, we define soft relationship templates. These act like relationship scaffolding - not rules, but interpretable mappings to label edges after similarity is calculated.

#### Sample Types:

##### Static Ontology Layer
```json
{
  "freedom": {
    "type": "value",
    "related_fears": ["control", "oppression", "dependency"],
    "related_motivations": ["autonomy", "self-direction"],
    "related_interests": ["political philosophy", "digital privacy"]
  },
  "competence": {
    "related_fears": ["inadequacy", "failure"],
    "related_motivations": ["mastery", "growth"],
    "related_skills": ["programming", "strategy"]
  }
}
``` 

##### Relationship Templates
```python
TEMPLATES = [
    ("fear", "value", "avoids"),     # fear of failure → value of competence
    ("motivation", "value", "seeks"),# motivation of mastery → value of growth
    ("interest", "skill", "develops"),
    ("skill", "value", "supports"),
]
```

---

### 2. `LifeIntelligenceEngine`
#### Purpose:
Generate a directed, navigable graph of choices, paths, opportunities, and strategies — rooted in Soul Profile.

#### Components:
- `LifeNode`: Action, habit, opportunity, decision point
- `LifeEdge`: Directed edge, weighted by utility/alignment
- `LifeGraph`: Graph container with traversal/query logic
- `LifePathfinder`: Finds optimal sequences based on goals or archetypes
- `AlignmentScorer`: Scores each node for soul alignment

#### Example Node:
```python
LifeNode(type="opportunity", label="Launch side project in web3 security", alignment_score=0.91)
```

#### Output:
- Interactive graph view of current decision space
- Ranked paths to goals or archetype profiles
- Suggested "next nodes" with reasoning

---

### 3. `DataLayer` (Optional Enhancer)
#### Purpose:
Ingest optional user artifacts to deepen understanding with no extra input.

#### Sources:
- Markdown notes (Obsidian, Logseq)
- Bookmarks (browser exports)
- Journals (free text)
- GitHub / commit history
- Personal metadata (file activity, system logs — local only)

#### Tools:
- `DataConnector`: Adapters for each source
- `TextEmbedder`: Embedding-based vector model for similarity search
- `InsightExtractor`: Matches external data with internal identity graph

---

## 🔄 Data Flow (Terminal Prototype)

1. Prompt user: minimal questions (e.g., 5–7 open-ended)
2. `SoulParser` → parses and instantiates SoulNodes
3. Build `SoulProfile`
4. Pass `SoulProfile` to `LifeIntelligenceEngine`
5. Generate `LifeGraph`
6. Return top LifeNodes and paths to CLI
7. Optional: allow rating feedback → updates graph weights

---

## 🛠 Technologies (Prototype Stack)

| Component            | Stack                         |
|----------------------|-------------------------------|
| Language             | Python                        |
| Graph Engine         | NetworkX (prototype)          |
| ML Embeddings        | HuggingFace / OpenAI / Local  |
| NLP/Parsing          | spaCy, Pydantic, Custom rules |
| CLI Interface        | Rich / Textual (optional)     |
| Storage              | JSON or local SQLite          |

---

## 🔐 Privacy Design

- All data processed locally by default
- Optional opt-in to anonymized contribution for improving LifeNode graph
- Long-term goal: differential privacy + federated learning + zkML

---

## 🧪 Validation Metrics (R&D Phase)

- Top-k node alignment score (match between suggestion and actual path taken)
- Drop-off rate after graph generation
- User satisfaction score after first 3 suggested paths
- Entropy change in user’s self-description over time

---

## 🧱 Future Exploration

- Archetype modeling (Builder, Hacker, Artist, Researcher)
- Psychological tests mapped to SoulNode generation (Big Five, MBTI → optional)
- Memory subsystem (node snapshots over time)
- Distributed soul computation: using zkML to process identity inference off-device without losing privacy

---

## 📎 Final Notes

The **Life Intelligence** graph is the *primary UX*, while the **Soul Engine** is the *underlying model*.  
Think of it like:  
🧠 = soul state model  
🗺️ = action map  

Both are technically graphs, but only Life Intelligence is **navigated** by the user.  
Soul Engine is only **inspected/edited/evolved**.

