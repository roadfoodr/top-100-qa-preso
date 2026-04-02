You are analyzing student questions from an AI engineering course Discord across four cohorts. Your task is to extract a ranked list of Frequently Asked Questions.

## Instructions

### Step 1: Build Subtopic Taxonomy
Review the attached lecture summaries and extract a complete list of granular subtopics. Output this as a structured list organized by workshop before proceeding.

### Step 2: Map and Normalize Questions
For each question in the CSV:
- Map to the most specific subtopic from your taxonomy
- If a question doesn't fit the lecture taxonomy, assign it to an emergent category (e.g., "Environment Setup," "Assignment Logistics," "Tool Installation," "General Python," etc.)—group similar off-taxonomy questions together under sensible labels
- Normalize to a canonical phrasing (clear, concise, stripped of Discord-specific language)

### Step 3: Group and Count
- Group semantically identical questions (same core question, different phrasing)
- Count frequency of each canonical question

## Output Format

**Part A: Subtopic Taxonomy**
List all subtopics organized by workshop, plus any emergent categories you created for off-taxonomy questions.

**Part B: FAQ Rankings**
Markdown table ranked by frequency (highest first):

| Rank | Canonical Question | Subtopic | Source | Count | Example Variants |
|------|-------------------|----------|--------|-------|------------------|

- **Source**: Workshop name if from taxonomy, or "Emergent" if off-taxonomy
- Include the top 20 FAQs
- In "Example Variants," show 1-2 original phrasings that were consolidated

## Notes

- Some items may not be true questions—skip those
- Use the **most specific subtopic** that applies
- Preserve technical accuracy when rewriting