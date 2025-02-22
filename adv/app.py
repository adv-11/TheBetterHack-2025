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

# Constructing Structured Prompts
messages = [
    {"role": "user", "content": "You are an AI Legacy Code Reviewer... (same as before)"},
    {"role": "user", "content": f"**1. Project Overview & Code Review**\n\n{tree}\n\n{content}"},
    {"role": "user", "content": "**2. Feasibility Analysis & Metrics** ..."},
    {"role": "user", "content": "**3. Migration Strategy Proposal** ..."},
    {"role": "user", "content": "**4. Potential Challenges & Risk Mitigation** ..."},
    {"role": "user", "content": "**5. Estimated Effort & Resources** ..."}
]

# Generate AI-driven Migration Strategy
migration_strategy_from_agent = reviewer_agent.generate_reply(messages=messages)

# Display the generated strategy
print("\n----- GENERATED MIGRATION STRATEGY -----\n")
print(migration_strategy_from_agent)

# Approval Logic: True (Approve) / False (Reject)
approval = input("\nDo you approve this migration strategy? (yes/no): ").strip().lower()

if approval in ['yes', 'y']:
    print("\n✅ Migration strategy approved. Proceeding with execution...")
    migration_approved = True
else:
    print("\n❌ Migration strategy rejected. Gathering feedback...")
    migration_approved = False
    feedback = input("Please provide feedback on what needs improvement: ")
    
    # Log feedback or modify prompts based on rejection reason
    print("\n🔄 Regenerating strategy based on feedback...")
    # Here, you can use `feedback` to refine the prompts and regenerate.






