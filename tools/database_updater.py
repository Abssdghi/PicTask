import json, shutil, ast
from tools import base64_convert as b64c

def update_json(page, json_var):
    json_var['reset'] = 0
    with open('database/database.json', 'w') as file:
        json.dump(json_var, file, indent=4)
    file.close()
    save_in_data(page, json_var)

def json_loader():
    error = True
    x=0
    while error:
        try:
            with open('database/database.json', 'r') as file:
                database = json.load(file)
            file.close()
            return database
        except:
            print('database error')
            x+=1
            if x == 500:
                # reset_database()
                pass

def reset_database(page):
    with open('database/reset.json', 'r') as ff:
        reset = json.load(ff)
    page.client_storage.clear()
    with open('database/database.json', 'w') as file:
        json.dump(reset, file, indent=4)
    file.close()
    save_in_data(page, reset)
    shutil.rmtree("assets/taskspics")
    shutil.rmtree("assets/shoppics")

def image_save_data(page, id):
    if str(id)[0] == "2":
        path = f'assets/shoppics/{id}.jpg'
    elif str(id)[0] == "1":
        path = f'assets/taskspics/{id}.jpg'
    value = b64c.path_to_base64(path)
    page.client_storage.set(str(id), value)


def save_in_data(page, json_var):
    # page.client_storage.clear()
    json_data = str(json_var)
    page.client_storage.set("json_data", json_data)


def get_data(page):
    retrieved_data = page.client_storage.get("json_data")
    if retrieved_data in [None, "None"]:
        print(' client data is none')
        return
    data = ast.literal_eval(retrieved_data)
    update_json(page,data)
    database = json_loader()
    for shop_id in range(2000000000, database['next_shop_id']):
        shop_base64 = page.client_storage.get(str(shop_id))
        b64c.base64_save(shop_base64, f'assets/shoppics/{shop_id}.jpg')
  
    for task_id in range(1000000000, database['next_task_id']):
        task_base64 = page.client_storage.get(str(task_id))
        b64c.base64_save(task_base64, f'assets/taskspics/{task_id}.jpg')
    
    return data

    
