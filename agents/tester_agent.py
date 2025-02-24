
# tester code 
from autogen import ConversableAgent
from autogen.coding import LocalCommandLineCodeExecutor
import tempfile
temp_dir = tempfile.TemporaryDirectory()

def tester_agent(migrated_code_output):

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

            Migrated Code: {migrated_code_output}

    '''
    },

    ]

    tester_output = testing_agent.generate_reply(messages= messages_for_tester)

    return tester_output
