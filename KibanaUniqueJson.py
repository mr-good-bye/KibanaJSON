import json
import os

jsonFile = "KibanaErrorsHelper.json"
t1 = ' :<>/\\|?*"'
t2 = '_--------_'


def file_enter():
    open(jsonFile, 'w+').close()
    os.system(f"notepad.exe {jsonFile}")


def handler(data):
    json_data = data[:data.rfind('}')+1]
    print(len(json_data))
    message = data[data.rfind('}')+1:]
    json_data = json.loads(json_data)
    json_as_string = json.dumps(json_data, indent=4, ensure_ascii=False).encode('utf-8').decode()
    json_as_string = json_as_string.replace("\\r\\n", "\n")
    json_as_string = json_as_string.replace("\\n", "\n")
    json_as_string = json_as_string.replace("\\t", "    ")
    json_as_string += message
    return json_as_string


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
        file_name = f"error_{host}_{timestamp}_{message[message.rfind(':')+1:]}.json"
        print(message)
        tt = file_name.maketrans(t1, t2)
        with open('errorJson/_' + file_name.translate(tt), 'w', encoding='utf-8') as f:
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
