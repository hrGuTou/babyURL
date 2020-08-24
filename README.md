# babyURL   
TinyURL-like url shortener.   
    
* Implemented base62 encoding and twitter snowflake generate unique ID to avoid hash collisions.      
* Using AWS dynamoDB as database storing unique ID as key and original URL as value.   
* Using Redis cloud to cache most frequence used short URL to original URL conversion to increase high queries performance and reduce database workload.       
* Implemented LRU caching algorithm locally to avoid repeatly generating short URL for the same original URL.        

## Tech Stack
Python Flask    
Jinja   
HTML, CSS   
AWS dynamoDB    
Redis Cloud   
AWS ec2   

## Deploying
1) Add '.env' file in root directory    
2) Write your redis configurations with the following format    
```
REDIS_HOST = <host>    
REDIS_PORT = <port>     
REDIS_PWD = <password>    
```   
3) Run `aws configure` in with aws cli to connect with your aws
4) pip install the following dependencies:   
```
pip install boto3   
pip install flask
pip install flask_login   
pip install redis   
```
5) Start app from `app.py`    

## Team members:
Jamila  
Haoran He    
Liz Calderon      
Musharrat Chowdhury   
Sadika    
