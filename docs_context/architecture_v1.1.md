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

## 📦 Data Structures (Simplified)

```python
class SoulNode:
    def __init__(self, type: str, label: str, weight: float = 1.0):
        ...

class LifeNode:
    def __init__(self, label: str, type: str, alignment_score: float, metadata: dict):
        ...

class SoulProfile:
    def __init__(self, nodes: List[SoulNode]):
        ...

class LifeGraph:
    def __init__(self, profile: SoulProfile):
        self.nodes = []
        self.edges = []
        self.build_graph(profile)
```

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
Soul Engine is only **inspected/edited**.

