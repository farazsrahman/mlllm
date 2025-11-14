"""
llm_agent.py — LLM-powered experiment suggestion (placeholder)

This module should handle:
- Processing natural language experiment requests
- Calling OpenAI API to generate run configurations
- Parsing LLM responses into structured configs
- Suggesting hyperparameter ranges based on user intent
- Learning from past runs to improve suggestions

Backend Implementation Steps:
1. Set up OpenAI API client with proper error handling
2. Design prompt templates for config generation
3. Implement response parsing to extract hyperparameters
4. Add validation to ensure configs are valid
5. Optional: Integrate with storage to learn from past runs
6. Optional: Use few-shot examples for better suggestions

Example Interface:
    agent = LLMAgent(openai_api_key)
    configs = agent.propose_configs("Test learning rates 0.001 to 0.0001")
    # Returns: [{"lr": 0.001, ...}, {"lr": 0.0005, ...}, {"lr": 0.0001, ...}]

Environment Variables Needed:
- OPENAI_API_KEY

This file is intentionally left incomplete for backend teammates to implement.
"""

# TODO: Implement LLMAgent class
# TODO: Add OpenAI API integration
# TODO: Design and test prompt templates
# TODO: Implement config parsing and validation
# TODO: Add error handling for API failures
# TODO: Optional: Add learning from historical runs
