import copy
from openpyxl import Workbook

class categoryTable(object):
    """Собирает таблицудля анализа"""

    def __init__(self, cat=None, prod=None, attFreq = None):
        if prod:
            self.categ = cat #copy.deepcopy(cat)
            self.count = cat['count']
            self.atListId = list(cat['attributes'].keys())
            self.atListNames = list(map(lambda x:  cat['attributes'][x], self.atListId))
            self.products = prod
            self.catName = self.products[0]['CategoryName']

            attW = [1] * len(self.atListId)
            sumW = sum(attFreq.values())
            attFW = []
            for i in self.atListId:
                attt = attFreq.get(cat['attributes'][i])
                if attt:
                    we = sumW /attt
                else:
                    we = 0
                attFW.append(we)
            #todo переделать на индексы потом
            ctTab = []
            for i in range(len(self.atListId)):
                attr = self.atListId[i]
                w = {}
                for p in prod:
                    a = p['Attributes'].get(attr)
                    if a:
                        attW[i] += 1
                        w[a] = w[a]+1 if w.get(a) else 1

                sumwProd = sum(w.values())
                wProd = list(map(lambda x: sumwProd / w[x['Attributes'][attr]]
                                            if attr in list(x['Attributes'].keys())
                                            else 0,
                                 prod))
                # print(wProd)
                ctTab.append(wProd)
                attW[i] = self.count / attW[i]
            self.attributeGenW = attFW
            self.attributeCatW = attW
            self.attributeMatW = ctTab
            pw = list(map(self.genWeight, list(range(len(prod)))))
            self.productW = copy.copy(pw)
            idxs = list(zip(pw, list(range(len(prod)))))  # [int(i['id']) for i in prod]))
            idxs.sort(key=lambda x: x[0], reverse=True)
            self.sortedId = idxs
        else:
            self.categtab = copy.deepcopy(prod)

    def outTable(self):
        keyList = ['id', 'ProductPositionName', 'ProductPositionShortName', 'ProductPositionOKPD2']
        outmx = []
        outmx.append([""]*len(keyList) + ["Встречаемость"] + self.attributeGenW)
        outmx.append([""]*len(keyList) + ["Заполненность"] + self.attributeCatW)
        outmx.append(['Вес'] + keyList + self.atListNames)

        for i in self.sortedId:
            prd = self.products[i[1]]
            pr = [i[0]]
            pr.extend(list(map(lambda x: prd[x], keyList)))
            pr.extend(list(map(lambda x: prd['Attributes'].get(x) if prd['Attributes'].get(x) else "", self.atListId)))
            outmx.append(pr)

        wb = Workbook()
        ws = wb.active
        ws.title = self.catName[:31]
        for i in range(len(outmx)):
            for j in range(len(outmx[i])):
                try:
                    ws.cell(row=i + 1, column=j+1).value = outmx[i][j]
                except:
                    print("Error", outmx[i][j])
        try:
            wb.save('../resultData/'+self.catName + '.xlsx')
        except:
            print("Ошибка сохранения:", self.catName)

    def genWeight(self, i):
        agw = self.attributeGenW
        aw = self.attributeCatW
        weight = 0
        for k in range(len(self.attributeMatW)):
            w = self.attributeMatW[k][i]
            weight += w * aw[k] + w * agw[k]
        return weight