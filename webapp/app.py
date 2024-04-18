import os
from flask import Flask, render_template, request, jsonify
from typing import List
from google.api_core.client_options import ClientOptions
from google.cloud import discoveryengine_v1 as discoveryengine
from typing import Optional
from typing import Any
from utils import *
from google.cloud import storage
from dotenv import load_dotenv
load_dotenv()

PROJECT_ID= os.environ["project_id"]
LOCATION = os.environ["location"]
ENGINE_ID= os.environ["engine_id"]
DATA_STORE_ID = os.environ["data_store_id"]
BUCKET_NAME = os.environ["bucket_name"]


app = Flask(__name__)

def search_sample(
    project_id: str,
    location: str,
    engine_id: str,
    search_query: str,
) -> discoveryengine.SearchResponse:
    client_options = (
        ClientOptions(api_endpoint=f"{location}-discoveryengine.googleapis.com")
        if location != LOCATION
        else None
    )

    client = discoveryengine.SearchServiceClient(client_options=client_options)

    serving_config = f"projects/{project_id}/locations/{location}/collections/default_collection/engines/{engine_id}/servingConfigs/default_config"

    content_search_spec = discoveryengine.SearchRequest.ContentSearchSpec(
        snippet_spec=discoveryengine.SearchRequest.ContentSearchSpec.SnippetSpec(
            return_snippet=True
        ),
        summary_spec=discoveryengine.SearchRequest.ContentSearchSpec.SummarySpec(
            summary_result_count=5,
            include_citations=True,
            ignore_adversarial_query=True,
            ignore_non_summary_seeking_query=True,
            model_prompt_spec=discoveryengine.SearchRequest.ContentSearchSpec.SummarySpec.ModelPromptSpec(
                preamble="Given the conversation between a user and a helpful assistant and some search results, create a final answer for the assistant. The answer should use all relevant information from the search results, not introduce any additional information, and use exactly the same words as the search results when possible. The assistant's answer should be no more than 20 sentences. The user is an expert who has an in-depth understanding of the subject matter. The assistant should answer in a technical manner that uses specialized knowledge and terminology when it helps answer the query."
            ),
            model_spec=discoveryengine.SearchRequest.ContentSearchSpec.SummarySpec.ModelSpec(
                version="preview",
            ),
        ),
    )

    request = discoveryengine.SearchRequest(
        serving_config=serving_config,
        query=search_query,
        page_size=10,
        content_search_spec=content_search_spec,
        query_expansion_spec=discoveryengine.SearchRequest.QueryExpansionSpec(
            condition=discoveryengine.SearchRequest.QueryExpansionSpec.Condition.AUTO,
        ),
        spell_correction_spec=discoveryengine.SearchRequest.SpellCorrectionSpec(
            mode=discoveryengine.SearchRequest.SpellCorrectionSpec.Mode.AUTO
        ),
    )

    response = client.search(request)
    return response

@app.route('/')
def index():
    return render_template('index.html', summary=None, query="")

@app.route('/search', methods=['POST'])
def search():
    
    project_id = PROJECT_ID
    location = LOCATION  # Values: LOCATION, "us", "eu"
    engine_id = ENGINE_ID
    search_query = request.form['query']

    result = search_sample(project_id, location, engine_id, search_query)

    summary = result.summary.summary_with_metadata.summary

    summary_text = result.summary.summary_text
    citations = [f"[{i + 1}] {ref.title}" for i, ref in enumerate(result.summary.summary_with_metadata.references)]

    return render_template('index.html', summary=summary ,summary_text=summary_text, citations=citations, query=search_query)

@app.route('/purge_documents', methods=['POST'])
def purge_documents():
    # Call your purge function here
    project_id = PROJECT_ID
    location = LOCATION         
    data_store_id = DATA_STORE_ID
    branch = "default_branch"
    response = purge_all_documents_sample(project_id, location, data_store_id, branch)
    # Extract the purge count from the response
    purge_count = response
    return str(purge_count)  # Return purge count as text

@app.route('/list_documents', methods=['POST'])
def list_documents():
    project_id = PROJECT_ID
    location = LOCATION         
    data_store_id = DATA_STORE_ID
    document_uris = list_documents_sample(project_id, location, data_store_id)
    document_uris = [f"Listed documents counts : {len(document_uris)}"] + document_uris
    return jsonify(document_uris)

@app.route('/import_documents', methods=['POST'])
def import_docs():
    project_id = PROJECT_ID
    location = LOCATION
    data_store_id = DATA_STORE_ID
    # Extracting the gcs_uris from the POST request
    gcs_uris = request.json.get('gcs_uris', [])
    result = import_documents(project_id, location, data_store_id, gcs_uris)
    return jsonify(result)

@app.route('/upload', methods=['POST'])
def upload():
    # Get the bucket name and files from the request
    bucket_name = BUCKET_NAME 
    files = request.files.getlist('files')

    # Save the files to a temporary directory
    temp_dir = 'books'  # Or any other temporary directory
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    filenames = []
    for file in files:
        filename = os.path.join(temp_dir, file.filename)
        file.save(filename)
        filenames.append(filename)
    print(filenames)

    # Upload the files to the specified bucket
    upload_many_blobs_with_transfer_manager(bucket_name, filenames)

    return 'Files uploaded successfully GCS bucket!'

@app.route('/list_documents_gcs', methods=['POST'])
def list_blobs():
    project_id = PROJECT_ID
    bucket_name = project_id
    document_uris = list_blobs_bucket(bucket_name)
    document_uris = [f"Total documents counts in bucket : {len(document_uris)}"] + document_uris
    return jsonify(document_uris)



if __name__ == '__main__':
    app.run(debug=True)
