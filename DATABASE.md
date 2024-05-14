### Table 1: 用戶登入系統
|Field|Data type|Attribute|
|--|--|--|
|user_id|INTEGER|Primary Key, Unique, Not null|
|user_name|TEXT|Not null|
|password|TEXT|Not null|
|email|TEXT|Not null|

### Table 2: Blog 貼文
|Field|Data type|Attribute|
|--|--|--|
|post_id|INTEGER|Primary Key, Unique, Not null|
|user_id|INTEGER|Foreign Key|
|title|TEXT|Not null|
|content|TEXT|Not null|
|tag|TEXT|Not null|
|time|TEXT|Not null|