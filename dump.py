import json
import os

def json_dump(data,name):
    name = str(name)

    path = os.path.join(os.getcwd(),'cookie',name+'.json')
    with open(path,'w') as f:
        json.dump(data,f)

    return path

def json_load(name):
    name = str(name)
    path = os.path.join(os.getcwd(),'cookie',name+'.json')
    with open(path,'r') as f:
        data = json.load(f)
    return data

def json_delete(name):
    name = str(name)
    path = os.path.join(os.getcwd(),'cookie',name+'.json')
    if os.path.exists(path):
        os.remove(path)
        print("%s 已删除！" % path)


def load_headimg_name(): #以后不需要使用
    path = os.path.join(os.getcwd(),'img')
    json_dump(os.listdir(path),'img')

if __name__ == '__main__':
    print(json_load('17054642905'))