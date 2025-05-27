
import json
from google.oauth2 import service_account
from google import genai
import os
# from vertexai.preview.generative_models import GenerativeModel, Part
from google.genai.types import (
ApiKeyConfig,
AuthConfig,
EnterpriseWebSearch,
GenerateContentConfig,
GenerateContentResponse,
GoogleMaps,
GoogleSearch,
LatLng,
Part,
Retrieval,
RetrievalConfig,
Tool,
ToolConfig,
VertexAISearch,
)

def get_analysis_markdown(response): 
  content=response['candidates'][0]['content']['parts']
  text=''
  print(len(content))
  for i in range(0, len(content)):
    text=text+content[i]['text']
  return text

def get_url_mapping(response):
  id=0
  grounding_sources=[]
  links={}
  uri_titles={}
  for i in response['candidates'][0]['grounding_metadata']['grounding_chunks']:
    links.update({id: i['web']['uri']})
    uri_titles.update({i['web']['uri']: i['web']['title']})
    id+=1
  # print(grounding_sources)
  print(links)
  print(uri_titles)
  return links, uri_titles

def get_claimwise_supports(response):
  detailed_claims=[]
  
  for i in response['candidates'][0]['grounding_metadata']['grounding_supports']:
    text=i['segment']['text']
    if '**Claim' in text:
      
      supports=[]
      for source_id in range(0,len(i['grounding_chunk_indices'])):
        supports.append({"source_id":i['grounding_chunk_indices'][source_id], "confidence": i['confidence_scores'][source_id]})
      print(text)
      print(supports)
      detailed_claims.append({"text":text, "supports":supports})
  return detailed_claims

# import vertexai


def get_fact_check_vertex(text):


  # Replace with your Google Cloud Project ID and desired region
  PROJECT_ID = "serious-house-459306-b1"
  LOCATION = "us-central1"
  MODEL_ID = "gemini-2.0-flash" # Or your desired region, e.g., "europe-west4"

  # Path to your service account key JSON file
  
  PROMPT = f"""You are a highly analytical and neutral fact-checking AI. Your primary goal is to verify the accuracy of the given text by performing thorough research using the Google Search tool and then providing a concise, evidence-based assessment.

Here's the process you must follow:

1.  **Analyze the Input:** Carefully read and understand the user's input text. Identify all factual claims, statistics, names, dates, events, or any other verifiable pieces of information.

2.  **Formulate Search Queries:** For each identified factual claim, generate highly specific and targeted Google Search queries. Aim for queries that are likely to lead to reliable sources (e.g., academic institutions, reputable news organizations, government agencies, scientific journals, established fact-checking websites). Prioritize queries that are neutral and avoid leading language.

    * **Example Query Strategy:**
        * For a claim like "The average global temperature increased by 2 degrees Celsius in the last decade," generate queries like:
            * `"average global temperature increase last decade"`
            * `"climate change temperature rise 2010-2020"`
            * `"IPCC report global temperature trends"`
        * For a claim about a specific event, like "XYZ company announced a new product on [date]," generate queries like:
            * `"XYZ company new product announcement [date]"`
            * `"XYZ company press release [new product name]"`

3.  **Execute Google Searches:** Use the generated queries to perform searches via the Google Search tool.

4.  **Evaluate Search Results & Extract Evidence:** Review the search results critically. Prioritize information from:
    * Official government websites (e.g., .gov, .org, .edu for specific research)
    * Reputable news organizations with a track record of accuracy (e.g., Associated Press, Reuters, BBC, The New York Times, The Wall Street Journal, recognized national news outlets)
    * Academic studies and peer-reviewed journals
    * Established fact-checking organizations (e.g., Snopes, PolitiFact, FactCheck.org)
    * Direct sources (e.g., company press releases on their official website for company-specific claims).

    Synthesize the information from multiple reliable sources to build a comprehensive understanding of each claim's veracity.

5.  **Formulate Fact-Check Assessment:** Based on the gathered evidence, provide a clear and concise assessment for each factual claim. Use one of the following labels:

    * **TRUE:** The claim is supported by strong, verifiable evidence from multiple reliable sources.
    * **MOSTLY TRUE:** The claim is largely accurate, but there might be minor inaccuracies, nuances, or missing context. Explain these caveats.
    * **PARTIALLY TRUE:** The claim contains a mix of accurate and inaccurate information, or it's presented in a misleading way. Explain which parts are true and which are not.
    * **FALSE:** The claim is contradicted by strong, verifiable evidence from multiple reliable sources.
    * **MISLEADING:** The claim might contain elements of truth but is presented in a way that intends to deceive or misinform, often by omitting crucial context.
    * **UNVERIFIED/LACKING EVIDENCE:** There is insufficient reliable evidence to either confirm or refute the claim. Explain why evidence is lacking.

6.  **Provide Supporting Evidence (Citations):** For each assessment, briefly explain *why* you assigned that label and cite the key pieces of evidence from your Google searches. Include the source (e.g., "According to the National Oceanic and Atmospheric Administration (NOAA)," "As reported by Reuters," "A study published in Nature journal states..."). Do not provide URLs directly in the final output, but use the information from the search results to explain your reasoning.

7.  **Overall Summary:** Conclude with a brief overall summary of the fact-check for the entire input text, highlighting the most significant findings.

**User Input Text:**
{text}
"""
  try:
    credentials_ = service_account.Credentials.from_service_account_file(
        '/etc/secrets/creds.json'
        ,scopes=["https://www.googleapis.com/auth/cloud-platform"]
    )
    
    client = genai.Client(vertexai=True, project=PROJECT_ID, location=LOCATION, credentials=credentials_)
    google_search_tool = Tool(google_search=GoogleSearch())


    response = client.models.generate_content(
        model=MODEL_ID,
        contents=PROMPT,
        config=GenerateContentConfig(tools=[google_search_tool]),
    )
    with open('rawResponse.json', 'w') as f:
        json.dump(response.to_json_dict(), f)
    return response.to_json_dict()
  except FileNotFoundError:
      print(f"Error: Service account key file not found.")
      raise
  except Exception as e:
      print(f"An error occurred: {e}")
      raise
