import google.generativeai as palm
from neo4j import GraphDatabase
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# URI = "neo4j+s://21769e3d.databases.neo4j.io"
# AUTH = ("neo4j", "sNLsVe6joJjNuRTNjOZRCoVJRSeNAMmAT1zr4-fiA_g")
URI = "neo4j+ssc://21769e3d.databases.neo4j.io"
AUTH = ("neo4j", "sNLsVe6joJjNuRTNjOZRCoVJRSeNAMmAT1zr4-fiA_g")
driver = GraphDatabase.driver(URI, auth=AUTH)

palm.configure(api_key="AIzaSyAM66Voz__ZZo43m-6pThWp1IeFcasF1vo")

def get_answer(input):
    defaults = {
        'model': 'models/text-bison-001',
        'temperature': 0.8,
        'candidate_count': 1,
        'top_k': 40,
        'top_p': 0.95,
        'max_output_tokens': 1024,
        'stop_sequences': [],
        'safety_settings': [
            {"category": "HARM_CATEGORY_DEROGATORY", "threshold": 1},
            {"category": "HARM_CATEGORY_TOXICITY", "threshold": 1},
            {"category": "HARM_CATEGORY_VIOLENCE", "threshold": 2},
            {"category": "HARM_CATEGORY_SEXUAL", "threshold": 2},
            {"category": "HARM_CATEGORY_MEDICAL", "threshold": 2},
            {"category": "HARM_CATEGORY_DANGEROUS", "threshold": 2}
        ],
    }

    prompt = f"""You are an expert in converting English questions to Neo4j Cypher Graph code! The Graph has following Node Labels - USER,PROJECT,TASK,TASK_STATUS and the properties according to each label as follows,

Generate a Cypher query to match the following nodes and relations:
Nodes:

USER: Represents user nodes in the graph. Properties include 'user_id' and 'username'.
PROJECT: Represents project nodes in the graph. Properties include 'project_id' and 'project_name'.
TASK: Represents task nodes in the graph. Properties include 'id', 'month_id', 'task_date', 'message', 'hours', 'created_at', and 'updated_at'.
TASK_STATUS: Represents task status nodes in the graph. Properties include 'status_id' and 'status_name'.
Relations:

works_on: Represents the relationship between a user (from) and a project (to). The label for this relationship is 'works_on'.
belongs_to: Represents the relationship between a task (from) and a project (to). The label for this relationship is 'belongs_to'.
created: Represents the relationship between a task (from) and a user (to). The label for this relationship is 'created'.
has: Represents the relationship between a task (from) and a task status (to). The label for this relationship is 'has'.
    For example,
    Example 1 - Get Count of all the projects updated on 2023-08-06?
    , the Cypher command will be something like this
    MATCH (u:USER )-[:works_on]->(p:PROJECT)
    MATCH (t:TASK)-[h:has]->(ts:TASK_STATUS)
    WHERE t.updated_at ="2023-08-06"
    RETURN COUNT(p) AS numberOfProjects

    Example 2 - get projects done by both Lakshmi and Ramadurgam?, the Cypher command will be something like this
    MATCH (l:USER)-[:works_on]->(project:PROJECT)
    WHERE l.username = 'Lakshmi'
    WITH collect(DISTINCT project) as projects_lakshmi
    MATCH (r:USER)-[:works_on]->(project:PROJECT)
    WHERE r.username = 'Ramadurgam' AND project IN projects_lakshmi
    RETURN project.project_name

    Example 3-Get the total projects done in 2023-08-06?, the Cypher command will be something like this
    MATCH (u:USER )-[:works_on]->(p:PROJECT)
    MATCH (t:TASK)-[h:has]->(ts:TASK_STATUS)
    WHERE t.updated_at ="2023-08-06"
    RETURN COUNT(p) AS numberOfProjects

    Example 4-Get the sum of total hours that a user worked on RH QMS project along with statuses?, the Cypher command will be something like this
    MATCH (u:USER)-[:works_on]->(p:PROJECT{{project_name:"RH QMS"}})
    MATCH (t:TASK)-[h:has]->(ts:TASK_STATUS)
    RETURN DISTINCT u.username as user, p.project_name, ts.status_name, SUM(t.hours) as totalhours

    Example 5-Get the count of projects that are created after 2023-08-06?, the Cypher command will be something like this
    MATCH (u:USER )-[:works_on]->(p:PROJECT)
    MATCH (t:TASK)-[h:has]->(ts:TASK_STATUS)
    WHERE t.created_at>="2023-08-06 "
    RETURN COUNT(p) AS numberOfProjects
       Example 6- list out the total hours spent by each user on each project?, the Cypher command will be something like this
    MATCH (t:TASK)-[:created]->(u:USER)-[:works_on]->(p:PROJECT)
    RETURN u.username,p.project_name,SUM(t.hours)

    Example 7-List out the users and also total hours spent on project RH QMS and in development status?, the Cypher command will be something like this
    MATCH (u:USER)-[:works_on]->(p:PROJECT{{project_name:"RH QMS"}})
    MATCH (t:TASK)-[h:has]->(ts:TASK_STATUS{{status_name:"Development"}})
    RETURN DISTINCT u.username as user,SUM(t.hours) as totalhours

    example 8-when did Nursing Portal project started?, the Cypher command will be something like this
    MATCH (project:PROJECT {{project_name: 'Nursing Portal'}})<-[:belongs_to]-(task:TASK)
    WITH MIN(task.task_date) AS project_start_date
    RETURN project_start_date
    Dont include ``` in the output 
    {input}
    """

    response = palm.generate_text(**defaults, prompt=prompt)
    response_text = response.result.replace("\n", "")
    return response_text



import streamlit as st

# Function to execute Cypher query and get results from Neo4j
def execute_cypher_query(query):
    with driver.session() as session:
        result = session.run(query)
        return result.data()

# st.title("Aurora Chat 🕊️")

# # User input
# user_question = st.text_input("Ask a question:")

import streamlit as st
import pandas as pd
import plotly.express as px

# ... (previous imports and code) ...

# if st.button("Generate"):
#     # Generate Cypher query based on user question
#     cypher_query = get_answer(user_question)

#     # Execute Cypher query and get results from Neo4j
#     results = execute_cypher_query(cypher_query)

#     # Display generated Cypher query
#     st.write("Generated Cypher Query:")
#     st.code(cypher_query)

#     # Display query results as table
#     st.write("Query Results :")
#     if results:
#         df = pd.DataFrame(results)
#         st.write(df)

#         numerical_column = None
#         if len(df.columns) > 1:
#             numerical_column = df.select_dtypes(include='number').columns[0]

#         if numerical_column:

#             fig_bar = px.bar(df, x=df.columns[0], y=numerical_column, labels={'x': df.columns[0], 'y': numerical_column})
#             # Pie Chart
#             fig_bar

#             fig_scatter = px.scatter(df, x=df.columns[0], y=numerical_column, labels={'x': df.columns[0], 'y': numerical_column})
#             fig_scatter
#             fig_pie = px.pie(df, names=df.columns[0], values=numerical_column, title=f"{numerical_column} by {df.columns[0]}", 
#                              hole=0 )
#             fig_pie.update_traces(textinfo='percent+label')
#             fig_pie

#             fig_line = px.line(df, x=df.columns[0], y=numerical_column, labels={'x': df.columns[0], 'y': numerical_column})
#             fig_line


#         else:
#             st.write("Insufficient data for visualization.")
#     else:
#         st.write("No results found.")





st.title('Aurora Chat 🕊️')
user_question = st.text_input("Enter your question:")
# Create tabs
tab1, tab2 = st.tabs(["Data", "Graphs"])

# Generate Cypher query based on user question

cypher_query = get_answer(user_question)

# Execute Cypher query and get results from Neo4j
results = execute_cypher_query(cypher_query)

# Display generated Cypher query
tab1.write("Generated Cypher Query:")
tab1.code(cypher_query)

# Display query results as table
if results:
  df = pd.DataFrame(results)
  tab1.write("Query Results :")
  tab1.write(df)

  # Display graphs on tab2
  if len(df.columns) > 1:
    numerical_column = df.select_dtypes(include='number').columns[0]

    if numerical_column:

      # Bar chart
      fig_bar = px.bar(df, x=df.columns[0], y=numerical_column, labels={'x': df.columns[0], 'y': numerical_column})
      tab2.plotly_chart(fig_bar)

      # Scatter plot
      fig_scatter = px.scatter(df, x=df.columns[0], y=numerical_column, labels={'x': df.columns[0], 'y': numerical_column})
      tab2.plotly_chart(fig_scatter)

      # Pie chart
      fig_pie = px.pie(df, names=df.columns[0], values=numerical_column, title=f"{numerical_column} by {df.columns[0]}",
                      hole=0 )
      fig_pie.update_traces(textinfo='percent+label')
      tab2.plotly_chart(fig_pie)

      # Line chart
      fig_line = px.line(df, x=df.columns[0], y=numerical_column, labels={'x': df.columns[0], 'y': numerical_column})
      tab2.plotly_chart(fig_line)

  else:
    tab2.write("Insufficient data for visualization.")
else:
  tab1.write("No results found.")





