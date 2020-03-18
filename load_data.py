from urllib import request
import os



def loadVHI():
    url = "https://www.star.nesdis.noaa.gov/smcd/emb/vci/VH/get_provinceData.php?country=UKR&provinceID={}&year1=1981&year2=2019&type=Mean"
    base_filename = r"pr_vhi/vhi_"
    for i in range(1, 28):
        if i == 12 or i == 20:
            continue
        j = swap_id(i)
        print('{}{}{}'.format('loading vhi_', j, '.csv'))
        local_url = url.format(str(i))
        response = request.urlopen(local_url)
        csv = response.read()
        csv_str = str(csv)
        lines = csv_str.split("\\n")
        fx = open(base_filename + str(j) + ".csv", "w")
        for line in lines:
            fx.write(line + "\n")
        fx.close()


def change_f_line():
    base_filename = r"pr_vhi/vhi_{}.csv"
    for i in range(1, 26):
        with open(base_filename.format(str(i)), "r") as f:
            f_content = f.readlines()
            # print(f_content[0])

        f_content[0] = "year,week,SMN,SMT,VCI,TCI,VHI\n"
        f_content[len(f_content) - 1] = "\0"

        with open(base_filename.format(str(i)), "w") as new:
            new.writelines(f_content)
def swap_id(i):
    if i == 1:
        return 22
    if i == 2:
        return 24
    if i == 3:
        return 23
    if i == 4:
        return 25
    if i == 5:
        return 3
    if i == 6:
        return 4
    if i == 7:
        return 8
    if i == 8:
        return 19
    if i == 9:
        return 20
    if i == 10:
        return 21
    if i == 11:
        return 9
    if i == 13:
        return 10
    if i == 14:
        return 11
    if i == 15:
        return 12
    if i == 16:
        return 13
    if i == 17:
        return 14
    if i == 18:
        return 15
    if i == 19:
        return 16
    if i == 21:
        return 17
    if i == 22:
        return 18
    if i == 24:
        return 1
    if i == 23:
        return 6
    if i == 25:
        return 2
    if i == 26:
        return 7
    if i == 27:
        return 5

#loadVHI()

#change_f_line()

