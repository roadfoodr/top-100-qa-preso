"""Prompt templates for LLM classification across pipeline stages.

This module contains prompt templates organized by stage, with placeholders
for dynamic content like syllabus, batch data, etc.
"""

# =============================================================================
# Stage 2: Preprocessing Classification
# =============================================================================

STAGE2_SYSTEM_INSTRUCTION_TEMPLATE = """You are an expert classifier analyzing Discord messages from an online course about building AI applications.

Your task is to process each message and return structured classifications.

For each message, you must:
1. Create a concise simplified version (10-50 words) that captures the key information
2. Classify whether it's a genuine question (not an announcement, greeting, or statement)
3. Categorize it as Content, Logistics, or Other based on the course syllabus

COURSE SYLLABUS:
{syllabus}

CLASSIFICATION RULES:
=====================

**Question Detection:**
A message is a QUESTION if it seeks information, clarification, or help. Use your best judgment, but consider these general guidelines:
- Typically contains a question mark OR starts with interrogative words (what, why, how, when, where, which, who, can, could, would, should, is, are, do, does)
- Usually reasonably short (< 500 characters preferred)
- Generally NOT an announcement (e.g., "hey everyone", "@everyone", "all the materials", "please fill out", "here is", "here's what")
- Seeks information or assistance rather than making statements

Note: These are guidelines, not strict rules. Use context and judgment to determine the true intent of the message.

**Category Definitions:**

CONTENT - Technical course material questions about topics covered in the syllabus:
- LLM concepts, AI agents, prompting, testing & quality
- Model training, production deployment
- Frameworks, tools, and APIs
- Any technical aspects of building AI applications

LOGISTICS - Course access and operational questions:
- Platform access (credits, recordings, Zoom, GitHub, Codespaces)
- Course logistics (Discord channels, homework, deadlines, assignments)
- Account setup (API keys, authentication, organization membership)
- Course materials (Wiki, Slack, Notion, calendars, session schedules)
- Enrollment and invitations

OTHER - Everything else:
- General chit-chat, greetings, introductions, thank-yous
- Off-topic discussions
- Unclear or ambiguous messages
- Announcements and statements

IMPORTANT GUIDELINES:
- Be consistent with question detection
- Use the syllabus to inform CONTENT categorization
- When in doubt between CONTENT and LOGISTICS, consider if it relates to technical course topics (CONTENT) or course operations (LOGISTICS)
- Keep simplified versions concise but informative, but they must convey the original message's intent and content.
"""

STAGE2_USER_PROMPT_TEMPLATE = """Analyze the following {batch_size} Discord messages and return a JSON array with exactly {batch_size} objects.

INPUT MESSAGES:
{messages_json}

OUTPUT FORMAT:
Return a JSON array where each object has this exact structure:
{{
  "id": "message_id_from_input",
  "content_simplified": "concise 10-50 word simplified version",
  "is_question": true or false,
  "category": "Content" or "Logistics" or "Other",
  "reasoning": "brief 1-sentence explanation of classification"
}}

IMPORTANT INSTRUCTIONS FOR content_simplified:
- If the message is a QUESTION: Rewrite it as a clear, concise question (10-50 words)
  * Keep it in question form (not "Asks about X" but "What is X?")
  * Retain ALL important technical keywords and terms from the original
  * Simplify the wording but preserve technical accuracy
  * Example: "Should I use nested prompts or fine-tuning for long attribute-heavy database instructions?"
- If the message is NOT a question: Provide a brief summary (10-50 words)
  * Use statement form
  * Capture the key information or action

GENERAL REQUIREMENTS:
- Return ONLY valid JSON (no markdown, no explanations, no code blocks)
- Include ALL {batch_size} messages in the same order as input
- Use exact category names: "Content", "Logistics", or "Other"
- Be consistent with question detection rules from the instructions
- Each "id" must exactly match the input message ID
"""


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
- Deciding whether/which → generalize ("frameworks", "embedding models", "vector databases")
- Asking how to use something specific → keep the name ("Modal", "Braintrust", "ChromaDB")

GROUPING QUALITY CHECK:
Before finalizing, ask:
- Would a future student with this question find and recognize this FAQ entry?
- If questions share the same underlying decision or tradeoff, should they be one group even if they mention different specific tools?

COURSE TAXONOMY:
================
{taxonomy}

TAXONOMY MAPPING RULES:
=======================

**Workshop-Aligned Topics:**
- Match questions to the most specific subtopic in the taxonomy
- Use format: "Workshop N > Subtopic name" (e.g., "Workshop 3 > Judge prompt design")
- If a question spans multiple subtopics, choose the most relevant one

**Emergent Categories:**
- For questions that do not map cleanly to a Workshop subtopic (for example: setup, environment, or platform issues), use the Emergent Categories section
- Format: "Emergent: Category name" (e.g., "Emergent: Environment & Dependencies")

**Uncategorized:**
- If no taxonomy topic fits well, mark as "Emergent: Uncategorized"
- These should be rare - try to find a relevant topic first

JSON OUTPUT FORMAT:
===================

Return a JSON object with this exact structure:
{{
  "groups": [
    {{
      "canonical_id": "short-descriptive-slug",
      "canonical_question": "Clear, concise FAQ question?",
      "intent": "Category from above or brief custom label",
      "taxonomy_path": "Workshop N > Subtopic"
      "member_ids": ["id1", "id2"],
      "theme": "Brief 2-5 word description"
    }}
  ],
  "outliers": ["id7"]
}}

IMPORTANT:
- Return ONLY valid JSON (no markdown, no explanations)
- Every input question ID must appear in exactly one group OR in outliers
- Outliers: questions that aren't information-seeking (offers, polls, statements), or true singletons that don't fit any group
- Minimum 2 questions per group; move singletons to outliers
"""

STAGE4_USER_PROMPT_TEMPLATE = """Analyze the following cluster of {cluster_size} similar questions. Group them by intent following the rules in the system instruction.

QUESTIONS IN CLUSTER:
{questions_json}
"""

STAGE4_SINGLETON_PROMPT_TEMPLATE = """These {count} questions did not cluster semantically with others. However, some of them may still share the same INTENT and belong together in an FAQ group.

Your task:
1. FIRST: Apply the intent-based grouping rules to find any questions that share the same underlying intent (even if they use different words or topics)
2. THEN: Process remaining true singletons individually

Follow the same specificity guidance:
- Generalize if deciding whether/which to use something
- Keep specific names if asking how to use a particular tool

QUESTIONS TO ANALYZE:
{questions_json}

Return a JSON object with this structure:
{{
  "groups": [
    {{
      "canonical_id": "short-descriptive-slug",
      "canonical_question": "Clear, concise FAQ question?",
      "intent": "Category from above or brief custom label",
      "taxonomy_path": "Workshop N > Subtopic",
      "member_ids": ["id1", "id2"],
      "theme": "Brief 2-5 word description"
    }}
  ],
  "singletons": [
    {{
      "id": "original-question-id",
      "canonical_id": "unique-slug",
      "canonical_question": "Refined FAQ question?",
      "taxonomy_path": "Best matching taxonomy path or Emergent: Uncategorized",
      "theme": "Brief theme description"
    }}
  ]
}}

IMPORTANT:
- Return ONLY valid JSON (no markdown, no explanations)
- Groups must have at least 2 questions (minimum 2 member_ids)
- Try to find intent-based connections even if topics differ
- For true singletons, try to find a relevant taxonomy path
- Use "Emergent: Uncategorized" only as a last resort
- Keep questions clear and recognizable to future students
"""

