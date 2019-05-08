import re
import itertools

class Select:

    def __init__(self):
        self.table = []
        for i in range(2,7):
            # print(i)

            self.Load(i)
        # print(self.table)

    def Load(self, i):
        path = "tag{0}.txt".format(i)
        with open(path, 'r', encoding='utf-8')as f:
            text = f.read()
        line_format = "([\u4E00-\u9FA5a-zA-Z\-0-9]+)[ \t\n]+([\u4E00-\u9FA5]+)[ \t\n]+([\u4E00-\u9FA5]+(，[\u4E00-\u9FA5]+)*)[ \t\n](是|否)"
        # ([\u4E00-\u9FA5]+[ \t\n]+[\u4E00-\u9FA5]+[\u4E00-\u9FA5]+[ \t\n]+    ，[\u4E00-\u9FA5]+)?[ \t\n]+(男|女)
        li = re.findall(line_format,text)

        for line in li:
            # print(line[0],line[1],line[2],line[-1])
            attri = line[2].split("，")
            if line[-1] is "否":
                continue
            self.table.append({"name":line[0],"position":line[1],"sttribute":attri,"star":i})

    def Search(self,tag_li):
        p_sati = []
        for p in self.table:
            flag = True
            for tag in tag_li:
                jud = tag in p["sttribute"]
                if not jud:
                    flag = False
                    break
            if '高级资深干员' in p["sttribute"] and not '高级资深干员'  in tag_li:
                flag = False
            if flag:
                p_sati.append(p)
        return p_sati

    def AverageStar(self, p_li):
        f = 7
        sum = 0
        num = 0
        for p in p_li:
            star =  p["star"]
            if star == 2:
                continue
            factor = f**(6-star)
            sum += star*factor
            num += factor

        return sum/num


    def Try(self, tag_li):
        recommend =[]
        for k in range(len(tag_li)+1):
            for tag_comb  in itertools.combinations(tag_li,k):
                # print(tag_comb,":")
                p_sat = self.Search(list(tag_comb))
                if len(p_sat) == 0:
                    continue
                ave_star = self.AverageStar(p_sat)
                # print(self.AverageStar(p_sat))
                # print(p_sat)
                recommend.append([tag_comb,ave_star,p_sat])
        recommend = sorted(recommend, key=lambda x: x[1], reverse=True)
        return recommend


if __name__ == '__main__':
    s = Select()
    import os
    os.system("pause")
    while True:
        input_ine = input("tag:")
        tag_li =input_ine.split()
        recommend = s.Try(tag_li)
        for choice in recommend:
            if choice[1] >=4:
                print("recommend!")
            print("choice :", choice[0])
            print("average: ", choice[1])
            print("posiable: ", choice[2][:4])
            print("#")
        # print(sat)

        ''' 
新手 
资深干员 
高级资深干员 
                  
远程位 
近战位 
                 
男性干员 
女性干员 
                 
先锋 
狙击 
医疗 
术师 
近卫 
重装 
辅助 
特种 
                 
治疗 
支援 
输出 
群攻 
减速 
生存 
防护 
削弱 
位移 
控场 
爆发 
召唤 
快速复活  

test:
男性干员 近战位 术师 先锋
资深干员 近卫 治疗
'''