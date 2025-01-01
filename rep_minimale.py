def représentation_minimale(c):
    virages = [[], ["G"], ["G", "G"], ["D"]]
    nbg = 0
    res = []

    for e in c:
        if e == "A":
            res.extend(virages[nbg])
            nbg = 0
            res.append("A")
        elif e == "G":
            nbg = (nbg + 1) % 4
        else:
            nbg = (nbg - 1) % 4
        res.extend(virages[nbg])
    
    return res