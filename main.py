from demo.client import new_client
from demo.main import start
from drce.options import fetch_options




# class Client:
#     def myfunc(self):
#         pass
#
#
# class MyClient(Client):
#     def __init__(self):
#         self.start = False
#
#     def start_client(self):
#         self.start = True
#         print('now you can start')
#
#
# def set_start_decorator(func):
#     def wrapper(self, *args, **kwargs):
#         self.start_client()
#         func(*args, **kwargs)  # No need to pass 'self' here
#
#     return wrapper
#
#
# class YourClient(MyClient):
#     @set_start_decorator
#     def myfunc(self):
#         print('porcodeddioooooo na naaaaaaaa')
#
#
# # Create an instance of YourClient
# your_client = YourClient()
#
# # Call myfunc (start_client is triggered by the decorator)
# your_client.myfunc(your_client)
#
# # QUICK START
# # This example requires the 'message_content' intent.
