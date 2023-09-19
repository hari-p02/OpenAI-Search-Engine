# UConn Data Science Club: Creating a Semantic Search Engine w/ the OpenAI API

Hey! This repo contains the files necessary for the first workshop of the club, which is centered around creating a search engine for all of UConn's clubs.

## Setting up

Several files are present in this repo. Firstly, make sure to clone the repo:

`git clone https://github.com/hari-p02/OpenAI-Search-Engine.git`

Then, ensure that you have the required libraries installed:

`pip install -r requirements.txt`

This command installs the necessary frameworks and libraries for this project.

## OpenAI & PineconeDB API Key

To run this project, you will need two API keys:

### OpenAI API Key:

1. Visit [platform.openai.com](platform.openai.com).
2. Log in using your OpenAI account (create one if you haven't already).
3. Click on your profile (top right).
4. Navigate to "Manage Account".
5. Click on the "API Keys" tab.
6. Choose "Create New Secret Key".

Once you've created the key, save it as you'll use it later.

### PineconeDB:

We're using Pinecone as the vector database to store all our embeddings (from `text-embedding-ada-002`).

1. Sign up for a free account at [https://www.pinecone.io/](https://www.pinecone.io/).

   - Note: A free account gives you only one pod with a single index, but this is sufficient for this project.

2. After logging in, ensure you create an index if you haven't already.
3. Navigate to the "API Keys" tab on the left, and save both your key AND environment. For instance, my environment is `asia-southeast1-gcp-free`.

## Creating a .env file

In your local repo, create a file named `.env` and insert the following lines:

```
OPENAI_API_KEY=''
PINECONE_API_KEY=''
```

Within the empty quotation marks, make sure to insert your respective keys.

## Storing Embeddings

I've already generated the embeddings for the UConn clubs. If you'd like to use these, create a new file (name it as you prefer, e.g., `upsert.py`) and include the following:

```python
import numpy as np
import pandas as pd
import pinecone
import itertools
from dotenv import load_dotenv
import os

load_dotenv()

pinecone.init(
    api_key=os.getenv("PINECONE_API_KEY"), environment="asia-southeast1-gcp-free"
)  # Modify the environment parameter as per yours

index = pinecone.Index("your-index-name")  # Replace with your index name

allclubsembds = np.load("./allclubsembds.npy")

df = pd.read_csv("./UCONN_CLUB_INFO.csv")

vecs = []
for i in range(len(df)):
    mtdta = dict()
    if isinstance(df.loc[i]["Club Long Descriptions"], str):
        mtdta["Club Long Description"] = df.loc[i]["Club Long Descriptions"]
    else:
        mtdta["Club Long Description"] = ""
    mtdta["Club Short Description"] = df.loc[i]["Club Short Descriptions"]
    mtdta["Club Name"] = df.loc[i]["Club Names"]
    vecs.append((df.loc[i]["Club Urls"], allclubsembds[i], mtdta))

def chunks(iterable, batch_size=100):
    it = iter(iterable)
    chunk = tuple(itertools.islice(it, batch_size))
    while chunk:
        yield chunk
        chunk = tuple(itertools.islice(it, batch_size))

for ids_vectors_chunk in chunks(vecs, batch_size=100):
    index.upsert(vectors=ids_vectors_chunk, namespace="uconn-clubs")
```

Ensure you replace placeholders with appropriate values (like the environment and index name). Then, execute the file:

`python upsert.py`

Afterwards, initiate the following command:

`streamlit run ./app.py`

This command launches the web UI, allowing you to start your searches!
