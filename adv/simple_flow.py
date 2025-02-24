from autogen import ConversableAgent     # agentic ai framework by microsoft

from gitingest import ingest   # library to fetch data from a github repo

import os 
from dotenv import load_dotenv
load_dotenv()


# step 1 get repo deets

repo_url = 'https://github.com/adv-11/RAG_from_scratch'

summary, tree, content = ingest(repo_url)      # ingest function to parse the repo


# check if repo is being fetched successfully 

print ('Summary: ',  summary )
print ('Tree: ',  tree )
print ('Contents: ', content )


# step 2 : agent creation

agent = ConversableAgent(

        "chatbot",                    # name

        llm_config={"config_list": [{"model": "gpt-4", "api_key": os.environ.get("OPENAI_API_KEY")}]},       
        
        # config -> (model name and api key)

        
    )


# step 3: send the agent a msg

# note -> follows a dict structure 

prompt = 'You are a summary agent, your task is to parse contents of a repository and summarise what the code base is doing. Be concise, limit your answer to a few sentences'


# this is the exact format of  the dict you need to strictly follow 
messages  =[
{
'role': 'system', 
'content' : prompt, 

'role' : 'user', 
'content': content

}

]


#step 4 get agent reply 


reply = agent.generate_reply(messages=messages)

print (reply)


