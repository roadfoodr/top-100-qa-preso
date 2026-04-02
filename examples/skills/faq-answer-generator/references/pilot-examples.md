# Pilot Examples

Two calibrated examples from the approved pilot batch. Use these as style references.

## Example 1 (coverage: strong, with named quote)

### Q8: What is the difference between system and user prompts, and when should I use each?

**coverage:** strong
**sources:** Prompt_Engineering_in_the_LLM_SDLC.md, 2_wiki.md

System prompts set persistent behavior; user prompts handle specific interactions. Both are internally merged by most models, but separating them is still best practice for clarity and maintainability.

**Put in system prompts:**
- Guardrails and safety constraints (medical disclaimers, prohibited language)
- Style guides, brand voice, tone requirements
- Broad rules that apply across the entire conversation

**Put in user prompts:**
- Specific task instructions and context for the current request
- Dynamic content like retrieved documents or user data

For heavily regulated applications, some teams put exact scripts word-for-word in system prompts to ensure compliance. One workshop example showed adding a system prompt that forced explicit disclaimers before health advice, which transformed a generic response into a properly cautious one.

**Important caveat:** Different models treat the system/user hierarchy differently. OpenAI, Anthropic, and Google all handle system prompt authority slightly differently. Always test your specific implementation rather than assuming behavior will transfer across providers.

## Example 2 (coverage: partial, supplemented with general knowledge)

### Q12: How should I use personas and demographic data in prompt engineering?

**coverage:** partial
**sources:** 2_wiki.md, Top10.md

Role prompting — assigning the model a persona — is effective for enforcing consistent voice, style, and domain expertise. A workshop exercise using Mario and Yoda personas demonstrated how role definition plus conversation history produces reliably distinct character behavior. This technique generalizes to practical applications: brand voice enforcement, domain-expert simulation, and user-facing chatbot personality.

**When personas help:**
- Keeping tone consistent across a conversation (e.g., "You are a friendly but precise customer support agent")
- Constraining the model to domain-appropriate language and expertise level
- Simulating specific professional perspectives for content generation

**When to be cautious with demographic data:**
- Models can exhibit stereotypical behavior when given demographic attributes. Test thoroughly for bias.
- Simulating specific real people raises ethical and accuracy concerns.
- For personalization, it's generally safer to provide behavioral preferences ("respond at a technical level suitable for a senior engineer") rather than demographic labels.

The structured prompting framework treats role as just one component alongside instructions, output constraints, context, and guardrails. Define the persona clearly, but don't expect it to carry the whole prompt — the other components matter at least as much.
