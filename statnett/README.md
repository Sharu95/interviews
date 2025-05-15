# Description of this document
This markdown file documents assumptions, thoughts, future work and everything related to this case interview with Statnett.

## Summary of case
### Requirements
* Application reading data from API in real time
* Application generates a 5-minute average every minute (moving average)
* Moving average is input to ML model

### Constraints / Flexibility
* Free to decide fields to process
    * Make it simple for case, but document the production use-case
* Free to decide how results are presented
    * Make it simple for case, but document the production use-case

### Recruiter intention with case
* Emphasis on how problem is solved
* 2-4 hours max
* Document things (solutions/ideas/future work) if not sufficient time

## Proposals and discussion
There are multiple ways to do this, all depending on the use case. My understanding of the task, is to develop a ingestion pipeline for an ML model. Depending on deployment and architecture, we can do this in 2 ways that I can think of;

1) Develop a batch job, trigger every minute, read 5 minutes of data, compute and store average. Any downstream processor can then read the updated data or trigger/act on the newly written data.
    * Solution is straightforward, and is very transactional. Might be computationally (and potentially financially) expensive. You process a lot of the same data every minute. If the API is not free, this is even more expensive (it isn't now, but might be).
2) Develop a running application (e.g streaming)
    * The optimal solution is a running application, doing some caching/buffering and some tricks to maintain a moving average window. If you want to reduce computational cost and memory footprint, you can rather cache the cumulative sum and infer the average from that (and number of data points). The result can be returned as an API response-json, or posted to some queue-based system that is consumed by the ML model (however it is deployed)

**I will go for proposal 2**. This assumes that the raw data is ingested/fetched into the application runtime at some point. In production environments it might be a queue system, or a batch job sending data to the application in the form of an API interaction, or simply what I want to go for here, a function that is polled every minute. 

## Considerations, assumptions and choices
* Having a polling function in this case might include a separate thread running on the side. I will keep it simple and not handle thread failures, or add any form for thread pooling to handle such cases, but this might be realistic to handle in a production environment.
* Simple exception handling is added, but I do not check all cases and be granular on HTTP response codes. 
* If we work with very high-resolution data, caching the window is a memory and processing cost (what I chose to do for now). In this case, having a cumulative sum/running average might reduce the memory footprint.
* I have only selected 1 field, but storing all data so its easier to work with during the interview. The code should be dynamic enough to average on other fields, or add changes to average multiple fields or have multiple sliding window averages.
* To begin with, I just fetch all data every minute. I am fully aware of the fact that the same data is fetched over and over with the current code, and the more optimal solution would be to fetch the latest data point, and append it to the queue. However, because we still do a request over the internet, and the scale is minimal, there is not much more to optimize. But for really large interactions, the ideal situation is just fetching (or injecting) from
upstream processors, the latest measurement.

## Notations
* https://api.energidataservice.dk/dataset/PowerSystemRightNow?start=now-PT5M&timezone=UTC, specifying timezone does not return any results, they probably use local time for "now", and does not normalize it down to UTC
when using 'now'.

## Future work
* 

## Running the application
I use [PDM](https://pdm-project.org/en/latest/#installation) to manage dependencies and have a pyproject.toml
for clarity and transparency on dependencies and structure of project.

1. Run `pdm install` to install deps and create virtual envs
2. Activate virtual env with `eval $(pdm venv activate in-project)` (Mac/Linux)
3. Run the application with `fastapi run main.py`