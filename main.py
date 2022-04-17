from pybit import HTTP
import pandas as pd
import time
from datetime import datetime
import calendar
import pytz
import decimal
    
session = HTTP(
    'https://api.bybit.com', 
    api_key='PBjwzUfGLsRp0ZnAto', 
    api_secret='MwmTT8epsYSGU2tOT3KrCjhF3By0DX2jI4Hr'
    )

sym_num1="XRPUSDT"
#sym_num1="GALAUSDT"

#sym_num1="XRPUSDT"
#time_itv = 15
delay_time = 60 #time_itv*60
#session.set_leverage(symbol=sym_num1, buy_leverage=15, sell_leverage=15)



def sma20_xrp(itv, symbol=sym_num1):
    
    tz = pytz.timezone('Asia/Seoul')
    cur_time = datetime.now(tz)
    now = datetime.utcnow()
    unixtime = calendar.timegm(now.utctimetuple())
    since = unixtime-itv*60*200;

    wallet=session.get_wallet_balance(coin="USDT")['result']
    my_usdt = pd.DataFrame(wallet).loc['wallet_balance']
    avail_usdt = pd.DataFrame(wallet).loc['available_balance']
    try_usdt = my_usdt*0.25

    response=session.query_kline(symbol=sym_num1,interval=str(itv),**{'from':since})['result']
    df = pd.DataFrame(response)
    sym_info=session.latest_information_for_symbol(symbol=sym_num1)['result']
    sym_price = float(pd.DataFrame(sym_info)['last_price'][0])
    order_respon=session.query_active_order(symbol=sym_num1)['result']
    res_ponse=session.my_position(symbol=sym_num1)['result']
    long_qty = pd.DataFrame(res_ponse)['size'][0]
    ll_loss = float(pd.DataFrame(res_ponse)['stop_loss'][0])
    ll_profit = float(pd.DataFrame(res_ponse)['take_profit'][0])
    short_qty = pd.DataFrame(res_ponse)['size'][1]
    ss_loss = float(pd.DataFrame(res_ponse)['stop_loss'][1])
    ss_profit = float(pd.DataFrame(res_ponse)['take_profit'][1])
    l_sym_laver = int(pd.DataFrame(res_ponse)['leverage'][0])
    s_sym_laver = int(pd.DataFrame(res_ponse)['leverage'][1])
    l_ent_price = float(pd.DataFrame(res_ponse)['entry_price'][0])
    s_ent_price = float(pd.DataFrame(res_ponse)['entry_price'][1])

#    order_respon=session.query_active_order(symbol=sym_num1)['result']
#    abc = pd.DataFrame(order_respon)['price'][0]
#    abcd = pd.DataFrame(order_respon)['price'][1]
#    print(order_respon)
#    print(abc, abcd)


#    sym_qty = (my_usdt*sym_laver*0.25)/sym_price

#    l_price=round(float(sym_price)*1.025,4)
#    s_price=round(float(sym_price)*0.975,4)

    sma_0 = sma1_calc(df,1).iloc[-1]
    sma_1 = sma1_calc(df,1).iloc[-2]
    sma_2 = sma1_calc(df,1).iloc[-3]
    sma1_h1 = sma1_h_calc(df,1).iloc[-1]
    sma1_l1 = sma1_l_calc(df,1).iloc[-1]
    sma1_h2 = sma1_h_calc(df,1).iloc[-2]
    sma1_l2 = sma1_l_calc(df,1).iloc[-2]
    sma_5_1 = sma5_calc(df,5).iloc[-1]
    sma_5_2 = sma5_calc(df,5).iloc[-2]
    sma_5_3 = sma5_calc(df,5).iloc[-3]
    sma_20_1 = sma20_calc(df,20).iloc[-1]
    sma_20_2 = sma20_calc(df,20).iloc[-2]
    sma_20_3 = sma20_calc(df,20).iloc[-3]

#    if (long_qty != 0):
#        l_new_loss_limit = abs(ll_profit - l_ent_price) * 0.5 + l_ent_price
#        l_new_loss = round(abs(ll_profit - l_ent_price) * 0.35 + l_ent_price,4)
#        if (l_new_loss_limit < sym_price) and (ll_loss != l_new_loss):
#            session.set_trading_stop(symbol=sym_num1, side="Buy", stop_loss=l_new_loss)
    
#    if (short_qty != 0):
#        s_new_loss_limit = s_ent_price - abs(ss_profit - s_ent_price) * 0.5 
#        s_new_loss = round(s_ent_price - abs(ss_profit - s_ent_price) * 0.35,4)
#        if (s_new_loss_limit > sym_price) and (ss_loss != s_new_loss):
#            session.set_trading_stop(symbol=sym_num1, side="Sell", stop_loss=s_new_loss)
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#long open
    if ((sma_5_2 > sma_20_2)):
      i = 2
      sma1l_i = {sma1_l_calc(df,1).iloc[-i]}
      sma1h_i = {sma1_h_calc(df,1).iloc[-i]}
      while True:
        sma5_i = sma5_calc(df,5).iloc[-i]
        sma20_i = sma20_calc(df,20).iloc[-i]
        if sma5_i >= sma20_i:
            i = i + 1
            sma1l_add = sma1_l_calc(df,1).iloc[-i]
            sma1l_i.add(sma1l_add)
            sma1h_add = sma1_h_calc(df,1).iloc[-i]
            sma1h_i.add(sma1h_add)
        elif sma5_i < sma20_i:
##            print("long start point, i, sma5_i=", i, round(sma5_i,4))     
            break
        else:
            sma1l_i = 0
            sma1h_i = 0
            sma1l_j = 0
            sma1h_j = 0
            sma1l_k = 0
            sma1h_k = 0
            sma1l_j1 = 0
            sma1h_j1 = 0
            sma1l_k1 = 0
            sma1h_k1 = 0
            break

      j = i
      sma1l_j = {sma1_l_calc(df,1).iloc[-j]}
      sma1h_j = {sma1_h_calc(df,1).iloc[-j]}
      while True:
        sma5_j = sma5_calc(df,5).iloc[-j]
        sma20_j = sma20_calc(df,20).iloc[-j]
        if sma5_j <= sma20_j:
            j = j + 1
            sma1l_add = sma1_l_calc(df,1).iloc[-j]
            sma1l_j.add(sma1l_add)
            sma1h_add = sma1_h_calc(df,1).iloc[-j]
            sma1h_j.add(sma1h_add)
        elif sma5_j > sma20_j:      
##            print("long stoploss_MIN sma1l_j =",min(sma1l_j))
#            print("long MAX sma1h_j =",max(sma1h_j))
            break
        else:
            sma1l_i = 0
            sma1h_i = 0
            sma1l_j = 0
            sma1h_j = 0
            sma1l_k = 0
            sma1h_k = 0
            sma1l_j1 = 0
            sma1h_j1 = 0
            sma1l_k1 = 0
            sma1h_k1 = 0
            break
            
      k = j
      sma1l_k = {sma1_l_calc(df,1).iloc[-k]}
      sma1h_k = {sma1_h_calc(df,1).iloc[-k]}
      while True:
        sma5_k = sma5_calc(df,5).iloc[-k]
        sma20_k = sma20_calc(df,20).iloc[-k]
        if sma5_k >= sma20_k:
            k = k + 1
            sma1l_add = sma1_l_calc(df,1).iloc[-k]
            sma1l_k.add(sma1l_add)
            sma1h_add = sma1_h_calc(df,1).iloc[-k]
            sma1h_k.add(sma1h_add)
        elif sma5_k < sma20_k:      
#            print("long MIN sma1l_k =",min(sma1l_k))
##            print("long profit_MAX sma1h_k =",max(sma1h_k))
            break
        else:
            sma1l_i = 0
            sma1h_i = 0
            sma1l_j = 0
            sma1h_j = 0
            sma1l_k = 0
            sma1h_k = 0
            sma1l_j1 = 0
            sma1h_j1 = 0
            sma1l_k1 = 0
            sma1h_k1 = 0
            break
            
      j1 = k
      sma1l_j1 = {sma1_l_calc(df,1).iloc[-j1]}
      sma1h_j1 = {sma1_h_calc(df,1).iloc[-j1]}
      while True:
        sma5_j1 = sma5_calc(df,5).iloc[-j1]
        sma20_j1 = sma20_calc(df,20).iloc[-j1]
        if sma5_j1 <= sma20_j1:
            j1 = j1 + 1
            sma1l_add = sma1_l_calc(df,1).iloc[-j1]
            sma1l_j1.add(sma1l_add) 
            sma1h_add = sma1_h_calc(df,1).iloc[-j1]
            sma1h_j1.add(sma1h_add)
        elif sma5_j1 > sma20_j1:      
#            print("long MIN sma1l_j1 =",min(sma1l_j1))
#            print("long MAX sma1h_j1 =",min(sma1h_j1))
            break
        else:
            sma1l_i = 0
            sma1h_i = 0
            sma1l_j = 0
            sma1h_j = 0
            sma1l_k = 0
            sma1h_k = 0
            sma1l_j1 = 0
            sma1h_j1 = 0
            sma1l_k1 = 0
            sma1h_k1 = 0
            break
            
      k1 = j1
      sma1h_k1 = {sma1_h_calc(df,1).iloc[-k1]}
      sma1l_k1 = {sma1_l_calc(df,1).iloc[-k1]}
      while True:
        sma5_k1 = sma5_calc(df,5).iloc[-k1]
        sma20_k1 = sma20_calc(df,20).iloc[-k1]
        if sma5_k1 >= sma20_k1:
            k1 = k1 + 1
            sma1h_add = sma1_h_calc(df,1).iloc[-k1]
            sma1h_k1.add(sma1h_add)
            sma1l_add = sma1_l_calc(df,1).iloc[-k1]
            sma1l_k1.add(sma1l_add)
        elif sma5_k1 < sma20_k1:      
#            print("long MIN sma1l_k1 =",max(sma1l_k1))
#            print("long MAX sma1h_k1 =",max(sma1h_k1))
            break
        else:
            sma1l_i = 0
            sma1h_i = 0
            sma1l_j = 0
            sma1h_j = 0
            sma1l_k = 0
            sma1h_k = 0
            sma1l_j1 = 0
            sma1h_j1 = 0
            sma1l_k1 = 0
            sma1h_k1 = 0
            break
      
###############################################################################      
      area_j = round((max(sma1h_j) - min(sma1l_j)) * (j - i),5)
      area_k = round((max(sma1h_k) - min(sma1l_k)) * (k - j),5)
      area_j1 = round((max(sma1h_j1) - min(sma1l_j1)) * (j1 - k),5)
      area_k1 = round((max(sma1h_k1) - min(sma1l_k1)) * (k1 - j1),5)
      area_f = area_j + area_j1
      area_b = area_k + area_k1
#      print("j, j1, k, k1, f, b", area_j,area_j1,area_k,area_k1,area_f,area_b)
#      if area_f > area_b:
#        print("area_f > area_b, long pass")
#      else:
#        print("area_f < area_b, long sell")
        
###############################################################################
      dh_l = round(abs(min(sma1l_j) - min(sma1l_j1)),5)
      dh_h = round(abs(max(sma1h_k) - max(sma1h_k1)),5)
      dt_l = abs(j-i) + abs(j1-k)
      dt_h = abs(k-j) + abs(k1-j1)
      area_h1=round(dh_h * dt_h,5)
      area_l1=round(dh_l * dt_l,5)
      area_h2=round(dh_h / dt_h * 100,4)
      area_l2=round(dh_l / dt_l * 100,4)
#      print("area_h1,area_l1",area_h1,area_l1)
#      print("area_h2,area_l2",area_h2,area_l2)
#      if(area_h1 > area_l1):
#        print(itv, "long, area, sell")
#      if(area_h2 > area_l2):
#        print(itv,"long, high, sell")
#      if((area_h1 > area_l1) and (area_h2 > area_l2)):
#        print(itv,sym_num1,"long, sell")
###############################################################################
      
      dh_i_j = round(abs(max(sma1h_j) - min(sma1l_j)),5)  
      dh_j_k = round(abs(max(sma1h_k) - min(sma1l_k)),5)
      exp_l_pf_price = round(sma5_i + (abs(max(sma1h_k) - sma5_i) * 0.8),4)
      max_l_sell = round(sma5_i + (abs(max(sma1h_k) - sma5_i) * 0.4),4)
      
#      print("exp pf price=",round(exp_l_pf_price,4))
#      print("last price",sym_price)

#long sell now 결정
#      l_sell_now = round(sma_5_2 + (abs(sma_1 - sma_5_2) / 2),4)
      l_sell_now = sym_price
#Set Laverage  
#Liq_price = ent price x l / (l + 1 - (2% x l))
# Liq_price = sma5_i * l / (l + 1 - (0.01 * l))
      p = 1
      while True:
        liq_l_p = (sym_price * p) / (p + 1 - (0.02 * p))
        liq_l_limit = min(sma1l_j1) - abs((sym_price - min(sma1l_j1)) * 0.2)             
        liq_l_max = min(sma1l_j1) - abs((sym_price - min(sma1l_j1)) * 0.1)
        max_l_perc = abs(1 - sym_price / liq_l_limit) * p
                     
        if (liq_l_p <= liq_l_limit):
            p = p + 1
        if ((liq_l_p > liq_l_limit) or (p == 26) or (max_l_perc > 0.3)):
            new_laver = p - 2
#            print("Liq_l_p, liq_l_limit, liq_l_max, p =", round(liq_l_p,4), round(liq_l_limit,4), round(liq_l_max,4), round(max_l_perc,4), p)
            #print("Liq_l_max=",round(liq_l_max,4))
            break

#long sell 결정, 1선-5선 중간, 최소 3% 수익 확보
      min_l_sell_m = round(l_sell_now + (l_sell_now * 0.03 / new_laver),4) 

#long stop loss 결정
      l_loss = round(liq_l_max,4)

#long take profit 결정
      l_profit = round(exp_l_pf_price,4)

#long l_sym_qty 결정
      l_sym_qty = (my_usdt *  new_laver * 0.25) / l_sell_now

#long order condition      
##      if(area_h < area_l):
##          print(itv,"area_h < area_l, long, pass")
##      if(min_l_sell_m > exp_l_pf_price):
##          print(itv,"min_l_sell_m > exp_l_pf_price, long, pass")
##      if(l_sell_now > max_l_sell):
##          print(itv,"l_sell_now > max_l_sell, long, pass")
##      if(long_qty != 0):
##          print(itv,"long_qty != 0, long, pass")
##      if(min(sma1l_j) > min(sma1l_i)):
##          print(itv,"min(sma1l_j) > min(sma1l_i), long, pass")
##      if(exp_l_pf_price < max(sma1h_i)):
##          print(itv,"exp_l_pf_price < max(sma1h_i, long, pass")

############################################################################### 
      if (sma5_i > sma5_k):
          print(sym_num1, itv, "sma5_i > sma5_k, long sell", float(sma5_i),float(sma5_k))
     
      if(((float(avail_usdt)) > (float(try_usdt))) and (min_l_sell_m < exp_l_pf_price) \
         and (l_sell_now < max_l_sell) and (sma5_i > sma5_k) \
         and (min(sma1l_j) < min(sma1l_i)) and (exp_l_pf_price > max(sma1h_i)) \
         and (long_qty == 0) and (order_respon == [])):
          print(itv, "long, sell")
          if (new_laver != l_sym_laver):
              print(session.set_leverage(symbol=sym_num1, buy_leverage=new_laver, sell_leverage=int(s_sym_laver)))
             
          print("long", sym_num1, itv, f'time: {cur_time}')
          print(session.place_active_order(   # 주문하기.
               symbol=sym_num1,   # 주문할 코인
               side='Buy',   # long주문
               order_type='Market', #'Limit',   # 시장가.
               #price=l_sell_now,
               qty=int(l_sym_qty),   # 개수
               time_in_force="GoodTillCancel",
               reduce_only=False,
               close_on_trigger=False,
               take_profit=float(l_profit),
               stop_loss=float(l_loss),
             ))

#        ta_profit=decimal.Decimal(low_min).quantize(decimal.Decimal("1.0000"))
#        sp_loss=decimal.Decimal(high_min).quantize(decimal.Decimal("1.0000"))

#(미체결 불필요-> 필요) 예상 최대 가격 도달시 long sell 미체결 취소
#      if ((sym_price > exp_l_pf_price) and (order_respon != [])): 
#         session.cancel_all_active_orders(symbol=sym_num1)
       # time.sleep(delay_time)
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#short open
    if ((sma_5_2 < sma_20_2)):
      i = 2
      sma1l_i = {sma1_l_calc(df,1).iloc[-i]}
      sma1h_i = {sma1_h_calc(df,1).iloc[-i]}
      while True:
        sma5_i = sma5_calc(df,5).iloc[-i]
        sma20_i = sma20_calc(df,20).iloc[-i]
        if sma5_i <= sma20_i:
            i = i + 1
            sma1l_add = sma1_l_calc(df,1).iloc[-i]
            sma1l_i.add(sma1l_add)
            sma1h_add = sma1_h_calc(df,1).iloc[-i]
            sma1h_i.add(sma1h_add)
        elif sma5_i > sma20_i:
##            print("short start point, i, sma5_i=", i, round(sma5_i,4))     
            break
        else:
            sma1l_i = 0
            sma1h_i = 0
            sma1l_j = 0
            sma1h_j = 0
            sma1l_k = 0
            sma1h_k = 0
            sma1l_j1 = 0
            sma1h_j1 = 0
            sma1l_k1 = 0
            sma1h_k1 = 0
            break
            
      j = i
      sma1l_j = {sma1_l_calc(df,1).iloc[-j]}
      sma1h_j = {sma1_h_calc(df,1).iloc[-j]}
      while True:
        sma5_j = sma5_calc(df,5).iloc[-j]
        sma20_j = sma20_calc(df,20).iloc[-j]
        if sma5_j >= sma20_j:
            j = j + 1
            sma1l_add = sma1_l_calc(df,1).iloc[-j]
            sma1l_j.add(sma1l_add)
            sma1h_add = sma1_h_calc(df,1).iloc[-j]
            sma1h_j.add(sma1h_add)
        elif sma5_j < sma20_j:      
#            print("short MIN sma1l_j =",min(sma1l_j))
##            print("short stoploss_MAX sma1h_j =",max(sma1h_j))
            break
        else:
            sma1l_i = 0
            sma1h_i = 0
            sma1l_j = 0
            sma1h_j = 0
            sma1l_k = 0
            sma1h_k = 0
            sma1l_j1 = 0
            sma1h_j1 = 0
            sma1l_k1 = 0
            sma1h_k1 = 0
            break
            
      k = j
      sma1l_k = {sma1_l_calc(df,1).iloc[-k]}
      sma1h_k = {sma1_h_calc(df,1).iloc[-k]}
      while True:
        sma5_k = sma5_calc(df,5).iloc[-k]
        sma20_k = sma20_calc(df,20).iloc[-k]
        if sma5_k <= sma20_k:
            k = k + 1
            sma1l_add = sma1_l_calc(df,1).iloc[-k]
            sma1l_k.add(sma1l_add)
            sma1h_add = sma1_h_calc(df,1).iloc[-k]
            sma1h_k.add(sma1h_add)
        elif sma5_k > sma20_k:      
#            print("short MIN sma1l_k =",min(sma1l_k))
##            print("short profit_MAX sma1h_k =",max(sma1h_k))
            break
        else:
            sma1l_i = 0
            sma1h_i = 0
            sma1l_j = 0
            sma1h_j = 0
            sma1l_k = 0
            sma1h_k = 0
            sma1l_j1 = 0
            sma1h_j1 = 0
            sma1l_k1 = 0
            sma1h_k1 = 0
            break
            
      j1 = k
      sma1l_j1 = {sma1_l_calc(df,1).iloc[-j1]}
      sma1h_j1 = {sma1_h_calc(df,1).iloc[-j1]}
      while True:
        sma5_j1 = sma5_calc(df,5).iloc[-j1]
        sma20_j1 = sma20_calc(df,20).iloc[-j1]
        if sma5_j1 >= sma20_j1:
            j1 = j1 + 1
            sma1l_add = sma1_l_calc(df,1).iloc[-j1]
            sma1l_j1.add(sma1l_add) 
            sma1h_add = sma1_h_calc(df,1).iloc[-j1]
            sma1h_j1.add(sma1h_add)
        elif sma5_j1 < sma20_j1:      
#            print("short MIN sma1l_j1 =",min(sma1l_j1))
#            print("short MAX sma1h_j1 =",min(sma1h_j1))
            break
        else:
            sma1l_i = 0
            sma1h_i = 0
            sma1l_j = 0
            sma1h_j = 0
            sma1l_k = 0
            sma1h_k = 0
            sma1l_j1 = 0
            sma1h_j1 = 0
            sma1l_k1 = 0
            sma1h_k1 = 0
            break
            
      k1 = j1
      sma1h_k1 = {sma1_h_calc(df,1).iloc[-k1]}
      sma1l_k1 = {sma1_l_calc(df,1).iloc[-k1]}
      while True:
        sma5_k1 = sma5_calc(df,5).iloc[-k1]
        sma20_k1 = sma20_calc(df,20).iloc[-k1]
        if sma5_k1 <= sma20_k1:
            k1 = k1 + 1
            sma1h_add = sma1_h_calc(df,1).iloc[-k1]
            sma1h_k1.add(sma1h_add)
            sma1l_add = sma1_l_calc(df,1).iloc[-k1]
            sma1l_k1.add(sma1l_add)
        elif sma5_k1 > sma20_k1:      
#            print("short MIN sma1l_k1 =",max(sma1l_k1))
#            print("short MAX sma1h_k1 =",max(sma1h_k1))
            break
        else:
            sma1l_i = 0
            sma1h_i = 0
            sma1l_j = 0
            sma1h_j = 0
            sma1l_k = 0
            sma1h_k = 0
            sma1l_j1 = 0
            sma1h_j1 = 0
            sma1l_k1 = 0
            sma1h_k1 = 0
            break

###############################################################################      
      area_j = round((max(sma1h_j) - min(sma1l_j)) * (j - i),5)
      area_k = round((max(sma1h_k) - min(sma1l_k)) * (k - j),5)
      area_j1 = round((max(sma1h_j1) - min(sma1l_j1)) * (j1 - k),5)
      area_k1 = round((max(sma1h_k1) - min(sma1l_k1)) * (k1 - j1),5)
      area_f = area_j + area_j1
      area_b = area_k + area_k1
#      print("j, j1, k, k1, f, b", area_j,area_j1,area_k,area_k1,area_f,area_b)
#      if area_f > area_b:
#        print("area_f > area_b, short pass")
#      else:
#        print("area_f < area_b, short sell")
        
###############################################################################

      dh_l = round(abs(min(sma1l_k) - min(sma1l_k1)),5)
      dh_h = round(abs(max(sma1h_j) - max(sma1h_j1)),5)
      dt_l = abs(k-j) + abs(k1-j1)
      dt_h = abs(j-i) + abs(j1-k)
      area_h1=round(dh_h * dt_h,5)
      area_l1=round(dh_l * dt_l,5)
      area_h2=round(dh_h / dt_h * 100,4)
      area_l2=round(dh_l / dt_l * 100,4)
#      print("area_h1,area_l1",area_h1,area_l1)
#      print("area_h2,area_l2",area_h2,area_l2)
#      if(area_h1 > area_l1):
#        print(itv, "short, area, sell")
#      if(area_h2 > area_l2):
#        print(itv,"short, high, sell")
#      if((area_h1 > area_l1) and (area_h2 > area_l2)):
#        print(itv,sym_num1,"short, sell")
###############################################################################        
      dh_i_j = round(abs(max(sma1h_j) - min(sma1l_j)),5)  
      dh_j_k = round(abs(max(sma1h_k) - min(sma1l_k)),5)

      exp_s_pf_price = round(sma5_i - (abs(min(sma1l_k) - sma5_i) * 0.8),4)
      max_s_sell = round(sma5_i - (abs(min(sma1l_k) - sma5_i) * 0.4),4)
      
#      print("exp pf price=",round(exp_s_pf_price,4))
#      print("last price",sym_price)

#short sell now 결정
#      s_sell_now = round(sma_5_2 - (abs(sma_1 - sma_5_2) / 2),4)
      s_sell_now = sym_price

#Set Laverage  
#Liq_price = ent price x l / (l - 1 + (2% x l))
# Liq_price = sma5_i * l / (l - 1 + (0.01 * l))
      p = 1
      while True:
        liq_s_p = (sym_price * p) / (p - 1 + (0.02 * p))
        liq_s_limit = max(sma1h_j1) + abs((sym_price - max(sma1h_j1)) * 0.2)             
        liq_s_max = max(sma1h_j1) + abs((sym_price - max(sma1h_j1)) * 0.1)
        max_s_perc = abs(1 - sym_price / liq_s_limit) * p
        
        if (liq_s_p > liq_s_limit):
            p = p + 1
        if ((liq_s_p <= liq_s_limit) or (p == 26) or (max_s_perc > 0.3)):
            new_laver = p - 2
#            print("Liq_s_p, liq_s_limit, liq_s_max, p =", round(liq_s_p,4), round(liq_s_limit,4), round(liq_s_max,4), round(max_s_perc,4), p)
            #print("Liq_s_max=",round(liq_s_max,4))
            break

#short sell 결정, 1선-5선 중간, 최소 3% 수익 확보
      min_s_sell_m = round(s_sell_now - (s_sell_now * 0.03 / new_laver),4) 

#short stop loss 결정
      s_loss = round(liq_s_max,4)

#short take profit 결정
      s_profit = round(exp_s_pf_price,4)

#short l_sym_qty 결정
      s_sym_qty = (my_usdt * new_laver * 0.25) / s_sell_now

#short order condition      
##      if(area_h > area_l):
##         print(itv,"area_h > area_l, short, pass")
##    if(min_s_sell_m < exp_s_pf_price):
##          print(itv,"min_s_sell_m < exp_s_pf_price, short, pass")
##      if(s_sell_now < max_s_sell):
##          print(itv,"s_sell_now < max_s_sell, short, pass")
##      if(short_qty != 0):
##          print(itv,"short_qty != 0, short, pass")
##      if(max(sma1h_j) < max(sma1h_i)):
##          print(itv,"max(sma1h_j) < max(sma1h_i), short, pass")
##      if(exp_s_pf_price > min(sma1l_i)):
##          print(itv,"exp_s_pf_price > min(sma1l_i), short, pass")
###############################################################################
      if (sma5_i < sma5_k):
          print(sym_num1, itv, "sma5_i < sma5_k, short sell", float(sma5_i),float(sma5_k))
          
      if(((float(avail_usdt)) > (float(try_usdt))) and (min_s_sell_m > exp_s_pf_price) \
         and (s_sell_now < max_s_sell) and (sma5_i < sma5_k) \
         and (max(sma1h_j) > max(sma1h_i)) and (exp_s_pf_price < min(sma1l_i)) \
         and (short_qty == 0) and (order_respon == [])):
          print(itv, "short, sell")
          if (new_laver != s_sym_laver):
              print(session.set_leverage(symbol=sym_num1, buy_leverage=int(s_sym_laver), sell_leverage=new_laver))
             
          print("short", sym_num1, itv, f'time: {cur_time}')
          print(session.place_active_order(   # 주문하기.
               symbol=sym_num1,   # 주문할 코인
               side='Sell',   # short주문
               order_type='Market', #'Limit',   # 시장가.
               #price=s_sell_now,
               qty=int(s_sym_qty),   # 개수
               time_in_force="GoodTillCancel",
               reduce_only=False,
               close_on_trigger=False,
               take_profit=float(s_profit),
               stop_loss=float(s_loss),
             ))

#        ta_profit=decimal.Decimal(low_min).quantize(decimal.Decimal("1.0000"))
#        sp_loss=decimal.Decimal(high_min).quantize(decimal.Decimal("1.0000"))

#(미체결 불필요-> 필요) 예상 최대 가격 도달시 short sell 미체결 취소
#      if ((sym_price < exp_s_pf_price) and (order_respon != [])): 
#         session.cancel_all_active_orders(symbol=sym_num1)
       # time.sleep(delay_time)

#------------------------------------------------------------------------------



def sma1_calc(ohlc: pd.DataFrame, period: int = 1):
    sma1 = ohlc['close'].astype(float)
    return pd.Series((sma1), name = "SMA1")

def sma1_h_calc(ohlc: pd.DataFrame, period: int = 1):
    sma1_h = ohlc['high'].astype(float)
    return pd.Series((sma1_h), name = "High")

def sma1_l_calc(ohlc: pd.DataFrame, period: int = 1):
    sma1_l = ohlc['low'].astype(float)
    return pd.Series((sma1_l), name = "Low")

def sma5_calc(ohlc: pd.DataFrame, period: int = 5):
    ohlc = ohlc['close'].astype(float)
    sma5 = ohlc.rolling(window=5).mean()   
    return pd.Series((sma5), name = "SMA5")

def sma20_calc(ohlc: pd.DataFrame, period: int = 20):
    ohlc = ohlc['close'].astype(float)
    sma20 = ohlc.rolling(window=20).mean()   
    return pd.Series((sma20), name = "SMA20")

def sma80_calc(ohlc: pd.DataFrame, period: int = 80):
    ohlc = ohlc['close'].astype(float)
    sma80 = ohlc.rolling(window=80).mean()   
    return pd.Series((sma80), name = "SMA80")

def stddev20_calc(ohlc: pd.DataFrame, period: int = 20):
    ohlc = ohlc['close'].astype(float)
    stddev20 = ohlc.rolling(window=20).std()
    return pd.Series((stddev20), name = "STDDEV20")

def stddev80_calc(ohlc: pd.DataFrame, period: int = 80):
    ohlc = ohlc['close'].astype(float)
    stddev80 = ohlc.rolling(window=80).std()
    return pd.Series((stddev80), name = "STDDEV80")

def vma20_calc(ohlc: pd.DataFrame, period: int = 20):
    ohlc = ohlc['volume'].astype(float)
    vma20 = ohlc.rolling(window=20).mean()   
    return pd.Series((vma20), name = "VMA20")

def vma80_calc(ohlc: pd.DataFrame, period: int = 80):
    ohlc = ohlc['volume'].astype(float)
    vma80 = ohlc.rolling(window=80).mean()   
    return pd.Series((vma80), name = "VMA80")

while True:
    
    sym_num1="XRPUSDT"

    print(sym_num1,"5 min")
    sma20_xrp(5)
    time.sleep(5)    
    print(sym_num1,"15 min")
    sma20_xrp(15)
    time.sleep(5)
    
    sym_num1="BSWUSDT"

    print(sym_num1,"5 min")
    sma20_xrp(5)
    time.sleep(5)
    print(sym_num1,"15 min")
    sma20_xrp(15)
    time.sleep(5)    
    
    sym_num1="MATICUSDT"

    print(sym_num1,"5 min")
    sma20_xrp(5)
    time.sleep(5)
    print(sym_num1,"15 min")
    sma20_xrp(15)
    time.sleep(5)    
    
    sym_num1="OGNUSDT"

    print(sym_num1,"5 min")
    sma20_xrp(5)
    time.sleep(5)
    print(sym_num1,"15 min")
    sma20_xrp(15)
    time.sleep(5)       

    sym_num1="GALAUSDT"

    print(sym_num1,"5 min")
    sma20_xrp(5)
    time.sleep(5)
    print(sym_num1,"15 min")
    sma20_xrp(15)
    time.sleep(5)
    
    sym_num1="CHZUSDT"

    print(sym_num1,"5 min")
    sma20_xrp(5)
    time.sleep(5)
    print(sym_num1,"15 min")
    sma20_xrp(15)
    time.sleep(5)    
   
    sym_num1="GMTUSDT"
    print(sym_num1,"5 min")
    sma20_xrp(5)
    time.sleep(5)
    print(sym_num1,"15 min")
    sma20_xrp(15)
    time.sleep(5)
    

    sym_num1="SANDUSDT"
    print(sym_num1,"5 min")
    sma20_xrp(5)
    time.sleep(5)
    print(sym_num1,"15 min")
    sma20_xrp(15)
    time.sleep(5)
    

    sym_num1="ADAUSDT"
    print(sym_num1,"5 min")
    sma20_xrp(5)
    time.sleep(5)
    print(sym_num1,"15 min")
    sma20_xrp(15)
    time.sleep(5)
    
    sym_num1="SLPUSDT"
    print(sym_num1,"5 min")
    sma20_xrp(5)
    time.sleep(5)
    print(sym_num1,"15 min")
    sma20_xrp(15)
    time.sleep(5)
    

    sym_num1="FTMUSDT"
    print(sym_num1,"5 min")
    sma20_xrp(5)
    time.sleep(5)
    print(sym_num1,"15 min")
    sma20_xrp(15)
    time.sleep(5)
    

    sym_num1="IOSTUSDT"
    print(sym_num1,"5 min")
    sma20_xrp(5)
    time.sleep(5)
    print(sym_num1,"15 min")
    sma20_xrp(15)
    time.sleep(5)
    
  
    
    print("Reset")
