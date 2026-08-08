---
name: feedback_formal_report_style
description: Grader rules for SPCE 5065 formal design reports, including the third-person exception to the standing first-person voice rule
metadata:
  node_type: memory
  type: feedback
---

Milestone 2 of the design project scored 92/100 and lost **3 points on grammar** for three specific things. All three apply to any formal report in this course, and all three are cheap to get right the first time:

1. **"Don't use first person in a formal report."** Write the design report impersonally. "The recommendation is a full TVAC campaign", not "I recommend". "All four torques were evaluated", not "I evaluated". "Category R parts are specified", not "I specify".
2. **"Include units in nomenclature section."** Split the nomenclature into an acronym table and a symbol table, and give the symbol table a Units column with an entry for every row. Mark dimensionless quantities with a dash rather than leaving the cell blank.
3. **"Define all variables with equations."** Every display equation, and every formula quoted inside a table, needs a `where $x$ is ... (units), $y$ is ...` line immediately after it. The nomenclature table does not substitute for this. While doing that pass, also resolve symbol collisions: MESA's report renamed the elementary charge to $q_e$ (against orbital eccentricity $e$), Earth's magnetic moment to $M_E$ (against slew torque $M$), orbital velocity to lowercase $v$ (against spacecraft potential $V$), and orbital period to $P_{orb}$ (against power $P$).

**The voice rule is a genuine exception, decided by Jordan on 7 Aug 2026.** [[feedback_submission_voice]] and the solution prompt call for first-person singular, and that still holds for **homework and exam submissions**. **Design-project reports go in third person**, because the grader marked the document type specifically. Do not "fix" homework voice to match this, and do not revert the report to first person.

Two other MS2 deductions were content, not style, and both are the same failure mode of quoting a result instead of showing where it came from:

- **Plasma, -2:** "Although your final answer is reasonable (potential) I don't know how you got that." The floating potential was boxed as $V = -2.5\,k_BT_e/q_e \approx -2.16$ kV with no electron temperature stated and no arithmetic. The fix: state $T_e = 10^7$ K, show $k_BT_e/q_e = 862$ V, then $-2.50 \times 862 = -2{,}155$ V, and say where the 2.50 coefficient comes from (current balance, electron-to-ion mass ratio, and the collection model assumed).
- **ADACS, -1:** "justification for 100% margin factor." A margin factor needs a defense in terms of what it buys. The report now justifies it three ways: it covers a client up to 14,100 kg rather than only the assumed 3,000 kg, it absorbs off-nominal capture rates and an unknown mated centre of mass, and it allows a 425 s slew instead of 600 s.

**A margin comment on a subsystem section means design margin, not page margins.** TCS lost 2 to a bare "Add margin" with the other three bullets check-marked. Answer it with a table of predicted value, limit, and margin per case, plus a load-growth sensitivity and the trade against whatever the margin costs elsewhere.

**This grader is by-the-book on formal-report convention, so do not propose anecdotal or personal-experience content for design-project submissions.** Jordan considered adding lessons from his AES pre-construction work (bid-versus-target behaviour, interconnection scope risk, back-to-back LD margin logic) to the cost, risk, and margin sections of the final report, and decided against it on 7 Aug 2026 for exactly this reason. A draft of what those insertions would have said is kept at `design_project/final_project/experience_insertions_DRAFT.md`, outside the submission folder. The underlying arguments were sound; the genre was wrong.

**Why:** direct grader feedback on Milestone 2, worth 8 points, and every item recurs on the final report rubric. **How to apply:** run these six checks before delivering any design-project document. Related: [[feedback_references]], [[feedback_conciseness]], [[project_final_report_anchor]], [[project_ms2_anchor]].
