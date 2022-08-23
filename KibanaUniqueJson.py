import json
import os


jsonFile = "KibanaErrorsHelper.json"
t1 = ':<>/\\|?*"'
t2 = '--------_'


def file_enter():
    open(jsonFile, 'w+').close()
    os.system(f"notepad.exe {jsonFile}")


def handler(data):
    json_data = data[:data.rfind('}')+1]
    message = data[data.rfind('}')+1:]
    json_data = json.loads(json_data)
    json_as_string = json.dumps(json_data, indent=4, ensure_ascii=False).encode('utf-8').decode()
    json_as_string = json_as_string.replace("\\r\\n", "\n")
    json_as_string = json_as_string.replace("\\n", "\n")
    json_as_string = json_as_string.replace("\\t", "    ")
    json_as_string += message
    return json_as_string


def create_name(host: str, timestamp: str):
    #  timestamp: YYYY-MM-DD'T'HH-mm-ss.SSS'Z'(-3hours)
    tt = timestamp.maketrans(t1, t2)
    timestamp = timestamp.translate(tt)
    _timestamp = timestamp.split('-')  # ['2022', '08', '15T10', '50', '12.413Z']
    if len(timestamp) < 6:
        return f"__{host}__{input('Enter error name: ')}"
    timestamp = {
        'year': int(_timestamp[0]),
        'month': int(_timestamp[1]),
        'day': int(_timestamp[2].split('T')[0]),
        'hour': int(_timestamp[2].split('T')[1]) + 3,
        'minute': int(_timestamp[3]),
        'seconds': _timestamp[4][:6]
    }
    if timestamp['hour'] > 23:

        timestamp['hour'] -= 24
        timestamp['day'] += 1
    res = f"{timestamp['year']}.{timestamp['month']}.{timestamp['day']}"
    res += f"__{timestamp['hour']}-{timestamp['minute']}-{timestamp['seconds']}"
    res += f"__{host}"
    return res


def main():
    file_enter()
    with open(jsonFile, 'r', encoding='utf-8') as f:
        data = f.read()

    try:
        json_data = json.loads(data)
        timestamp = json_data["_source"]["@timestamp"]
        host = json_data["_source"]["host"]["name"]
        json_as_string = handler(json_data["_source"]["message"])
        message = json_as_string[json_as_string.rfind('}')+1:]
        file_name = f"{create_name(host, timestamp)}{message[message.rfind(':')+1:]}.json"
        tt = file_name.maketrans(t1, t2)
        with open('errorJson/' + file_name.translate(tt), 'w', encoding='utf-8') as f:
            f.write(json_as_string)
    except Exception as e:
        print(e)
        with open(f"errorJson/_error_UNKNOWN.json", 'w', encoding='utf-8') as f:
            f.write(handler(data))


if __name__ == "__main__":
    s = 'n'
    while s.lower() == 'n':
        main()
        s = input("n to parse next\nEnter to exit\n")
