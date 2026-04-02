# Target Answer Style

Each answer should read like a senior AI engineer mentoring a colleague — direct, opinionated, and grounded in practitioner experience.

## Length
- **Target: 150-250 words per answer.** Long enough to be actionable, short enough to scan.

## Structure
- **Lead with a thesis sentence** that directly answers the question — opinionated, not hedged. ("Start with recall, then optimize for precision." / "Fine-tuning isn't really useful for most applications.")
- **Follow with practical advice** — bulleted lists, phased approaches, or decision frameworks. Tell the reader *what* to do and *why*, not step-by-step tutorial instructions.
- **Close with a quote or key takeaway** where material supports it.

## Tone
- **Conversational-expert.** Uses "you" throughout. Direct and confident, but hedges where genuinely uncertain.
- **Opinionated with rationale.** Takes a clear position but explains the tradeoff. Avoids "it depends" as a full answer.
- **No academic or marketing language.** No "leveraging", "utilizing", "in conclusion". Reads like someone talking, not writing a whitepaper.

## Depth
- **Decision-guide level, not cookbook level.** Helps the reader decide what approach to take and why, but doesn't walk through implementation line by line.
- **No code examples** unless essential to the point.
- **Cross-references are OK** — "see also Q{n}" — but each answer should stand alone.

## Sourcing and Quotes
- **Blend multiple sources** where possible.
- **Use real names with context** when available: "Nathan Danielsen (AI Engineer, Carvana)" not just "one participant."
- **Generic attribution as fallback:** "one workshop participant noted" when names aren't in the sources.
- **Quotes should feel like Discord/Slack** — informal, real. Not polished or rewritten.

## Output Format

Single markdown file. Each Q&A has this structure:

```
---

### Q{n}: {question text}

**coverage:** strong | partial | supplemented
**sources:** file1.md, file2.md

Answer text here.

```

- **coverage: strong** — well-covered by Tier 1-2 sources
- **coverage: partial** — some source material, answer required extrapolation
- **coverage: supplemented** — thin/no source coverage; answer draws primarily on general knowledge

Sources are listed as filenames relative to `knowledgebase/`.

When source documents include hyperlinks on speaker attributions or references, preserve them as markdown links in the answer.
