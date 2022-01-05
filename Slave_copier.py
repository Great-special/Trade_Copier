import time
import socket
import pickle
import tkinter as tk
import MetaTrader5 as mt5

# display data on the MetaTrader 5 package
print("MetaTrader5 package author: ",mt5.__author__)
print("MetaTrader5 package version: ",mt5.__version__)


Account = 20239249
TradeServer = 'Deriv-Demo'
Password = 'LeviteFoundation1'
AccountBalance = 0.0
SYMBOLNAME = ''
VOLUME = 0.0
ORDERTYPE = 0
PRICE = 0.0
STOPLOSS = 0.0
TAKEPROFIT = 0.0
RESULT = ''
OPEN_POSITION = []
RECEIVED_ORDER = []

HEADER_BYBTE = 1024
PORT = 5050
#SERVER = socket.gethostbyname(socket.gethostname())
#Base server >>> '192.168.0.100' Phone server '192.168.43.8'
SERVER = '192.168.43.8'
print(f'[Server Name] {SERVER}')
ADDRESS = (SERVER, PORT)
CODE_FORMAT = 'utf-8'
DISCONNECT_MSG = '!! Disconnected'

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDRESS)


# Sending Message to the server
def transfer(msg):
    message = msg.encode(CODE_FORMAT)
    msg_len = len(message)
    send_len = str(msg_len).encode(CODE_FORMAT)
    send_len += b' ' * (HEADER_BYBTE - len(send_len))
    client.send(send_len)
    client.send(message)
    print(f'[BYBTE Message] {client.recv(2048).decode(CODE_FORMAT)}')

# Receiving Pickled message from Server
def received():
    raw_msg = client.recv(2048)
    clean_msgs = pickle.loads(raw_msg)
    print(clean_msgs)
    len_clean_msgs = len(clean_msgs)

    count = 0
    for clean_msg in clean_msgs:
        if count != len_clean_msgs:
            SYMBOLNAME = clean_msgs[count + 0]
            VOLUME = clean_msgs[count + 1]
            ORDERTYPE = clean_msgs[count + 2]
            PRICE = clean_msgs[count + 3]
            STOPLOSS = clean_msgs[count + 4]
            TAKEPROFIT = clean_msgs[count + 5]
            count = count + 6

            print(f'[NAME]{SYMBOLNAME}')
            print(f'[lots]{VOLUME}')
            print(ORDERTYPE)
            print(PRICE)
            print(STOPLOSS)
            print(TAKEPROFIT)
            RECEIVED_ORDER.append(SYMBOLNAME)
            RECEIVED_ORDER.append(VOLUME)
            RECEIVED_ORDER.append(ORDERTYPE)
            RECEIVED_ORDER.append(PRICE)
            RECEIVED_ORDER.append(STOPLOSS)
            RECEIVED_ORDER.append(TAKEPROFIT)

            #sending Order To Open Position On MT5
            #sendOrderToOpenPosition(SYMBOLNAME, VOLUME, ORDERTYPE, PRICE, STOPLOSS, TAKEPROFIT)
            check_New_order()

    # client.send('Pickled Message Received'.encode(CODE_FORMAT))
    


# establish MetaTrader 5 connection [Starting MT5]
def startMT5(): 
    if not mt5.initialize():
        print("initialize() failed, error code =",mt5.last_error())
        quit()

    # display data on MetaTrader 5 version
    print(f'[MT5 Version] {mt5.version()}')

    # connect to the trade account 
    authorized=mt5.login(login=Account, server=TradeServer, password=Password)
    if authorized:
        print(f"connected to account {Account}")
    else:
        print(f"failed to connect at account {Account}, error code: {mt5.last_error()}")

    # display data on connection status, server name and trading account
    print(mt5.terminal_info())

    print(f'[CONNECTING TO SERVER] ')
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDRESS)

    transfer('Initiating Handshake...')
    while True: 
        received()
    #sendOrderToOpenPosition(SYMBOLNAME,VOLUME,ORDERTYPE,PRICE,STOPLOSS,TAKEPROFIT)


def accountDetails():
    account_details = mt5.account_info()
    login_no = account_details.login
    balance = account_details.balance
    equity = account_details.equity

# get open positions
def getOpenPosition():
    positions=mt5.positions_get()
    if positions==None:
        print(f"No positions error code={mt5.last_error()}")
    elif len(positions)>0:
        print("Total positions =",len(positions))
        # display all open positions
        pos_count = 0
        for position in positions:
            print(position.ticket)
            position_id = position.ticket
            SYMBOLNAME = position.symbol
            ORDERTYPE = position.type
            VOLUME = position.volume
            PRICE = position.price_open
            STOPLOSS = position.sl
            TAKEPROFIT = position.tp
            pos_count += 1

            OPEN_POSITION.append(pos_count)
            OPEN_POSITION.append(position_id)
            OPEN_POSITION.append(SYMBOLNAME)
            OPEN_POSITION.append(VOLUME)
            OPEN_POSITION.append(ORDERTYPE)
            OPEN_POSITION.append(PRICE)
            OPEN_POSITION.append(STOPLOSS)
            OPEN_POSITION.append(TAKEPROFIT)
            

def check_New_order():
    print('Checking New Order')
    count = 0
    for order_ in len(RECEIVED_ORDER):
        if count != len(RECEIVED_ORDER):
            SYMBOLNAME = RECEIVED_ORDER[count + 0]
            VOLUME = RECEIVED_ORDER[count + 1]
            ORDERTYPE = RECEIVED_ORDER[count + 2]       
            PRICE = RECEIVED_ORDER[count + 3]
            STOPLOSS = RECEIVED_ORDER[count + 4]
            TAKEPROFIT = RECEIVED_ORDER[count + 5]
            count = count + 6
            # print('sending open position order')
            # sendOrderToOpenPosition(SYMBOLNAME, VOLUME, ORDERTYPE, PRICE, STOPLOSS, TAKEPROFIT)
            position = mt5.positions_get()
            if position is None:
                print('sending open position order 1')
                sendOrderToOpenPosition(SYMBOLNAME, VOLUME, ORDERTYPE, PRICE, STOPLOSS, TAKEPROFIT)
            elif len(position) > 0:
                for pos in position:
                    POS_ID = pos.ticket
                    SYM_NAME = pos.symbol
                    ORDER_TYPE = pos.type
                    VOL = pos.volume
                    Price = pos.price_open

                    if POS_ID in OPEN_POSITION and SYM_NAME in OPEN_POSITION and ORDER_TYPE in OPEN_POSITION and VOL in OPEN_POSITION and Price in OPEN_POSITION:
                        continue
                    elif POS_ID in OPEN_POSITION and SYM_NAME in OPEN_POSITION and ORDER_TYPE not in OPEN_POSITION and VOL in OPEN_POSITION and Price not in OPEN_POSITION:
                        print('sending close position order')
                        closeOpenPosition(SYMBOLNAME, VOLUME, ORDERTYPE, PRICE)
                    else:
                        print('sending open position order 2')
                        sendOrderToOpenPosition(SYMBOLNAME, VOLUME, ORDERTYPE, PRICE, STOPLOSS, TAKEPROFIT)


#prepare the request structure
def sendOrderToOpenPosition(symbolname,volume,ordertype,price,stoploss,takeprofit):
    global symbol
    symbol = symbolname
    symbol_info = mt5.symbol_info(symbol)
    if symbol_info is None:
        print(symbol, "not found, can not call order_check()")
    
    # if the symbol is unavailable in MarketWatch, add it
    if not symbol_info.visible:
        print(symbol, "is not visible, trying to switch on")
        if not mt5.symbol_select(symbol,True):
            print("symbol_select({}) failed, exit",symbol)

    
    #Checking for Type of Order
    lot = volume
    # point = mt5.symbol_info(symbol).point
    # price = mt5.symbol_info_tick(symbol).ask if ordertype == 0 else tick.bid
    deviation = 20
    #Checking if Order Exits in open positions##
    
    #Request Structure
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": mt5.ORDER_TYPE_BUY if ordertype == 0 else mt5.ORDER_TYPE_SELL,
        "price": price,
        "sl": stoploss,
        "tp": takeprofit,
        "deviation": deviation,
        "magic": 505050,
        "comment": "python script open",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }
    # send a trading request
    result = mt5.order_send(request)
    RESULT = result

    # check the execution result
    print(">>> order_send(): by {} {} lots at {} with deviation={} points".format(symbol,lot,price,deviation))
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print(">>> order_send failed, retcode={}".format(result.retcode))
    else:
        print(">>> order_send done, ", result)
        print("   opened position with POSITION_TICKET={}".format(result.order))


# create a close request
def closeOpenPosition(symbolname,volume,ordertype,price):
    position_id = RESULT.order
    #price = mt5.symbol_info_tick(symbol).ask if ordertype == 1 else tick.bid
    deviation = 20
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbolname,
        "volume": volume,
        "type": mt5.ORDER_TYPE_SELL if ordertype.type == 0 else mt5.ORDER_TYPE_BUY,
        "position": position_id,
        "price": price,
        "deviation": deviation,
        "magic": 505050,
        "comment": "python script close",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }
    # send a trading request
    result=mt5.order_send(request)

###############################################################
print('[STARTING] MetaTrader5 starting....')
startMT5()
transfer('Initiating Handshake...')

