"""
Agent Modules for Video Generation Pipeline
Each agent handles one responsibility in the pipeline.

Phase 1: ScriptGenerationAgent (script_generation_agent.py)
Phase 2: SEOMetadataAgent
Phase 3: TTSAgent + ImageGenerationAgent
Phase 4: VideoAssemblyAgent
"""

from .script_generation_agent import generate_script, save_script_to_file

__all__ = [
    "generate_script",
    "save_script_to_file",
]
