
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
os.environ["GOOGLE_CREDENTIALS_JSON"] = {"type":"service_account","project_id":"serious-house-459306-b1","private_key_id":"73176ff4df57ee490e93b9131efd98fa1524270b","private_key":"-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDp/p63kn22cH6+\nKHpEIxKk6g2AP87Iee6FZ2vXiZo7hSYngae1okQvdU6sj8Sfv9+0mRaHUzVUPnlA\nDdOS6mReyWCfMwhWDOIKFeIDH67UKPJN+EItufJ0eWCc2Qh2ql0mgb2EfwJsPTRq\n7VYJSDmSMDYOcGV7Dzq+in21ek/uwQCVFmdP/eNZGdu21oZpSxhsGFde/vCulHhV\niRIvmu6/5ANoMUTIJLNoTCYjqGSXtvUZSOJ8+2WhJegHv+N0ZP6k3puXTIcmBsJo\n+h8oMTlN27I4xPgekdIgOSKU0P1/E7xtCevvkdyvAyNBGOMg/6Nej1E1zX4fJ4h0\nPXaY3uRFAgMBAAECggEAOvGuD7YyPsv10Xcm3ZUsNCjVf9ITCANXJ3nW+7OpC4dO\nBjOuCJ44qO/XArcwo8FU3AyYVTyLuY4HQzB4dJDg+dOmqFPVrL+QDVRX28uWYdFy\nwFtiaFxoDBkrUjeF30apMnMKR58rABMm6iyhOLNd9Up5w4diuO4sMSV350hJbG3s\no4O5rJ88hAnkc96k8dfFD5MQSnlm9J6x0bj3x+sEvPNiK0f15T9uhSEL4qbbgDoe\n7Bsnz2icxOed5GCx1lDZhcwDegaKMJOdARd+H9KfZPMleD3yNUypTa+54MpBJetx\n3mkFTVTwDU1YHpp5YYENXMwA4jVK99D6gfba+5gNfQKBgQD3lO004rVu6Eo3YZ7S\nHaLL82MKYLGfbwGV0O8q6Gl6CmebfyyUA4FI1r70iCxDu+LfMu8Zi5Ub8uSXmiuL\n8Ej9ZSNryf3NGSWF3p5KLwpBQgDTcElG+IsZlDOBbdwJro5DC6ZwJW0blvvQMcwU\nG6mk3bytPXVlxPxlKiv6AwHQAwKBgQDx82yd/c6KAZc8iOZf4pKvEr/wwE+fB5Gr\nIxkwqFSJkN9uBmrAuKWHXw2O1pmyfwrSZUmM/D9o5zSKMMi8UyzVB4LYvy5AnZdi\ndXqf92tdlzx6dt1wb2/cx9yi9V1IStQ4bNWSHSG1gbNZYyaploisDnSNBFP7rbwi\ny0OyulG8FwKBgQCaGgBrYpE7rypCvmh0sC2cdKm40+a7LgT2k03Kj07Xv5Itn0LH\n/kaCZ+gDnJ6wqknUU4evhsoQ02alVji0qaNE1abueJOZDYXlhWNRGWZwp/yLnuB9\nZEZwbWaBsTe8bwHtiVrXgvQesCOcuuIjwfQdwkamLhLcfXf8H/uvah++sQKBgHJu\nguymYcz7u5+xz+OBsYaEA6vGCOJaHhcm3n8Y3gLCNio/drX3nrJLzonEDaVSWLfx\nl7vKgeMHlt3U/Nu1KvsGNmh041dEMZkrnveReYImSUBSf6Dx06JEFKIuEhRi78RQ\nFSKqDItf8IdSUbLbs4BMxer8JQxfux9pq3cYkBe5AoGBANAo0R8R3Xg1eQrLgQle\nnypcOYOXtPWrFaukmyKY+ZLBXoP1cSJ6RHkjhGsKlydJ0IhF3DSxHLYmeXw8yCDy\nNYMFzBu2L8WEBP/bNYmm03ZpA2E3fLPN/tT6lOB4TrgTBgCa7wNenCv03Gt+NUc5\nQFyLtZmB8/8fsnJrTNykVA8T\n-----END PRIVATE KEY-----\n","client_email":"lakshya-vpa@serious-house-459306-b1.iam.gserviceaccount.com","client_id":"113134046570424498678","auth_uri":"https://accounts.google.com/o/oauth2/auth","token_uri":"https://oauth2.googleapis.com/token","auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs","client_x509_cert_url":"https://www.googleapis.com/robot/v1/metadata/x509/lakshya-vpa%40serious-house-459306-b1.iam.gserviceaccount.com","universe_domain":"googleapis.com"}
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

    
    credentials_json = os.getenv("GOOGLE_CREDENTIALS_JSON")
    if credentials_json:
        credentials_info = json.loads(credentials_json)
        credentials = service_account.Credentials.from_service_account_info(credentials_info, scopes=["https://www.googleapis.com/auth/cloud-platform"])
    else:
        raise Exception("Missing GOOGLE_CREDENTIALS_JSON environment variable")

    
    client = genai.Client(vertexai=True, project=PROJECT_ID, location=LOCATION, credentials=credentials)
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
