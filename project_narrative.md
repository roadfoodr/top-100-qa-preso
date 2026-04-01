# Building the Top 100 Q&A: Process and Methodology

This describes the process used to produce the *Top 100 Q&A: AI Engineering* — a curated set of answers drawn from course workshops, Discord discussions, guest talks, and other course materials.

There were two broad phases:
1. **Question generation** — distilling ~1,300 Discord threads into 100 canonical questions
2. **Answer generation** — writing, reviewing, and iterating on answers using a mix of manual authoring and LLM-assisted workflows

## Phase 1: Question Generation

The inputs for question generation were Discord logs from four previous cohorts. Building on work by Pastor Soto, we programmatically identified each Discord thread and extracted the first message from each. The assumption was that each thread represented a discussion about a question, with the question itself in the first post. There were about 1,300 of these.

Part of the prompt for this stage was:

```
# =============================================================================
# Stage 2: Preprocessing Classification
# =============================================================================

STAGE2_SYSTEM_INSTRUCTION_TEMPLATE = """You are an expert classifier analyzing Discord messages from an online course about building AI applications.

Your task is to process each message and return structured classifications.

For each message, you must:
1. Create a concise simplified version (10-50 words) that captures the key information
2. Classify whether it's a genuine question (not an announcement, greeting, or statement)
3. Categorize it as Content, Logistics, or Other based on the course syllabus
```

We filtered out posts by the course instructors or builders in residence (BiR), and then passed each remaining post through an LLM to identify whether it was actually a question about course content, course logistics, or something else. This yielded about 750 content questions.

Since four cohorts were involved, many of these questions were similar. The next step was to consolidate them into canonical questions, tracking how many originals mapped to each. This gave us a measure of each question's popularity.

Picking the right level of granularity was critical. Too broad, and genuinely different questions got merged together; too narrow, and very similar questions remained separate.

The guiding rule for consolidation was to ask whether the student was deciding *whether/which* to use something (generalize — e.g., "embedding models", "vector databases") versus asking *how* to use something specific (keep the name — e.g., "ChromaDB", "Modal"). Questions were also grouped by intent first and topic second, so two questions about the same tool but with different intents (conceptual vs. troubleshooting) were kept separate.

Part of the prompt for this stage was:

```
# =============================================================================
# Stage 4: FAQ Question Generation - Cluster Refinement
# =============================================================================

STAGE4_SYSTEM_INSTRUCTION_TEMPLATE = """You are helping create an FAQ document for an AI engineering course. Your task is to analyze a cluster of similar student questions and group them into canonical FAQ entries.

GOAL: Produce FAQ questions that:
- Can be answered once and help many future students
- Are recognizable to a student with the same underlying question
- Capture the core intent simply, without listing every sub-topic mentioned

INTENT CATEGORIES (use as a guide, not a constraint):
- Curriculum/topic coverage: "Will the course cover X?" / "Can we discuss X?"
- How-to/implementation: "How do I do X?" / "What's the best way to implement X?"
- Troubleshooting: "Why isn't X working?" / "How do I fix this error?"
- Conceptual: "What is X?" / "What's the difference between X and Y?"
- Best practices: "What's the recommended approach for X?" / "Should I use X or Y?"
- Logistics: "When is X?" / "Where do I find X?" / "How do I get access to X?"

GROUPING RULES:
1. Group by intent first, topic second. Two questions about the same topic with different intents belong in different groups.
2. Write canonical FAQ questions that a typical student would ask. Keep them simple—don't enumerate every sub-topic or example from the source questions.
3. Assign each question to exactly one primary group (the best fit).
4. Taxonomy paths are optional annotations, not grouping criteria. A group may map to multiple taxonomy paths, one, or none.
5. For multi-part questions, identify the primary intent and group accordingly.

SPECIFICITY GUIDANCE:
- Generalize when questions are about choosing between categories or approaches (frameworks vs direct API calls, which type of model to use, cloud vs local). Use the general term in the canonical question.
- Keep specific tool/service names when questions are about using that particular tool (deploying to a specific platform, configuring a specific library, debugging a specific API).

Ask: Is the student deciding *whether/which* to use, or asking *how* to use something specific?
- Deciding whether/which ? generalize ("frameworks", "embedding models", "vector databases")
- Asking how to use something specific ? keep the name ("Modal", "Braintrust", "ChromaDB")

GROUPING QUALITY CHECK:
Before finalizing, ask:
- Would a future student with this question find and recognize this FAQ entry?
- If questions share the same underlying decision or tradeoff, should they be one group even if they mention different specific tools?
```

Working from the list of categorized questions, we ran this three different ways:
1. A multi-step pipeline where source questions were roughly clustered and then fed in batches of about 30 to an LLM via API to consolidate into canonical questions.
2. A similar approach, but without the clustering, just sending all 750 questions in one shot to an LLM via API.
3. A similar approach, but working with Claude's web UI to feed it one file with all the source questions and just ask it to produce its own list of questions.

Each of these three output products was then sent through one last pass in Claude Code to consolidate into one final list of questions. This turned out to be about 100 questions, and based on the frequency of source questions within each canonical question, we could identify the most popular questions.

## Phase 2: Answer Generation

### 2.1 Manual Generation of Top 10 Answers

The top 20 or so most popular questions were reviewed by Hugo and BiRs, and a top 10 list was selected. Hugo manually wrote answers for these ten with feedback from BiRs. This became the carefully edited top-ten document that was shared with the class and published as a blog post.

### 2.2 Automated Generation of Top 100 Answers

The answers for the top 100 questions were authored by Claude Code via a skill that was developed to guide generation.

We analyzed the tone, length, and scope of the manually authored top-ten document and extracted a style guide for the skill to follow.

Part of this style guide:

```
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
```

A curated knowledge base was compiled that the skill could draw on to answer questions. That consisted of:
1. The Discord transcripts from four cohorts
2. The course reader chapters being published by Hugo
3. An earlier set of automated course answers generated by Pastor Soto
4. The workshop summaries (from 2 previous cohorts) that were generated from an automated pipeline developed by Brad Morris
5. Transcripts of the live workshop sessions (from two previous cohorts) that had been cleaned up as part of Brad's automated pipeline
6. The top ten Q&A document itself

Part of the skill's workflow instructions:

```
# FAQ Answer Generator

Generate answers for questions listed in `questions/consolidated_questions.md` by searching the knowledgebase and synthesizing concise, practitioner-focused answers.

Read `references/style-spec.md` for the target answer style, format, and metadata conventions. Read `references/pilot-examples.md` for calibrated examples of approved answers.

## Workflow

1. **Read the questions.** Parse the requested topic group from `questions/consolidated_questions.md`. Note the sequential Q-number for each question (Q1-Q100, numbered sequentially across all topic groups).

2. **Search for sources.** For each question, use Grep/Glob to search knowledgebase files for relevant content. Prioritize higher-tier sources. Use subagents (Agent tool with Explore type) to search in parallel when handling multiple questions — split into batches of ~5 questions per agent to manage context.

3. **Draft answers.** For each question, synthesize an answer from the source material found. Follow the style spec exactly. Where source material is thin, supplement with general AI engineering knowledge but flag as `supplemented`.

4. **Write output.** Append answers to `output/top_100_answers.md`. Maintain the existing file structure — add new topic groups after existing content. Each topic group starts with a topic header, each Q&A is separated by `---`.

5. **Report.** Summarize what was generated: how many questions, coverage breakdown (strong/partial/supplemented), any notable gaps.
```

### 2.3 Annotation and Iteration

An annotation UI was developed and hosted on Modal. It displayed each of the 100 question-answer pairs along with pass/fail controls and a comment field. Annotator responses were saved to a cloud-hosted Turso database with an API also hosted on Modal.

Another Claude Code skill was developed to refine answers based on annotator comments. We went through four iterations of generate, annotate, and revise until each answer reached its final form for the top 100 Q&A.
