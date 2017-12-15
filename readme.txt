EONETask readme 
Michael Desson

The code is pretty straightforward and hopefully self-explanatory.

I decided to obtain a list of the source titles and IDs to populate a reference table as a first step towards making a practical database; this affords selecting events by source. 

The code could be more elegant in terms of the event selection; (lines 43 -88) there’s unwarranted repetition, which if reduced would make searching for alternative categories easier. (e.g. by making the categories input variables rather than hard-wiring them into the code. 

I had originally intended to create an sql table for each event category, but decided to combine results for simplicity. It would make sense to create code for individual category that repeats, rather than doing all three at once, but I wanted a single program that covered all the ground without interaction. 

Ideally the structure would be more modular, affording flexibility and resilience. The code relies on initially drawing down source IDs to inform an API call to the specific categories, 8, 10 and 14.

Unfortunately I ran out of time to develop an elegant means of managing the coordinate data - some results are embedded lists, and the data format varies. One option I considered (but didn’t have time for) was a separate coordinate data table. Taking some time to understand the data better, and how it is used would inform this design step. The time and date data needs to be separated, and is currently stored in string format.

The ‘source’  table has a unique identifier column which is relatively redundant. The cat_id column obviously serves as a key to the event_values table.

Embarrassingly, the program seems to additionally return category 9 events. I hope this is the fault of the API rather than my code!

I didn’t have time to convert the tables into a spreadsheet or automate emailing although that process wouldn’t take long.

EONET is an absolutely remarkable resource that could be used to power and inform myriad applications and research projects. I’ve enjoyed working with it immensely.

							Mike Desson
							December 2017
