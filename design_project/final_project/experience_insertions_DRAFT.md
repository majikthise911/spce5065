# Draft: energy-industry experience insertions

Not part of the submission. This is a decision document: four candidate additions to
`submission/Clayton_spce5065_final_submission.md`, each shown with its exact anchor so a
merge is mechanical. Nothing here has been applied to the report.

**Total if all four are taken:** 342 words in the impersonal versions, roughly half a
page. No new figures, tables, equations, or references.

---

## Two things to decide before any of this goes in

**Voice.** The Milestone 2 grader took three points for first person in a formal report.
Each insertion below is written twice: an **impersonal** version that preserves that fix,
and a **first-person** variant. The impersonal versions are the recommendation, because
they carry the same substance and cost nothing on the grammar line.

**Confidentiality.** The underlying material is internal commercial work: client bid
prices, interconnection cost gaps, and liquidated-damages rates on named projects. None of
that belongs in a university submission. Every draft below states the *pattern* and omits
the employer, the clients, and the figures. Worth a look from you specifically, since you
know where the line is better than I do.

---

## Insertion 1: Section 7.5, Cost

**Draws on:** the Grand Mayes bid comparison, where the binding EPC proposal came back
well above the internal target on the comparable basis, and the descope and negotiation
cycle that followed.

**Why here:** Section 7.5 is the weakest part of the report. It allocates the $100M cap
top-down and holds a $5M reserve without saying what the reserve is actually for. This
turns a soft section into a defensible one, and it adds a real engineering artifact, the
descope list, rather than a platitude.

**Anchor:** after the paragraph beginning "Two caveats belong on this table rather than in
a footnote" (line 584), before "The value argument closes the case."

> **Impersonal version.**
> Design-to-cost only holds if the reserve is honest about how first bids behave. On
> capital projects procured this way, the first binding proposal routinely lands above the
> internal target once the bidder prices its own risk, and the recovery mechanism is scope
> rather than reserve. Five percent covers estimating noise, not a scope surprise, so the
> program carries a ranked descope list against the reserve rather than pretending the
> reserve absorbs one: the second star tracker, the arm's secondary servicing tooling, and
> the inspection payload come out in that order, none of which touches the primary
> life-extension mission.

> **First-person variant.** Replace the first two sentences with: "In pre-construction work
> on utility-scale energy projects, the most common estimating error I have seen is
> treating the internal target price as the expected price. The first binding proposal
> routinely lands above it once the bidder prices its own risk, and the recovery mechanism
> is scope rather than reserve."

---

## Insertion 2: Section 13.3, risk register

**Draws on:** the PR Thermal CAPEX review, where the cost exposure was not in the
generating plant but in the interconnection scope defined by another party.

**Why here:** it names the pattern the register is actually tracking, and it explains why
R1 and R4 stay highest after mitigation instead of leaving that as an observation. This is
the strongest analogy in the set, because the structure of the problem is identical.

**Anchor:** after the paragraph beginning "Two observations matter more than the
individual scores" (line 994).

> **Impersonal version.**
> There is a pattern under those two observations worth naming, because it is what the
> register is really tracking. On large capital projects the cost and schedule surprises
> rarely come from the plant itself, which the builder controls and has built before. They
> come from the interface to a system somebody else controls, where scope is defined late
> and by another party. MESA's equivalent is the client vehicle: its mass, its residual
> rates, its surface materials, and its state of health are all set by the customer and are
> not fully known until capture. Designing that interface for the range rather than the
> point estimate is the only defense available, and it is why the two docking risks stay at
> the top of the register even after mitigation.

> **First-person variant.** Open with: "The pattern under those two observations is one I
> have seen repeatedly on large capital projects, where the cost surprises rarely come from
> the plant itself..."

---

## Insertion 3: Section 11.2, the ADACS margin justification

**Draws on:** the Monarch back-to-back liquidated-damages structure, where the guaranteed
contractor completion date was deliberately set ahead of the downstream obligation so the
contractor's exposure shields the owner's.

**Why here:** the grader docked this line once already. The report now defends the margin
with three specific reasons, and this generalizes them into a principle, which is what
turns a justification into an argument.

**Anchor:** replaces the closing paragraph at line 804, "The margin is therefore not a
round number applied out of habit. It is what makes the design insensitive to the one
parameter, client mass, that the customer rather than the contractor controls."

> **Impersonal version.**
> The margin is therefore not a round number applied out of habit. The general principle is
> the one worth stating, because it decides where margin is worth paying for: margin belongs
> against the parameters somebody else controls. Client mass, residual capture rates, and
> the mated centre of mass are the customer's to set. Slew time, wheel count, and
> pyramid geometry are the contractor's. Buying margin against the first set is what makes
> a design robust; buying it against the second is mostly what makes it heavy.

> **First-person variant.** Same text with the middle sentence as: "The principle I would
> apply here is one that carries over from contracting: margin belongs against the
> parameters somebody else controls."

---

## Insertion 4: Section 8.2, thermal design margin

**Draws on:** the assumption-book-versus-engineering-estimate gaps on PR Thermal, where
every material gap sat in a line that had been captured once as an estimate and never
re-levied as a constraint.

**Why here:** the report already says the 1,200 W is a not-to-exceed requirement rather
than a best estimate. One sentence explains why that distinction earns its place.

**Anchor:** appended to the paragraph beginning "**The hot case is the binding one**"
(line 630), which currently ends "...is a not-to-exceed number levied on the subsystems,
not a best estimate."

> **Impersonal version.**
> That distinction is not pedantry. Overruns on complex systems accumulate almost entirely
> in line items that were captured once as estimates and never converted into constraints
> anybody was accountable to.

> **First-person variant.** Prefix with "In my experience," and drop "not pedantry" to
> "worth insisting on."

---

## Considered and rejected

- **Cashflow S-curve estimator to Sections 10.1 and 13.1.** The small-sample,
  single-owner model and the honesty about its scope limits map well onto the assumed
  5 krad(Si)/yr dose rate and the Grun flux fit. But the report already handles both
  honestly, so this would restate rather than add.
- **Bid-comparison source fidelity to Section 7.4.** The rule against redistributing a
  value to make it fit the destination structure is exactly why the propellant table splits
  xenon and hydrazine instead of reporting one 600 kg number. The report already does this
  correctly, and explaining why would be self-congratulatory.
- **Gated go/no-go milestones to Section 2.4.** The discipline of a hard kill date maps to
  the space-weather hold gate and the capture abort criteria, but Section 13.2 already sets
  abort criteria at the mechanism's qualified envelope, which is the same point made better.

---

## If you want these merged

Say which insertions and which voice. Applying them means: edit the markdown, rebuild the
docx, reprint the PDF, run `sync_toc_pages.py`, reprint once more. 342 words is about half a page, so this may or may not
push one section across a page break; running the sync is how you find out.
