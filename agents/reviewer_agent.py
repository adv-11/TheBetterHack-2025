import os
from dotenv import load_dotenv
from autogen import ConversableAgent
from docx import Document
from docx.shared import Pt

load_dotenv()

def reviewer_agent(tree, content, human_expectations, human_guidelines):

    # Legacy Code Reviewer Agent
    reviewer_agent = ConversableAgent(
        "chatbot",
        llm_config={"config_list": [{"model": "o1-mini", "api_key": os.environ.get("OPENAI_API_KEY")}]},
        human_input_mode="NEVER",  # No manual intervention
    )

    # Constructing Structured Prompts as Separate Messages
    messages = [
        {
            "role": "user",
            "content": f"""
            You are an AI *Legacy Code Reviewer* with expertise in *code analysis and migration planning*. 
            Your task is to review a legacy project and generate a structured *migration strategy* using AI agents, not human intervention.

            You will receive:
            1. *Project Directory Structure*
            2. *Full Codebase Dump*
            3. *Human-defined Expectations and Guidelines*

            Expectations: {human_expectations}
            Guidelines: {human_guidelines}

            Your task is divided into five key sections.
            """
        },
        {
            "role": "user",
            "content": f"""
            *1. Project Overview & Code Review*
            - Analyze the project structure and architecture.
            - Identify languages, frameworks, and dependencies.
            - Detect deprecated technologies, security risks, and technical debt.

            *Project Structure:*
            {tree}

            *Codebase Content:*
            {content}
            """
        },
        {
            "role": "user",
            "content": """
            *2. Feasibility Analysis & Metrics*
            - Calculate code complexity (Cyclomatic Complexity, Maintainability Index).
            - Evaluate coupling, cohesion, redundancy, and duplication.
            - Identify dependency risks, outdated libraries, and compatibility issues.
            - Assess database migration complexity.
            - Analyze external service & API dependencies.
            - Review test coverage and identify gaps.
            """
        },
        {
            "role": "user",
            "content": """
            *3. Migration Strategy Proposal*
            - Define an AI-driven *step-by-step migration strategy*.
            - Choose the best migration approach (Refactor, Rewrite, Rehost, Re-platform).
            - Recommend modern tech stacks.
            - Define a *phased migration plan* (priorities, risk mitigation, automation strategies).
            - Suggest *AI-based automation tools* for efficiency.
            """
        },
        {
            "role": "user",
            "content": """
            *4. Potential Challenges & Risk Mitigation*
            - Identify key roadblocks that AI migration agents might face.
            - Propose AI-driven solutions for risk mitigation.
            - Highlight any areas requiring *manual intervention* (if unavoidable).
            """
        },
        {
            "role": "user",
            "content": """
            *5. Estimated Effort & Resources*
            - Estimate the time, cost, and AI agent workload for migration.
            - Define AI agent roles: Fragmentor, Migrator, Reviewer, Executor, and Documentor.
            - Specify expertise required to fine-tune the migration process.
            """
        }
    ]

    # Generate AI-driven Migration Strategy
    migration_strategy_from_agent = reviewer_agent.generate_reply(messages=messages)
    return migration_strategy_from_agent

'''
print("\n----- GENERATED MIGRATION STRATEGY -----\n")
#print(migration_strategy_from_agent)

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
    # Here, you can use feedback to refine the prompts and regenerate.

'''
