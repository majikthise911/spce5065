Plan to implement                                                                                                       │
│                                                                                                                         │
│ Plan: Hybrid Weekly Study Guide Prompt                                                                                  │
│                                                                                                                         │
│ Context                                                                                                                 │
│                                                                                                                         │
│ The current WES_PROMPT.md produces output that is too thin -- no derivations, shallow flashcards, no worked examples.   │
│ The user wants a single optimized prompt that combines:                                                                 │
│ - WES: Concise executive-summary feel, analogies, mermaid diagrams, high-yield formula focus, visualization code,       │
│ active recall                                                                                                           │
│ - Study Guide (v5.1): Socratic phases with guiding questions, "pause and attempt" breaks, pitfalls per phase,           │
│ reflection                                                                                                              │
│ - Mastery Guide: First-principles progressive structure, worked examples, evidence-based learning, glossary             │
│                                                                                                                         │
│ Design Decisions (from user input)                                                                                      │
│                                                                                                                         │
│ - Output: Single .md file; code block included only when the topic genuinely benefits from visualization                │
│ - Derivation depth: Adaptive -- full for new/hard concepts, condensed for review concepts                               │
│ - Scope: Orbital mechanics specific (astrodynamics domain knowledge baked in)                                           │
│                                                                                                                         │
│ Prompt Structure (7 sections)                                                                                           │
│                                                                                                                         │
│ Section 0: Role & Meta-Instructions                                                                                     │
│                                                                                                                         │
│ - Role: Senior orbital mechanics engineer + learning scientist                                                          │
│ - Visual learner, active recall, first principles                                                                       │
│ - Adaptive derivation depth rule: "If this concept is new this week, derive from scratch. If it was covered before,     │
│ state the result and cite the prior week."                                                                              │
│ - Single .md output, code only when visualization genuinely aids understanding                                          │
│                                                                                                                         │
│ Section 1: The Intuition (from WES, enhanced)                                                                           │
│                                                                                                                         │
│ - Analogy (concrete, non-space)                                                                                         │
│ - Visual anchor (mental 3D image)                                                                                       │
│ - NEW: 1-paragraph "Why This Matters" connecting to real mission ops                                                    │
│                                                                                                                         │
│ Section 2: Concept Map (from Mastery Guide + WES mermaid)                                                               │
│                                                                                                                         │
│ - Mermaid diagram showing topic dependencies and how this week connects to prior weeks                                  │
│ - Progressive: starts with what you already know, arrows to new concepts                                                │
│                                                                                                                         │
│ Section 3: The Theory (hybrid of Mastery Guide derivations + Study Guide Socratic phases)                               │
│                                                                                                                         │
│ - For each key concept:                                                                                                 │
│   - Guiding Question (from Study Guide) -- "Before reading, ask yourself..."                                            │
│   - Pause marker -- "Attempt this yourself before continuing."                                                          │
│   - Derivation (adaptive depth per mastery guide)                                                                       │
│   - Worked Example with actual numbers from the homework/lecture                                                        │
│   - Common Pitfall (from Study Guide + WES "Trap")                                                                      │
│   - Reflection -- link to broader principle                                                                             │
│                                                                                                                         │
│ Section 4: The Toolbox (from WES, enhanced)                                                                             │
│                                                                                                                         │
│ - 3-5 high-yield formulas required for the homework                                                                     │
│ - Each with: LaTeX, variables+units, usage context                                                                      │
│ - NEW: One quick numerical "sanity check" per formula (plug in known values, verify output)                             │
│                                                                                                                         │
│ Section 5: Visualization (from WES, conditional)                                                                        │
│                                                                                                                         │
│ - Only included when the topic benefits from a plot                                                                     │
│ - Complete, standalone Python script                                                                                    │
│ - Must demonstrate the physics, not just plot data                                                                      │
│                                                                                                                         │
│ Section 6: Active Recall & Spaced Retrieval (upgraded from WES flashcards + Mastery Guide practice)                     │
│                                                                                                                         │
│ - Tier 1: Recall (5 Q&A flashcards -- quick facts)                                                                      │
│ - Tier 2: Apply (2-3 mini-problems -- "Given this orbit, compute X")                                                    │
│ - Tier 3: Predict (1 conceptual "what happens if..." question)                                                          │
│ - Answer key at the bottom                                                                                              │
│                                                                                                                         │
│ Section 7: Quick Reference Card                                                                                         │
│                                                                                                                         │
│ - 1-page condensed summary: all formulas, key constants, decision rules                                                 │
│ - Designed to be printed or screenshot for exam review                                                                  │
│                                                                                                                         │
│ File to create                                                                                                          │
│                                                                                                                         │
│ - /Users/jordanclayton/code/spce_5025/WES_PROMPT.md -- overwrite with the new hybrid prompt                             │
│                                                                                                                         │
│ Verification                                                                                                            │
│                                                                                                                         │
│ - After writing the prompt, regenerate the Week 5 WES using the new prompt to verify it produces better output          │
│ - Compare sections side-by-side with the original                                                                       │
╰─────────────────────────────────────────────────────────────────────────────────────