from typing import Protocol
import win32com.client

class Transaction(Protocol):
    file_name: str
    transaction_code: str
    fields: dict

    async def open(self, session: win32com.client.CDispatch) -> 'Transaction':
        ...

    async def config(self, session: win32com.client.CDispatch) -> 'Transaction':
        ...

    async def exec(self, session: win32com.client.CDispatch) -> 'Transaction':
        ...

    async def config_report(self, session: win32com.client.CDispatch) -> 'Transaction':
        ...

    async def save(self, session: win32com.client.CDispatch) -> 'Transaction':
        ...

    async def close(self, session: win32com.client.CDispatch) -> 'Transaction':
        ...
