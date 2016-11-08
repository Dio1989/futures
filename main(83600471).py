# encoding: UTF-8

import sys
from time import sleep

from PyQt4 import QtGui

from vnctpmd import *
from vnctptd import *


#----------------------------------------------------------------------
def print_dict(d):
    """按照键值打印一个字典"""
    for key,value in d.items():
        print key + ':' + str(value)
        

########################################################################
class MdApi(MdApi):
    """测试用实例"""

    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        super(MdApi, self).__init__()
        
        self.connectionStatus = False
        self.loginStatus = False
        self.contractData = {}
        
    #----------------------------------------------------------------------
    def onFrontConnected(self):
        """服务器连接"""
        self.connectionStatus = True
        
        print u'行情服务器连接成功'
    
    #----------------------------------------------------------------------
    def onFrontDisconnected(self, n):
        """服务器断开"""
        self.connectionStatus = False
        self.loginStatus = False
        
        print u'行情服务器连接断开'
        
    #----------------------------------------------------------------------
    def onHeartBeatWarning(self, n):
        """心跳报警"""
        print n
    
    #----------------------------------------------------------------------   
    def onRspError(self, error, n, last):
        """错误"""
        print_dict(error)
    
    
    #----------------------------------------------------------------------
    def onRspUserLogin(self, data, error, n, last):
        """登陆回报"""
        if error['ErrorID'] == 0:
            self.loginStatus = True
            
            print u'行情服务器登录成功'
            
        else:
            print_dict(error)
        
    #----------------------------------------------------------------------
    
    def onRspUserLogout(self, data, error, n, last):
        """登出回报"""
        if error['ErrorID'] == 0:
            self.loginStatus = False
            
            print u'行情服务器登出完成'
            
        else:
            print_dict(error)
        
    #----------------------------------------------------------------------
    
    def onRspSubMarketData(self, data, error, n, last):
        """订阅合约回报"""
        #print_dict(data)
        #print_dict(error)
        
    #----------------------------------------------------------------------
    
    def onRspUnSubMarketData(self, data, error, n, last):
        """退订合约回报"""
        print_dict(data)
        print_dict(error)    
        
    #----------------------------------------------------------------------
    
    def onRtnDepthMarketData(self, data):
        """行情推送"""
        #print_dict(data)
        if data['InstrumentID'][:5] not in ['m1611', 'm1701', 'm1705']:
            if len(self.contractData[data['InstrumentID']]) < 5:
                self.contractData[data['InstrumentID']].append(data['Volume'])
            else:
                del self.contractData[data['InstrumentID']][0]
                self.contractData[data['InstrumentID']].append(data['Volume'])
            if len(self.contractData[data['InstrumentID']]) == 1:
                vol = 0
            else:
                vol = int(self.contractData[data['InstrumentID']][-1]) - int(self.contractData[data['InstrumentID']][-2])
            if vol > 199:
                print data['UpdateTime'], data['InstrumentID'], data['UpperLimitPrice'], data['LastPrice'], data['LowerLimitPrice'], str(vol)
        if data['BidPrice1'] > data['UpperLimitPrice']:
            BidPrice1 = data['LowerLimitPrice']
        else:
            BidPrice1 = data['BidPrice1']
        if data['AskPrice1'] > data['UpperLimitPrice']:
            AskPrice1 = data['UpperLimitPrice']
        else:
            AskPrice1 = data['AskPrice1']
        #f = open('D:/OptionData/'+str(data['InstrumentID'])+'.txt', 'a')
        #f.write(','.join([str(data['InstrumentID']), str(data['UpdateTime']), str(data['LastPrice']), str(data['Volume']), str(data['OpenInterest']), str(BidPrice1), str(data['BidVolume1']), str(AskPrice1), str(data['AskVolume1'])])) + '\n'
        print data['InstrumentID'], data['UpdateTime'], data['LastPrice'], data['Volume'], data['OpenInterest'], BidPrice1, data['BidVolume1'], AskPrice1, data['AskVolume1']
        #f.close()
    
    #----------------------------------------------------------------------
    
    def onRspSubForQuoteRsp(self, data, error, n, last):
        """订阅合约回报"""
        print_dict(data)
        print_dict(error)
        
    #----------------------------------------------------------------------
    
    def onRspUnSubForQuoteRsp(self, data, error, n, last):
        """退订合约回报"""
        print_dict(data)
        print_dict(error)    
        
    #----------------------------------------------------------------------
    
    def onRtnForQuoteRsp(self, data):
        """行情推送"""
        print_dict(data)


########################################################################
class TdApi(TdApi):
    """测试用实例"""

    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        super(TdApi, self).__init__()
        
        self.InID = []
        self.connectionStatus = False
        self.loginStatus = False 
        
        self.orderRef = 0  # 订单编号
        
    #----------------------------------------------------------------------
    def onFrontConnected(self):
        """服务器连接"""
        self.connectionStatus = True
        
        print u'交易服务器连接成功'
        
        
    
    #----------------------------------------------------------------------
    def onFrontDisconnected(self, n):
        """服务器断开"""
        self.connectionStatus = False
        self.loginStatus = False
        
        print u'交易服务器连接断开'
        
    #----------------------------------------------------------------------
    def onHeartBeatWarning(self, n):
        """心跳报警"""
        print n
    
    #----------------------------------------------------------------------
    def onRspError(self, error, n, last):
        """错误"""
        print_dict(error)
    
    #----------------------------------------------------------------------
    def onRspUserLogin(self, data, error, n, last):
        """登陆回报"""
        # 如果登录成功，推送日志信息
        if error['ErrorID'] == 0:
            self.loginStatus = True
            
            print u'交易服务器登录成功'              
                
        # 否则，推送错误信息
        else:
            print_dict(error)
        
    #----------------------------------------------------------------------
    def onRspUserLogout(self, data, error, n, last):
        """登出回报"""
        # 如果登出成功，推送日志信息
        if error['ErrorID'] == 0:
            self.loginStatus = False
            
            print u'交易服务器登出完成'
                
        # 否则，推送错误信息
        else:
            print_dict(error)

    #----------------------------------------------------------------------
    def onRspSettlementInfoConfirm(self, data, error, n, last):
        """确认结算信息回报"""
        print u'结算信息确认完成'       
        
    #----------------------------------------------------------------------
    def onRspQryInstrument(self, data, error, n, last):
        """查询合约回报"""
        #print_dict(data)
        #print_dict(error)
        if len(data['InstrumentID']) <= 6 and data['InstrumentID'] not in self.InID:
            self.InID.append(data['InstrumentID'])
            #print data['InstrumentID']
        #print n
        #print last
        
    #----------------------------------------------------------------------
    def onRspError(self, error, n, last):
        """错误回报"""
        print error['ErrorID'], error['ErrorMsg'].decode('gbk')
    
    #----------------------------------------------------------------------
    def onRspOrderInsert(self, data, error, n, last):
        """发单错误"""
        print error['ErrorID'], error['ErrorMsg'].decode('gbk')
        
    #----------------------------------------------------------------------
    def Buy(self, InstrumentID, Price, Vol, reqid, loginReq):
        """买开"""
        req = {}
        self.orderRef += 1
        reqid += 1
        
        req['InvestorID'] = loginReq['UserID']
        req['UserID'] = loginReq['UserID']
        req['BrokerID'] = loginReq['BrokerID']        
        
        req['InstrumentID'] = InstrumentID
        req['LimitPrice'] = float(Price)
        req['VolumeTotalOriginal'] = int(Vol)
        
        req['OrderPriceType'] = '2'                                         #报价类型
        req['Direction'] = '0'                                              #买卖类型
        req['CombOffsetFlag'] = '0'                                         #开平类型
        
        req['OrderRef'] = str(self.orderRef)
        
        req['CombHedgeFlag'] = '1'                                          # 投机单
        req['ContingentCondition'] = '1'                                    # 立即发单
        req['ForceCloseReason'] = '0'                                       # 非强平
        req['IsAutoSuspend'] = 0                                            # 非自动挂起
        req['TimeCondition'] = '3'                                          # 今日有效
        req['VolumeCondition'] = '1'                                        # 任意成交量
        req['MinVolume'] = 1                                                # 最小成交量为1
        
        #print req
        
        self.reqOrderInsert(req, reqid)
        
        return self.orderRef, reqid
    
    #----------------------------------------------------------------------
    def Sell(self, InstrumentID, Price, Vol, reqid, loginReq):
        """卖平"""
        req = {}
        self.orderRef += 1
        reqid += 1
        
        req['InvestorID'] = loginReq['UserID']
        req['UserID'] = loginReq['UserID']
        req['BrokerID'] = loginReq['BrokerID']        
        
        req['InstrumentID'] = InstrumentID
        req['LimitPrice'] = float(Price)
        req['VolumeTotalOriginal'] = int(Vol)
        
        req['OrderPriceType'] = '2'                                         #报价类型
        req['Direction'] = '1'                                              #买卖类型
        req['CombOffsetFlag'] = '1'                                         #开平类型
        
        req['OrderRef'] = str(self.orderRef)
        
        req['CombHedgeFlag'] = '1'                                          # 投机单
        req['ContingentCondition'] = '1'                                    # 立即发单
        req['ForceCloseReason'] = '0'                                       # 非强平
        req['IsAutoSuspend'] = 0                                            # 非自动挂起
        req['TimeCondition'] = '3'                                          # 今日有效
        req['VolumeCondition'] = '1'                                        # 任意成交量
        req['MinVolume'] = 1                                                # 最小成交量为1
        
        self.reqOrderInsert(req, reqid)
        
        return self.orderRef, reqid    
    
    #----------------------------------------------------------------------
    def Short(self, InstrumentID, Price, Vol, reqid, loginReq):
        """卖开"""
        req = {}
        self.orderRef += 1
        reqid += 1
        
        req['InvestorID'] = loginReq['UserID']
        req['UserID'] = loginReq['UserID']
        req['BrokerID'] = loginReq['BrokerID']   
        
        req['InstrumentID'] = InstrumentID
        req['LimitPrice'] = float(Price)
        req['VolumeTotalOriginal'] = int(Vol)
        
        req['OrderPriceType'] = '2'                                         #报价类型
        req['Direction'] = '1'                                              #买卖类型
        req['CombOffsetFlag'] = '0'                                         #开平类型
        
        req['OrderRef'] = str(self.orderRef)
        
        req['CombHedgeFlag'] = '1'                                          # 投机单
        req['ContingentCondition'] = '1'                                    # 立即发单
        req['ForceCloseReason'] = '0'                                       # 非强平
        req['IsAutoSuspend'] = 0                                            # 非自动挂起
        req['TimeCondition'] = '3'                                          # 今日有效
        req['VolumeCondition'] = '1'                                        # 任意成交量
        req['MinVolume'] = 1                                                # 最小成交量为1
        
        self.reqOrderInsert(req, reqid)
        
        return self.orderRef, reqid    
    
    #----------------------------------------------------------------------
    def Cover(self, InstrumentID, Price, Vol, reqid, loginReq):
        """买平"""
        req = {}
        self.orderRef += 1
        reqid += 1
        
        req['InvestorID'] = loginReq['UserID']
        req['UserID'] = loginReq['UserID']
        req['BrokerID'] = loginReq['BrokerID']           
        
        req['InstrumentID'] = InstrumentID
        req['LimitPrice'] = float(Price)
        req['VolumeTotalOriginal'] = int(Vol)
        
        req['OrderPriceType'] = '2'                                         #报价类型
        req['Direction'] = '0'                                              #买卖类型
        req['CombOffsetFlag'] = '1'                                         #开平类型
        
        req['OrderRef'] = str(self.orderRef)
        
        req['CombHedgeFlag'] = '1'                                          # 投机单
        req['ContingentCondition'] = '1'                                    # 立即发单
        req['ForceCloseReason'] = '0'                                       # 非强平
        req['IsAutoSuspend'] = 0                                            # 非自动挂起
        req['TimeCondition'] = '3'                                          # 今日有效
        req['VolumeCondition'] = '1'                                        # 任意成交量
        req['MinVolume'] = 1                                                # 最小成交量为1
        
        self.reqOrderInsert(req, reqid)
        
        return self.orderRef, reqid        
              
        
#----------------------------------------------------------------------#----------------------------------------------------------------------
def main():
    """主测试函数，出现堵塞时可以考虑使用sleep"""
    reqid = 0
    
    # 内网使用还是外网使用
    in_config = False
    
    # 创建Qt应用对象，用于事件循环
    app = QtGui.QApplication(sys.argv)

    # 创建API对象
    Mdapi = MdApi()
    Tdapi = TdApi()
    
    # 在C++环境中创建MdApi对象，传入参数是希望用来保存.con文件的地址
    Mdapi.createFtdcMdApi('')
    Tdapi.createFtdcTraderApi('')
    
    # 设置数据流重传方式，测试通过
    Tdapi.subscribePrivateTopic(1)
    Tdapi.subscribePublicTopic(1)    
    
    # 注册前置机地址
    if in_config:
        Mdapi.registerFront("tcp://10.100.200.27:41213")
        Tdapi.registerFront("tcp://10.100.200.27:41205")
    else:
        Mdapi.registerFront("tcp://180.169.77.111:41213")
        Tdapi.registerFront("tcp://180.169.77.111:41205")        
    
    # 初始化api，连接前置机
    Mdapi.init()
    Tdapi.init()
    sleep(0.5)
    
    # 登陆
    loginReq = {}                           # 创建一个空字典
    loginReq['UserID'] = '83600471'         # 参数作为字典键值的方式传入
    loginReq['Password'] = '888888'      # 键名和C++中的结构体成员名对应
    loginReq['BrokerID'] = '2071'    
    reqid = reqid + 1                       # 请求数必须保持唯一性
    i = Mdapi.reqUserLogin(loginReq, reqid)
    reqid = reqid + 1                       # 请求数必须保持唯一性
    i = Tdapi.reqUserLogin(loginReq, reqid)
    sleep(0.5)
    # 确认结算信息
    if Tdapi.loginStatus == True:
        req = {}
        req['BrokerID'] = loginReq['BrokerID']
        req['InvestorID'] = loginReq['UserID']
        reqid = reqid + 1
        Tdapi.reqSettlementInfoConfirm(req, reqid)
    sleep(0.5)
    
    
    ## 登出，测试出错（无此功能）
    #reqid = reqid + 1
    #i = Mdapi.reqUserLogout({}, 1)
    #sleep(0.5)
    
    ## 安全退出，测试通过
    #i = Mdapi.exit()
    
    ## 获取交易日，目前输出为空
    #day = Mdapi.getTradingDay()
    #print 'Trading Day is:' + str(day)
    #sleep(0.5)
    
    ## 订阅合约，测试通过
    #i = Mdapi.subscribeMarketData('m1611-C-2150')
    
    
    ## 退订合约，测试通过
    #i = Mdapi.unSubscribeMarketData('IF1505')
    
    ## 订阅询价，测试通过
    #i = Mdapi.subscribeForQuoteRsp('ag1701')
    
    ## 退订询价，测试通过
    #i = Mdapi.unSubscribeForQuoteRsp('ag1701')
    
    ## 查询合约, 测试通过
    reqid = reqid + 1
    i = Tdapi.reqQryInstrument({}, reqid)
    sleep(0.5)
    
    print u'豆粕期权合约数:'+str(len(Tdapi.InID))
    for eachInID in Tdapi.InID:
        i = Mdapi.subscribeMarketData(eachInID)
        Mdapi.contractData[eachInID] = []
    sleep(0.5)
        
    ## 查询结算, 测试通过
    #req = {}
    #req['BrokerID'] = Tdapi.brokerID
    #req['InvestorID'] = Tdapi.userID
    #reqid = reqid + 1
    #i = Tdapi.reqQrySettlementInfo(req, reqid)
    #sleep(0.5)
    
    ## 确认结算, 测试通过
    #req = {}
    #req['BrokerID'] = Tdapi.brokerID
    #req['InvestorID'] = Tdapi.userID    
    #reqid = reqid + 1
    #i = Tdapi.reqSettlementInfoConfirm(req, reqid)
    #sleep(0.5)
    
    ## 交易测试
    #orderRef, reqid = Tdapi.Short('m1709-C-2950', '33.5', '1', reqid, loginReq)
    #print orderRef, reqid
    sleep(0.5)
    
    ## 连续运行，用于输出行情
    app.exec_()
    
    
    
if __name__ == '__main__':
    main()