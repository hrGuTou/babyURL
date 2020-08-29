# babyURL   
TinyURL-like url shortener with qrcode.   
    
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

## How to Deploy
#### Required packages
`pip install boto3 flask flask_login redis pyqrcode python-dotenv requests`

#### Using WSGI        
1) Install and start apache2 or httpd
2) Clone the repository into `/var/www/`
3) Modify the `flaskapp.wsgi` as needed
4) Add the following script to the server configuration file  
5) Restart your apache or httpd     
     
```
<VirtualHost *:80>
                ServerName <ServerName>
                ServerAdmin <ServerAdmin>

                SetEnv AWS_ACCESS_KEY_ID <Your AWS ID>
                SetEnv AWS_SECRET_ACCESS_KEY <Your AWS KEY>
                SetEnv REDIS_HOST <Your Redis Host>
                SetEnv REDIS_PORT <Your Redis port>
                SetEnv REDIS_PWD <Your Redis password>
                SetEnv DOMAIN <Your server domain ex: http://www.example.com/>


                WSGIScriptAlias / /var/www/babyURL/flaskapp.wsgi
                <Directory /var/www/babyURL/babyURL/>
                        Order allow,deny
                        Allow from all
                </Directory>
                Alias /static /var/www/babyURL/babyURL/static
                <Directory /var/www/babyURL/babyURL/static/>
                        Order allow,deny
                        Allow from all
                </Directory>

</VirtualHost>
```

#### Deploy locally
* Configure AWS credentials with aws cli
* Add `.env` the project root directory 
```
REDIS_HOST = '<Your Redis host>'
REDIS_PORT = <Your Redis port>
REDIS_PWD = '<Your Redis password>'

DOMAIN = '127.0.0.1:5000/'
```

```
$ export FLASK_APP=flaskapp.py
$ flask run
```

## Team members:
Jamila  
Haoran He    
Liz Calderon      
Musharrat Chowdhury   
Sadika    

## References
[Designing a URL Shortening service like TinyURL](https://www.educative.io/courses/grokking-the-system-design-interview/m2ygV4E81AR)        
[如何将一个长URL转换为一个短URL](https://juejin.im/post/6844903853830176776)        
[短 URL 系统是怎么设计的](https://www.zhihu.com/question/29270034/answer/46446911)       
[python-snowflake by cablehead](https://github.com/cablehead/python-snowflake)