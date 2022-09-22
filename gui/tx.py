from typing import Protocol
import win32com.client

class Transaction(Protocol):
    def open(self, session: win32com.client.CDispatch) -> 'Transaction':
        ...

    def process(self, session: win32com.client.CDispatch) -> 'Transaction':
        ...

    def save(self, session: win32com.client.CDispatch) -> 'Transaction':
        ...

    def close(self, session: win32com.client.CDispatch) -> 'Transaction':
        ...
