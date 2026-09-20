# Phase 1: Script Generation Agent - Implementation Guide

## Overview

Phase 1 implements the **Core Agent Orchestration** layer with a focus on learning Claude API tool use and basic agent loops. This phase generates YouTube video scripts from topics using Claude API.

## Architecture

```
User Input (CLI)
    ↓
Topic Validation (Pydantic)
    ↓
Claude API Script Generation Agent
    ↓
Quality Validation
    ↓
Output to File (script.txt + metadata.json)
```

## Key Files

- **`scripts/cli.py`** - CLI entry point (generate, validate commands)
- **`src/agents/script_generation_agent.py`** - Core agent with Claude API integration
- **`src/models.py`** - Data validation (Script, TopicInput, SEOMetadata)
- **`src/config.py`** - Configuration and environment setup

## Setup & Installation

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment
```bash
# Copy the example and fill in your API keys
cp config/.env.example config/.env

# Edit config/.env with:
export ANTHROPIC_API_KEY="your_anthropic_key_here"
export OPENAI_API_KEY="your_openai_key_here"
```

### 3. Verify Setup
```bash
python scripts/cli.py --help
```

## Usage

### Generate a Script

**Interactive Mode (Recommended for Learning):**
```bash
python scripts/cli.py generate
```
Then enter your topic when prompted:
```
Topic: How to make small talk at parties
Additional context (optional): Focus on greeting strategies
```

**Command Line Mode:**
```bash
python scripts/cli.py generate --topic "How to apologize politely" --context "Professional workplace"
```

### Validate an Existing Script
```bash
python scripts/cli.py validate --script-path outputs/how_to_apologize/script.txt
```

## Learning Objectives - Phase 1

### 1. Claude API Tool Use
- Understand how to call Claude API with system prompts
- Learn multi-turn conversation patterns
- Work with prompt engineering for consistent output

### 2. Agent State Management
- Parse and validate agent output
- Store results in structured formats (JSON/TXT)
- Handle errors gracefully

### 3. Data Validation
- Use Pydantic for input validation
- Validate script quality criteria
- Provide clear error messages

## Output Structure

Each script generation creates a folder like:

```
outputs/
└── how_to_apologize/
    ├── script.txt              # Full dialogue (Sarah + Alex)
    └── script_metadata.json    # Statistics and metadata
```

### Example Script Output

```
Sarah : Imagine this. Your boss asks you to work on Sunday. Your friend asks you for a big favor. Your client wants something impossible.
Alex : Oh wow. That is hard. I always feel nervous when I say no.
Sarah : Me too. But today, we learn how to say no politely in English.
Alex : I really need this lesson.
...
```

### Metadata Example

```json
{
  "topic": "How to apologize politely",
  "word_count": 1750,
  "estimated_duration_minutes": 13.5,
  "line_count": 145,
  "generated_at": "2024-01-15T10:30:00.123456"
}
```

## Script Quality Criteria

The agent validates scripts against these criteria:

✅ Word count: 1500-2000 words  
✅ Estimated duration: 10-15 minutes  
✅ YouTube search demand: Popular keywords  
✅ Beginner-friendly: Simple English  
✅ Has opening hook: Engaging first line  
✅ Both characters present: Sarah (teacher) + Alex (learner)  
✅ Has CTA: Like, Comment, Subscribe  
✅ Evergreen content: Timeless value  

## Implementation Notes

### Prompt Engineering
The agent uses a system prompt that includes:
- Role definition (expert English teacher)
- Output format requirements (dialogue structure)
- Quality criteria checklist
- Example script for reference

### Dialogue Format
Scripts follow this format:
```
Sarah : Teacher dialogue here
Alex : Learner dialogue here
Sarah : Can include reactions like (laughs), (smiles), (thinks for a moment)
```

### Validation Strategy
Post-generation validation includes:
- Word count range check
- Speaker consistency check
- Hook and CTA detection via heuristics
- Character presence validation

## Troubleshooting

### "ANTHROPIC_API_KEY not set"
```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

### "Word count too low"
The prompt may have generated a shorter script. You can:
- Rerun with more specific context
- Check if the topic naturally has less content
- Review output and manually expand if needed

### API Rate Limiting
If you hit rate limits:
- Wait a few seconds before retrying
- Check your API quota at https://console.anthropic.com
- Consider batching scripts with delays

## What Happens Next?

After Phase 1 is working smoothly, Phase 2 adds:

1. **SEO Metadata Agent** - Generate title, description, hashtags, tags
2. **Multi-Agent Coordination** - Run agents in parallel
3. **File-based Handoffs** - Pass data between agents via JSON
4. **Enhanced Error Handling** - Retry logic and logging

## Testing Phase 1

Try generating scripts for different topics:

1. **Easy (evergreen):**
   ```
   Topic: How to greet someone in English
   ```

2. **Medium (teaching):**
   ```
   Topic: Common mistakes English learners make
   ```

3. **Hard (specific):**
   ```
   Topic: Interview tips for non-native speakers
   Context: Focus on body language and confidence
   ```

Observe how the agent adapts to different topics while maintaining the Sarah-Alex dialogue format.

## Next Steps

1. ✅ **Phase 1 (You are here):** Script generation working
2. 🔜 **Phase 2:** Add SEO metadata agent (run after script generation)
3. 🔜 **Phase 3:** Add TTS agent (Google Studio, separate voices)
4. 🔜 **Phase 4:** Add image generation (thumbnails + video scenes)
5. 🔜 **Phase 5:** Add video assembly (FFmpeg combines audio + image)

## Resources

- **Claude API Docs:** https://docs.anthropic.com
- **Script Examples:** `references/examples/Script- Say No Politely.txt`
- **Prompts:** `references/prompts/Script Writer-prompt.txt`
- **Plan:** `docs/PLAN.md` or `../.claude/plans/i-want-you-to-lively-gadget.md`
