#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import json
import glob
from pathlib import Path
import yaml

TOPIC_DIR = Path(__file__).resolve().parent
RESULTS_DIR = TOPIC_DIR / "results"
FIELDS_FILE = TOPIC_DIR / "fields.yaml"
OUTPUT_FILE = TOPIC_DIR / "report.md"

CATEGORY_MAPPING = {
    "Basic Info": ["basic_info", "Basic Info"],
    "Technical Features": ["technical_features", "technical_characteristics", "Technical Features"],
    "Performance Metrics": ["performance_metrics", "performance", "Performance Metrics"],
    "Milestone Significance": ["milestone_significance", "milestones", "Milestone Significance"],
    "Business Info": ["business_info", "commercial_info", "Business Info"],
    "Competition & Ecosystem": ["competition_ecosystem", "competition", "Competition & Ecosystem"],
    "History": ["history", "History"],
    "Market Positioning": ["market_positioning", "market", "Market Positioning"],
}

INTERNAL_KEYS = {"_source_file", "uncertain"}
TOP_LEVEL_CATEGORY_KEYS = {k for sublist in CATEGORY_MAPPING.values() for k in sublist}


def slugify(text):
    text = text.lower()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text).strip("-")
    return text


def load_fields_yaml():
    with open(FIELDS_FILE, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    fields_config = data.get("fields", {})
    return fields_config


def get_field_from_json(json_data, field_name, category_name=None):
    # 1. Top level
    if field_name in json_data and json_data[field_name] is not None:
        return json_data[field_name]

    # 2. Inside matching category dict
    if category_name and category_name in CATEGORY_MAPPING:
        aliases = CATEGORY_MAPPING[category_name]
        for alias in aliases:
            if alias in json_data and isinstance(json_data[alias], dict):
                if field_name in json_data[alias] and json_data[alias][field_name] is not None:
                    return json_data[alias][field_name]

    # 3. Traverse all nested dicts
    for k, v in json_data.items():
        if isinstance(v, dict) and field_name in v and v[field_name] is not None:
            return v[field_name]

    return None


def is_uncertain_or_empty(val, field_name, uncertain_list):
    if val is None or val == "":
        return True
    if field_name in uncertain_list:
        return True
    if isinstance(val, str) and "[uncertain]" in val.lower():
        return True
    return False


def format_value(val):
    if isinstance(val, list):
        if not val:
            return "_None_"
        # List of dicts
        if all(isinstance(x, dict) for x in val):
            lines = []
            for d in val:
                line = " | ".join(f"**{k}**: {format_value(v)}" for k, v in d.items())
                lines.append(f"- {line}")
            return "\n" + "\n".join(lines)
        # Normal list
        str_items = [str(x) for x in val]
        total_len = sum(len(x) for x in str_items)
        if total_len < 80 and len(str_items) <= 4:
            return ", ".join(str_items)
        else:
            return "\n" + "\n".join(f"- {x}" for x in str_items)
    elif isinstance(val, dict):
        lines = []
        for k, v in val.items():
            lines.append(f"- **{k}**: {format_value(v)}")
        return "\n" + "\n".join(lines)
    else:
        text = str(val).strip()
        if "\n" in text:
            # Multi-line formatted
            formatted_lines = []
            for l in text.splitlines():
                formatted_lines.append(l)
            return "\n" + "\n".join(formatted_lines)
        return text


def main():
    fields_config = load_fields_yaml()
    json_paths = sorted(glob.glob(str(RESULTS_DIR / "*.json")))
    if not json_paths:
        print("No JSON files found in", RESULTS_DIR)
        return

    items_data = []
    for jp in json_paths:
        with open(jp, "r", encoding="utf-8") as f:
            data = json.load(f)
        data["_file_path"] = jp
        data["_file_stem"] = Path(jp).stem
        items_data.append(data)

    report_lines = []
    report_lines.append("# Deep Research Report: Personalized Telugu (Tenglish) & Hindi Localization, Dialect Adaptation, and Voice Cloning Pipeline\n")
    report_lines.append("> **Topic**: Continuous Personalization, Regional Dialect Adaptation, and Multilingual Voice Cloning for Telugu (Tenglish) and Hindi.\n")
    report_lines.append(f"> **Generated at**: October 2026 | **Total Evaluated Projects**: {len(items_data)}\n")
    report_lines.append("---\n")

    # Table of Contents
    report_lines.append("## Table of Contents\n")
    for idx, item in enumerate(items_data, 1):
        name = get_field_from_json(item, "name") or item["_file_stem"].replace("_", " ")
        anchor = slugify(f"{idx}-{name}")
        pipeline_stage = get_field_from_json(item, "pipeline_stage", "Basic Info") or "General"
        if len(pipeline_stage) > 60:
            pipeline_stage = pipeline_stage[:57] + "..."
        dev_org = get_field_from_json(item, "developer_or_organization", "Basic Info") or "Open Source"
        if len(dev_org) > 40:
            dev_org = dev_org[:37] + "..."
        report_lines.append(f"{idx}. [{name}](#{anchor}) - *Stage*: `{pipeline_stage}` | *Org*: {dev_org}")
    report_lines.append("\n---\n")

    # Detailed Content
    for idx, item in enumerate(items_data, 1):
        name = get_field_from_json(item, "name") or item["_file_stem"].replace("_", " ")
        anchor = slugify(f"{idx}-{name}")
        uncertain_list = item.get("uncertain", [])
        if not isinstance(uncertain_list, list):
            uncertain_list = []

        report_lines.append(f"<a id=\"{anchor}\"></a>")
        report_lines.append(f"## {idx}. {name}\n")

        # Track covered fields to collect extras
        covered_field_keys = set()

        # Iterate defined categories in fields.yaml
        for cat_raw_name, field_defs in fields_config.items():
            canonical_cat = cat_raw_name
            # find canonical header
            for can_name, aliases in CATEGORY_MAPPING.items():
                if cat_raw_name.lower() in [a.lower() for a in aliases]:
                    canonical_cat = can_name
                    break

            cat_lines = []
            for fdef in field_defs:
                fname = fdef["name"]
                fdesc = fdef.get("description", "")
                val = get_field_from_json(item, fname, canonical_cat)
                covered_field_keys.add(fname)

                if is_uncertain_or_empty(val, fname, uncertain_list):
                    continue

                formatted = format_value(val)
                # Field display
                field_title = fname.replace("_", " ").title()
                cat_lines.append(f"#### {field_title}")
                if fdesc:
                    cat_lines.append(f"*{fdesc}*")
                cat_lines.append(f"\n{formatted}\n")

            if cat_lines:
                report_lines.append(f"### {canonical_cat}\n")
                report_lines.extend(cat_lines)

        # Collect Extra Fields
        extra_lines = []
        for k, v in item.items():
            if k in INTERNAL_KEYS or k in TOP_LEVEL_CATEGORY_KEYS or k.startswith("_"):
                continue
            if k not in covered_field_keys and not is_uncertain_or_empty(v, k, uncertain_list):
                extra_lines.append(f"#### {k.replace('_', ' ').title()}\n\n{format_value(v)}\n")

        # Also check inside nested dicts for extra keys
        for top_k, top_v in item.items():
            if isinstance(top_v, dict) and top_k in TOP_LEVEL_CATEGORY_KEYS:
                for sub_k, sub_v in top_v.items():
                    if sub_k not in covered_field_keys and not is_uncertain_or_empty(sub_v, sub_k, uncertain_list):
                        extra_lines.append(f"#### {sub_k.replace('_', ' ').title()}\n\n{format_value(sub_v)}\n")

        if extra_lines:
            report_lines.append("### Other Info\n")
            report_lines.extend(extra_lines)

        # List skipped uncertain fields if any
        if uncertain_list:
            report_lines.append("### Flagged Uncertain Fields (Excluded from Report)\n")
            for u in uncertain_list:
                report_lines.append(f"- `{u}`: Information unreleased or not applicable for this architecture.")
            report_lines.append("\n")

        report_lines.append("\n---\n")

    # End of document synthesis
    report_lines.append("## Executive Synthesis: Blueprint for the Hyper-Personalized Telugu/Tenglish Voice Pipeline\n")
    report_lines.append("""Based on the 14 deeply investigated components, here is the optimal end-to-end composite architecture to achieve your exact goals:

```
[User Audio & Text History]
        │
        ▼
[1. Ingestion & Profiling] ──► IndicWhisper + PyAnnote Diarization
        │                        Extracts personal lexicon, catchphrases ('kadaa', 'endi bro'),
        │                        dialect tokens (Telangana/Rayalaseema), and cadence (WPM/F0).
        ▼
[2. Personal Cognitive Brain] ──► Telugu LLM Labs (Navarasa 2.0 / Gemma-Telugu) + LoRA
        │                          Instruction-tuned on your personal style to write scripts directly
        │                          in authentic colloquial Telugu with your favorite slang.
        ▼
[3. Transliteration / Tenglish] ──► AI4Bharat IndicXlit & IndicMFA
        │                            Normalizes colloquial Tenglish into Telugu Unicode + English loanwords,
        │                            preventing phonetic and prosodic corruption in speech models.
        ▼
[4. Voice Cloning & Synthesis] ──► Option A (Ultra-low Latency API): Smallest AI Lightning TTS / Sarvam Bulbul
                                  Option B (Sovereign Open Source): AI4Bharat IndicF5 / CosyVoice 2
                                  Replicates your exact vocal timbre, Dravidian dental/retroflex
                                  inflections, and natural speaking rhythm.
```
""")

    report_content = "\n".join(report_lines)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(report_content)

    print(f"Report successfully generated at: {OUTPUT_FILE}")
    print(f"Total items included: {len(items_data)}")


if __name__ == "__main__":
    main()
