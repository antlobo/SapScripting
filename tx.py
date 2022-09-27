from typing import Protocol
import win32com.client

class Transaction(Protocol):
    file_name: str
    transaction_code: str

    def open(self, session: win32com.client.CDispatch) -> 'Transaction':
        ...

    def config(self, session: win32com.client.CDispatch) -> 'Transaction':
        ...

    def exec(self, session: win32com.client.CDispatch) -> 'Transaction':
        ...

    def config_report(self, session: win32com.client.CDispatch) -> 'Transaction':
        ...

    def save(self, session: win32com.client.CDispatch) -> 'Transaction':
        ...

    def close(self, session: win32com.client.CDispatch) -> 'Transaction':
        ...
