from typing import Dict, Any, List
from pathlib import Path
from aiofiles import open as async_open
import json

filename = "data/data.json"

if not Path(filename).exists():
    with open(filename, "w+") as file:
        file.write('{}')

class DataStorage:
    @staticmethod
    async def add_data(date: str, data: dict) -> None:
        async with async_open(filename, "r+") as file:
            json_data = json.loads(await file.read())

            if date not in json_data:
                json_data[date] = []

            arr: List[object] = json_data[date]

            arr.append(data)
            arr.sort(key=lambda x: float(x["time"].replace(":", ".")))

            json_data[date] = arr
            await file.seek(0)
            await file.truncate()
            await file.write(json.dumps(json_data, indent=4))

    @staticmethod
    async def get_data(date: str) -> List[Dict[str, Any]]:
        async with async_open(filename, "r") as file:
            json_data = json.loads(await file.read())

            return json_data.get(date) or []

    @staticmethod
    async def get_alldata(date: str) -> Dict[str, List[Dict[str, Any]]]:
        async with async_open(filename, "r") as file:
            json_data = json.loads(await file.read())

            return json_data

    @staticmethod
    async def update_data(date: str, time: str, data: dict):
        async with async_open(filename, "r+") as file:
            json_data = json.loads(await file.read())

            arr = json_data.get(date) or []

            for i in range(len(arr)):
                if arr[i]["time"] == time:
                    arr[i] = data
                    break

            json_data[date] = arr

            await file.seek(0)
            await file.truncate()
            await file.write(json.dumps(json_data, indent=4))

    @staticmethod
    async def replace_data(needed_date: str, needed_time: str):

        async with async_open(filename, 'r') as file:
            data = json.loads(await file.read())

        res = []
        for day in data.values():
            for t in day:
                if t['time'] == needed_time and t['date'] == needed_date:
                    t['fi'] += '. Запись была отменена!'
                    res.append(t)

        #print(data)
        with open(filename, 'w+') as file:
            json.dump(data, file, indent=4)

        return res

    @staticmethod
    async def edit_data(needed_date: str, needed_time: str, par: str, new_par: str):

        async with async_open(filename, 'r') as file:
            data = json.loads(await file.read())

        case_dict = {
            'ФИ': 'fi',
            'Телефон': 'phone',
            'Дата': 'date',
            'Время': 'time',
            'Процедура': 'procedure'
        }

        par = case_dict.get(par, 'price')

        res = []
        #print(data)
        for day in data.values():
            #print(day)
            for t in day:
                if t['time'] == needed_time and t['date'] == needed_date:
                    t[par] = new_par
                    res.append(t)

        #print(data)
        with open(filename, 'w+') as file:
            json.dump(data, file, indent=4)

        return res


    @staticmethod
    async def get_ndnt(needed_date: str, needed_time: str):

        async with async_open(filename, 'r') as file:
            data = json.loads(await file.read())

        # print(data)
        res = []
        for day in data.values():
            # print(day)
            for t in day:
                if t['time'] == needed_time and t['date'] == needed_date:
                    res.append(t)

        return res