import time
import socket
import threading
import pickle
import MetaTrader5 as mt5


# display data on the MetaTrader 5 package
print("MetaTrader5 package author: ",mt5.__author__)
print("MetaTrader5 package version: ",mt5.__version__)


# Account = 3500279
# TradeServer = 'Deriv-Demo'
# Password = 'Lastarrow97'
# AccountBalance = 0.0
SYMBOLNAME = ' '
VOLUME = 0.0
ORDERTYPE = 0
PRICE = 0.0
STOPLOSS = 0.0
TAKEPROFIT = 0.0
RESULT = ''

OBJECTS = [SYMBOLNAME, VOLUME, ORDERTYPE, PRICE, STOPLOSS, TAKEPROFIT]
#Holds order to open a new position
#OBJECTS = [] 
Obj_Pos_Id = []
#Holds order to close an existing position
NEG_OBJECTS = []

HEADER_BYBTE = 1024
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
print(f'[Server Name] {SERVER}')
ADDRESS = (SERVER, PORT)
CODE_FORMAT = 'utf-8'
DISCONNECT_MSG = '!! Disconnected'

# Binding Server to ADDRESS
Server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
Server.bind(ADDRESS)


def client_handle(conn, addr):
    print(f'[NEW CONNECTION] {addr} connected.')

    connected = True
    while connected:
        
        msg_length = conn.recv(HEADER_BYBTE).decode(CODE_FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(CODE_FORMAT)
            
            if msg == DISCONNECT_MSG:
                connected = False

            print(f'[{addr}] {msg}')
            
            # SENDING MSG TO CLIENT
            conn.send('Handshake In Progress'.encode(CODE_FORMAT))
            
            print('[Sending] Pickle Message')
            if NEG_OBJECTS is None:
                print('[Sending] Pickle Message 1')
                cleaned_message = pickle.dumps(OBJECTS)
                conn.send(cleaned_message)
            elif OBJECTS is None:
                print('[Sending] Pickle Message 2')
                continue
            elif NEG_OBJECTS not in OBJECTS:
                print('[Sending] Pickle Message 3')
                cleaned_message = pickle.dumps(OBJECTS)
                conn.send(cleaned_message)
            else:
                print('[Sending] Pickle Message 4')
                cleaned_message = pickle.dumps(NEG_OBJECTS)
                conn.send(cleaned_message)
            # cleaned_message = pickle.dumps(OBJECTS)
            # conn.send(cleaned_message)
                       
    conn.close()


def startServer():
    Server.listen()
    print(f'[LISTENING] Server is listening on {SERVER}')
    while True:
        conn, addr = Server.accept()
        thread = threading.Thread(target=client_handle, args=(conn, addr))
        thread.start()
        print(f'[ACTIVE CONNECTIONS] {threading.activeCount() - 1}')
        print('[Checking] For Open Positions...')
        # getOpenPosition()        


# establish MetaTrader 5 connection [Starting MT5]
def startMT5(account, server, password):
    
    Account = account
    TradeServer = server
    Password = password 
    
    if not mt5.initialize():
        print("initialize() failed, error code =",mt5.last_error())
    
    # display data on MetaTrader 5 version
    print(f'[MT5 Version] {mt5.version()}')

    # connecting to the trade account
    print(f'[account] {Account} [Trade Server] {server}')
    authorized=mt5.login(Account, server=TradeServer, password=Password)
  
    if authorized:
        print(f"connected to account {Account}")
    else:
        print(f"failed to connect at account {Account}, error code: {mt5.last_error()}")

    # display data on connection status, server name and trading account
    print(f'[MT5 Terminal Info] {mt5.terminal_info()}')
    # displaying Account Balance
    # accountDetails()
    # AccountBalanceInit = accountDetails.balance
    # AccountBalance = AccountBalance + AccountBalanceInit
    # print(f'[AccountBalance] is: {AccountBalance}')
    
    # print('[STARTING] server starting....')
    # startServer()
    

def accountDetails():
    account_details = mt5.account_info()
    login_no = account_details.login
    balance = account_details.balance
    equity = account_details.equity


# get open positions and sends it to OBJECTS for client use
def getOpenPosition():
    # global postiton
    pos_count = 0
    while True:
        positions=mt5.positions_get()
        #pos_len = len(positions.ticket)
        if pos_count <= len(positions):
            if positions==None:
                print(f"No positions error code={mt5.last_error()}")
            elif len(positions)>0:
                print("Total positions =",len(positions))
                # display all open positions
                for position in positions:
                    print(f'[ POS TICKET ] {position.ticket} get open positions')
                    obj_pos_id = pos_count + 1
                    POS_ID = position.ticket
                    SYMBOLNAME = position.symbol
                    ORDERTYPE = position.type
                    VOLUME = position.volume
                    PRICE = position.price_open
                    STOPLOSS = position.sl
                    TAKEPROFIT = position.tp
                    
                    OBJECTS.append(SYMBOLNAME)
                    OBJECTS.append(VOLUME)
                    OBJECTS.append(ORDERTYPE)
                    OBJECTS.append(PRICE)
                    OBJECTS.append(STOPLOSS)
                    OBJECTS.append(TAKEPROFIT)
                    
                    Obj_Pos_Id.append(obj_pos_id)
                    Obj_Pos_Id.append(POS_ID)
                    Obj_Pos_Id.append(SYMBOLNAME)
                    Obj_Pos_Id.append(VOLUME)
                    Obj_Pos_Id.append(ORDERTYPE)
                    Obj_Pos_Id.append(PRICE)
                    Obj_Pos_Id.append(STOPLOSS)
                    Obj_Pos_Id.append(TAKEPROFIT)
                    # while pos_count == pos_len:
                    #     positions=mt5.positions_get()
                    print('[Checking] For Positions To Close...')
                    check_position_To_close()


#Checking if position still exits/open if not sends it to NEG_OBJECTS for client use
def check_position_To_close():
    
    positions=mt5.positions_get()
    if positions==None:
        print(f"No positions error code={mt5.last_error()}")
    elif len(positions)>0:
        print("Total positions =",len(positions))
        # display all open positions
        for pos in positions:
            print(f'[ POS TICKET ] {pos.ticket} positions to close')
            POS_ID = pos.ticket
            SYM_NAME = pos.symbol
            ORDER_TYPE = pos.type
            VOL = pos.volume
            Price = pos.price_open
            
            if POS_ID in Obj_Pos_Id and SYM_NAME in Obj_Pos_Id and ORDER_TYPE in Obj_Pos_Id and Price in Obj_Pos_Id and VOL in Obj_Pos_Id:
                continue
            else:
                SYMBOLNAME = SYM_NAME
                VOLUME = VOL
                ORDERTYPE = 0 if ORDER_TYPE == 1 else 1
                PRICE = Price
                STOPLOSS = 0.0
                TAKEPROFIT = 0.0
                
                NEG_OBJECTS.append(SYMBOLNAME)
                NEG_OBJECTS.append(VOLUME)
                NEG_OBJECTS.append(ORDERTYPE)
                NEG_OBJECTS.append(PRICE)
                NEG_OBJECTS.append(STOPLOSS)
                NEG_OBJECTS.append(TAKEPROFIT)
                

#prepare the request structure
def sendOrderToOpenPosition():
    global symbol
    symbol = SYMBOLNAME
    symbol_info = mt5.symbol_info(symbol)
    if symbol_info is None:
        print(symbol, "not found, can not call order_check()")
    
    # if the symbol is unavailable in MarketWatch, add it
    if not symbol_info.visible:
        print(symbol, "is not visible, trying to switch on")
        if not mt5.symbol_select(symbol,True):
            print("symbol_select({}}) failed, exit",symbol)
    
    #Checking for Type of Order
    lot = VOLUME
    point = mt5.symbol_info(symbol).point
    price = mt5.symbol_info_tick(symbol).ask if position.type == 0 else tick.bid
    deviation = 20
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": mt5.ORDER_TYPE_BUY if position.type == 0 else mt5.ORDER_TYPE_SELL,
        "price": price,
        "sl": STOPLOSS,
        "tp": TAKEPROFIT,
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
def closeOpenPosition():
    position_id = RESULT.order
    price = mt5.symbol_info_tick(symbol).ask if position.type == 1 else tick.bid
    deviation = 20
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": mt5.ORDER_TYPE_SELL if position.type == 0 else mt5.ORDER_TYPE_BUY,
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

#############################################################################################

print('[STARTING] MetaTrader5 starting....')
#startMT5()

print('[STARTING] server starting....')
#startServer()

