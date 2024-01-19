import requests
import json
import configparser
# import related models here
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 \
import Features, SentimentOptions
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, **kwargs):
    response = None

    api_key = kwargs.get("api_key")
    print("GET from {} ".format(url))
    try:
        # Call get method of the requests library with URL and parameters
        if api_key:
            params = dict()
            params["text"] = kwargs["text"]
            params["version"] = kwargs["version"]
            params["features"] = kwargs["features"]
            params["return_analyzed_text"] = kwargs["return_analyzed_text"]
            response = requests.get(url, params=kwargs, headers={'Content-Type': 'application/json'},
                                    auth=HTTPBasicAuth('apikey', api_key))
        else:
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
    except Exception as e:
        # If any error occurs
        print(f"Network exception occurred: {e}")

    status_code = response.status_code
    print("With status {} ".format(status_code))

    try:
        json_data = json.loads(response.text)
    except json.JSONDecodeError:
        # Handle the case where the response text is not valid JSON
        print("Error decoding JSON: Response is not valid JSON")
        json_data = None

    return json_data


# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, json_payload, **kwargs):
    print(kwargs)
    print("POST to {} ".format(url))
    #try:
    response = requests.post(url, json=json_payload, params=kwargs)
    #except:
       # print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, **kwargs)
    if json_result:
        # Ensure that the response is a list
        if isinstance(json_result, list):
            # For each dealer object
            for dealer in json_result:
                if isinstance(dealer, dict):  # Ensure each dealer is a dictionary
                    # Create a CarDealer object with values in `dealer` dictionary
                    dealer_obj = CarDealer(
                        address=dealer.get("address", ""),
                        city=dealer.get("city", ""),
                        full_name=dealer.get("full_name", ""),
                        id=dealer.get("id", ""),
                        lat=dealer.get("lat", ""),
                        long=dealer.get("long", ""),
                        short_name=dealer.get("short_name", ""),
                        st=dealer.get("st", ""),
                        zip=dealer.get("zip", "")
                    )
                    results.append(dealer_obj)
                else:
                    print("Invalid dealer format: {}".format(dealer))
        else:
            print("Invalid response format: {}".format(json_result))

    return results
# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_dealer_reviews_from_cf(url, **kwargs):
    results = []
    json_result = get_request(url, id=kwargs['id'])
    if(json_result):
        dealer_reviews = json_result;
        for dealer_review in dealer_reviews:
            sentiment = analyze_review_sentiments(dealer_review['review'])
            dealer_review_obj = DealerReview(dealership=dealer_review['dealership'], name=dealer_review['name'],
                                    purchase=dealer_review['purchase'], review=dealer_review['review'], purchase_date=dealer_review['purchase_date'],
                                    car_make=dealer_review['car_make'], car_model=dealer_review['car_model'], car_year=dealer_review['car_year'],
                                    id=dealer_review['id'], sentiment=sentiment)
            results.append(dealer_review_obj)
    return results

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative

def analyze_review_sentiments(dealerreview):
    url = "https://api.eu-gb.natural-language-understanding.watson.cloud.ibm.com/instances/8562c122-7fa1-40a2-95d4-9f131666d1b5"
    api_key = "EwOvapliOuOFdh-7DsfQxF65pSM_Vkvj34NnYjNASbg5"
    # params = dict()
    # params["text"] = dealerreview,
    # params["version"] = "2022-04-07"
    # params["features"] = ["sentiment"]
    # params["return_analyzed_text"] = False
    #response = get_request(url, api_key, params=params)

    authenticator = IAMAuthenticator(api_key)
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version='2022-04-07',
        authenticator=authenticator
    )

    natural_language_understanding.set_service_url(url)

    try:
        response = natural_language_understanding.analyze(
            text = dealerreview,
            features=Features(sentiment=SentimentOptions())).get_result()
    except:
        return 0
    print(response)
    return response['sentiment']['document']['score']

