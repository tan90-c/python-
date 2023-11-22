# -*- coding: utf-8 -*-
import requests,datetime,time,threading
class baidu_tieba():
    def __init__(self,bduss):
        self.Cookie = {"Cookie":bduss}
    #获取关注贴吧
    def get_tieba_list(self):
        url = "https://tieba.baidu.com/mo/q/newmoindex?"
        reqh = requests.get(url,headers=self.Cookie).json()
        return reqh
    #签到指定贴吧
    def sign_add(self,tieba):
        url = "https://tieba.baidu.com/sign/add"
        data = {'ie':'utf-8','kw':tieba,'captcha_input_str':'y1s1'}
        reqh = requests.post(url,headers=self.Cookie,data=data).json()
        if reqh['no'] != 0:
            data['captcha_vcode_str'] = reqh['data']['captcha_vcode_str']
            reqh = requests.post(url,headers=self.Cookie,data=data).json()
        return reqh

def get_times():
    now_time = datetime.datetime.now()
    tomorrow_time = now_time.replace(hour=23, minute=59, second=59, microsecond=59)
    seconds_diff = int((tomorrow_time - now_time).total_seconds()) + 60
    return seconds_diff

def auto_sign(user_bduss):
    new_user = baidu_tieba(user_bduss)
    while True:
        try:
            tieba_list = new_user.get_tieba_list()
            max_num = len(tieba_list['data']['like_forum'])
            num = 0
            for tieba in tieba_list['data']['like_forum']:
                reqh = new_user.sign_add(tieba['forum_name'])
                if reqh['no'] in [0,1101]:
                    num += 1
                #print(f"【{tieba['forum_name']}】吧==>{'签到成功' if reqh['no'] == 0 else '签到失败，原因：'+reqh['error']}！")
            if num/max_num > 0.9:
                print(f"【{datetime.datetime.now().strftime('%Y年%m月%d日')}】签到成功{num}个贴吧，签到失败{max_num-num}个贴吧")
                time.sleep(get_times())
            else:
                print(f"【{datetime.datetime.now().strftime('%Y年%m月%d日')}】签到成功{num}个贴吧，签到失败{max_num-num}个贴吧，由于签到失败过多，一小时后尝试重新签到！")
                time.sleep(3600)
        except Exception as msg:
            print(f"自动签到报错，一小时后尝试重新签到：{msg}")
            time.sleep(3600)

if __name__ == "__main__":
    #如何获取百度bduss：https://jingyan.baidu.com/article/95c9d20d073afbec4e7561d4.html
    Thread_list = []
    bduss_num = 0
    for bduss in open('tieba_bduss.txt',encoding='utf-8'):
        if bduss.strip():
            bduss_num += 1
            t = threading.Thread(target=auto_sign,kwargs={'user_bduss':bduss.strip()})
            t.start()
            Thread_list.append([t,f"bduss{bduss_num}"])
    #------------进程监控------------#
    print(f"共{len(Thread_list)}个签到进程")
    while True:
        for Thread in Thread_list:
            if Thread[0].is_alive() != True:
                print(f"{time_sss()}\n注意：监控进程已终止【{Thread[1]}】")
        time.sleep(600)

    
