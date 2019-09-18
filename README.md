# Parking Rate Service
A service to store and search for parking rates

 #### Setup
 In a python 3.6+ virtual environment:
 
```$ pip install -r requirements.txt```
 
 #### Run
 
 Ensure `PYTHONPATH` env var is set to the root directory of the repo

 From root directory of repo,

```$ python app/main.py --config config.local.json```

Intial parking rates are loaded from `files/rates.json` upon startup.

 #### Test with Coverage Report
 Ensure `PYTHONPATH` env var is set to the root directory of the repo
 
 ```$ ./run_tests.sh``` or ```$ pytest --cov=app tests/```
 
 
 ## API Usage
 
 ### Rates - `/api/v1/rates`
 
 #### GET 
 Request the price to park during a specified time period
 - Start and end times must be on the same date
 - If parking is not available for the specified time period, the request will not return a result
 - If two different rates exist for the specified time period, the request will not return a result as one cannot be determined
    -   Shifting or narrowing the time range may help find a rate 
 
 Query Params:
 - `start_timestamp`
    - ISO-8601 with timezone, e.g. `2015-07-04T10:00:00+00:00`
 - `end_timestamp`
    - ISO-8601 with timezone, e.g. `2015-07-04T12:00:00+00:00`
 
 Example Request:
 ```GET /api/v1/rates?start_timestamp=2015-07-04T10:00:00%2B00:00&end_timestamp=2015-07-04T20:00:00%2B00:00```
 
 Remember to URL-encode `+` as `%2B` if your HTTP client does not handle this for you
 
 #### POST
 Replace the stored parking rates with a new set of rates
 
 Currently no business-logic validation is done on the rates. It is up to the user to submit rates with accurate time periods and prices.
 POST will fail atomically if any invalid or incorrectly-formatted data is supplied.
 
 JSON Rate objects:
 - `days`: `string`
    - comma-separated list of lowercase weekday abbreviations, e.g. `"mon,tues,wed,thurs,fri,sat,sun"`
 - `times`: `string`
    - time range expressed in the format `hhmm-hhmm`, e.g. `"0900-2100"`
 - `tz`: `string`
    - timezone name from the [international standard tz database](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones), e.g. `"America/Chicago"`
 - `price`: `integer`
    - rate for parking during the specified time period 
 
 See `files/rates.json`, `tests/stubs/rates/initial_rates.json`, or `tests/stubs/rates/POST.json` for examples of a full POST body
 
 
 
 ### Extra Credit & Further Work
 I did not proceed with extra credit in the interest of time, as I have several other coding projects and technical interviews ongoing at once.
 
 If I were to develop further on this application, my top priorities would likely be:
 - Write tests specifically for the `RateRepo`
    - Endpoint handler tests currently cover this by calling RateRepo functionality, but having more specific test allow for quicker understanding of where & how a change causes breakage
 - Write tests to ensure any timezone conversion logic corner cases are being handled
 - Add more helpful responses about the reason for a rate request returning `Unavailable`
  
 
 
 
 
