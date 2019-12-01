import pickle
import csv
import copy

import inspect
import os
import sys
from dataBase.categoryTable import categoryTable

def get_script_dir(follow_symlinks=True):
    if getattr(sys, 'frozen', False): # py2exe, PyInstaller, cx_Freeze
        path = os.path.abspath(sys.executable)
    else:
        path = inspect.getabsfile(get_script_dir)
    if follow_symlinks:
        path = os.path.realpath(path)
    return os.path.dirname(path)

pathToThisFile = get_script_dir()

class productData(object):
    """Обсепечивает работу со всей базой, которая есть"""

    def __init__(self, path = pathToThisFile + '/dataBase.bin', flag=False):
        if flag:
            with open(path, 'r') as f:
                prod = dict()
                cat = dict()
                atFrq = dict()
                reader = csv.DictReader(open(path, "r", encoding='utf-8'), delimiter=';')
                # head = reader.fieldnames
                cont = 0
                for line in reader:
                    cont+=1
                    if cont %50000 == 0: print(cont)
                    d = dict(line)
                    for i in d:
                        if d[i] == 'NULL': d[i] = None
                        # d[i] = d[i].decode('utf-8-sig').encode('utf8')
                    id = d.pop('PositionID')
                    attributeID = d.pop('ProductPositionAttributeID')
                    attVal = d.pop('ProductPositionAttribute')
                    atName = d.pop('AttributeName')
                    if not (id in prod):
                        prod[id] = d
                        prod[id]['Attributes'] = {}
                        ak = atFrq.get(atName)
                        if ak:
                            atFrq[atName] += 1
                        else:
                            atFrq[atName] = 1
                    if attVal: prod[id]['Attributes'][attributeID] = attVal
                    prod[id]['id'] = id
                    # обновляем словарь категорий
                    catK = cat.get(d['CategoryName'])
                    if catK:
                        if not id in catK['prodList']:
                            catK['prodList'].append(id)
                            catK['count'] += 1
                        catK['attributes'][attributeID] = atName
                    else:
                        cat[d['CategoryName']] = {
                            'prodList': [id],
                            'count': 1,
                            'attributes': {attributeID: atName}
                        }
            print(cont)
            self.categories = cat
            self.products = prod
            self.attFreq = atFrq
        else:
            with open(path, 'rb') as f:
                temp = copy.copy(pickle.load(f))
                self.categories = temp.categories
                self.products = temp.products
                self.attFreq = temp.attFreq


    def saveData(self, path = pathToThisFile + '/dataBase.bin'):
        with open(path, 'wb') as f:
            pickle.dump(self, f)

    def getCategoryTable(self, id):
        cat = self.categories[id]
        prod = list(map(lambda x: self.products[x], cat['prodList']))
        ct = categoryTable(cat, prod, self.attFreq)

        # ct = cat.get("catTable")
        # if not ct:
        #     prod = list(map(lambda x: self.products[x],cat['prodList']))
        #     ct = categoryTable(cat, prod)
        #     cat['catTable'] = ct

        return ct



    def __del__(self):
        pass
        # print("сохраняю данные базы")
        # self.saveData()
        # print("сохранено")


if __name__ == '__main__':
    data = productData("../data/prod2.csv", True)
    data.saveData()
    test = productData()
    pass





