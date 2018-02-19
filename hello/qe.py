import nltk,re,bs4,urllib,requests,docx,os,pickle,time
from urllib import parse
from bs4 import BeautifulSoup

class QuickExam:
    current_path,featuresets,train_set,test_set,classifier = "",[],[],[],[]
    def __init__(self,current_path):
        QuickExam.current_path = current_path
        QuickExam.featuresets = [(self.ti_features(n),ti) for (n,ti) in pickle.load(open("tixing.moxing",'rb'))]
        QuickExam.train_set, QuickExam.test_set = QuickExam.featuresets, QuickExam.featuresets[100:]
        QuickExam.classifier = nltk.NaiveBayesClassifier.train(QuickExam.train_set)
        requests.packages.urllib3.disable_warnings()

    def parseDocxFile(self,file):
        document = docx.Document(file)
        docTxt = " ".join([p.text for p in document.paragraphs])
        return docTxt

    def suoyou_ti_moxing(self,tixing_jieguo):
        tixing = []
        for j in tixing_jieguo:
            linshi = [(t,"dan_xuan_ti") for t in j if re.search(r'单项?选择?题',t)] \
            + [(t,"mingci_jieshi") for t in j if re.search(r'名词解释',t)] \
            + [(t,"duo_xuan_ti") for t in j if re.search(r'多项?选择?题',t)] \
            + [(t,"panduan_ti") for t in j if re.search(r'判断.*?题',t)] \
            + [(t,"lunshu_ti") for t in j if re.search(r'论述题',t)] \
            + [(t,"wenda_ti") for t in j if re.search(r'.?答题',t)] \
            + [(t,"xuanze_ti") for t in j if re.search(r'[^单多]项?选择题',t)] \
            + [(t,"anli_fenxi_ti") for t in j if re.search(r'.案例分?析?',t)] \
            + [(t,"tiankong_ti") for t in j if re.search(r'填空题',t)] \
            + [(t,"jisuan_ti") for t in j if re.search(r'计算题',t)] \
            + [(t,"bianxi_ti") for t in j if re.search(r'辨析题',t)] \
            + [(t,"xiezuo_ti") for t in j if re.search(r'写作.*?题',t)]
            for l in linshi:
                tixing.append(l)
        return tuple(tixing)

    def suoyou_ti_xing(self):
        tixings = []
        tixings.append(self.tixing_an_wenjian(r'单[项]?选[择]?题.*?[\）\)]'))
        tixings.append(self.tixing_an_wenjian(r'名词解释.*?[\）\)]'))
        tixings.append(self.tixing_an_wenjian(r'多[项]?选[择]?题.*?[\）\)]'))
        tixings.append(self.tixing_an_wenjian(r'判断题.*?[\）\)]'))
        tixings.append(self.tixing_an_wenjian(r'论述题.*?[\）\)]'))
        tixings.append(self.tixing_an_wenjian(r'.?答题[^纸].*?[\）\)]'))
        tixings.append(self.tixing_an_wenjian(r'[^"单项"]选择题.*?[\）\)]'))
        tixings.append(self.tixing_an_wenjian(r'.案例分析.*?[\）\)]'))
        tixings.append(self.tixing_an_wenjian(r'.填空题.*?[\）\)]'))
        tixings.append(self.tixing_an_wenjian(r'计算题.*?[\）\)]'))
        return tixings


    def tixing_an_wenjian(self):
        os.chdir("quickexam/moxing")
        try:
            jieguo = []
            for fn in os.listdir():
                document = docx.Document(fn)
                docTxt = " ".join([p.text for p in document.paragraphs])
                jieguo.append(re.findall(r"[一二三四五六七八九十][\s\.、]?[^一二三四五六七八九十]*?题\s?[（(].*?[)）]","".join(docTxt)))
        except:
            a = "a"
        os.chdir(QuickExam.current_path)
        return jieguo

    def xieru_tixing(self,dizhi,tixings):
        f = open(dizhi,"w")
        for tixing in tixings:
            for t in tixing:
                f.writelines(t + "\n\r")
        f.close()

    def xieru_ti_moxing(self,dizhi,ti_moxing):
        with open(dizhi,"wb") as out_file:
            out_file.write(pickle.dumps(ti_moxing))
        #f.writelines("[")
        #for i,(c,t) in enumerate(ti_moxing):
            #if i == len(ti_moxing) - 1:
                #f.writelines("(" + c + "," + t + ")")
            #else:
                #f.writelines("(" + c + "," + t + "),")
        #f.writelines("]")

    def ti_features(self,ti):
        features = {}
        if re.search(r'单项?选择?题',ti):
            features["has(dan_xuan_ti)"] = True
        else:
            features["has(dan_xuan_ti)"] = False
        if re.search(r'名词解释',ti):
            features["has(mingci_jieshi)"] = True
        else:
            features["has(mingci_jieshi)"] = False
        if re.search(r'多项?选择?题',ti):
            features["has(duo_xuan_ti)"] = True
        else:
            features["has(duo_xuan_ti)"] = False
        if re.search(r'判断.*?题',ti):
            features["has(panduan_ti)"] = True
        else:
            features["has(panduan_ti)"] = False
        if re.search(r'论述题',ti):
            features["has(lunshu_ti)"] = True
        else:
            features["has(lunshu_ti)"] = False
        if re.search(r'.?答题',ti):
            features["has(wenda_ti)"] = True
        else:
            features["has(wenda_ti)"] = False
        if re.search(r'[^单多]项?选择题',ti):
            features["has(xuanze_ti)"] = True
        else:
            features["has(xuanze_ti)"] = False
        if re.search(r'.案例分?析?',ti):
            features["has(anli_fenxi)"] = True
        else:
            features["has(anli_fenxi)"] = False
        if re.search(r'填空题',ti):
            features["has(tiankong_ti)"] = True
        else:
            features["has(tiankong_ti)"] = False
        if re.search(r'计算题',ti):
            features["has(jisuan_ti)"] = True
        else:
            features["has(jisuan_ti)"] = False
        if re.search(r'辨析题',ti):
            features["has(bianxi_ti)"] = True
        else:
            features["has(bianxi_ti)"] = False
        if re.search(r'写作.*?题',ti):
            features["has(xiezuo_ti)"] = True
        else:
            features["has(xiezuo_ti)"] = False
        shuzi = re.findall(r"\d",ti)
        if(len(shuzi) > 0):
            features["tishu"] = shuzi[0]
        return features

    def suoyou_ti_neirong_suoyin(self,neirong):
        jieguo = []
        keneng_tixing = re.findall(r"[一二三四五六七八九十][\s\.、]?[^一二三四五六七八九十]*?题\s?[（(].*?[)）]","".join(neirong))
        if keneng_tixing:
            for ti in keneng_tixing:
                dangqian_tixing = self.pipei_tixing(ti)
                zuhe_dangqian_ti = (dangqian_tixing,neirong.find(ti))
                jieguo.append(zuhe_dangqian_ti)
        return jieguo
    def pipei_tixing(self,ti):
        yiyou_tixing = ['dan_xuan_ti','xuanze_ti','duo_xuan_ti','mingci_jieshi','wenda_ti','lunshu_ti','anli_fenxi_ti','tiankong_ti','jisuan_ti','bianxi_ti','xiezuo_ti']
        for yyt in yiyou_tixing:
            if QuickExam.classifier.classify(self.ti_features(ti)) == yyt:
                return yyt

    def chongzu_timu(self,ti):
        jieguo = []
        tihao = [re.search(r"^\.?(\d\d?)[\.、]?",t).group(1) for i,t in enumerate(ti) if re.search(r"^\.?\d\d?[\.、]?",t)]
        if not [w for w in tihao if w]:
            tihao = [t for i,t in enumerate(ti) if re.search(r"^\.?\d\d?[\.、]?$",t)]
        for count,suoyin in enumerate(tihao):
            dangqian_suoyin = ti.index([t for i,t in enumerate(ti) if re.search(r"^\.?" + suoyin + "[\.、]?",t)][0])
            if (count + 1) < len(tihao):
                xiati_suoyin = ti.index([t for i,t in enumerate(ti) if re.search(r"^\.?" + tihao[count + 1] + "[\.、]?",t)][0])
                jieguo.append(ti[dangqian_suoyin:xiati_suoyin])
            else:
                jieguo.append(ti[dangqian_suoyin:])
        if not jieguo:
            return(ti)
        return jieguo

    def neirong_an_leixing(self,kaojuan):
        neirong = {}
        linshi_neirong = sorted(self.suoyou_ti_neirong_suoyin(kaojuan), key=lambda x: (x[1]))
        for i,(tixing,suoyin) in enumerate(linshi_neirong):
            dangqian_suoyin = suoyin
            if (i + 1) < len(linshi_neirong):
                xiati_suoyin = linshi_neirong[i + 1][1]
                neirong[tixing] = nltk.word_tokenize(kaojuan[dangqian_suoyin:xiati_suoyin])
            else:
                neirong[tixing] = nltk.word_tokenize(kaojuan[dangqian_suoyin:])
        for w in neirong:
            del neirong[w][-1]
        return neirong

    def liechu_wenti_daan_an_tixing(self,ti,yeshu,tixing):
        daan_ji = []
        for i,ti in enumerate(ti):
            print("".join(ti) + "\n")
            daan = tixing(ti,yeshu)
            if daan:
                #打印答案可能会报GBK错误if type(daan) == list:
                    #for w in daan:
                        #print(w + "\n")
                #else:
                    daan_ji.append({"wenti":"".join(ti),"daan":daan})
                    #print(daan + "\n")
            else:
                #print("没找到答案" + "\n")
                daan_ji.append({"wenti":"".join(ti),"daan":"没找到答案"})
        return daan_ji

    def jieda_docx_wenjian(self,wenjian,yeshu):
        daan_ji = []
        docTxt = self.parseDocxFile(wenjian)
        neirong = self.suoyou_ti(docTxt)
        if not neirong:
            shuzi_guolv_neirong = [nltk.word_tokenize(w) for w in docTxt.split("\n") if re.search(r"^[\.。、\s]?\d+",w)]
            neirong = {"wenda_ti":shuzi_guolv_neirong}
            if not shuzi_guolv_neirong:
                neirong = {"wenda_ti":[nltk.word_tokenize(w) for w in docTxt.split("\n")]}
        for tixing in neirong:
            if tixing == "dan_xuan_ti" or tixing == "xuanze_ti":
                daan = self.liechu_wenti_daan_an_tixing(neirong[tixing],yeshu,self.zhao_daan_an_xuanze_ti)
                if daan:
                    daan_ji.append({tixing:daan})
            elif tixing == "duo_xuan_ti":
                daan = self.liechu_wenti_daan_an_tixing(neirong[tixing],yeshu,self.zhao_daan_an_duo_xuan_ti)
                if daan:
                    daan_ji.append({tixing:daan})
            elif tixing == "mingci_jieshi" or tixing == "wenda_ti" or tixing == "lunshu_ti" or tixing == "anli_fenxi" or tixing == "tiankong_ti" or tixing == "bianxi_ti" or tixing == "xiezuo_ti" or tixing == "jisuan_ti":
                daan = self.liechu_wenti_daan_an_tixing(neirong[tixing],yeshu,self.zhao_daan_an_wenda_ti)
                if daan:
                    daan_ji.append({tixing:daan})
        return daan_ji

    def suoyou_ti(self,kaojuan):
        neirong = self.neirong_an_leixing(kaojuan)
        for w in neirong:
            neirong[w] = self.chongzu_timu(neirong[w])
        return neirong

    def zhao_daan_an_xuanze_ti(self,wenti,yeshu):
        soups,result,count,total= [],[],0,10
        try:
            chaijie_wenti = [w for w in wenti if re.search("[a-zA-Z]",w)]
            meixiang_changdu = [(w,len(w) - len(re.findall(r"[a-zA-Z]\s?[\.、]?",w)[0])) for w in chaijie_wenti]
            for i in range(0,yeshu * 10,10):
                search_path = "http://www.baidu.com/s?wd=%s&pn=%d" % ("".join(wenti),i)
                page = requests.get(search_path)
                soups.append(BeautifulSoup(urllib.parse.unquote(page.text),"html.parser"))
            for soup in soups:
                for i in range(count,total,1):
                    daan =  re.findall(r"答案.{3,}?",soup.find(id=str(i+1)).get_text())
                    if daan:
                        daan = self.qu_genyuansu([re.findall("[A-Z]",w) for w in daan if re.search("[A-Z]",w)])
                        if daan:
                            chaijie_daan = re.findall(r"A[^A]*?B[^AB]*?C[^ABC]*?D.{,"+str(meixiang_changdu[3][1])+"}",soup.find(id=str(i+1)).get_text())
                            if chaijie_daan:
                                chaijie_daan = chaijie_daan[0]
                                if daan != "D":
                                    if self.xuanze_ti_wenti_neirong(chaijie_wenti,daan) == self.xuanze_ti_wenti_neirong(chaijie_daan,daan):
                                        result.append(daan)
                                    else:
                                        if self.xuanze_ti_wenti_neirong(chaijie_wenti,"A") == self.xuanze_ti_wenti_neirong(chaijie_daan,"A") and \
                                            self.xuanze_ti_wenti_neirong(chaijie_wenti,"B") == self.xuanze_ti_wenti_neirong(chaijie_daan,"B") and \
                                            self.xuanze_ti_wenti_neirong(chaijie_wenti,"C") == self.xuanze_ti_wenti_neirong(chaijie_daan,"C"):
                                            result.append(daan)
                            else:
                                result.append(daan)
                total = total + 10
                count = total - 10
            if type(result) == list and len(result) > 2:
                result = max(result)
            elif type(result) == list and len(result) >= 1:
                result = result[0]
        except:
            a = "a"
        return result

    def zhao_daan_an_duo_xuan_ti(self,wenti,yeshu):
        soups,result,count,total= [],[],0,10
        try:
            chaijie_wenti = [w for w in wenti if re.search("[a-zA-Z]",w)]
            meixiang_changdu = [(w,len(w) - len(re.findall(r"[a-zA-Z]\s?[\.、]?",w)[0])) for w in chaijie_wenti]
            for i in range(0,yeshu * 10,10):
                search_path = "http://www.baidu.com/s?wd=%s&pn=%d" % ("".join(wenti),i)
                page = requests.get(search_path)
                soups.append(BeautifulSoup(urllib.parse.unquote(page.text),"html.parser"))
            for soup in soups:
                for i in range(count,total,1):
                        if soup.find(id=str(i+1)):
                            daan = soup.find(id=str(i+1)).get_text()
                            daan =  re.findall(r"答案.{8,}?",daan)
                            if daan:
                                daan = self.qu_genyuansu([re.findall("^.*?([A-F]{1,6}).*?$",w) for w in daan if re.search("[a-zA-Z]",w)])
                                if daan:
                                    result.append(daan)
                                #if daan:
                                    #chaijie_daan = self.chaijie_xuanze_ti_daan(soup.find(id=str(i+1)).get_text(),wenti)
                                    #if chaijie_daan:
                                        #if len([w for w in daan if not self.xuanze_ti_wenti_neirong(chaijie_wenti,w) == self.xuanze_ti_wenti_neirong(chaijie_daan,w)]) == 0:
                                            #result.append(daan)
                                    #else:
                                        #result.append(daan)
                total = total + 10
                count = total - 10
            if result and type(result) == list and len(result) > 1:
                guolv_chongfu_daan = {w for w in result}
                diyici_zuichang_daan = max([len(w) for w in guolv_chongfu_daan])
                diyici_daan = [w for w in guolv_chongfu_daan if len(w) == diyici_zuichang_daan]
                guolv_chongfu_daan.remove(diyici_daan[0])
                if diyici_daan:
                    result = diyici_daan
                if guolv_chongfu_daan:
                    dierci_zuichang_daan = max([len(w) for w in guolv_chongfu_daan])
                    dierci_daan = [w for w in guolv_chongfu_daan if len(w) == dierci_zuichang_daan] 
                    result = result + dierci_daan
        except:
            a = "a"
        return result

    def zhao_daan_an_wenda_ti(self,wenti,yeshu):
        soups,result,count,total= [],[],0,10
        try:
            for i in range(0,int(yeshu) * 10,10):
                search_path = "http://www.baidu.com/s?wd=%s&pn=%d" % ("".join(wenti),i)
                page = requests.get(search_path)
                soups.append(BeautifulSoup(urllib.parse.unquote(page.text),"html.parser"))
            for soup in soups:
                for i in range(count,total,1):
                    
                        daan =  re.search(r"答案.*",soup.find(id=str(i+1)).get_text())
                        if daan:
                            zhuandao_dizhi = soup.find("div",id=str(i+1)).find("a")["href"]
                            zhuandao_soup = requests.get(zhuandao_dizhi,verify=False)
                            zai_tiaozhuan_dizhi = zhuandao_soup.history[0].headers["Location"]
                            if re.search(r"zhidao",zai_tiaozhuan_dizhi):
                                time.sleep(1)
                                result.append("可能答案" + str(i+1) + ":" + self.baidu_zhidao_daan(zhuandao_soup))
                total = total + 10
                count = total - 10
        except:
            a = "a"
        return result

    def chaijie_xuanze_ti_daan(self,daan,wenti):
        e_fuhao_chang,f_fuhao_chang,g_fuhao_chang = 0,0,0
        chaijie_wenti = [w for w in wenti if re.search("[a-zA-Z]",w)]
        meixiang_changdu = [(w,len(w) - len(re.findall(r"[a-zA-Z]\s?[\.、]?",w)[0])) for w in chaijie_wenti]
        d_fuhao_chang = re.findall("([Cc]\s?[\.、]?[^Cc]*?)+([Dd]\s?[\.、]?[^Dd]*?)",daan)
        if d_fuhao_chang:
            d_fuhao_chang = len(d_fuhao_chang[0][1])
            if re.search("E\s?[\.、]?",daan,re.I) and len(meixiang_changdu) == 5:
                e_fuhao_chang = re.findall("([Dd]\s?[\.、]?[^Dd]*?)+([Ee]\s?[\.、]?[^Ee]*?)",daan)
                if e_fuhao_chang:
                    e_fuhao_chang = len(e_fuhao_chang[0][1])
                    chaijie_daan = re.findall(r"A[^A]*?B[^AB]*?C[^ABC]*?D[^A-D]{," + str(d_fuhao_chang + meixiang_changdu[3][1]) + "}.*?E[^A-E]{," + str(e_fuhao_chang + meixiang_changdu[4][1]) + "}",daan)
            else:
                chaijie_daan = re.findall(r"A[^A]*?B[^AB]*?C[^ABC]*?D[^A-D]{," + str(d_fuhao_chang + meixiang_changdu[3][1]) + "}",daan)
            if chaijie_daan:
                chaijie_daan = chaijie_daan[0]
            return chaijie_daan

    def qu_genyuansu(self,liebiao):
        if type(liebiao) == list and len(liebiao) > 0:
            return self.qu_genyuansu(liebiao[0])
        else:
            return liebiao

    def xuanze_ti_wenti_neirong(self,chaijie_de_ti,daan_fuhao):
        daan_neirong = ""
        daan_shuliang = len(re.findall("[a-zA-Z]","".join(chaijie_de_ti)))
        if daan_shuliang == 4:
            if daan_fuhao == "D" or daan_fuhao == "d":
                daan_neirong = re.findall(r"" + daan_fuhao +"\s?[\.、]?(.*)","".join(chaijie_de_ti))
            else:
                daan_neirong = re.findall(r"" + daan_fuhao + "\s?[\.、]?(.*?)[a-zA-Z]","".join(chaijie_de_ti))
        elif daan_shuliang == 5:
            if daan_fuhao == "E" or daan_fuhao == "e":
                daan_neirong = re.findall(r"" + daan_fuhao +"\s?[\.、]?(.*)","".join(chaijie_de_ti))
            else:
                daan_neirong = re.findall(r"" + daan_fuhao + "\s?[\.、]?(.*?)[a-zA-Z]","".join(chaijie_de_ti))
        if daan_neirong:
            daan_neirong = daan_neirong[0].strip()
        return daan_neirong

    def baidu_zhidao_daan(self,response):
        redirect_path = response.history[0].headers['Location']
        zhidao_headers = self.baidu_zhidao_headers(self.baidu_headers())
        page = requests.get(redirect_path,verify = False,headers = zhidao_headers)
        page.encoding = 'gbk'
        soup = BeautifulSoup(urllib.parse.unquote(page.text),"html.parser")
        return soup.find(id=re.compile("best-content-[0-9]{,10}")).get_text()

    def baidu_zhidao_headers(self,baidu_headers):
        Hm_lvt = 'Hm_lvt_6859ce5aaf00fb00387e6434e4fcc925=' + baidu_headers['PSTM'] + ";"
        Hm_lpvt = 'Hm_lpvt_6859ce5aaf00fb00387e6434e4fcc925=' + baidu_headers['PSTM'] + ";"
        baidu_headers['Cookie'] = baidu_headers['Cookie'] + Hm_lvt + Hm_lpvt
        baidu_headers['Host'] = 'zhidao.baidu.com'
        return baidu_headers

    def baidu_headers(self):
        cookie = self.baidu_cookie()
        headers = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8', \
        'Accept-Encoding':'gzip,deflate,sdch', \
        'Accept-Language':'zh-CN,zh;q=0.8,ja;q=0.6,en;q=0.4', \
        'Connection':'keep-alive', \
        'Cookie':'', \
        'Host':'www.baidu.com', \
        'PSTM':cookie['PSTM'], \
        'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.117 Safari/537.36'}
        headers['Cookie'] = self.cookie_convert_headers(cookie)
        return headers

    def baidu_cookie(self):
        headers = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8', \
        'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.117 Safari/537.36'}
        url = "https://www.baidu.com/"
        response = requests.get(url,headers = headers,verify=False)
        return response.cookies

    def cookie_convert_headers(self,cookies):
        str = ""
        str = str + "BAIDUID=" + cookies['BAIDUID'] + ";"
        str = str + "BIDUPSID=" + cookies['BIDUPSID'] + ";"
        str = str + "H_PS_PSSID=" + cookies['H_PS_PSSID'] + ";"
        str = str + "PSTM=" + cookies['PSTM'] + ";"
        return str

    def save_upload_file(self,file):
        os.chdir("mysite/static/upload/")
        fobj = open(file.name,'wb');
        for chrunk in file.chunks():
            fobj.write(chrunk);
        fobj.close();
        os.chdir(QuickExam.current_path)

    def zhao_daan_an_wenben(self,wenben,yeshu):
        guolv_wenben = re.findall(r"(.*)([\,\s,、\:\;\/\\\-])(.*)",wenben)
        daan = ""
        if guolv_wenben:
            guolv_wenben = guolv_wenben[0][0].split(guolv_wenben[0][1]) + [guolv_wenben[0][2]]
            daan = self.liechu_wenti_daan_an_tixing(guolv_wenben,yeshu,self.zhao_daan_an_wenda_ti)
        else:
            daan = self.zhao_daan_an_wenda_ti(wenben,yeshu)
            temp = []
            for d in daan:
                temp.append({"wenti":wenben,"daan":d})
            daan = temp
        if not daan:
                daan = [{"wenti":wenben,"daan":"没找到答案"}]
        return daan