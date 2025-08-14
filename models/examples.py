"""
Centralized examples for exercise generation and validation.
"""

# Exercise examples organized by type
EXERCISE_EXAMPLES = {
    "single_mcq": {
        "titles": [
            "To agent or not to agent",
            "Agentic applications", 
            "Enforcing the pillars of scalable design"
        ],
        "contexts": [
            """A new tech start-up called _AutoMate_ has hired you as an outside AI consultant on their new AI automation product, which uses an agentic system. The product manager hands you these design specifications for your initial review:

```
🚨Top-Secret Automation🚨

🗒️ High-Level Plan
1. ✅ Write a single agent to handle all aspects of the automation.
2. ✅ Collaborate with the infrastructure team to develop a smart solution for scaling compute and storage.
3. ✅ Implement robust evaluation for each component.
4. ✅ Design smart user feedback loops.
```""",
            "One of the key breakthroughs in scalable agentic systems is the development of standard protocols like the Model Context Protocol (MCP)."
        ],
        "questions": [
            "Which pillar of scalable agentic design needs improvements here?",
            "Which of the following accurately describes MCP?"
        ],
        "hints": [
            "Remember the analogy from the video of a universal travel adaptor? Instead of connecting devices to an electrical power source, however, MCP connects AI systems with data sources.",
            "Continuous evaluation and feedback loops relates to the need for logging and tracking on all major components and processes.",
            "Robust infrastructure and tooling in the context of AI agents, relates to scalable storage and compute resources, reliable deployment pipelines, and using established agent frameworks and methodologies.",
            "Modularity in application development requires different components to be written separately, so they can be independently written and maintained."
        ]
    },
    "multiple_mcq": {
        "titles": [
            "Making the leap from single to multi-agents",
            "Designing collaborative agent systems",
            "Multi-agent coordination patterns"
        ],
        "contexts": [
            """You're an experienced Staff Engineer that's been brought in to mentor a Junior AI Engineer. This colleague has built an AI agent that looks impressive in demos, but reviewing the codebase, you think there are improvements to be made.

You think their single agent system could be _refactored_ as a multi-agent system.""",
            """A fintech company is building an AI system to handle customer support, fraud detection, and transaction processing. The current single-agent approach is becoming unwieldy as the system grows in complexity."""
        ],
        "questions": [
            "Which of the following are benefits of a multi-agent design over single agents?",
            "What are the key advantages of using multiple specialized agents instead of one generalist agent?"
        ],
        "hints": [
            "Single agents can struggle to manage a large number of tools, especially if the tools are different but similar.",
            "Think about how specialization can improve both performance and maintainability in complex systems."
        ]
    }
}
