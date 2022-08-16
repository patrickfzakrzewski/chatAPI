Thank you for allowing me to participate in this challenge

I tried to group any classes function to py files accordingly. My db schema can be found in models.py, my flask app
config settings in config.py, and my input/token validation and security functions in security.py. Otherwise I tried
to keep the logic of each endpoint contained within its respective file. I opted to use wrapper functions to handle 
token and input validation in order to abstract and encapsulate as much as possible.

In terms of additional packages I opted to use sql_alchemy and jwt. sql_alchemy was compatible with sqlite3 for easy
interface with my db's and allowed me to simply use parameterized queries. I opted for JWT to act as my bearer token
so that I may easily include an expiration time.

As username and password restrictions were not specified, I assumed loose restrictions and just checked to ensure that
the input for both were between 1 and 50 chars. Similarly, as the number of users/ number of messages was not specified,
I set a modest max numerical input of 10000 for now. 

In messages, I made assumptions that the start input indicated no messages earlier than start, not that the message id 
necessarily had to begin at start. I also assumed that the only valid sources for video content were youtube and vimeo.

I did not notice the test_config file until the end; though it is unchanged from the boilerplate I conducted many of my
own tests including but not limited to:
    -invalid username
    -incorrect input length
    -intentially malicious SQL injections
    -duplicate usernames
    -correct vs incorrect login
    -input validation
    -valid vs invalid token
    -invalid message content
    -excessively large GET messages request
    -valid input/invalid token, invalid token/valid input

I recognize there are likely many possible improvements. I attempted to address as many as I could within the given time
period. Thank you again and I am very much looking forward to the discussion. 