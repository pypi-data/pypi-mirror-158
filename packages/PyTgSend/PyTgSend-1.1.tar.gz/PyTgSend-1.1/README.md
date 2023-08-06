# PyTgSend
Lightweight python snipet to send message(s) to telegram through bot api.
There are many like it, but this one is mine 

Only requires requests lib. 
Was done using python 3.9, full supported python versions list - conveniently left for end user to deal with.

Only sends text messages at the moment. No images or anything, just text.

Installation example:
```commandline
python3 -m pip install PyTgSend
```

Usage example:

```python
from PyTgSend import tg_send_message

tg_send_message(
    'your message here', 
    conf={
        'token': '<your_bot_token>', 
        'chat_id': '<your_chat_id>'
    }
)
```