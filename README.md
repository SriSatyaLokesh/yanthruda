# Yanthruda (యంత్రుడ)

> **Hyper-Personalized Telugu/Tenglish AI Persona, Regional Dialect Adaptation & Voice Cloning Pipeline**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python: 3.10+](https://img.shields.io/badge/Python-3.10%2B-brightgreen.svg)](https://python.org)
[![Focus: Indic NLP & Voice](https://img.shields.io/badge/Focus-Telugu%20%7C%20Tenglish%20%7C%20Hindi-orange.svg)](docs/RESEARCH_REPORT.md)
[![Status: Research & Blueprint](https://img.shields.io/badge/Status-Research%20%26%20Blueprint-purple.svg)](docs/MISSION.md)

---

## 🎯 Mission

**Yanthruda (యంత్రుడ)** is an open-source AI project designed to clone not just a person’s acoustic voice, but their complete linguistic identity:
- **Regional Dialect**: Authentic colloquialisms across Telangana, Coastal Andhra, and Rayalaseema.
- **Personal Vocabulary & Idioms**: Mining unique catchphrases, discourse markers (*kadaa*, *antey*, *mari*, *le*), and code-switching ratios.
- **Romanized "Tenglish" Handling**: Speaking Telugu written phonetically in English/Latin script (*"nenu repu morning kaluddhaam bro"*) without phonetic breakdowns or foreign accents.
- **Continuous Learning Over Time**: Progressively evolving as the user feeds more audio monologues, voice notes, and text chats.

---

## 🧩 The Core Problem

Current AI voice cloning and translation solutions (ElevenLabs, Google Translate, Whisper, generic LLMs) fall short in regional Indian contexts:
1. **Unnatural Bookish Tone**: Standard models output formal, journalistic Telugu rather than everyday colloquial speech.
2. **The "Tenglish" Pronunciation Breakdown**: Passing Romanized Telugu directly into standard TTS invokes English Grapheme-to-Phoneme (G2P) rules, producing an unintelligible anglicized accent.
3. **Dialect Ignorance**: Inability to differentiate regional markers (e.g., Telangana's *gatla*, *dhaawat*, *kirrak* vs. Rayalaseema's *mande*, *dhabba*).
4. **Static Cloning**: Existing systems take a 30-second audio snippet once, but never learn how the person *actually talks, thinks, or constructs sentences*.

---

## 🏗️ System Architecture

```mermaid
flowchart TD
    subgraph S1 ["1. Continuous Audio & Text Ingestion"]
        A["User Voice Notes & Text Chats"] --> B["Silero VAD + Noise Filter"]
        B --> C["AI4Bharat IndicWhisper (ASR)"]
        C --> D["Timestamped Transcripts + Clean Audio Chunks"]
        D --> E["TF-ICF Lexical Profiler & Cadence Analyzer"]
        E --> F[("Dynamic Persona Profile\n(Catchphrases, Dialect Tokens, F0/WPM)")]
    end

    subgraph S2 ["2. Cognitive Persona Scripting"]
        G["Input Prompt / English Script"] --> H["Telugu LLM Labs (Navarasa 2.0 / Gemma-Telugu)"]
        F -.-> |DSPy Few-Shot Prompt Injection| H
        F -.-> |Periodic Unsloth LoRA Adapter| H
        H --> I["Colloquial Dialect Script\n(Telugu & Code-Mixed Tenglish)"]
    end

    subgraph S3 ["3. Orthographic & Phonetic Bridge"]
        I --> J["Token Classifier (Telugu vs English Loanwords)"]
        J --> K["AI4Bharat IndicXlit Transliteration"]
        K --> L["AI4Bharat IndicMFA (G2G Alignment)"]
        L --> M["Phonetically Normalized Code-Mixed Script"]
    end

    subgraph S4 ["4. Voice Synthesis & Cloning"]
        D -.-> |10-30s Reference Audio| N["Speaker Embedding Cache"]
        M --> O{"Synthesis Engine"}
        N --> O
        O -->|Realtime Streaming (<100ms)| P["Smallest AI Lightning TTS / Sarvam Bulbul"]
        O -->|Self-Hosted Sovereign GPU| Q["AI4Bharat IndicF5 / CosyVoice 2"]
        P --> R["Synthesized Audio Stream"]
        Q --> R
    end

    R --> S["Final Personalized Telugu/Tenglish Voice Output"]
```

---

## 🔬 Evaluated Technologies & Benchmark Summary

We conducted deep research across **14 foundational technologies** evaluated over 16 technical criteria:

| Component | Architecture / Model | Primary Role | License |
| :--- | :--- | :--- | :--- |
| **ASR & Ingestion** | **AI4Bharat IndicWhisper** | Transcribes regional Indic audio; extracts personal lexicon & speech tempo | MIT / CC-BY |
| **Cognitive LLM** | **Telugu LLM Labs (Navarasa 2.0 / Gemma-Telugu)** | Indic-optimized tokenization; colloquial slang & dialect script generation | Open Weights / Apache 2.0 |
| **Personalization Engine** | **DSPy + Unsloth LoRA** | In-context dynamic catchphrase injection & lightweight user LoRA adaptation | Open Source |
| **Transliteration Bridge** | **AI4Bharat IndicXlit** | Converts Romanized Tenglish into canonical Telugu Unicode while keeping loanwords intact | MIT |
| **Phonetic Normalizer** | **AI4Bharat IndicMFA** | Enforces Dravidian *ajanta* vowel endings & prevents inappropriate schwa deletion | MIT |
| **Low-Latency Voice API** | **Smallest AI Waves (Lightning TTS)** | Sub-100ms TTFA voice synthesis with native mid-sentence code-switching stability | Commercial API |
| **Sovereign Voice Cloner** | **AI4Bharat IndicF5 & Indic Parler-TTS** | 337M flow-matching zero-shot cloning across 11 Indic languages | Open Source / MIT |
| **Dubbing Orchestration** | **AI4Bharat Chitralekha** | Turnkey open-source video/audio transcreation and dubbing alignment pipeline | MIT |
| **Dialect Corpora** | **Swecha Telugu AI & Luel Corpora** | 1,200+ hours of community-collected conversational Telangana & AP dialect speech | Community Open Dataset |

> 📖 **Read the full 1,300+ line technical analysis in [docs/RESEARCH_REPORT.md](docs/RESEARCH_REPORT.md).**

---

## 📂 Repository Structure

```
yanthruda/
├── README.md               # Project overview & architectural guide
├── .gitignore              # Python, environment & audio cache exclusions
└── docs/
    ├── MISSION.md          # Project pitch, problem breakdown & contributor guide
    ├── ARCHITECTURE.md     # Detailed pipeline specifications, schemas & data flow
    ├── RESEARCH_REPORT.md  # Comprehensive research report covering all 14 evaluated models
    └── research/
        ├── outline.yaml    # Research objects & batching parameters
        ├── fields.yaml     # 16-field technical evaluation criteria
        ├── generate_report.py # Report compilation script
        └── results/        # 14 verified JSON evaluation profiles
            ├── AI4Bharat_Chitralekha.json
            ├── AI4Bharat_IndicF5_Indic_Parler-TTS.json
            ├── AI4Bharat_IndicMFA_G2G_Phonetic_Alignment.json
            ├── AI4Bharat_IndicTrans2_IndicXlit.json
            ├── Bhashini_National_Language_Translation_Mission.json
            ├── Commercial_Voice_Cloning_Localization_ElevenLabs_Camb_ai_Dubverse.json
            ├── IndicWhisper_Lexicon_Extraction_Framework.json
            ├── Meta_SeamlessM4T_v2_SeamlessExpressive.json
            ├── Open-Source_Zero-Shot_Voice_Cloning_XTTS-v2_F5-TTS_CosyVoice.json
            ├── Persona-Conditioned_LLM_Fine-Tuning_In-Context_Adaptation.json
            ├── Sarvam_AI_Suite_Sarvam-1_2_Bulbul_TTS_Mayura.json
            ├── Smallest_AI_Waves_Platform_Lightning_TTS.json
            ├── Swecha_Telugu_AI_Luel_Conversational_Dialect_Corpora.json
            └── Telugu_LLM_Labs_Navarasa_2_0_Gemma-Telugu.json
```

---

## 🚀 Implementation Roadmap

```
[Phase 1: Ingestion & Profiling] ──► [Phase 2: Dialect LLM Transcreation] ──► [Phase 3: End-to-End Voice Synthesis]
```

- [ ] **Phase 1: Ingestion & Persona Profiler (Weeks 1–2)**
  - Audio file uploader with `Silero VAD` chunking.
  - `IndicWhisper` transcription pipeline.
  - TF-ICF script extracting user catchphrases, dialect markers, and $F_0$ speech cadence.
- [ ] **Phase 2: Dialect Transcreation & Tenglish Normalization (Weeks 3–4)**
  - `Telugu LLM Labs Gemma-Telugu` deployment with DSPy persona prompting.
  - Dual-script output generator (Telugu Unicode + Romanized Tenglish review text).
  - `IndicXlit` phonetic normalization bridge.
- [ ] **Phase 3: Voice Cloning & Audio Rendering (Weeks 5–6)**
  - Integration with `Smallest AI Waves` / `AI4Bharat IndicF5`.
  - Reference audio enrollment pipeline.
  - End-to-end test harness measuring Mean Opinion Score (MOS) and pronunciation accuracy.

---

## 🤝 Contributing & Collaboration

We are actively looking for collaborators:
- **ML / AI Engineers**: Indic LLM fine-tuning (LoRA / Unsloth) and diffusion speech synthesis (IndicF5 / CosyVoice).
- **Full-Stack Engineers**: FastAPI / Next.js audio ingestion workflows.
- **Linguists & Community Members**: Telugu regional dialect (Telangana, Rayalaseema, Coastal Andhra) datasets and validation.

Check out [**`docs/MISSION.md`**](docs/MISSION.md) for collaboration details and reach out!

---

## 📜 License

This repository is licensed under the [MIT License](LICENSE).
