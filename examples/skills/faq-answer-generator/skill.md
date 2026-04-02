---
name: faq-answer-generator
description: Generate answers for FAQ questions by searching a knowledgebase of course materials (workshops, Discord chats, guest talks, transcripts) and synthesizing concise, practitioner-focused Q&A entries. Use when asked to generate answers for the Top 100 FAQ, write Q&A entries, draft answers for consolidated questions, or continue/resume answer generation for any topic group.
---

# FAQ Answer Generator

Generate answers for questions listed in `questions/consolidated_questions.md` by searching the knowledgebase and synthesizing concise, practitioner-focused answers.

Read `references/style-spec.md` for the target answer style, format, and metadata conventions. Read `references/pilot-examples.md` for calibrated examples of approved answers.

## Source Material

Knowledgebase is at `knowledgebase/` with sources ranked by quality:

| Tier | Source | Notes |
|------|--------|-------|
| 1 | Top10.md | Polished, detailed |
| 1 | course_reader/ | Official course reader PDFs. Use the `*_index.md` files (e.g. `course_reader_ch1_index.md`) to find relevant pages, then read specific pages from the corresponding PDF. |
| 1 | Discord-BuildWithAI-summaries/ | Already Q&A format |
| 2 | workshop_to_wiki_summaries/ | Structured wiki summaries |
| 2 | workshop_to_wiki_guest_talks/ | Expert perspectives |
| 3 | workshop_to_wiki_transcripts/ | Raw but rich |
| 4 | discord_chat_transcripts/ | Low signal-to-noise, mine selectively |

## Workflow

1. **Read the questions.** Parse the requested topic group from `questions/consolidated_questions.md`. Note the sequential Q-number for each question (Q1-Q100, numbered sequentially across all topic groups).

2. **Search for sources.** For each question, use Grep/Glob to search knowledgebase files for relevant content. Prioritize higher-tier sources. Use subagents (Agent tool with Explore type) to search in parallel when handling multiple questions — split into batches of ~5 questions per agent to manage context.

3. **Draft answers.** For each question, synthesize an answer from the source material found. Follow the style spec exactly. Where source material is thin, supplement with general AI engineering knowledge but flag as `supplemented`.

4. **Write output.** Append answers to `output/top_100_answers.md`. Maintain the existing file structure — add new topic groups after existing content. Each topic group starts with a topic header, each Q&A is separated by `---`.

5. **Report.** Summarize what was generated: how many questions, coverage breakdown (strong/partial/supplemented), any notable gaps.

## Coverage Assessment

When assessing coverage for the metadata tag:
- **strong** — multiple Tier 1-2 sources directly address the question, answer is well-grounded
- **partial** — some relevant source material exists but answer required extrapolation or inference
- **supplemented** — thin/no coverage in knowledgebase; answer draws primarily on general knowledge (flag these explicitly to the user)

## Key Rules

- Questions are numbered Q1-Q100 sequentially across the entire file, not restarting per topic group.
- Keep metadata (coverage, sources) visible as bold text — do not use HTML comments.
- Source filenames in metadata are relative to `knowledgebase/` (just the filename, not full path).
- Do not regenerate existing answers unless explicitly asked. Check what's already in the output file.
- When the user asks to "continue" or "do the next batch", read the output file to determine where to pick up.

## Source Links

When quoting or attributing a speaker, check whether the source document
includes a hyperlink for that person or reference. If so, include it as a
markdown link on the attribution. Sources that contain URLs:

- `Top10.md` — speaker names and key references are hyperlinked inline
- `course_reader_ch1_index.md` — Named Experts section has guest talk /
  blog post URLs
- `course_reader_ch2_index.md` — Named Experts section has speaker quotes

**Format:** Use the speaker attribution as the link text:
- Yes: As [Samuel Colvin (Pydantic)](https://...) put it: "..."
- Yes: See [Jeff Huber's research at Chroma](https://...)
- No: As Samuel Colvin (Pydantic) put it (see https://...) ← don't do this

Only include URLs that appear in the source material. Do not fabricate or
guess URLs.

## Revision Pass Mode

When asked to do a revision pass, revise answers, or address reviewer feedback:

1. **Fetch feedback.** Run:
   ```
   python .claude/skills/faq-annotator/scripts/fetch_feedback.py
   ```
   This calls the annotation API and outputs a markdown report of questions
   that failed or received reviewer comments. The report includes each
   flagged question's current answer text and all reviewer comments.

2. **Determine revision numbers.** Find the latest `output/top_100_answers_r{N}.md`
   file. That is the current revision. The new output will be `r{N+1}`.
   This is re-runnable: r1→r2, r2→r3, etc.

3. **Read the current answers.** Parse `output/top_100_answers_r{N}.md` to
   get all 100 current answers.

4. **For each flagged question:** Re-search the knowledgebase and revise
   the answer. The current answer text is included in the feedback report —
   use it as a starting point since much of it may already be good.
   Incorporate the reviewer feedback as revision instructions:
   - "Too long" → tighten
   - "Missing X" → search for X and incorporate
   - "Inaccurate claim about Y" → verify against sources, correct or remove
   - "Needs example" → find a concrete example from source material
   - Failed with no comment → re-examine for style-spec compliance and source
     grounding; improve coverage and specificity

   **Question revisions:** Some reviewer comments may target the question
   text itself (e.g. "question is confusing", "too broad", "simplify the
   wording"). When feedback clearly relates to the question rather than the
   answer, revise the question text accordingly. Rules:
   - The question number (Q{N}) must NOT change — only update the wording.
   - The revised question must stay within its current topic group.
   - Also re-examine the answer to ensure it still fits the revised question.

5. **Preserve unchanged answers.** All questions NOT in the feedback report
   appear in r{N+1} with their original text, unchanged.

6. **Write r{N+1}.** Write the complete 100-question answer set to
   `output/top_100_answers_r{N+1}.md`. Same format as the current revision.
   Add metadata line `**revised:** yes` only to answers that changed in
   this revision pass (r{N} → r{N+1}). Remove any `**revised:** yes` tags
   carried over from prior revisions — each revision file should only mark
   what changed in that specific transition.

7. **Write report.** Save a revision report to
   `output/revision_report_r{N+1}.md` summarizing: how many questions
   revised, how many questions reworded, what feedback was addressed per
   question, and any items where feedback couldn't be fully addressed.

### Important
- Do NOT post revised answers back to the annotation API.
- Process revised questions using the same parallel subagent batching as
  initial generation (batches of ~5 questions per agent).
