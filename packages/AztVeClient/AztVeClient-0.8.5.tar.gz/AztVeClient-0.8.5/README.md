# 1 安装SDK
**注意**：在安装SDK之前，请确认已经正确安装**3.6**及以上版本Python环境，下载地址[www.python.org](https://www.python.org/ftp/python/)
以Windows为例，打开可调用Python3的命令行终端，键入以下代码安装：
```bash
pip install AztVeClient
```
**提示：**

- MacOS和Linux环境下可能需要使用`pip3`代替`pip`进行安装

---

# 2 数据结构
## 2.1 信息类
### 2.1.1 AccMargin - 账户资产信息
| 属性 | 类型 | 说明 |
| --- | --- | --- |
| account | str | 账户ID |
| total_amount | float | 账户总资金 |
| available_amount | float | 账户可用资金 |
| deposit | float | 账户入金总额 |
| open_balance | float | 期初结存 |
| trade_frozen_margin | float | 交易冻结金额 |
| position_market_amount | float | 持仓市值 |
| total_buy_amount | float | 买入总金额 |
| total_buy_fee | float | 买入总手续费 |
| total_sell_amount | float | 卖出总金额 |
| total_sell_fee | float | 卖出总手续费 |

### 2.1.2 CancelOrder - 撤单信息
| 属性 | 类型 | 说明 |
| --- | --- | --- |
| client_ref | str | 本地订单编号，由客户端自动生成 |
| sender_user | str | 账户标识，由系统自动生成 |
| account | str | 账户ID |
| org_order_id | str | 需要撤销的委托订单编号 |
| send_time | datetime.datetime | 发送时间，由系统自动生成 |

### 2.1.3 CancelOrderReject - 撤单拒绝回报信息
| 属性 | 类型 | 说明 |
| --- | --- | --- |
| client_ref | str | 本地订单编号，由客户端自动生成 |
| org_order_id | str | 撤单交易平台委托订单编号 |
| reject_reason | int | 撤单拒绝原因，具体含义与取值参见枚举常量`ECxRejReasonType` |
| report_time | datetime.datetime | 回报时间，由系统自动生成 |

### 2.1.4 HisDeposit - 历史入金信息
| 属性 | 类型 | 说明 |
| --- | --- | --- |
| settlement_date | datetime.datetime | 结算日期 |
| account | str | 账户ID |
| client_ref | str | 本地入金请求编号，由客户端自动生成 |
| deposit | float | 入金金额 |

### 2.1.5 LoginInfo - 登录信息
| 属性 | 类型 | 说明 |
| --- | --- | --- |
| account | str | 账户ID |
| trading_day | str | 当前交易日 |
| exchange_name | str | 交易所名称 |
| exchange_time | datetime.datetime | 当前交易时间 |

### 2.1.6 OrdReport - 委托回报信息
| 属性 | 类型 | 说明 |
| --- | --- | --- |
| place_order | PlaceOrder | 委托订单信息 |
| status_msg | OrdStatusMsg | 委托订单状态信息 |

### 2.1.7 OrdStatusMsg - 委托订单状态信息
| 属性 | 类型 | 说明 |
| --- | --- | --- |
| order_status | int | 委托订单执行状态，具体含义与取值见枚举常量`EOrderStatus` |
| traded_qty | int | 订单交易数量，以股等基础单位为单位 |
| traded_amount | float | 订单交易金额 |
| total_fee | float | 订单交易手续费 |
| frozen_margin | float | 订单对账户冻结金额 |
| frozen_price | float | 订单对账户冻结价格 |
| reject_reason | int | 拒单原因，具体含义与取值参见枚举常量`EOrderRejectReason` |
| report_time | datetime.datetime | 回报时间，由系统自动生成 |

### 2.1.8 PlaceOrder - 委托订单信息
| 属性 | 类型 | 说明 |
| --- | --- | --- |
| client_ref | str | 本地订单编号，由客户端自动生成 |
| sender_user | str | 账户标识，由系统自动生成 |
| account | str | 账户ID |
| market | str | 交易所代码 |
| code | str | 标的代码 |
| order_type | int | 委托类型，具体含义与取值参见枚举常量`EOrderType` |
| business_type | int | 业务类型，具体含义与取值参见枚举常量`EBusinessType` |
| order_side | int | 买入卖出委托方向，具体含义与取值参见枚举常量`EOrderSide` |
| effect | int | 开仓平仓委托方向，具体含义与取值参见枚举常量`EPositionEffect` |
| order_price | float | 委托价格，适用于限价单 |
| order_qty | int | 委托数量 |
| order_id | str | 订单编号，由服务端自动生成 |
| discretion_price | float | 市价委托转限价委托时采用的限价 |
| send_time | datetime.datetime | 发送时间，由系统自动生成 |

### 2.1.9 StockPosition - 持仓信息
| 属性 | 类型 | 说明 |
| --- | --- | --- |
| account | str | 账户ID |
| market | str | 交易所代码 |
| code | str | 标的 |
| total_qty | int | 持有总数量 |
| today_qty | int | 今日新增持有数量 |
| open_avg_price | float | 成本价格 |
| surplus_close_qty | int | 可平仓数量 |
| frozen_qty | int | 冻结数量 |

### 2.1.10 TradeReport - 成交回报信息
| 属性 | 类型 | 说明 |
| --- | --- | --- |
| order_id | str | 对应的委托订单编号 |
| client_ref | str | 对应的本地订单编号 |
| account | str | 账户ID |
| market | str | 交易所代码 |
| code | str | 标的 |
| traded_id | str | 成交编号 |
| traded_index | int | 对应委托的成交序号，从0递增 |
| exec_type | int | 成交回报类型，具体含义与取值参见枚举常量`EExecType` |
| traded_qty | int | 成交数量 |
| traded_price | float | 成交价格 |
| fee | float | 成交费用 |
| transact_time | datetime.datetime | 执行报送时间 |

### 2.1.11 UserRegisterInfo - 账户注册回复信息
| 属性 | 类型 | 说明 |
| --- | --- | --- |
| strategy_id | str | 策略ID |
| account | str | 账户ID |
| passwd | str | 账户密码 |
| acc_status | int | 账户状态码，具体含义与取值参见枚举常量`ERegisterRet` |

## 2.2 Spi响应类
### 2.2.1 AccDepositAck - 账户入金响应
| 属性 | 类型 | 说明 |
| --- | --- | --- |
| acc_margin | AccMargin | 账户资产信息 |
| error_code | int | 入金错误返回码，具体含义与取值参见枚举常量`EDepositRetCode` |

### 2.2.2 QryHisAccAck - 历史资产信息查询
| 属性 | 类型 | 说明 |
| --- | --- | --- |
| acc_margins | list[AccMargin] | 账户历史资产信息列表 |

### 2.2.3 QryHisDepositAck - 历史入金信息查询
| 属性 | 类型 | 说明 |
| --- | --- | --- |
| his_deposits | list[HisDeposit] | 账户历史入金信息列表 |

### 2.2.4 LoginAck - 登录响应
| 属性 | 类型 | 说明 |
| --- | --- | --- |
| login_info | LoginInfo | 登录信息 |
| ret_code | int | 登录成功情况返回码，具体含义与取值参见枚举常量`ELoginRetCode` |

### 2.2.5 QueryOrdersAck - 委托查询响应
| 属性 | 类型 | 说明 |
| --- | --- | --- |
| order_reports | list[OrdReport] | 委托回报信息列表 |

### 2.2.6 QueryTradesAck - 交易明细查询响应
| 属性 | 类型 | 说明 |
| --- | --- | --- |
| trade_reports | list[TradeReport] | 成交回报信息列表 |

### 2.2.7 QueryPositionsAck - 持仓查询响应
| 属性 | 类型 | 说明 |
| --- | --- | --- |
| positions | list[StockPosition] | 持仓信息列表 |

### 2.2.8 RegisterAck - 注册响应
| 属性 | 类型 | 说明 |
| --- | --- | --- |
| registe_info | UserRegisterInfo | 账户注册回复信息 |
| regist_code | int | 注册完成情况返回码，具体含义与取值参见枚举常量`ERegisterRet` |


---

## 2.3 枚举常量
### 2.3.1 EAccStatus - 账户状态码
```python
KAccStatus_Unknown    = 0 
KAccStatus_Normal     = 1  # 正常
KAccStatus_WrittenOff = 2  # 已注销
KAccStatus_Disable    = 3  # 已禁用
```
### 2.3.2 EBusinessType - 业务类型
```python
KBusinessType_Unknown  =  0
KBusinessType_NORMAL   =  1  # 普通交易
```
### 2.3.3 ECxRejReasonType - 撤单拒绝原因类型
```python
  KCxRejReasonType_TooLateCancel   =  0  # 撤单太晚（Too late to cancel）
  KCxRejReasonType_UnknowOrder     =  1  # 未知订单（Unknown order）
  KCxRejReasonType_Broker          =  2  # 自选原因（Broker / Exchange Option）
  KCxRejReasonType_PendingCancel   =  3  # 正在撤消（Order already in Pending Cancel or Pending Replace status）
  KCxRejReasonType_Duplicate       =  6  # 收到重复单（Duplicate ClOrdID received）
  KCxRejReasonType_Other           = 99  # 其他（other）
```
### 2.3.4 EDepositRetCode - 入金错误返回码
```python
KDepositReCode_Unknown        = 0
KDepositReCode_NoError        = 1
KDepositReCode_NoEnoughCash   = 2  # 资金不足
KDepositReCode_CapitalOverrun = 3  # 资金超限9*10^17(added 20170410)
KDepositReCode_IllegalAccount = 4  # 非法交易账号(added 20170518)
KDepositReCode_IllegalPara    = 5  # 请求参数错误(amount==0, type is unknow)
```
### 2.3.5 EExecType - 成交回报类型
```python
KExecType_Unknown        =  0  # 未知
KExecType_New            =  1  # 已报
KExecType_DoneForDay     =  3  # 当日已完成
KExecType_Canceled       =  4  # 已撤销
KExecType_Replaced       =  5  # 已修改
KExecType_PendingCancel  =  6  # 待撤销
KExecType_Stopped        =  7  # 已停止(已终止)
KExecType_Rejected       =  8  # 已拒绝
KExecType_Suspended      =  9  # 挂起(已延缓)
KExecType_PendingNew     = 65  #  'A' 待报
KExecType_Calculated     = 66  #  'B' 已计算
KExecType_Expired        = 67  #  'C' 过期
KExecType_Restated       = 68  #  'D' 重置(主动发送)
KExecType_PendingReplace = 69  #  'E' 待修改
KExecType_Trade          = 70  #  'F' 成交或部分成交
KExecType_TradeCorrect   = 71  #  'G' 成交更正
KExecType_TradeCancel    = 72  #  'H' 成交撤销
KExecType_OrderStatus    = 73  #  'I' 委托状态
```
### 2.3.6 ELoginRetCode - 登录成功情况返回码
```python
KLoginReCode_Unknown       = 0  # 未知错误
KLoginReCode_LoginSucc     = 1  # 登录成功
KLoginReCode_UnknownAcc    = 2  # 未知账号 或 密码错误
KLoginReCode_AccUnNormal   = 3  # 非正常状态的账号(已注销/已禁用)
```
### 2.3.7 EOrderRejectReason - 委托拒绝原因
```python
KOrderRejectReason_NoError           =   0 
KOrdRejReason_UnknownSymbol          =   1   # 证券代码非法（Unknown symbol）
KOrdRejReason_ExchangeClosed         =   2   # 交易关闭（Exchange closed）
KOrdRejReason_OrdExceedsLimit        =   3   # 订单超过限价（Order exceeds limit）
KOrdRejReason_TooLateEnter           =   4   # 订单太迟（Too late to enter）
KOrdRejReason_UnknowOrd              =   5   # 未知订单（Unknown Order）
KOrdRejReason_DuplicateOrd           =   6   # 重复订单（ Duplicate Order (e.g. dupe ClOrdID)）
KOrdRejReason_StaleOrd               =   8   # 失效订单（Stale Order）
KOrdRejReason_InvalidAcc             =  10   # 无效账户（Invalid Investor ID）
KOrdRejReason_UnsupportedOrdChara    =  11   # 不支持的订单特征（Unsupported order characteristic）
KOrdRejReason_IncorrectQty           =  13   # 数量错误（Incorrect quantity）
KOrdRejReason_UnknownAcc             =  15   # 未知账号（Unknown account(s)）
KOrdRejReason_NotEnoughPosition      =  16   # 持仓不足
KOrdRejReason_QtyNonMultipleBuyUnit  =  103  # 买订单数量不是SJSXX.XXBLDW 的整数倍；或
KOrdRejReason_PriceNonMultipleTick   =  106  # 委托价格不是SJSXX.XXJGDW 的整数倍
KOrdRejReason_SecuritiesTrading      =  102  # 证券停牌(获取行情失败)
KOrdRejReason_LackDeposit            =  117  # 参与者业务单元资金可用量不足
KOrdRejReason_PriceError             =  125  # 价格错误
KOrdRejReason_NonTradingTime         =  204  # 非交易时间（This stock is not in tradinghours）
KOrdRejReason_PriceZero              =  219  # 申报价不能为零（Price may not be 0 fora limit order）
```
### 2.3.8 EOrderSide - 买卖方向
```python
KOrderDirection_Unknown         =  0
KOrderDirection_Buy             = 49  # '1'买
KOrderDirection_Sell            = 50  # '2'卖
KOrderDirection_Call            = 68  # 'D' 认购
KOrderDirection_Callable        = 69  # 'E' 赎回
KOrderDirection_FinancingToBuy  = 70  # 'F' 融资买入(融入或出借)
KOrderDirection_FinancingToSell = 71  # 'G' 融资卖出(融出或借入)
```
### 2.3.9 EOrderStatus - 委托状态
```python
KOrderStatus_Unknown            =  0  # 未知
KOrderStatus_New                =  1  # 已报
KOrderStatus_PartiallyFilled    =  2  # 部成
KOrderStatus_Filled             =  3  # 已成
KOrderStatus_DoneForDay         =  4  # 当日已完成
KOrderStatus_Canceled           =  5  # 已撤
KOrderStatus_PendingCancel      =  6  # 待撤
KOrderStatus_Stopped            =  7  # 停止
KOrderStatus_Rejected           =  8  # 拒绝
KOrderStatus_Suspended          =  9  # 挂起
KOrderStatus_PendingNew         = 65  # 'A'待报
KOrderStatus_Calculated         = 66  # 'B'计算
KOrderStatus_Expired            = 67  # 'C'已过期
KOrderStatus_AcceptedForBidding = 68  # 'D'接受竞价
KOrderStatus_PendingReplace     = 69  # 'E'待修改
```
### 2.3.10 EOrderType - 委托类型
```python
KOrderType_Unknown               =  0
KOrderType_Market                =  1  # (market)
KOrderType_Limit                 =  2  # 限价委托
KOrderType_Stop                  =  4  # 止损
KOrderType_Best_5_Then_Cancel    =  7  # 市价最优五档剩余撤销(best 5 then cancel)
KOrderType_Best_5_Then_Limit     =  8  # 市价最优五档剩余转限价(best 5 then limit)
KOrderType_Immediately_Or_Cancel =  9  # 市价即时成交剩余撤销(immediately or cancel)
KOrderType_All_Or_Cancel         = 10  # 市价即时全部成交或撤销(immediately or cancel)
KOrderType_Market_Then_Limit     = 75  # 'K'市价剩余转限价(market then limit)
KOrderType_Best_Of_Party         = 85  # 'U'本方最优价格(best of party)
KOrderType_Best_Of_Conterparty   = 86  # 'V'对方最优价格(best of counterparty)
```
### 2.3.11 EPositionEffect - 开平方向
```python
KPositionEffect_Unknown         =  0;
KPositionEffect_Open            = 48  # '0';开仓
KPositionEffect_Close           = 49  # '1';平仓
KPositionEffect_ForceClose      = 50  # '2';强平
KPositionEffect_CloseToday      = 51  # '3';平今
KPositionEffect_CloseYesterday  = 52  # '4';平昨
```
### 2.3.12 ERegisterRet - 注册完成情况返回码
```python
KRegisterRet_Unknown         = 0  # 未知错误
KRegisterRet_Success         = 1  # 注册成功
KRegisterRet_ReRegister      = 2  # 重复注册
KRegisterRet_InvalidStrategy = 3  # 无效或非法 strategy_id
```

---

# 3 Api介绍
## 3.1 使用须知
### 3.1.1 基本函数 - Start
`Start`函数用于初始化Api实例对象、连接模拟柜台服务、注册回调Spi（用于异步接收服务器的响应消息）、设置日志输出文件等。
**函数签名：**
```python
Start(self, server_addr: str, spi: AztVeSpi = None, hb_times: int = 3, hb_interval: int = 5)
```
**参数：**

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| server_addr | str | 无，必填 | 模拟柜台服务地址，由[aztquant.com](https://www.aztquant.com)提供 |
| spi | AztVeSpi | None | 回调Spi类或实例，用于异步接收服务器的响应消息 |
| hb_times | int | 3 | 心跳检测次数，默认3次，即若连续3次检测与服务器连接异常，即可认为连接中断 |
| hb_interval | int | 5 | 心跳检测间隔，单位：秒，默认5秒，即每隔5秒确认一次与服务器的连接是否正常。建议`hb_interval≥3`，避免心跳检测占用过多资源 |

**返回：**

- 如果初始化成功，返回`None`；如果初始化失败，返回可`raise`的`error`

**提示：**

- 用户只有在实现了`AztVeSpi`回调类时才需要设置spi参数，反之则不需要关注
- 参数spi既可以填入`AztVeSpi`类，也可以填入`AztVeSpi()`类实例，如**3.1.3 使用示例**所示
### 3.1.2 基本函数 - Join
用于阻塞主线程。由于客户端会开启一个线程用于接收服务器异步响应信息，当用户通过注册Spi接收消息时，如果主线程过早退出，可能会导致客户端无法正确接收响应信息，因此用户必须主动阻塞主线程，如**3.1.3 使用示例**所示
**函数签名：**
```python
def Join(self, timeout: int=None)
```
**参数：**

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| timeout | int | None | 阻塞时间，`None`表示一直阻塞，单位：秒 |

**提示：**

- 只有在需要异步接收响应消息（实现了Spi）的情况下才需要阻塞主线程
### 3.1.3 基本函数使用示例

```python
import AztVe


# 以继承的方式实现回调Spi -----------------------------------------------------------
class MySpi(AztVe.AztVeSpi):
    def onLogin(self, msg):
        print(msg)

    ......


if __name__ == '__main__':
    # 1 实例化Api，传入虚拟交易所服务的地址 ------------------------------------------
    myapi = AztVe.AztVeApi()

    # 2 初始化Api，设置模拟柜台服务地址，注册Spi，设置心跳检测参数----------------------
    init_error = myapi.Start(server_addr="tcp://xxx.xxx.xxx.xxx:xxxx", spi=MySpi, hb_times=3, hb_interval=5)
    # 注：实现了MySpi才需要填spi参数，并且既可以直接传入类，也可以传入类实例，如：
    # spi=MySpi()
    if init_error:  # 如果初始化失败，报错
        raise init_error

    # 3 执行一些你需要做的工作 ------------------------------------------------------
    # ......

    # 4 阻塞当前主线程(实现了Spi才需要阻塞) -----------------------------------------
    myapi.Join(timeout=1000)  # 阻塞1000秒

```
### 3.1.4 日志记录功能
Api基于logging模块实现日志记录功能，其中`log`函数可以代替`print`函数使用。默认情况下`log`函数会将消息直接打印到命令行终端中，此外用户也可以在使用`init_azt_log`函数初始化Api时设置`log_file`参数指定日志输出文件路径，这样消息就会被记录到指定的文件中，而不会直接打印出来。
**函数签名：**
```python
# 日志初始化函数
def init_azt_log(log_file: str=None, **kwargs)
# 日志记录函数
def debug(*msgs)  # 记录测试信息，日志等级（10）
def log(*msgs)  # 记录正常信息，日志等级（20）
def warning(*msgs)  # 记录警告信息，日志等级（30）
def error(*msgs)  # 记录错误信息，日志等级（40）
```
**示例：**
```python
import AztVe
# 初始化日志，日志输出到"log.txt"文件中，日志记录等级设置为debug（10）以上
AztVe.init_azt_log(log_file='log.txt', log_debug=True)

AztVe.debug("hello", "world")  # 记录测试信息
AztVe.log("hello", "world", "!")  # 记录正常信息
AztVe.warning("world", "hello", "!")  # 记录警告信息
AztVe.error("hello", "!", "world")  # 记录错误信息
```
**示例结果：**
```
[2022-06-21 14:31:57] [测试] hello world
[2022-06-21 14:31:57] hello world !
[2022-06-21 14:31:57] [警告] world hello !
[2022-06-21 14:31:57] [错误] hello ! world
```
**提示：**

- 默认日志输出到命令行终端，日志记录等级为log（20）
- 只有需要将日志输出到文件或者修改日志记录等级，才需要调用`init_azt_log`函数
- 案例中`init_azt_log`函数的参数log_debug=True表示将日志等级设为debug（10）以上，即测试信息、正常信息、警告信息和错误信息都会被记录；默认log_info=True，即默认记录除测试信息外所有信息
- 日志等级调整参数有4个，分别为`log_debug=True`、`log_info=True`、`log_warning=True`和`log_error=True`，四者不可共存，用户只能四选一填入`init_azt_log`函数中；若同时出现，则取等级最高的进行设置

---

### 3.1.5 概念 - 同步模式与异步模式
在Api中，凡是有`sync`参数的接口，都同时支持同步模式和异步模式，否则就只支持异步模式。

- 同步模式时，服务器响应消息会作为接口返回值直接返回，因此用户调用接口后需要等待返回值
- 而异步模式时，服务器所有的响应消息都会通过Spi告知用户，因此用户需要实现用于接收消息的回调Spi，调用接口后不需要等待返回值

所有接口接口默认`sync=False`，即默认异步模式，用户可以设置`sync=True`来开启同步模式（仅限支持`sync`参数的接口，如查询类接口等）；开启同步模式时，用户依旧可以通过实现Spi来接收消息，同一个响应消息会先通过Spi回调通知，再作为返回值通过Api接口返回。
具体区别和使用，参见各接口的使用示例。

---

## 3.2 账户管理
### 3.2.1 RegisterAccount - 注册模拟柜台账户
用户可以使用在网站上申请获得的策略ID和策略校验码，通过本接口注册模拟柜台账户，每个策略ID只能注册一个模拟柜台账户。
**函数签名：**
```python
def RegisterAccount(self, strategy_id: str, strategy_check_code: str, sync: bool = False, timeout: int = None)
```
**参数：**

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| strategy_id | str | 无，必填 | 策略ID |
| strategy_check_code | str | 无，必填 | 策略校验码 |
| sync | bool | False | 是否开启同步模式 |
| timeout | int | None | 同步模式时超时时间，超时返回`None`，单位：秒 |

**返回：**

- 当`sync=False`时，返回值永远为`None`
- 当`sync=True`时，返回`RegisterAck`信息；若设置了超时时间，超时无响应则返回`None`

**示例1 - 同步模式**

```python
import AztVe  # 导入客户端库

# 1 获取策略ID和策略校验码并填入 --------------------------------------------------
strategy_id = "xxxx"  # 策略ID
strategy_check_code = "xxxx"  # 策略校验码

# 2 初始化Api -------------------------------------------------------------------
myapi = AztVe.AztVeApi()  # 实例化Api
init_error = myapi.Start(server_addr="tcp://xxx.xxx.xxx.xxx:xxxx")  # 初始化Api
if init_error:  # 如果初始化失败，报错
    raise init_error

# 3 注册账户,并直接返回结果 -------------------------------------------------------
ret_register = myapi.RegisterAccount(strategy_id, strategy_check_code, sync=True)
AztVe.log("注册结果：", ret_register)
```
**示例2 -  异步模式**

```python
import AztVe  # 导入客户端库

# 1 获取策略ID和策略校验码并填入 -------------------------------------------------
strategy_id = "xxxx"  # 策略ID
strategy_check_code = "xxxx"  # 策略校验码


# 2 实现回调Spi ----------------------------------------------------------------
class MySpi(AztVe.AztVeSpi):
    def onRegisterAccount(self, msg):
        AztVe.log("注册结果：", msg)


# 3 初始化Api ------------------------------------------------------------------
myapi = AztVe.AztVeApi()  # 实例化Api
# 初始化Api，注册Spi，直接打印日志
init_error = myapi.Start(server_addr="tcp://xxx.xxx.xxx.xxx:xxxx", spi=MySpi)
if init_error:  # 如果初始化失败，报错
    raise init_error

# 4 注册账户 -------------------------------------------------------------------
myapi.RegisterAccount(strategy_id, strategy_check_code)

# 5 阻塞主线程等待结果返回 ------------------------------------------------------
myapi.Join()
```
**示例结果**
```
[2022-06-20 17:41:45] 注册结果: RegisterAck(registe_info=UserRegisterInfo(strategy_id='8ba79550-73a6-4a91-a62f-23b184e2e970', account='600001', passwd='1TwGXh9o', acc_status=1), regist_code=2)
```
**提示：**

- 策略ID和策略校验码可以在[个人中心]()处生成获取（待修改）

---

### 3.2.2 Login - 登录
**函数签名：**
```python
def Login(self, account: str, passwd: str, sync: bool = False, timeout: int = None)
```
**参数：**

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| account | str | 无，必填 | 账户ID |
| passwd | str | 无，必填 | 账户密码 |
| sync | bool | False | 是否开启同步模式 |
| timeout | int | None | 同步模式时超时时间，超时返回`None`，单位：秒 |

**返回：**

- 当`sync=False`时，返回值永远为`None`
- 当`sync=True`时，返回`LoginAck`信息；若设置了超时时间，超时无响应则返回`None`

**示例1 - 同步模式：**

```python
import AztVe  # 导入客户端库

# 1 获取账户ID和密码并填入 ------------------------------------------------------
account = "xxxx"  # 账户ID
passwd = "xxxx"  # 账户密码

# 2 初始化Api -------------------------------------------------------------------
myapi = AztVe.AztVeApi()  # 实例化Api
init_error = myapi.Start(server_addr="tcp://xxx.xxx.xxx.xxx:xxxx")  # 初始化Api
if init_error:  # 如果初始化失败，报错
    raise init_error

# 3 登录Api,设置5秒超时 ----------------------------------------------------------
ret_login = myapi.Login(account, passwd, sync=True, timeout=5)
if ret_login is None:  # 如果登陆失败,直接报错终止程序
    raise Exception("服务器未响应！")
AztVe.log("登录结果：", ret_login)
```
**示例2 - 异步模式：**

```python
import AztVe  # 导入客户端库

# 1 获取账户ID和密码并填入 ------------------------------------------------------
account = "xxxx"  # 账户ID
passwd = "xxxx"  # 账户密码


# 2 实现回调Spi ----------------------------------------------------------------
class MySpi(AztVe.AztVeSpi):
    # 实现登录响应信息回调
    def onLogin(self, msg):
        AztVe.log("登录结果：", msg)


# 3 初始化Api ------------------------------------------------------------------
myapi = AztVe.AztVeApi()  # 实例化Api
# 初始化Api，注册Spi，直接打印日志
init_error = myapi.Start(server_addr="tcp://xxx.xxx.xxx.xxx:xxxx", spi=MySpi)
if init_error:  # 如果初始化失败，报错
    raise init_error

# 4 登录账户 -------------------------------------------------------------------
myapi.Login(account, passwd)

# 5 阻塞主线程等待结果返回 ------------------------------------------------------
myapi.Join()
```
**示例结果：**
```
[2022-06-20 17:41:45] 登录结果: LoginAck(login_info=LoginInfo(account='600001', trading_day='', exchange_name='', exchange_time=datetime.datetime(2022, 6, 20, 17, 41, 47)), ret_code=1)
```

---

### 3.2.3 Logout - 退出登录
**函数签名：**
```python
def Logout(self)
```
**示例：**

```python
import AztVe  # 导入客户端库

# 1 获取账户ID和密码并填入 ------------------------------------------------------
account = "xxxx"  # 账户ID
passwd = "xxxx"  # 账户密码

# 2 初始化Api -------------------------------------------------------------------
myapi = AztVe.AztVeApi()  # 实例化Api
init_error = myapi.Start(server_addr="tcp://xxx.xxx.xxx.xxx:xxxx")  # 初始化Api
if init_error:  # 如果初始化失败，报错
    raise init_error

# 3 登录Api,设置5秒超时 ----------------------------------------------------------
ret_login = myapi.Login(account, passwd, sync=True, timeout=5)
if ret_login is None:  # 如果登陆失败,直接报错终止程序
    raise Exception("服务器未响应！")
AztVe.log("已成功登录！")
# 4 成功登录后直接退出登录 -------------------------------------------------------
myapi.Logout()
```
```
[2022-06-20 17:41:45] 已成功登录！
[2022-06-20 17:41:46] 已退出登录，欢迎下次使用！

进程已结束，退出代码为 0
```
**提示：**

- 只有在登录之后才需要也才能退出登录，退出登录后程序会直接结束，服务器不会再返回任何消息

---

### 3.2.4 DepositAsset - 账户入金
每个模拟柜台账户在刚创建时都会有`200,000,000.00`总资金，在使用过程中如果资金不足，用户也可以自行通过入金的方式添加总资金。
**函数签名：**
```python
def DepositAsset(self, amount: float, sync: bool = False, timeout: int = None)
```
**参数：**

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| amount | float | 无，必填 | 入金总额 |
| sync | bool | False | 是否开启同步模式 |
| timeout | int | None | 同步模式时超时时间，超时返回`None`，单位：秒 |

**返回：**

- 当`sync=False`时，返回值永远为`None`
- 当`sync=True`时，返回`AccDepositAck`信息；若设置了超时时间，超时无响应则返回`None`

**示例1 - 同步模式：**

```python
import AztVe  # 导入客户端库

# 1 获取账户ID和密码并填入 ------------------------------------------------------
account = "xxxx"  # 账户ID
passwd = "xxxx"  # 账户密码

# 2 初始化Api -------------------------------------------------------------------
myapi = AztVe.AztVeApi()  # 实例化Api
init_error = myapi.Start(server_addr="tcp://xxx.xxx.xxx.xxx:xxxx")  # 初始化Api
if init_error:  # 如果初始化失败，报错
    raise init_error

# 3 登录Api,设置5秒超时 ----------------------------------------------------------
ret_login = myapi.Login(account, passwd, sync=True, timeout=5)
if ret_login is None:  # 如果登陆失败,直接报错终止程序
    raise Exception("服务器未响应！")

# 4 账户入金20w,并直接返回结果 ----------------------------------------------------
ret_accdeposit = myapi.DepositAsset(amount=200000, sync=True)
AztVe.log("入金结果：", ret_accdeposit)
```
**示例2 - 异步模式：**

```python
import AztVe  # 导入客户端库

# 1 获取账户ID和密码并填入 ------------------------------------------------------
account = "xxxx"  # 账户ID
passwd = "xxxx"  # 账户密码


# 2 实现回调Spi ----------------------------------------------------------------
class MySpi(AztVe.AztVeSpi):
    # 2.1 先实现登录响应信息回调,登陆后使用Api入金20w
    def onLogin(self, msg):
        self.api.DepositAsset(200000)

    # 2.2 实现入金响应信息回调
    def onDepositAsset(self, msg):
        AztVe.log("入金结果：", msg)


# 3 初始化Api ------------------------------------------------------------------
myapi = AztVe.AztVeApi()  # 实例化Api
# 初始化Api，注册Spi，直接打印日志
init_error = myapi.Start(server_addr="tcp://xxx.xxx.xxx.xxx:xxxx", spi=MySpi)
if init_error:  # 如果初始化失败，报错
    raise init_error

# 4 登录账户 -------------------------------------------------------------------
myapi.Login(ret_userinfo.account, ret_userinfo.passwd)

# 5 阻塞主线程等待结果返回 ------------------------------------------------------
myapi.Join()
```
**示例结果：**
```
[2022-06-20 17:41:45] 入金结果: AccDepositAck(acc_margin=AccMargin(account='600001', total_amount=206788950.0, available_amount=206779347.0, deposit=3000000.0, open_balance=203788950.0, trade_frozen_margin=9603.0, position_market_amount=0.0, total_buy_amount=11050.0, total_buy_fee=0.0, total_sell_amount=0.0, total_sell_fee=0.0), error_code=1)
```
**提示：**

- 使用入金接口必须先登录
## 3.3 查询方法
### 3.3.1 QueryAccountInfo - 查询账户信息
**函数签名：**
```python
def QueryAccountInfo(self, strategy_id: str = None, strategy_check_code: str = None, account: str = None, passwd: str = None, sync: bool = False, timeout: int = None)
```
**参数：**

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| strategy_id | str | None | 策略ID |
| strategy_check_code | str | None | 策略校验码 |
| account | str | None | 账户ID |
| passwd | str | None | 账户密码 |
| sync | bool | False | 是否开启同步模式 |
| timeout | int | None | 同步模式时超时时间，超时返回`None`，单位：秒 |

**返回：**

- 当`sync=False`时，返回值永远为`None`
- 当`sync=True`时，返回`UserRegisterInfo`信息；若设置了超时时间，超时无响应则返回`None`

**示例1 - 同步模式：**

```python
import AztVe  # 导入客户端库

# 1 获取策略ID和策略校验码并填入 --------------------------------------------------
strategy_id = "xxxx"  # 策略ID
strategy_check_code = "xxxx"  # 策略校验码

# 2 初始化Api -------------------------------------------------------------------
myapi = AztVe.AztVeApi()  # 实例化Api
init_error = myapi.Start(server_addr="tcp://xxx.xxx.xxx.xxx:xxxx")  # 初始化Api
if init_error:  # 如果初始化失败，报错
    raise init_error

# 3 查询账户,并直接返回结果 -------------------------------------------------------
ret_userinfo = myapi.QueryAccountInfo(strategy_id, strategy_check_code, sync=True)
AztVe.log("账户查询结果：", ret_userinfo)
```
**示例2 - 异步模式：**

```python
import AztVe  # 导入客户端库

# 1 获取策略ID和策略校验码并填入 -------------------------------------------------
strategy_id = "xxxx"  # 策略ID
strategy_check_code = "xxxx"  # 策略校验码


# 2 实现回调Spi ----------------------------------------------------------------
class MySpi(AztVe.AztVeSpi):
    def onQueryAccountInfo(self, msg):
        AztVe.log("账户查询结果：", msg)


# 3 初始化Api ------------------------------------------------------------------
myapi = AztVe.AztVeApi()  # 实例化Api
# 初始化Api，注册Spi，直接打印日志
init_error = myapi.Start(server_addr="tcp://xxx.xxx.xxx.xxx:xxxx", spi=MySpi)
if init_error:  # 如果初始化失败，报错
    raise init_error

# 4 查询账户 -------------------------------------------------------------------
myapi.QueryAccountInfo(strategy_id, strategy_check_code)

# 5 阻塞主线程等待结果返回 ------------------------------------------------------
myapi.Join()
```
**示例结果：**
```
[2022-06-20 17:41:45] 账户查询结果: UserRegisterInfo(strategy_id='8ba79550-73a6-4a91-a62f-23b184e2e970', account='600001', passwd='1TwGXh9o', acc_status=1)
```
**提示：**

- 用户既可以填写`strategy_id`和`strategy_check_code`查询，也可以填写`account`和`passwd`来查询

---

### 3.3.2 QueryAsset - 查询账户资产信息
**函数签名：**
```python
def QueryAsset(self, sync: bool = False, timeout: int = None)
```
**参数：**

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| sync | bool | False | 是否开启同步模式 |
| timeout | int | None | 同步模式时超时时间，超时返回`None`，单位：秒 |

**返回：**

- 当`sync=False`时，返回值永远为`None`
- 当`sync=True`时，返回`AccMargin`信息；若设置了超时时间，超时无响应则返回`None`

**示例1 - 同步模式：**

```python
import AztVe  # 导入客户端库

# 1 获取账户ID和密码并填入 ------------------------------------------------------
account = "xxxx"  # 账户ID
passwd = "xxxx"  # 账户密码

# 2 初始化Api -------------------------------------------------------------------
myapi = AztVe.AztVeApi()  # 实例化Api
init_error = myapi.Start(server_addr="tcp://xxx.xxx.xxx.xxx:xxxx")  # 初始化Api
if init_error:  # 如果初始化失败，报错
    raise init_error

# 3 登录Api,设置5秒超时 ----------------------------------------------------------
ret_login = myapi.Login(account, passwd, sync=True, timeout=5)
if ret_login is None:  # 如果登陆失败,直接报错终止程序
    raise Exception("服务器未响应！")

# 4 查询账户资产信息,并直接返回结果 -----------------------------------------------
ret_asset = myapi.QueryAsset(sync=True)
AztVe.log("账户资产信息查询结果：", ret_asset)
```
**示例2 - 异步模式：**

```python
import AztVe  # 导入客户端库

# 1 获取账户ID和密码并填入 ------------------------------------------------------
account = "xxxx"  # 账户ID
passwd = "xxxx"  # 账户密码


# 2 实现回调Spi ----------------------------------------------------------------
class MySpi(AztVe.AztVeSpi):
    # 2.1 先实现登录响应信息回调,登陆后查询账户资产信息
    def onLogin(self, msg):
        self.api.QueryAsset()

    # 2.2 实现查询账户资产信息回调
    def onQueryAsset(self, msg):
        AztVe.log("账户资产信息查询结果：", msg)


# 3 初始化Api ------------------------------------------------------------------
myapi = AztVe.AztVeApi()  # 实例化Api
# 初始化Api，注册Spi，直接打印日志
init_error = myapi.Start(server_addr="tcp://xxx.xxx.xxx.xxx:xxxx", spi=MySpi)
if init_error:  # 如果初始化失败，报错
    raise init_error

# 4 登录账户 -------------------------------------------------------------------
myapi.Login(account, passwd)

# 5 阻塞主线程等待结果返回 ------------------------------------------------------
myapi.Join()
```
**示例结果：**
```
[2022-06-20 17:41:45] 账户资产信息查询结果: AccMargin(account='xxxx', total_amount=206788950.0, available_amount=206779347.0, deposit=3000000.0, open_balance=203788950.0, trade_frozen_margin=9603.0, position_market_amount=0.0, total_buy_amount=11050.0, total_buy_fee=0.0, total_sell_amount=0.0, total_sell_fee=0.0)
```
**提示：**

- 查询账户资产信息必须先登录

---

### 3.3.3 QueryHistoryAsset - 查询账户历史资产信息
**函数签名：**
```python
def QueryHistoryAsset(self, date: datetime.datetime = None, sync: bool = False, timeout: int = None)
```
**参数：**

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| date | datetime.datetime | None | 指定查询的历史日期，若无指定则查询账户所有的历史资产信息 |
| sync | bool | False | 是否开启同步模式 |
| timeout | int | None | 同步模式时超时时间，超时返回`None`，单位：秒 |

**返回：**

- 当`sync=False`时，返回值永远为`None`
- 当`sync=True`时，返回`QryHisAccAck`信息；若设置了超时时间，超时无响应则返回`None`

**示例1 - 同步模式：**

```python
import AztVe  # 导入客户端库

# 1 获取账户ID和密码并填入 ------------------------------------------------------
account = "xxxx"  # 账户ID
passwd = "xxxx"  # 账户密码

# 2 初始化Api -------------------------------------------------------------------
myapi = AztVe.AztVeApi()  # 实例化Api
init_error = myapi.Start(server_addr="tcp://xxx.xxx.xxx.xxx:xxxx")  # 初始化Api
if init_error:  # 如果初始化失败，报错
    raise init_error

# 3 登录Api,设置5秒超时 ----------------------------------------------------------
ret_login = myapi.Login(account, passwd, sync=True, timeout=5)
if ret_login is None:  # 如果登陆失败,直接报错终止程序
    raise Exception("服务器未响应！")

# 4 查询账户历史资产信息,并直接返回结果 -----------------------------------------------
ret_asset = myapi.QueryHistoryAsset(sync=True)
AztVe.log("账户历史资产信息查询结果：", ret_asset)
```
**示例2 - 异步模式：**

```python
import AztVe  # 导入客户端库

# 1 获取账户ID和密码并填入 ------------------------------------------------------
account = "xxxx"  # 账户ID
passwd = "xxxx"  # 账户密码


# 2 实现回调Spi ----------------------------------------------------------------
class MySpi(AztVe.AztVeSpi):
    # 2.1 先实现登录响应信息回调,登陆后查询账户历史资产信息
    def onLogin(self, msg):
        self.api.QueryHistoryAsset()

    # 2.2 实现查询账户历史资产信息回调
    def onQueryHistoryAsset(self, msg):
        AztVe.log("账户历史资产信息查询结果：", msg)


# 3 初始化Api ------------------------------------------------------------------
myapi = AztVe.AztVeApi()  # 实例化Api
# 初始化Api，注册Spi，直接打印日志
init_error = myapi.Start(server_addr="tcp://xxx.xxx.xxx.xxx:xxxx", spi=MySpi)
if init_error:  # 如果初始化失败，报错
    raise init_error

# 4 登录账户 -------------------------------------------------------------------
myapi.Login(account, passwd)

# 5 阻塞主线程等待结果返回 ------------------------------------------------------
myapi.Join()
```
**示例结果：**
```
[2022-06-26 11:02:24] 历史资金信息: QryHisAccAck(acc_margins=[AccMargin(account='xxxx', total_amount=203788950.0, available_amount=203788950.0, deposit=0.0, open_balance=203788950.0, trade_frozen_margin=0.0, position_market_amount=0.0, total_buy_amount=11050.0, total_buy_fee=0.0, total_sell_amount=0.0, total_sell_fee=0.0, update_time=datetime.datetime(2022, 6, 16, 0, 0)), AccMargin(account='xxxx', total_amount=203988027.0, available_amount=203988027.0, deposit=0.0, open_balance=203988027.0, trade_frozen_margin=0.0, position_market_amount=0.0, total_buy_amount=11973.0, total_buy_fee=0.0, total_sell_amount=0.0, total_sell_fee=0.0, update_time=datetime.datetime(2022, 6, 21, 0, 0)), AccMargin(account='xxxx', total_amount=204147498.0, available_amount=204147498.0, deposit=0.0, open_balance=204147498.0, trade_frozen_margin=0.0, position_market_amount=0.0, total_buy_amount=52502.0, total_buy_fee=0.0, total_sell_amount=0.0, total_sell_fee=0.0, update_time=datetime.datetime(2022, 6, 23, 0, 0))])
```
**提示：**

- 查询账户历史资产信息必须先登录

---

### 3.3.4 QueryHistoryDeposit - 查询历史入金信息
**函数签名：**
```python
def QueryHistoryDeposit(self, date: datetime.datetime = None, sync: bool = False, timeout: int = None)
```
**参数：**

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| date | datetime.datetime | None | 指定查询的历史日期，若无指定则查询账户所有的历史入金信息 |
| sync | bool | False | 是否开启同步模式 |
| timeout | int | None | 同步模式时超时时间，超时返回`None`，单位：秒 |

**返回：**

- 当`sync=False`时，返回值永远为`None`
- 当`sync=True`时，返回`QryHisDepositAck`信息；若设置了超时时间，超时无响应则返回`None`

**示例1 - 同步模式：**

```python
import AztVe  # 导入客户端库

# 1 获取账户ID和密码并填入 ------------------------------------------------------
account = "xxxx"  # 账户ID
passwd = "xxxx"  # 账户密码

# 2 初始化Api -------------------------------------------------------------------
myapi = AztVe.AztVeApi()  # 实例化Api
init_error = myapi.Start(server_addr="tcp://xxx.xxx.xxx.xxx:xxxx")  # 初始化Api
if init_error:  # 如果初始化失败，报错
    raise init_error

# 3 登录Api,设置5秒超时 ----------------------------------------------------------
ret_login = myapi.Login(account, passwd, sync=True, timeout=5)
if ret_login is None:  # 如果登陆失败,直接报错终止程序
    raise Exception("服务器未响应！")

# 4 查询账户历史入金信息,并直接返回结果 -----------------------------------------------
ret_deposit = myapi.QueryHistoryDeposit(sync=True)
AztVe.log("账户历史入金信息查询结果：", ret_deposit)
```
**示例2 - 异步模式：**

```python
import AztVe  # 导入客户端库

# 1 获取账户ID和密码并填入 ------------------------------------------------------
account = "xxxx"  # 账户ID
passwd = "xxxx"  # 账户密码


# 2 实现回调Spi ----------------------------------------------------------------
class MySpi(AztVe.AztVeSpi):
    # 2.1 先实现登录响应信息回调,登陆后查询账户历史入金信息
    def onLogin(self, msg):
        self.api.QueryHistoryDeposit()

    # 2.2 实现查询账户历史入金信息回调
    def onQueryHistoryDeposit(self, msg):
        AztVe.log("账户历史入金信息查询结果：", msg)


# 3 初始化Api ------------------------------------------------------------------
myapi = AztVe.AztVeApi()  # 实例化Api
# 初始化Api，注册Spi，直接打印日志
init_error = myapi.Start(server_addr="tcp://xxx.xxx.xxx.xxx:xxxx", spi=MySpi)
if init_error:  # 如果初始化失败，报错
    raise init_error

# 4 登录账户 -------------------------------------------------------------------
myapi.Login(account, passwd)

# 5 阻塞主线程等待结果返回 ------------------------------------------------------
myapi.Join()
```
**示例结果：**
```
[2022-06-26 11:02:24] 历史入金信息: QryHisDepositAck(his_deposits=[])
```
**提示：**

- 查询账户历史入金信息必须先登录

---

### 3.3.5 QueryOrders - 查询委托订单信息
**函数签名：**
```python
def QueryOrders(self, market: str = None, code: str = None, client_ref: str = None, order_id: str = None, unfinished: bool = False, sync: bool = False, timeout: int = None)
```
**参数：**

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| market | str | None | 交易所代码 |
| code | str | None | 标的代码 |
| client_ref | str | None | 订单编号（客户端生成） |
| order_id | str | None | 订单编号（服务端生成） |
| unfinished | bool | False | 是否只查询未结委托 |
| sync | bool | False | 是否开启同步模式 |
| timeout | int | None | 同步模式时超时时间，超时返回`None`，单位：秒 |

**返回：**

- 当`sync=False`时，返回值永远为`None`
- 当`sync=True`时，返回`QueryOrdersAck`信息；若设置了超时时间，超时无响应则返回`None`

**示例1 - 同步模式：**

```python
import AztVe  # 导入客户端库

# 1 获取账户ID和密码并填入 ------------------------------------------------------
account = "xxxx"  # 账户ID
passwd = "xxxx"  # 账户密码

# 2 初始化Api -------------------------------------------------------------------
myapi = AztVe.AztVeApi()  # 实例化Api
init_error = myapi.Start(server_addr="tcp://xxx.xxx.xxx.xxx:xxxx")  # 初始化Api
if init_error:  # 如果初始化失败，报错
    raise init_error

# 3 初始化Api ------------------------------------------------------------------
myapi = AztVe.AztVeApi()  # 实例化Api
# 初始化Api，注册Spi，直接打印日志
init_error = myapi.Start(server_addr="tcp://xxx.xxx.xxx.xxx:xxxx", spi=MySpi)
if init_error:  # 如果初始化失败，报错
    raise init_error

# 4 查询委托订单信息,并直接返回结果 -----------------------------------------------
ret_orders = myapi.QueryOrders(sync=True)
AztVe.log("委托订单信息查询结果：", ret_orders)
```
**示例2 - 异步模式：**

```python
import AztVe  # 导入客户端库

# 1 获取账户ID和密码并填入 ------------------------------------------------------
account = "xxxx"  # 账户ID
passwd = "xxxx"  # 账户密码


# 2 实现回调Spi ----------------------------------------------------------------
class MySpi(AztVe.AztVeSpi):
    # 2.1 先实现登录响应信息回调,登陆后查询委托订单信息
    def onLogin(self, msg):
        self.api.QueryOrders()

    # 2.2 实现查询委托订单信息回调
    def onQueryOrders(self, msg):
        AztVe.log("委托订单信息查询结果：", msg)


# 3 初始化Api ------------------------------------------------------------------
myapi = AztVe.AztVeApi()  # 实例化Api
# 初始化Api，注册Spi，直接打印日志
myapi.Start(server_addr="tcp://xxx.xxx.xxx.xxx:xxxx", spi=MySpi)

# 4 登录账户 -------------------------------------------------------------------
myapi.Login(account, passwd)

# 5 阻塞主线程等待结果返回 ------------------------------------------------------
myapi.Join()
```
**示例结果：**
```
[2022-06-20 17:41:46] 委托订单信息查询结果: QueryOrdersAck(order_reports=[])
```
**提示：**

- 查询委托订单信息必须先登录
- 只填写`market`参数，则查询指定交易所相关的委托订单信息
- 只填写`market`和`code`参数，则查询指定标的代码相关的委托订单信息
- 只填写`order_id`参数，则查询指定订单编号（由服务端生成）委托订单信息，此时不需要填写其他参数
- 只填写`client_ref`参数，则查询指定订单编号（由客户端生成）委托订单信息，此时不需要填写其他参数
- 如果令`unfinished=True`，则查询未结委托订单的信息，可与`market`、`code`参数配合使用
- 不填写以上参数时，则默认查询当前账户当日所有有效的委托订单信息

---

### 3.3.6 QueryTrades - 查询成交信息
**函数签名：**
```python
QueryTrades(self, market: str = None, code: str = None, order_id: str = None, trade_id: str = None, sync: bool = False, timeout: int = None)
```
**参数：**

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| market | str | None | 交易所代码 |
| code | str | None | 标的代码 |
| order_id | str | None | 订单编号 |
| trade_id | str | None | 成交编号 |
| sync | bool | False | 是否开启同步模式 |
| timeout | int | None | 同步模式时超时时间，超时返回`None`，单位：秒 |

**返回：**

- 当`sync=False`时，返回值永远为`None`
- 当`sync=True`时，返回`QueryTradesAck`信息；若设置了超时时间，超时无响应则返回`None`

**示例1 - 同步模式：**

```python
import AztVe  # 导入客户端库

# 1 获取账户ID和密码并填入 ------------------------------------------------------
account = "xxxx"  # 账户ID
passwd = "xxxx"  # 账户密码

# 2 初始化Api -------------------------------------------------------------------
myapi = AztVe.AztVeApi()  # 实例化Api
init_error = myapi.Start(server_addr="tcp://xxx.xxx.xxx.xxx:xxxx")  # 初始化Api
if init_error:  # 如果初始化失败，报错
    raise init_error

# 3 登录Api,设置5秒超时 ----------------------------------------------------------
ret_login = myapi.Login(account, passwd, sync=True, timeout=5)
if ret_login is None:  # 如果登陆失败,直接报错终止程序
    raise Exception("服务器未响应！")

# 4 查询成交信息,并直接返回结果 --------------------------------------------------
ret_trades = myapi.QueryTrades(sync=True)
AztVe.log("成交信息查询结果：", ret_trades)
```
**示例2 - 异步模式：**

```python
import AztVe  # 导入客户端库

# 1 获取账户ID和密码并填入 ------------------------------------------------------
account = "xxxx"  # 账户ID
passwd = "xxxx"  # 账户密码


# 2 实现回调Spi ----------------------------------------------------------------
class MySpi(AztVe.AztVeSpi):
    # 2.1 先实现登录响应信息回调,登陆后查询成交信息
    def onLogin(self, msg):
        self.api.QueryTrades()

    # 2.2 实现查询成交信息回调
    def onQueryTrades(self, msg):
        AztVe.log("成交信息查询结果：", msg)


# 3 初始化Api ------------------------------------------------------------------
myapi = AztVe.AztVeApi()  # 实例化Api
# 初始化Api，注册Spi，直接打印日志
init_error = myapi.Start(server_addr="tcp://xxx.xxx.xxx.xxx:xxxx", spi=MySpi)
if init_error:  # 如果初始化失败，报错
    raise init_error

# 4 登录账户 -------------------------------------------------------------------
myapi.Login(account, passwd)

# 5 阻塞主线程等待结果返回 ------------------------------------------------------
myapi.Join()
```
**示例结果：**
```
[2022-06-20 17:41:46] 成交信息查询结果: QueryTradesAck(trade_reports=[])
```
**提示：**

- 查询成交信息必须先登录
- 只填写`market`参数，则查询指定交易所相关的成交信息
- 只填写`market`和`code`参数，则查询指定标的代码相关的成交信息
- 只填写`order_id`参数，则查询指定委托订单的成交信息，此时不需要填写其他参数
- 只填写`trade_id`参数，则查询指定成交编号的成交信息，此时不需要填写其他参数
- 不填写以上参数时，则默认查询当前登录账户当日所有的成交信息

---

### 3.3.7 QueryPositions - 查询持仓信息
**函数签名：**
```python
def QueryPositions(self, market: str = None, code: str = None, sync: bool = False, timeout: int = None)
```
**参数：**

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| market | str | None | 交易所代码 |
| code | str | None | 标的代码 |
| sync | bool | False | 是否开启同步模式 |
| timeout | int | None | 同步模式时超时时间，超时返回`None`，单位：秒 |

**返回：**

- 当`sync=False`时，返回值永远为`None`
- 当`sync=True`时，返回`QueryPositionsAck`信息；若设置了超时时间，超时无响应则返回`None`

**示例1 - 同步模式：**

```python
import AztVe  # 导入客户端库

# 1 获取账户ID和密码并填入 ------------------------------------------------------
account = "xxxx"  # 账户ID
passwd = "xxxx"  # 账户密码

# 2 初始化Api -------------------------------------------------------------------
myapi = AztVe.AztVeApi()  # 实例化Api
init_error = myapi.Start(server_addr="tcp://xxx.xxx.xxx.xxx:xxxx")  # 初始化Api
if init_error:  # 如果初始化失败，报错
    raise init_error

# 3 登录Api,设置5秒超时 ----------------------------------------------------------
ret_login = myapi.Login(account, passwd, sync=True, timeout=5)
if ret_login is None:  # 如果登陆失败,直接报错终止程序
    raise Exception("服务器未响应！")

# 4 查询持仓信息,并直接返回结果 --------------------------------------------------
ret_positions = myapi.QueryPositions(sync=True)
AztVe.log("持仓信息查询结果：", ret_positions)
```
**示例2 - 异步模式：**

```python
import AztVe  # 导入客户端库

# 1 获取账户ID和密码并填入 ------------------------------------------------------
account = "xxxx"  # 账户ID
passwd = "xxxx"  # 账户密码


# 2 实现回调Spi ----------------------------------------------------------------
class MySpi(AztVe.AztVeSpi):
    # 2.1 先实现登录响应信息回调,登陆后查询持仓信息
    def onLogin(self, msg):
        self.api.QueryPositions()

    # 2.2 实现查询持仓信息回调
    def onQueryPositions(self, msg):
        AztVe.log("持仓信息查询结果：", msg)


# 3 初始化Api ------------------------------------------------------------------
myapi = AztVe.AztVeApi()  # 实例化Api
# 初始化Api，注册Spi，直接打印日志
init_error = myapi.Start(server_addr="tcp://xxx.xxx.xxx.xxx:xxxx", spi=MySpi)
if init_error:  # 如果初始化失败，报错
    raise init_error

# 4 登录账户 -------------------------------------------------------------------
myapi.Login(account, passwd)

# 5 阻塞主线程等待结果返回 ------------------------------------------------------
myapi.Join()
```
**示例结果：**
```
[2022-06-20 17:41:46] 持仓信息查询结果: QueryPositionsAck(positions=[StockPosition(account='600001', market='SHSE', code='601985', total_qty=1200, today_qty=0, open_avg_price=7.67, surplus_close_qty=1200, frozen_qty=0)])持仓信息查询结果: QueryPositionsAck(positions=[StockPosition(account='xxxx', market='SHSE', code='601985', total_qty=1200, today_qty=0, open_avg_price=7.67, surplus_close_qty=1200, frozen_qty=0])
```
**提示：**

- 查询持仓信息必须先登录
- 填写`market`和`code`参数时，查询指定标的相关的持仓信息
- 不填写以上参数时，查询当前登录账户所有的持仓信息

---

### 3.3.8 QueryHistoryOrders - 查询历史委托信息
**函数签名：**
```python
def QueryHistoryOrders(self, market: str = None, code: str = None, start_time: datetime.datetime = None, end_time: datetime.datetime = None, sync: bool = False, timeout: int = None)
```
**参数：**

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| market | str | None | 交易所代码 |
| code | str | None | 标的代码 |
| start_time | datetime.datetime | None | 查询起始时间 |
| end_time | datetime.datetime | None | 查询结束时间 |
| sync | bool | False | 是否开启同步模式 |
| timeout | int | None | 同步模式时超时时间，超时返回`None`，单位：秒 |

**返回：**

- 当`sync=False`时，返回值永远为`None`
- 当`sync=True`时，返回`QueryOrdersAck`信息；若设置了超时时间，超时无响应则返回`None`

**示例1 - 同步模式：**

```python
import AztVe  # 导入客户端库

# 1 获取账户ID和密码并填入 ------------------------------------------------------
account = "xxxx"  # 账户ID
passwd = "xxxx"  # 账户密码

# 2 初始化Api -------------------------------------------------------------------
myapi = AztVe.AztVeApi()  # 实例化Api
init_error = myapi.Start(server_addr="tcp://xxx.xxx.xxx.xxx:xxxx")  # 初始化Api
if init_error:  # 如果初始化失败，报错
    raise init_error

# 3 登录Api,设置5秒超时 ----------------------------------------------------------
ret_login = myapi.Login(account, passwd, sync=True, timeout=5)
if ret_login is None:  # 如果登陆失败,直接报错终止程序
    raise Exception("服务器未响应！")

# 4 查询历史委托订单信息,并直接返回结果 -----------------------------------------------
ret_historyorders = myapi.QueryHistoryOrders(sync=True)
AztVe.log("历史委托订单信息查询结果：", ret_historyorders)
```
**示例2 - 异步模式：**

```python
import AztVe  # 导入客户端库

# 1 获取账户ID和密码并填入 ------------------------------------------------------
account = "xxxx"  # 账户ID
passwd = "xxxx"  # 账户密码


# 2 实现回调Spi ----------------------------------------------------------------
class MySpi(AztVe.AztVeSpi):
    # 2.1 先实现登录响应信息回调,登陆后查询历史委托订单信息
    def onLogin(self, msg):
        self.api.QueryHistoryOrders()

    # 2.2 实现查询历史委托订单信息回调
    def onQueryHistoryOrders(self, msg):
        AztVe.log("历史委托订单信息查询结果：", msg)


# 3 初始化Api ------------------------------------------------------------------
myapi = AztVe.AztVeApi()  # 实例化Api
# 初始化Api，注册Spi，直接打印日志
init_error = myapi.Start(server_addr="tcp://xxx.xxx.xxx.xxx:xxxx", spi=MySpi)
if init_error:  # 如果初始化失败，报错
    raise init_error

# 4 登录账户 -------------------------------------------------------------------
myapi.Login(account, passwd)

# 5 阻塞主线程等待结果返回 ------------------------------------------------------
myapi.Join()
```
**示例结果：**
```
[2022-06-20 17:41:46] 历史委托订单信息查询结果：QueryOrdersAck(order_reports=[])
```
**提示：**

- 查询历史委托订单信息必须先登录
- 填写`market`和`code`参数时，查询指定标的相关的历史委托订单信息
- 填写`start_time`和`end_time`时，查询指定时间段内的历史委托订单信息，与`market`和`code`参数兼容
- 不填写以上参数时，默认查询当前登录账户所有的历史委托订单信息

---

### 3.3.9 QueryHistoryTrades - 查询历史成交信息
**函数签名：**
```python
def QueryHistoryTrades(self, market: str = None, code: str = None, start_time: datetime.datetime = None, end_time: datetime.datetime = None, sync: bool = False, timeout: int = None)
```
**参数：**

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| market | str | None | 交易所代码 |
| code | str | None | 标的代码 |
| start_time | datetime.datetime | None | 查询起始时间 |
| end_time | datetime.datetime | None | 查询结束时间 |
| sync | bool | False | 是否开启同步模式 |
| timeout | int | None | 同步模式时超时时间，超时返回`None`，单位：秒 |

**返回：**

- 当`sync=False`时，返回值永远为`None`
- 当`sync=True`时，返回`QueryTradesAck`信息；若设置了超时时间，超时无响应则返回`None`

**示例1 - 同步模式：**

```python
import AztVe  # 导入客户端库

# 1 获取账户ID和密码并填入 ------------------------------------------------------
account = "xxxx"  # 账户ID
passwd = "xxxx"  # 账户密码

# 2 初始化Api -------------------------------------------------------------------
myapi = AztVe.AztVeApi()  # 实例化Api
init_error = myapi.Start(server_addr="tcp://xxx.xxx.xxx.xxx:xxxx")  # 初始化Api
if init_error:  # 如果初始化失败，报错
    raise init_error

# 3 登录Api,设置5秒超时 ----------------------------------------------------------
ret_login = myapi.Login(account, passwd, sync=True, timeout=5)
if ret_login is None:  # 如果登陆失败,直接报错终止程序
    raise Exception("服务器未响应！")

# 4 查询历史成交信息,并直接返回结果 -----------------------------------------------
ret_historytrades = myapi.QueryHistoryTrades(sync=True)
AztVe.log("历史成交信息查询结果：", ret_historytrades)
```
**示例2 - 异步模式：**

```python
import AztVe  # 导入客户端库

# 1 获取账户ID和密码并填入 ------------------------------------------------------
account = "xxxx"  # 账户ID
passwd = "xxxx"  # 账户密码


# 2 实现回调Spi ----------------------------------------------------------------
class MySpi(AztVe.AztVeSpi):
    # 2.1 先实现登录响应信息回调,登陆后查询历史成交信息
    def onLogin(self, msg):
        self.api.QueryHistoryTrades()

    # 2.2 实现查询历史成交信息回调
    def onQueryHistoryTrades(self, msg):
        AztVe.log("历史成交信息查询结果：", msg)


# 3 初始化Api ------------------------------------------------------------------
myapi = AztVe.AztVeApi()  # 实例化Api
# 初始化Api，注册Spi，直接打印日志
init_error = myapi.Start(server_addr="tcp://xxx.xxx.xxx.xxx:xxxx", spi=MySpi)
if init_error:  # 如果初始化失败，报错
    raise init_error

# 4 登录账户 -------------------------------------------------------------------
myapi.Login(account, passwd)

# 5 阻塞主线程等待结果返回 ------------------------------------------------------
myapi.Join()
```
**示例结果：**
```
[2022-06-20 17:41:46] 历史成交信息查询结果: QueryTradesAck(trade_reports=[])
```
**提示：**

- 查询历史成交信息必须先登录
- 填写`market`和`code`参数时，查询指定标的相关的历史成交信息
- 填写`start_time`和`end_time`时，查询指定时间段内的历史成交信息，与`market`和`code`参数兼容
- 不填写以上参数时，默认查询当前登录账户所有的历史成交信息

---

## 3.4 交易函数
### 3.4.1 Buy - 买入委托
**函数签名：**
```python
def Buy(self, market: str, code: str, order_qty: int = 100, order_type: int = KOrderType_Market, effect: int = KPositionEffect_Open, order_price: float = None, discretion_price: float = None)
```
**参数：**

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| market | str | 无，必填 | 交易所代码 |
| code | str | 无，必填 | 标的代码 |
| order_qty | int | 100 | 委托数量，单位：股（以股票为例） |
| order_type | int | KOrderType_Market | 委托类型，默认市价委托，具体取值与含义参见`EOrderType` |
| effect | int | KPositionEffect_Open | 多空方向，默认多头，具体取值与含义参见`EPositionEffect` |
| order_price | float | None | 委托限价，适用于限价委托，保留两位小数 |
| discretion_price | float | None | 市价转限价后委托限价，适用于市转限委托，保留两位小数 |

**示例：**

```python
import AztVe  # 导入客户端库

# 1 获取账户ID和密码并填入 ------------------------------------------------------
account = "xxxx"  # 账户ID
passwd = "xxxx"  # 账户密码


# 2 实现回调Spi ----------------------------------------------------------------
class MySpi(AztVe.AztVeSpi):
    # 2.1 先实现登录响应信息回调,登陆后提交买入委托
    def onLogin(self, msg):
        # 买入1手SHSE.600259
        self.api.Buy(market="SHSE", code="600259", order_qty=100)

    # 2.2 实现委托执行回报信息回调
    def onOrderReport(self, msg):
        AztVe.log("收到委托执行回报信息：", msg)

    # 2.3 实现成交回报信息回调
    def onTradeReport(self, msg):
        AztVe.log("收到成交回报信息：", msg)


# 3 初始化Api ------------------------------------------------------------------
myapi = AztVe.AztVeApi()  # 实例化Api
# 初始化Api，注册Spi，直接打印日志
init_error = myapi.Start(server_addr="tcp://xxx.xxx.xxx.xxx:xxxx", spi=MySpi)
if init_error:  # 如果初始化失败，报错
    raise init_error

# 4 登录账户 -------------------------------------------------------------------
myapi.Login(account, passwd)

# 5 阻塞主线程等待结果返回 ------------------------------------------------------
myapi.Join()
```
**示例结果：**
```
[2022-06-20 17:41:46] 收到委托执行回报信息： OrdReport(place_order=PlaceOrder(client_ref='xxxx', sender_user='xxxx', account='xxxx', market='SHSE', code='600259', order_type=1, business_type=1, order_side=49, effect=48, order_price=0.0, order_qty=100, order_id='', discretion_price=0.0, send_time=datetime.datetime(2022, 6, 19, 16, 57, 36)), status_msg=OrdStatusMsg(order_status=8, traded_qty=0, traded_amount=0.0, total_fee=0.0, frozen_margin=0.0, frozen_price=0.0, reject_reason=204, report_time=datetime.datetime(2022, 6, 19, 16, 57, 37)))
```
**提示：**

- 买入委托前必须先登录
- 服务器对委托订单的处理时间无法保证，因此无法启用同步模式，只能采用异步模式；因此用户必须实现相关的回调函数才能收取到委托订单相关的执行消息和成交消息

---

### 3.4.2 Sell - 卖出委托
**函数签名：**
```python
def Sell(self, market: str, code: str, order_qty: int = 100, order_type: int = KOrderType_Market, effect: int = KPositionEffect_Close, order_price: float = None, discretion_price: float = None)
```
**参数：**

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| market | str | 无，必填 | 交易所代码 |
| code | str | 无，必填 | 标的代码 |
| order_qty | int | 100 | 委托数量，单位：股（以股票为例） |
| order_type | int | KOrderType_Market | 委托类型，默认市价委托，具体取值与含义参见`EOrderType` |
| effect | int | KPositionEffect_Close | 多空方向，默认空头，具体取值与含义参见`EPositionEffect` |
| order_price | float | None | 委托限价，适用于限价委托，保留两位小数 |
| discretion_price | float | None | 市价转限价后委托限价，适用于市转限委托，保留两位小数 |

**示例：**

```python
import AztVe  # 导入客户端库

# 1 获取账户ID和密码并填入 ------------------------------------------------------
account = "xxxx"  # 账户ID
passwd = "xxxx"  # 账户密码


# 2 实现回调Spi ----------------------------------------------------------------
class MySpi(AztVe.AztVeSpi):
    # 2.1 先实现登录响应信息回调,登陆后提交卖出委托
    def onLogin(self, msg):
        # 卖出1手SHSE.600259
        self.api.Sell(market="SHSE", code="600259", order_qty=100)

    # 2.2 实现委托执行回报信息回调
    def onOrderReport(self, msg):
        AztVe.log("收到委托执行回报信息：", msg)

    # 2.3 实现成交回报信息回调
    def onTradeReport(self, msg):
        AztVe.log("收到成交回报信息：", msg)


# 3 初始化Api ------------------------------------------------------------------
myapi = AztVe.AztVeApi()  # 实例化Api
# 初始化Api，注册Spi，直接打印日志
init_error = myapi.Start(server_addr="tcp://xxx.xxx.xxx.xxx:xxxx", spi=MySpi)
if init_error:  # 如果初始化失败，报错
    raise init_error

# 4 登录账户 -------------------------------------------------------------------
myapi.Login(account, passwd)

# 5 阻塞主线程等待结果返回 ------------------------------------------------------
myapi.Join()
```
**提示：**

- 卖出委托前必须先登录
- 服务器对委托订单的处理时间无法保证，因此无法启用同步模式，只能采用异步模式；因此用户必须实现相关的回调函数才能收取到委托订单相关的执行消息和成交消息

---

### 3.4.3 Cancel - 撤单委托
**函数签名：**
```python
def Cancel(self, order_id: str)
```
**参数：**

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| order_id | str | 无，必填 | 需要撤销的委托订单编号 |


---

