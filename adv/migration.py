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

# validation logic 



fragmentor_agent = ConversableAgent(
    "chatbot",
    llm_config={"config_list": [{"model": "o1-mini", "api_key": os.environ.get("OPENAI_API_KEY")}]},
    human_input_mode="NEVER",  # No manual intervention
)


messages_for_fragmentor  =  [

    {"role" : "system", 
     "content" : ''' 

You are an expert Code Fragmentation and Migration Specialist with deep expertise in analyzing, modularizing, and transforming legacy codebases into structured, modern architectures. Your task is to analyze the given migration strategy and full codebase and generate a structured fragmentation and migration report.

---

Inputs Given to You:

1. Migration Strategy:
- A step-by-step migration strategy outlining how the project should be transformed.

2. Complete Codebase (Before Migration):
- Full source code of the existing legacy system.
- Project directory structure, including all files, modules, and dependencies.


Your Expected Output:

1. Comprehensive Feature-Based Fragmentation Report:
- Analyze the provided legacy codebase and break it down into logical feature-based fragments.
- Identify total features in the system and categorize them by functionality, dependencies, and purpose.
- Clearly define each feature's role in the system and the files associated with it.
- Segment dependencies, services, and business logic while ensuring minimal coupling.
- Ensure each module can be independently migrated and tested.



'''
     },

    {"role": "user", 
     "content" : f'''

        Migration Strategy: {migration_strategy_from_agent}
'''
     },

    {"role": "user", 
     "content" : f'''
        Code Structure: {tree}
        Code base : {content}
'''},


]



fragmented_output_from_agent = fragmentor_agent.generate_reply(messages= messages_for_fragmentor)


messages_for_migrator =  [

    {"role" : "system", 
     "content" : ''' 

You are an expert Code Migration Specialist with deep expertise in transforming legacy codebases into modern architectures. Your task is to analyze the *fragmentation report* and the *entire legacy codebase* and generate a *fully migrated version of the code* based on provided report.


Inputs Given to You: 


1. *Fragmentation Report:*
- A structured breakdown of the legacy codebase into *functional features*.
- Each feature's functionality, dependencies, and files associated with it.
- Detailed Feature Definitions.
- The mapping of old files to their modern equivalents feature wise.

2. Complete Codebase (Before Migration):
- Full source code of the existing legacy system.
- Project directory structure, including all files, modules, and dependencies.

3. Human Expectations

4. Human Guidelines

Your Expected Output:

1. Provide Migrated Code for Each Feature**
- *For each feature listed in the fragmentation report, generate its fully migrated equivalent*.
- Ensure the new code:
  - *Uses the modern tech stack and adheres to best practices.*
  - *Preserves business logic while improving performance and security.*
  - *Refactors outdated code structures to enhance readability and maintainability.*
  - *Ensures compatibility with the new database, API structures, and dependencies.*


'''
     },

 {"role": "user", 
     "content" : f'''

        Fragmentation Report: 
{fragmented_output_from_agent}


Human Expectations: 
{human_expectations}

Human Guidelines: 
{human_guidelines}

'''
     },



    {"role": "user", 
     "content" : f'''
        Code Structure: {tree}
        Code base : {content}
'''},


]

migrator_agent = ConversableAgent(
    "chatbot",
    llm_config={"config_list": [{"model": "gpt-4o", "api_key": os.environ.get("OPENAI_API_KEY")}]},
    human_input_mode="NEVER",  # No manual intervention
)



migrated_code_output = migrator_agent.generate_reply(messages= messages_for_migrator)


# tester code 
from autogen.coding import LocalCommandLineCodeExecutor
import tempfile
temp_dir = tempfile.TemporaryDirectory()


executor = LocalCommandLineCodeExecutor(
    timeout=10,  # Timeout for each code execution in seconds.
    work_dir=temp_dir.name,  # Use the temporary directory to store the code files.
)


testing_agent = ConversableAgent(
    "testing",
    llm_config=False,  # Turn off LLM for this agent.
    code_execution_config={"executor": executor},  # Use the local command line code executor.
    human_input_mode="ALWAYS",  # Always take human input for this agent for safety.
)


# msg
messages_for_tester =  [

    {"role" : "system", 
     "content" : ''' 

You are an expert Code Testing and Execution Specialist with deep expertise in validating modernized codebases. You are given access to the local command-line executor. Your task is to analyze the *migrated code*, compile and execute it using a local command-line executor, and report its execution status.

---

## Inputs Given to You:**

### 1. *Migrated Code from the Migrator Agent*
- Fully transformed source code that was migrated from a legacy system.
- Updated dependencies, database queries, and API structures.



---

## Your Expected Output:**

### *1. Compile and Execute the Migrated Code*
- *Use the local command-line executor* to attempt *compiling and running the migrated code*.
- Capture and report:
  - *Successful execution* (if the code runs without errors).
  - *Compilation errors* (if any, specify file names and exact error messages).
  - *Partial success* (list parts of the system that executed successfully and those that failed).
  


'''
     },

 {"role": "user", 
     "content" : f'''

        Migrated Code: 
{migrated_code_output}


'''
},

]

tester_output = testing_agent.generate_reply(messages= messages_for_tester)
