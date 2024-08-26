from azure.storage.blob import BlobServiceClient
from io import BytesIO
from langchain_experimental.agents.agent_toolkits import create_csv_agent
from langchain_openai import ChatOpenAI
import os
import pandas as pd
import re
from flask import Flask, request
# from pyngrok import ngrok

# Set your OpenAI API Key
# os.environ["OPENAI_API_KEY"] = "sk-ePEcgDG72z4phj13x8kyoK-mkqnRFvr8DHAmwgMFnvT3BlbkFJbJRtDVhV14wq_tkZ1GcXdjATXh-Gz-HHY2-69YsLYA"

# Azure Storage account details
# storage_account_name = 'eipocstorageaccount'
# storage_account_key = 'aO3kERXNDK27DHalRQ1o7QAo4uBXiYlx6T7eKBA13Qbv8uL7jSjVWJJJn8/98A04CpYynnUf6Ndy+AStfmANtA=='
# container_name = 'eipocstogragecontainer'
# blob_name = 'Data Set Sample.csv'

app = Flask(__name__)

# port_no = 8000

# ngrok.set_auth_token('2l3RJV2ej50XCIEljjjgUpDwEaQ_6Jd1KWPTk4Ee4zaUCP3D7')
# public_url = ngrok.connect(port_no).public_url

@app.route("/customer_details", methods=["POST"])
def cust():
    # Inputs from boomi - Question
    questions = request.form['Ques']
 
    
    # Create a BlobServiceClient and download the CSV
    blob_service_client = BlobServiceClient(account_url=f"https://{storage_account_name}.blob.core.windows.net", credential=storage_account_key)
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
    stream = BytesIO(blob_client.download_blob().readall())

    # Read the CSV file from the blob into a Pandas DataFrame
    df = pd.read_csv(stream)

    # Convert the DataFrame to CSV format (in memory)
    csv_data = df.to_csv(index=False)
    
    '''
    # Create the language model with OpenAI
    llm = ChatOpenAI(temperature=0.5)

    # Create the CSV agent using the in-memory CSV data
    agent_executer = create_csv_agent(llm, BytesIO(csv_data.encode()), verbose=True, allow_dangerous_code=True)

    # Invoke the agent with your query
    outcome = agent_executer.invoke(questions)
    '''
    return csv_data

if __name__ == "__main__":
    # print(f'Public URL is : {public_url}')
    app.run(debug=True,host="0.0.0.0", port=8000)
