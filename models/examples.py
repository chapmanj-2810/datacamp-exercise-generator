# Add this to your existing EXERCISE_EXAMPLES dictionary in models/examples.py

    "coding": {
        "titles": [
            "Embedding more detailed descriptions",
            "Building your first agent function",
            "Implementing vector similarity search",
            "Creating a custom evaluation metric",
            "Processing agent responses"
        ],
        "contexts": [
            """One of the last predicted labels didn't seem representative of the review; this was probably down to the lack of information being captured when we're only embedding the class labels. This time, descriptions of each class will be embedded instead, so the model better "understands" that you're classifying restaurant reviews.

The following objects are available for you to use:

```
sentiments = [{'label': 'Positive',
               'description': 'A positive restaurant review'},
              {'label': 'Neutral',  
               'description':'A neutral restaurant review'},
              {'label': 'Negative',
               'description': 'A negative restaurant review'}]

reviews = ["The food was delicious!",
           "The service was a bit slow but the food was good", 
           "The food was cold, really disappointing!"]
```""",
            
            """You've learned about the key components of an AI agent system, and now it's time to implement your first agent function. This function will serve as the core decision-making component that processes user inputs and determines the appropriate response.

The agent function needs to handle different types of queries and route them to the correct tools or provide direct responses when appropriate.""",
            
            """Now that you understand how vector embeddings work, let's implement a similarity search function. This is a core component in many AI applications, from recommendation systems to semantic search engines.

You'll be working with a dataset of movie descriptions that have already been converted to embeddings using a pre-trained model."""
        ],
        "instructions": [
            "Extract a list containing the sentiment descriptions and embed them.",
            "Complete the agent function to handle user queries and return appropriate responses.",
            "Implement the similarity search function to find the most relevant movies.",
            "Create a function that calculates custom evaluation metrics for the model.",
            "Parse the agent's response and extract the relevant information."
        ],
        "hints": [
            "Use a list comprehension to extract the 'description' key from each dictionary in sentiments.",
            "Remember to handle different query types using conditional statements.",
            "The cosine similarity function is available in the scipy.spatial.distance module.",
            "Consider using numpy functions for efficient array operations.",
            "Regular expressions might be helpful for parsing structured text responses."
        ],
        "code_patterns": [
            "List comprehensions for data extraction: [item['key'] for item in collection]",
            "Function definitions with multiple parameters and return values",
            "Conditional logic for handling different input types",
            "Loop structures for processing collections of data",
            "Dictionary and list manipulation for data processing"
        ]
    }
