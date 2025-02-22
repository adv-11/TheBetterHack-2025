import os
from dotenv import load_dotenv
from autogen import ConversableAgent
from repo_to_text import repo_to_text

load_dotenv()

# Inputs
summary, tree, content = repo_to_text()

# Human Input
human_expectations = input('Please provide your expectations from the code migration: ')
human_guidelines = input('Please provide the guidelines that the Agent needs to follow while migrating: ')

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

print(migration_strategy_from_agent)

