import tkinter as tk
import requests
import websocket
import threading
import json
from datetime import datetime
import time
import hashlib
import hmac


class BinancePriceApp:
    def __init__(self):
        self.futures_base_url = "https://fapi.binance.com"
        self.root = tk.Tk()
        self.root.title("Binance Symbol Price")
        self.root.geometry("800x600+100+100")
        self.root.iconbitmap('../resources/binance.ico')

        '''
        标签、按钮、文本组件
        '''
        # Label
        self.apiKey_label = tk.Label(self.root, text='Enter API key', font=("Arial", 10))
        self.apiSecret_label = tk.Label(self.root,text='Enter API Secret',font=("Arial", 10))
        self.account_label = tk.Label(self.root, text='Enter API endpoint', font=("Arial", 10))
        self.apiKey_label.grid(row=0, column=0, padx=5, pady=10)
        self.apiSecret_label.grid(row=1, column=0, padx=5, pady=10)

        self.account_label.grid(row=2, column=0, padx=5, pady=10)
        self.request_method_label = tk.Label(self.root, text='Enter request method', font=("Arial", 10))
        self.request_method_label.grid(row=3, column=0, padx=5, pady=10)
        self.request_param_label = tk.Label(self.root, text='Enter parameters', font=("Arial", 10))
        self.request_param_label.grid(row=4, column=0, padx=5, pady=10)
        self.result_text_label = tk.Label(self.root, text='response data', font=("Arial", 10))
        self.result_text_label.grid(row=5, column=0, padx=5, pady=10)
        self.request_text_label = tk.Label(self.root, text='request data', font=("Arial", 10))
        self.request_text_label.grid(row=7, column=0, padx=5, pady=10)

        # Entry
        self.apiKey_entry = tk.Entry(self.root,font=("Arial", 10),width=80)
        self.apiSecret_entry = tk.Entry(self.root,font=("Arial", 10),show='*',width=80)
        self.account_endpoint_entry = tk.Entry(self.root, font=("Arial", 10))
        self.apiKey_entry.grid(row=0, column=1, padx=30, pady=10)
        self.apiSecret_entry.grid(row=1, column=1, padx=30, pady=10)
        self.account_endpoint_entry = tk.Entry(self.root, font=("Arial", 10))
        self.account_endpoint_entry.grid(row=2, column=1, padx=5, pady=10)
        self.request_method_entry = tk.Entry(self.root, font=("Arial", 10))
        self.request_method_entry.grid(row=3, column=1, padx=5, pady=10)
        self.request_param_entry = tk.Entry(self.root, font=("Arial", 10))
        self.request_param_entry.grid(row=4, column=1, padx=5, pady=10)

        # Button
        #self.apiKey_button = tk.Button(self.root, text='enter', command=self.getKey)
        #self.apiSecret_button = tk.Button(self.root, text='enter', command=self.getSecret)
        self.request_button = tk.Button(self.root, text='request', command=self.send_signed_request_no_params)
        self.clear_response_button = tk.Button(self.root, text='clear', command=self.clear_response_text)
        self.clear_request_button = tk.Button(self.root, text='clear', command=self.clear_request_text)
        #self.apiKey_button.grid(row=0, column=2, padx=5, pady=10)
        #self.apiSecret_button.grid(row=1, column=2, padx=5, pady=10)
        self.request_button.grid(row=4,column=2,padx=5,pady=10)
        self.clear_response_button.grid(row=5, column=1, padx=5, pady=10)
        self.clear_request_button.grid(row=7, column=1, padx=5, pady=10)
        self.convert_button = tk.Button(self.root, text="Convert to JSON", command=self.convert_to_json)
        self.convert_button.grid(row=5, column=2, padx=5, pady=10)

        # Text
        self.result_text = tk.Text(self.root,height=13,width=150,font=("Arial", 10))
        self.result_text.grid(row=6, columnspan=3)
        self.request_text = tk.Text(self.root,height=13,width=150,font=("Arial", 10))
        self.request_text.grid(row=8, columnspan=3)


        self.ws_symbol = None
        self.ws_running = False
        self.ws_thread = None
        self.root.mainloop()

    def convert_to_json(self):
        text_data = self.result_text.get("1.0", tk.END)  # 获取文本控件中的内容
        try:
            json_data = json.loads(text_data)  # 尝试将文本转换为JSON
            pretty_json = json.dumps(json_data, indent=4)  # 生成格式化后的JSON字符串
            self.result_text.config(state=tk.NORMAL)  # 允许编辑输出文本控件
            self.result_text.delete("1.0", tk.END)  # 清空输出文本控件内容
            self.result_text.insert(tk.END, pretty_json)  # 将格式化的JSON数据插入输出文本控件
            self.result_text.config(state=tk.DISABLED)  # 禁止编辑输出文本控件
        except json.JSONDecodeError as e:
            self.result_text.config(state=tk.NORMAL)
            self.result_text.delete("1.0", tk.END)
            self.result_text.insert(tk.END, f"Invalid Json：{e}")
            self.result_text.config(state=tk.DISABLED)

    def clear_response_text(self):
        self.result_text.config(state=tk.NORMAL)  # Enable editing the result text widget
        self.result_text.delete("1.0", tk.END)  # Clear the content of the result text widget
        #self.result_text.config(state=tk.DISABLED)  # Disable editing the result text widget

    def clear_request_text(self):
        self.request_text.delete("1.0", "end")

    def get_sign(self, data):
        key = self.apiSecret_entry.get().encode('utf-8')
        data = data.encode('utf-8')
        sign = hmac.new(key, data, hashlib.sha256).hexdigest()
        return sign

    def get_timestamp(self):
        timestamp = str(int(float(time.time()) * 1000))
        return timestamp

    def send_signed_request_no_params(self):
        headers = {"Content-Type": "application/json;charset=utf-8", "X-MBX-APIKEY": self.apiKey_entry.get()}
        if len(self.request_param_entry.get()) <1 and self.account_endpoint_entry.get() != "/fapi/v1/listenKey":
            params = f'timestamp={self.get_timestamp()}'
            sign = self.get_sign(params)
            url = self.futures_base_url + self.account_endpoint_entry.get() + "?" + f'timestamp={self.get_timestamp()}' + f'&signature={sign}'

        elif self.account_endpoint_entry.get() == "/fapi/v1/listenKey":
            url = self.futures_base_url + self.account_endpoint_entry.get()
            print(url)

        else:
            print(self.request_param_entry.get())
            params = self.request_param_entry.get() + f'&timestamp={self.get_timestamp()}'
            sign = self.get_sign(params)
            url = self.futures_base_url + self.account_endpoint_entry.get() + "?" + self.request_param_entry.get() + f'&timestamp={self.get_timestamp()}' + f'&signature={sign}'

        method = self.request_method_entry.get().lower()
        print("method is : ", method)
        endpoint = self.account_endpoint_entry.get()
        print("endpoint is: ",endpoint,self.account_endpoint_entry.get() == "/fapi/v1/listenKey")
        resp = requests.request(method.upper(),url, headers=headers)

        print(resp.request.url)
        print(resp.status_code)
        print(resp.text)
        request_url = "request url: "+str(resp.request.url)
        request_header = "request header: "+str(resp.request.headers)
        request_status_code =  "request status code: " +str(resp.status_code)
        self.result_text.insert(tk.END, resp.text + "\n")
        self.result_text.see(tk.END)
        self.request_text.insert(tk.END,request_url+'\n'+'\n')
        self.request_text.insert(tk.END, request_status_code + '\n' + '\n')
        self.request_text.insert(tk.END, request_header + '\n'+'\n')
        self.request_text.see(tk.END)
        print('finished')

    def getKey(self):
        print(self.apiKey_entry.get())
        print(len(self.apiKey_entry.get()))

    def getSecret(self):
        print(self.apiSecret_entry.get())

    def getEndpoint(self):
        print(self.account_endpoint_entry.get())

    def ts_time(self, ts):
        time_obj = datetime.fromtimestamp(ts / 1000)
        time_obj = datetime.strftime(time_obj, "%Y-%m-%d %H:%M:%S")
        return time_obj

    def stop_ws(self):
        if self.ws_running:
            self.ws_running = False
            self.ws_result_text.insert(tk.END, "结束订阅\n")
            self.ws_result_text.see(tk.END)

    def ws_run(self):
        self.ws_symbol = self.ws_entry.get().strip()
        if self.ws_symbol:
            url = f"wss://fstream.binance.com/ws/{self.ws_symbol.lower()}@markPrice"
            self.ws_running = True
            self.ws_thread = threading.Thread(target=self.websocket_request, args=(url,))
            self.ws_thread.start()
        else:
            self.ws_result_text.insert(tk.END, "fail to subscribe websocket\n")
            self.ws_result_text.see(tk.END)

    def websocket_request(self, url):
        ws = websocket.create_connection(url)
        while self.ws_running:
            ws_price = json.loads(ws.recv())
            mark_price = ws_price['p']
            symbol = ws_price.get('s')
            price_time = ws_price.get("E")
            results_text = json.dumps(
                {'Event_time': self.ts_time(price_time), 'Event_timestamp': price_time, 'symbol': symbol,
                 "markPrice": mark_price})
            # use lambda to update UI in the main thread
            self.root.after(0, lambda: self.ws_result_text.insert(tk.END, results_text + "\n"))
            self.root.after(0, lambda: self.ws_result_text.see(tk.END))

    def get_price(self):
        symbol = self.symbol_entry.get().strip()
        if symbol:
            url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol.upper()}"
            response = requests.get(url)
            if response.status_code == 200:
                price_info = response.json()
                price = price_info.get('price')
                # use lambda to update UI in the main thread
                self.root.after(0, lambda: self.result_label.config(text=f"{symbol.upper()}价格: {price}"))
            else:
                # use lambda to update UI in the main thread
                self.root.after(0, lambda: self.result_label.config(text="获取价格失败，请检查symbol名称"))
        else:
            # use lambda to update UI in the main thread
            self.root.after(0, lambda: self.result_label.config(text="请输入symbol名称"))


if __name__ == "__main__":
    app = BinancePriceApp()
