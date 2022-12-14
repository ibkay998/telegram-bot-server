import os
import telegram.ext
import requests
from app.utils import get_binancep2p_rate, format_binance_response_data
import asyncio



Token = os.getenv("TELEGRAM_API_KEY")
endpoint_base = "https://api.streetrates.hng.tech/api/currency/currency/"
endpoint_list="https://api.streetrates.hng.tech/api/currency/currencies/flag"
updater = telegram.ext.Updater(Token,use_context=True)
dispatcher = updater.dispatcher
iso_code_list = set(("ARS","EUR","USD","AED","AUD","BDT","BHD","BOB","BRL","CAD","CLP","CNY","COP","CRC","CZK","DOP","DZD","EGP","GBP","GEL","GHS","HKD","IDR","INR","JPY","KES","KHR","KRW","KWD","KZT","LAK","LBP","LKR","MAD","MMK","MXN","MYR","NGN","OMR","PAB","PEN","PHP","PKR","PLN","PYG","QAR","RON","RUB","SAR","SDG","SEK","SGD","THB","TND","TRY","TWD","UAH","UGX","UYU","VES","VND","ZAR"))


def start(update,context):
    # update.message.sendMessage(chat_id=context.message.chat_id, text="I'm a bot, please talk to me!")
    update.message.reply_text("Welcome to streetrates telegram bot where we provide real time black market rate of any currency you need check /help to see the commands available")


def help(update,context):
    update.message.reply_text(
"""
/start -> Welcome to the channel

/help -> View all the Commands

/convert -> You type in the isocode of the currency you want to convert then the isocode of the currency you want to convert to.
e.g /convert USD NGN

/list -> Lists all the avalable iso_codes the bot can get rates for

/calculate -> Calculate the actual amount of any available currency to another put the from and to currency.
e.g /calculate 100 USD to NGN
"""
    )

def list(update,context):
    url = f"{endpoint_list}"
    response = requests.get(url)
    data = response.json()
    for item in data:
        country = item["country"]
        isocode = item["isocode"]
        name = item["name"]
        reply = f"{isocode} -> {country} ({name})"
        update.message.reply_text(reply)
        


# async def usd(update,context):
#     value = "".join(context.args[0]).upper()
#     if value not in iso_code_list:
#         update.message.reply_text("This isocode does not have a black market rate")
#     else:
#         url = f"{endpoint_base}{value}"
#         response = requests.get(url)
#         data = response.json()
#         name = data["data"]["name"]
#         if data["success"]:
#             sell = data["data"]["rate"]["parallel_sell"]
#             reply=f"One USD to {value} is {sell} {name}"
#         else:
#             reply = "request failed"
#         update.message.reply_text(reply)

async def convert(update,context):
    if len(context.args) < 2:
        update.message.reply_text("Enter in the format e.g/convert USD NGN")
    else:
        from_currency = "".join(context.args[0]).upper()
        to_currency = "".join(context.args[1]).upper()
        if from_currency not in iso_code_list and to_currency not in iso_code_list:
            update.message.reply_text("One of this isocodes does not have a black market rate")
        else:
            url1 = f"{endpoint_base}{from_currency}"
            response1 = requests.get(url1)
            url2 = f"{endpoint_base}{to_currency}"
            response2 = requests.get(url2)
            data1 = response1.json()
            name1 = data1["data"]["name"]
            data2 = response2.json()
            name2 = data2["data"]["name"]
            if data1["success"] and data2["success"]:
                sell1 = data1["data"]["rate"]["parallel_sell"]
                sell2 = data2["data"]["rate"]["parallel_sell"]
            else:
                print("request failed")
            final_result = round(float(sell2) / float(sell1),3)
            reply=f"One {from_currency} to {to_currency} is {final_result} {name2}"
            update.message.reply_text(reply)
        
async def calculate(update,context):
    if len(context.args) < 3:
        update.message.reply_text("Enter in the format e.g/calculate 100 USD to NGN")
    else:
        from_currency = "".join(context.args[1]).upper()
        to_currency = "".join(context.args[3]).upper()
        amount = float(context.args[0])
        if from_currency not in iso_code_list and to_currency not in iso_code_list:
            update.message.reply_text("One of this isocodes does not have a black market rate")
        else:     
            url1 = f"{endpoint_base}{from_currency}"
            response1 = requests.get(url1)
            url2 = f"{endpoint_base}{to_currency}"
            response2 = requests.get(url2)
            data1 = response1.json()
            name1 = data1["data"]["name"]
            data2 = response2.json()
            name2 = data2["data"]["name"]
            if data1["success"] and data2["success"]:
                sell1 = data1["data"]["rate"]["parallel_sell"]
                sell2 = data2["data"]["rate"]["parallel_sell"]
            else:
                print("request failed")
            final_result = round(float(sell2) / float(sell1),6) * amount
            reply = f"{amount} {name1} is {final_result} {name2}"
            update.message.reply_text(reply)

def loop_runner(action):
    loop = asyncio.new_event_loop()
    return loop.run_until_complete(action)

def loop_runner_2(action):
    loop = asyncio.new_event_loop()
    return loop.run_until_complete(action)

def loop_runner_3(action):
    loop = asyncio.new_event_loop()
    return loop.run_until_complete(action)

# def sync_run(update,context):
#     return loop_runner(usd(update,context))

def sync_run_2(update,context):
    return loop_runner_2(convert(update,context))

def sync_run_3(update,context):
    return loop_runner_3(calculate(update,context))


dispatcher.add_handler(telegram.ext.CommandHandler('start',start))
dispatcher.add_handler(telegram.ext.CommandHandler('help',help))
dispatcher.add_handler(telegram.ext.CommandHandler('list',list))
dispatcher.add_handler(telegram.ext.CommandHandler('convert',sync_run_2))
dispatcher.add_handler(telegram.ext.CommandHandler('calculate',sync_run_3))

if __name__ == "__main__":
    updater.start_polling()
    updater.idle()
