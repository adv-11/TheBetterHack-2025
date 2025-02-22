import os
from dotenv import load_dotenv
from autogen import ConversableAgent

load_dotenv()

# Inputs
tree = ''
content = ''

# Human Input
human_expectations = input('Please provide your expectations from the code migration: ')
human_guidelines = input('Please provide the guidelines that the Agent needs to follow while migrating: ')

# Legacy Code Reviewer Agent
reviewer_agent = ConversableAgent(
    "chatbot",
    llm_config={"config_list": [{"model": "o3-mini", "api_key": os.environ.get("OPENAI_API_KEY")}]},
    human_input_mode="NEVER",  # No manual intervention
)

# Constructing Structured Prompts as Separate Messages
messages = [
    {
        "role": "user",
        "content": f"""
        You are an AI **Legacy Code Reviewer** with expertise in **code analysis and migration planning**. 
        Your task is to review a legacy project and generate a structured **migration strategy** using AI agents.

        Expectations: {human_expectations}
        Guidelines: {human_guidelines}
        """
    },
    {
        "role": "user",
        "content": f"""
        **1. Project Overview & Code Review**
        {tree}
        {content}
        """
    },
    {
        "role": "user",
        "content": """ **2. Feasibility Analysis & Metrics** (Complexity, Dependencies, Testing Coverage) """
    },
    {
        "role": "user",
        "content": """ **3. Migration Strategy Proposal** (Refactor, Rewrite, Tools, Phased Approach) """
    },
    {
        "role": "user",
        "content": """ **4. Potential Challenges & Risk Mitigation** """
    },
    {
        "role": "user",
        "content": """ **5. Estimated Effort & Resources** (Time, Cost, AI Agent Roles) """
    }
]

# Generate Migration Strategy
migration_strategy = reviewer_agent.generate_reply(messages=messages)

# Display Migration Strategy
print("\n--- Generated Migration Strategy ---\n")
print(migration_strategy)

# Approval Logic
approval = input("\nDo you approve this migration strategy? (yes/no): ").strip().lower()

if approval == "yes":
    print("\n✅ Migration strategy approved! Proceeding with the next steps...")
    # Call the next AI agent (Fragmentor, Migrator, etc.)
elif approval == "no":
    feedback = input("\n❌ Migration strategy rejected! Please provide feedback on improvements: ")
    print("\n🔄 Refining the migration strategy based on your feedback...")
    # Optionally, send feedback to improve next prompt iteration
else:
    print("\n⚠️ Invalid input! Please enter 'yes' or 'no'.")
