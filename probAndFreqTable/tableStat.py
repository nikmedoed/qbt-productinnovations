from dataBase.workWithDatabase import productData


if __name__ == '__main__':
    base = productData()
    bigcats = []
    max = 0
    maxId = -1
    for i in base.categories:
        selected = base.categories[i]
        if selected['count'] > len (selected['attributes']) and selected['count'] > 10:
            bigcats.append(i)
        if selected['count'] > max:
            max = selected['count']
            maxId = i
    # print(len(bigcats))
    cat = base.getCategoryTable(maxId)

    analtab = ['USB-флеш-накопители', 'Видеокамеры', 'IP-камеры', 'Диски внешние', 'Диски жесткие', 'Носки', 'Полотенца бумажные']
    for i in analtab:
        base.getCategoryTable(i).outTable()
