from typing import Dict, Any, Optional
from aiogram.fsm.storage.base import BaseStorage, StorageKey, StateType
from pathlib import Path
from aiofiles import open as async_open
import json


def build_key(key: StorageKey) -> str:
    parts = [str(key.bot_id), str(key.chat_id), str(key.thread_id), str(key.user_id), key.destiny]

    return ":".join(parts)


filename = "datastates.json"

try:
    with open(filename, 'r') as file:
        data = json.loads(file.read())
except json.JSONDecodeError as e:
    print(f"Ошибка при чтении JSON: {e}")


class Storage(BaseStorage):
    def __init__(self):
        if not Path(filename).exists():
            with open(filename, "w+") as file:
                file.write('{"state": {}, "data": {}}')

    async def set_state(self, key: StorageKey, state: StateType = None) -> None:
        key_str = build_key(key)

        async with async_open(filename, "r+") as file:
            json_data = json.loads(await file.read())

            states = json_data["state"]
            states[key_str] = state.state if state else ""

            json_data["state"] = states

            await file.seek(0)
            await file.truncate()
            await file.write(json.dumps(json_data, indent=4))

    async def get_state(self, key: StorageKey) -> Optional[str]:
        key_str = build_key(key)

        async with async_open(filename, "r") as file:
            json_data = json.loads(await file.read())

            return json_data["state"].get(key_str)

    async def set_data(self, key: StorageKey, data: Dict[str, Any]) -> None:
        key_str = build_key(key)

        async with async_open(filename, "r+") as file:
            json_data = json.loads(await file.read())

            states = json_data["data"]
            states[key_str] = data

            json_data["data"] = states

            await file.seek(0)
            await file.truncate()
            await file.write(json.dumps(json_data, indent=4))

    async def get_data(self, key: StorageKey) -> Dict[str, Any]:
        key_str = build_key(key)

        async with async_open(filename, "r") as file:
            json_data = json.loads(await file.read())

            return json_data["data"].get(key_str) or dict()

    async def close(self) -> None:
        pass
