# Project Mission: Hyper-Personalized Telugu/Tenglish AI Voice & Persona Clone

## Executive Pitch

### Mission Statement
Build an AI system that clones not just a person’s acoustic voice, but their complete linguistic identity—their regional dialect, personal vocabulary, sentence rhythm, and conversational slang—enabling them to generate localized audio content in **Telugu and Romanized "Tenglish"** (Telugu written phonetically in English script).

---

### The Core Problem
Current AI voice clones and translators (e.g., ElevenLabs, Google Translate, Whisper) sound either like formal newsreaders or produce awkward, anglicized pronunciations when handling Indic languages and code-mixed scripts (Tenglish / Hinglish). They fundamentally fail at:
1. **Regional Dialects:** Telangana slang vs. Coastal Andhra vs. Rayalaseema colloquialisms.
2. **Personal Style:** A person’s unique catchphrases, sentence endings (*kadaa*, *mari*, *antey*, *le*), and code-switching habits.
3. **Continuous Learning:** Progressively adapting as more voice notes, audio monologues, and text messages are provided over time.

---

### High-Level System Workflow
```
[User Voice Notes & Texts]
          │
          ▼
[1. Persona & Lexicon Miner] ──► (IndicWhisper + TF-ICF Lexicon Profiling)
          │
          ▼
[2. Dialect Cognitive Brain] ──► (Telugu LLM Labs Navarasa 2.0 / Gemma-Telugu + LoRA)
          │
          ▼
[3. Phonetic Normalizer]     ──► (AI4Bharat IndicXlit + IndicMFA)
          │
          ▼
[4. Indic Voice Cloner]      ──► (Smallest AI Waves / AI4Bharat IndicF5 / Sarvam Bulbul)
          │
          ▼
[Final Personalized Telugu / Tenglish Speech]
```

---

### Roles & Help Needed
- **AI / ML Engineers**: Experience with fine-tuning open Indic LLMs (LoRA/QLoRA via Unsloth on Gemma/Llama) and neural audio synthesis (AI4Bharat IndicF5, CosyVoice 2, or Smallest AI Lightning TTS).
- **Full-Stack / Pipeline Engineers**: Build the ingestion pipeline (audio file upload $\rightarrow$ VAD chunking $\rightarrow$ ASR transcription $\rightarrow$ dynamic persona memory $\rightarrow$ script generation $\rightarrow$ audio rendering).
- **Telugu Linguistic & Community Curators**: Collect regional idioms, slang dictionaries, and validate dialect authenticity.

---

## Detailed Technical Approach & Architecture

> For the comprehensive 1,300+ line technical evaluation across all 14 evaluated models and benchmark datasets, read [**`telugu-personalized-localization-tenglish/report.md`**](./telugu-personalized-localization-tenglish/report.md).

### Stage 1: Continuous Audio & Text Ingestion (Over-Time Learning)
- **Goal**: Convert raw, unstructured voice recordings and chat logs into a dynamic, evolving user persona profile.
- **ASR & Diarization**: Uses [`IndicWhisper`](./telugu-personalized-localization-tenglish/report.md#7-indicwhisper-lexicon-extraction-framework) fine-tuned on Vistaar/Kathbath (1,680+ hours of Indic speech) paired with Silero VAD and PyAnnote Diarization to isolate clean speech segments.
- **Lexical Mining (TF-ICF)**: Compares the user's transcript frequency against standard formal Coastal Andhra corpora to detect:
  - **Regional Dialect Slang**: *Telangana:* `gatla`, `dhaawat`, `kirrak`, `paisal`, `endi bro`; *Rayalaseema:* `mande`, `dhabba`, `endappa`.
  - **Discourse Markers**: `kadaa`, `antey`, `mari`, `le`, `boss`.
  - **Code-Mixing Ratio**: Percentage of English loanwords embedded in everyday sentences.
- **Acoustic Profiling**: Measures average speech rate (WPM), pitch variance ($F_0$), and pause durations to parameterize downstream voice cloning models.

### Stage 2: The Cognitive Persona Brain (Scripting & Dialect Localization)
- **Goal**: Ingest an English outline, script idea, or prompt, and generate colloquial Telugu / Tenglish matching the user's personality.
- **Foundation Model**: [`Telugu LLM Labs (Navarasa 2.0 / Gemma-Telugu)`](./telugu-personalized-localization-tenglish/report.md#14-telugu-llm-labs-navarasa-20-gemma-telugu-tinyllama-romanization), which features an Indic-optimized SentencePiece tokenizer (1.6–2.4 tokens/word vs. 6.0–9.0 on standard models).
- **Adaptation Strategy**:
  - *Short-term / In-Context*: Dynamic few-shot prompt injection (via DSPy) injecting the top-20 user catchphrases and tone instructions into the system prompt.
  - *Long-term / Fine-Tuning*: Periodically train a lightweight (~50MB) LoRA adapter on accumulated user transcripts using Unsloth in <30 minutes on a single GPU.

### Stage 3: The "Tenglish" Orthographic & Phonetic Bridge
- **The Core Problem**: Direct text-to-speech on informal Romanized Latin text (e.g., *"nenu repu morning office ki vastanu"*) causes standard TTS engines to adopt an unnatural, anglicized accent or choke on consonants.
- **Solution ([`AI4Bharat IndicXlit`](./telugu-personalized-localization-tenglish/report.md#4-ai4bharat-indictrans2-indicxlit) + [`IndicMFA`](./telugu-personalized-localization-tenglish/report.md#3-ai4bharat-indicmfa-g2g-phonetic-alignment))**:
  - Converts Romanized Telugu phonemes into canonical Telugu Unicode while leaving legitimate English loanwords intact (e.g., `నేను రేపు morning office కి వస్తాను`).
  - Grapheme-to-Grapheme (G2G) alignment preserves Dravidian *ajanta* vowel endings (`రాముడు`) and retroflex consonant distinctions (`ట` vs `త`), preventing erroneous Hindi-style schwa deletion.

### Stage 4: Zero-Shot Indic Voice Cloning & Acoustic Synthesis
- **Goal**: Synthesize the normalized script in the user's exact vocal timbre, cadence, and emotion from as little as 10–30 seconds of clean audio.
- **Implementation Options**:
  - **Ultra-Low Latency Managed API (<100ms TTFA)**: [`Smallest AI (Waves Platform & Lightning TTS)`](./telugu-personalized-localization-tenglish/report.md#12-smallest-ai-waves-platform-lightning-tts) or [`Sarvam AI (Bulbul TTS)`](./telugu-personalized-localization-tenglish/report.md#11-sarvam-ai-suite-sarvam-12-bulbul-tts-mayura) natively built for Indian code-switching.
  - **Sovereign Open-Source Self-Hosted**: [`AI4Bharat IndicF5 & Indic Parler-TTS`](./telugu-personalized-localization-tenglish/report.md#2-ai4bharat-indicf5-indic-parler-tts) or [`CosyVoice 2`](./telugu-personalized-localization-tenglish/report.md#9-open-source-zero-shot-voice-cloning-xtts-v2-f5-tts-cosyvoice) running on self-hosted NVIDIA RTX 4090 / A10G GPUs with zero per-minute API fees.

---

## MVP Milestones & Implementation Roadmap

```
[Phase 1: Ingestion & Profiler] ──► [Phase 2: Dialect LLM Playground] ──► [Phase 3: End-to-End Voice Synthesis]
```

1. **Phase 1 (Week 1–2): Audio Ingestion & Persona Profiler**
   - Build a CLI/web interface to drop in user voice clips (WAV/MP3).
   - Run IndicWhisper transcription + Silero VAD to produce timestamped text and clean 10–15s reference voice samples.
   - Run TF-ICF script to extract user-specific catchphrases, dialect tokens, and speech tempo.

2. **Phase 2 (Week 3–4): Dialect Transcreation & Tenglish Normalization**
   - Set up `Telugu LLM Labs Gemma-Telugu (2B/7B)` with DSPy prompt conditioning.
   - Input: English script $\rightarrow$ Output: Dialect-accurate colloquial Telugu / Tenglish.
   - Connect `IndicXlit` to generate dual-script outputs (canonical Telugu Unicode for TTS, Romanized Tenglish for user review).

3. **Phase 3 (Week 5–6): Voice Cloning Integration**
   - Connect Smallest AI Waves API or self-hosted IndicF5 container.
   - Enroll the user's cached reference audio.
   - Render the personalized voice note and measure speaker similarity (MOS) and pronunciation naturalness.

---

## Quick Reference Links
- [Complete Deep Research Report (`report.md`)](./telugu-personalized-localization-tenglish/report.md)
- [Research Configuration & Execution Settings (`outline.yaml`)](./telugu-personalized-localization-tenglish/outline.yaml)
- [Comprehensive Field Specifications (`fields.yaml`)](./telugu-personalized-localization-tenglish/fields.yaml)
- [All 14 Raw JSON Result Profiles (`results/`)](./telugu-personalized-localization-tenglish/results/)
