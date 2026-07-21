---
name: feedback_no_professor_mentions
description: Never reference the professor/instructor/lecture-author inside a submission document; it breaks the first-person student voice
metadata:
  node_type: memory
  type: feedback
---

**Hard rule: a submission document must NEVER mention the professor (or "the instructor", "the lecturer", "the prof", etc.), and must never frame a result as "matching"/"confirming" what the professor or their slides said.** The submission IS being handed to the professor, so wording like "these match the professor's 20,000 km/s" or "matches the professor's approximation V = -2.5 kBTe/e" reads as if some third party did the work and is explaining it back to the grader. It shatters the first-person student voice and sounds weird in a paper the professor is reading.

**How to fix / avoid:**
- State the result as the student's own: "I get 20,000 km/s" not "these match the professor's 20,000 km/s."
- If a value needs sourcing, cite the course material by number/name only ("Lesson 4 Part 3 [4]", "the day/solar-max profile", "the standard $-2.5\,k_BT_e/e$ result"), never as belonging to the professor.
- For sanity checks, verify against physics/independent methods, NOT against "what the professor got" (this already overlaps the grading-prompt rule "do NOT compare against the professor's numerical values directly").
- Applies to code comments too (e.g. "# Verification: professor's approximation" -> "# Verification: standard -2.5 kT/e result").

**Why:** Jordan flagged it directly and with some heat: "there should never ever be mention of the professor in the document ... that sounds like someone else did the work and is explaining it to me when this is meant to be a submission document to the professor." Also an AI-artifact tell (like the em-dash and meta-commentary bans). Related: [[feedback_no_em_dashes]], [[feedback_submission_voice]], [[feedback_conciseness]].
