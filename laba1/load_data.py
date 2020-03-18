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

my_dict = {
    1:22,
    2:24,
    3:23,
    4:25,
    5:3,
    6:4,
    7:8,
    8:19,
    9:20,
    10:21,
    11:9,
    13: 10,
    14:11,
    15:12,
    16:13,
    17:14,
    18:15,
    19:16,
    21:17,
    22:18,
    23:6,
    24:1,
    25:2,
    26:7,
    27:5
}
def swap_id(i):
    global my_dict
    return my_dict[i]
#loadVHI()

#change_f_line()

