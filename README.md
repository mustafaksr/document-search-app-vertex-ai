
# Search and Conversation App a.k.a Agent Builder

This repository contains code for a search and conversation web application powered by Vertex AI's search and conversation features. Basically app, upload unstruced documents to GCS, store, list, delete documents and search in single page for specific usage. 

## Pre-requisites

Before running the application, ensure you have the following:

- **Google Cloud Platform Account:** You need a GCP account with billing enabled.
- **Python:** Ensure you have Python installed on your system.
- **Google Cloud SDK:** Install the Google Cloud SDK for managing your GCP resources.
- **Environment Variables:** You'll need to set up environment variables for your project ID, location, engine ID, and data store ID. These should be placed in a `.env` file in the root directory of the project. See the provided `.env.example` file for reference.
- **Search and Conversation App:** You'll need to create search and conversation app manually. Explained detailed how to create app in Setup steps 0.
- **Create a Google Cloud Storage Bucket:** You'll need to create Google Cloud Storage Bucket.

## Setup

0. **Create Google Cloud Storage Bucket:** Create a gcs bucket for search and conversation app.

    ```bash
    gsutil mb gs://"your-bucket-name"
    ```

1. **Create Search and Conversation App:** 

        1. Go to Agent Builder from google cloud console.
        2. Pick Search app
        3. Give a name your app and your company name (company name can be as "null" for example).
        4. Leave rest default and Click Continue.
        5. Click Create Data Store and Select Cloud Storage and pick your folder location, leave data type as unstructred.
        6. İf you have permission problem with selecting bucket folder, give Storage Legacy Object Reader permission to Viewers of project: "Your Project" from cloud storage permissions and then try select again folder.
        7. Give name your data store after selecting folder.
        8. Check your data store and Click create your app is ready.
        9. Note your data store id and app engine id to your .env file.


2. **Clone the Repository:** Clone this repository to your local machine.

    ```bash
    git clone https://github.com/mustafaksr/document-search-app-vertex-ai.git
    ```

3. **Install Dependencies:** Navigate to the project directory and install the Python dependencies.

    ```bash
    cd document-search-app-vertex-ai
    pip install -r requirements.txt
    ```
    
4. **Set Up Environment Variables:** Create a `.env` file in the root directory and populate it with your GCP project ID, location, engine ID, and data store ID.

    ```plaintext
    export project_id='your-project-id'
    export location='your-location'  
    export engine_id='your-engine-id'
    export data_store_id='your-data-store-id'
    export bucket_name='your-bucket-name'
    ```

5. **Run the Application:** Start the Flask web server.

    ```bash
    python webapp/app.py
    ```

    

6. **Access the Web App:** Open a web browser and navigate to `http://localhost:5000` to access the search and conversation app. Using Front-end, Add document GCS then store it data store and start search within documents using search widget.



## File Structure

The repository has the following structure:

- `.env`: Configuration file for environment variables.
- `README.md`: Instructions and documentation.
- `webapp/`: Directory containing the web application code.
    - `app.py`: Flask application script.
    - `templates/`: HTML templates for the web pages.
    - `utils.py`: Utility functions for interacting with Google Cloud services.

## Usage

- **Upload Documents:** Use the provided form to upload documents to a Google Cloud Storage bucket.
- **List Documents:** View the list of documents in the Google Cloud Storage bucket.
- **Add Documents:** Add documents by providing their GCS URIs.
- **Search:** Enter a search query to retrieve relevant information from the uploaded documents.
- **Purge Documents:** Remove all documents from the data store.



## License

This project is licensed under the [Apache License](LICENSE).

