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
    },
    "drag_drop_classify": {
        "titles": [
            "Multi-agent design patterns",
            "Getting tested on tests",
            "Classifying AI model types", 
            "Database normalization levels",
            "Programming paradigms"
        ],
        "contexts": [
            """One of things you notice as you review your colleague's codebase is that they've built their own multi-agent collaboration framework, which includes a substantial amount of custom code.

You suggest that they adopt an establish design pattern, such as a **network**/swarm/decentralized or a **supervisor** architecture, so they can leverage pre-existing open-source libraries and improve the interpretability of the codebase.""",
            
            """As the lead engineer on a new AI-powered weather app, you've been working for months to build a reliable and accurate agentic system to handle queries about historical weather data and international weather forecasts.

Before putting this into production, you want to perform a series of tests to give you confidence that it can survive the choppy waters of a production environment.""",
            
            """You're working as a data scientist at a tech company and need to help train junior developers on different machine learning approaches. The team has been mixing up supervised, unsupervised, and reinforcement learning concepts.""",
            
            """As a database architect, you're mentoring a new developer who is struggling to understand when to apply different levels of database normalization in their schema design."""
        ],
        "instructions": [
            "Classify these statements as describing either a **supervisor** or a **network** multi-agent.",
            "Match the checks to the type of testing they belong to.",
            "Drag each technique into the correct machine learning category.",
            "Sort these database design principles into their appropriate normalization levels.",
            "Classify each programming concept into its corresponding paradigm."
        ],
        "hints": [
            "Recall that a supervisor multi-agent is like a manager at a company with worker agents underneath to delegate tasks to.",
            "Unit testing ensures that each component is working correctly. Integration testing ensures that each component is communicating and operating correctly. Performance testing focuses on how the system performs under different circumstances.",
            "In supervised learning, the algorithm learns from labeled training data with known correct outputs.",
            "Remember that higher normalization levels reduce redundancy but may require more complex queries.",
            "Think about whether the paradigm focuses on data transformation, object modeling, or explicit instructions."
        ]
    },
    "drag_drop_order": {
        "titles": [
            "API data flow",
            "Machine learning pipeline steps",
            "Software development lifecycle",
            "Data preprocessing workflow",
            "Model deployment process"
        ],
        "contexts": [
            """As you've seen, an Application Programming Interface (API) allows for communication between services. This allows your application to communicate data to and from the machine learning model.

![Application programming interface excluding information](https://assets.datacamp.com/production/repositories/6056/datasets/08241d8a27e23be51b22dc453edbbe72235c3d1e/microservice_communication.png)

In this exercise, you will order the steps in the data flow of an API request to a machine learning model.""",
            
            """You're leading a data science team that's building their first end-to-end machine learning pipeline. The junior engineers understand the individual components but are struggling with the correct sequence of steps.

As the technical lead, you need to help them understand the proper workflow for training and deploying a machine learning model.""",
            
            """Your startup is implementing agile development practices, and the new developer on your team is confused about the software development lifecycle. They understand what each phase involves but aren't sure about the proper order.

As a senior developer, you want to help them understand the sequential nature of software development."""
        ],
        "instructions": [
            "Order the sequence of an API request to a machine learning model.",
            "Arrange the machine learning pipeline steps in the correct order.",
            "Put the software development lifecycle phases in the proper sequence.",
            "Order the data preprocessing steps from raw data to model-ready data.",
            "Sequence the model deployment steps from training to production."
        ],
        "hints": [
            "First, new, unseen input data comes in, then the model makes a prediction, and returns the output through the API.",
            "Remember that data must be collected before it can be cleaned, and models must be trained before they can be evaluated.",
            "Planning comes before implementation, and testing comes before deployment.",
            "Raw data needs to be cleaned before feature engineering, and features must be selected before model training.",
            "Models must be trained and validated before they can be deployed to production environments."
        ]
    }
}
