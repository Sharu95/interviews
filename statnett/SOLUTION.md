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
    * Solution is straightforward, but both computationally (and potentially financially) expensive. You process a lot of the same data every minute. If the API 
    is not free, this is even more expensive (it isn't now, but might be).
2) Develop a running application (e.g streaming)
    * The optimal solution is a running application, doing some caching/buffering and some tricks to maintain a moving average window. If you want to reduce computational cost and memory footprint, you can rather cache the cumulative sum and infer the average from that (and number of data points). The result can be returned as an API response-json, or posted to some queue-based system that is consumed by the ML model (however it is deployed, but)

I will go for solution 2.


