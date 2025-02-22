import os
from dotenv import load_dotenv
from autogen import ConversableAgent

load_dotenv()

def migrator_agent(tree, content, fragmented_output_from_agent, human_expectations, human_guidelines):

    messages_for_migrator =  [

        {"role" : "system",
        "content" : ''' 
        
            You are an expert Code Migration Specialist with deep expertise in transforming legacy codebases into modern architectures. Your task is to analyze the fragmentation report and the entire legacy codebase and generate a fully migrated version of the code based on provided report.
            
            
            Inputs Given to You: 
            
            
            1. Fragmentation Report:
            - A structured breakdown of the legacy codebase into functional features.
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
            - For each feature listed in the fragmentation report, generate its fully migrated equivalent.
            - Ensure the new code:
            - Uses the modern tech stack and adheres to best practices.
            - Preserves business logic while improving performance and security.
            - Refactors outdated code structures to enhance readability and maintainability.
            - Ensures compatibility with the new database, API structures, and dependencies.
            
            
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

    migrated_output_from_agent = migrator_agent.generate_reply(messages= messages_for_migrator)
    return migrated_output_from_agent