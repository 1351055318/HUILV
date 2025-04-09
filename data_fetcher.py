import requests
import time

class DataFetcher:
    def __init__(self):
        self.metals_url = "https://free.xwteam.cn/api/gold/trade"
        self.forex_url = "https://api.exchangerate-api.com/v4/latest/CNY"
        self.last_forex_fetch = 0
        self.forex_cache = None
        self.forex_cache_ttl = 300  # 5分钟缓存
    
    def get_metals_data(self):
        try:
            response = requests.get(self.metals_url)
            data = response.json()
            
            if data.get("code") == 200:
                metals = data["data"]["LF"]
                return {
                    "gold": next(item for item in metals if item["Symbol"] == "Au"),
                    "silver": next(item for item in metals if item["Symbol"] == "Ag"),
                    "platinum": next(item for item in metals if item["Symbol"] == "Pt"),
                    "palladium": next(item for item in metals if item["Symbol"] == "Pd"),
                    "update_time": data["data"]["UpTime"]
                }
            return None
        except Exception as e:
            print(f"获取贵金属数据时出错: {e}")
            return None
    
    def get_forex_data(self, force_refresh=True):
        current_time = time.time()
        
        # 如果强制刷新或缓存过期，则重新获取数据
        if force_refresh or self.forex_cache is None or (current_time - self.last_forex_fetch) > self.forex_cache_ttl:
            try:
                response = requests.get(self.forex_url)
                data = response.json()
                self.forex_cache = data["rates"]
                self.last_forex_fetch = current_time
            except Exception as e:
                print(f"获取汇率数据时出错: {e}")
                if self.forex_cache is None:
                    return None
        
        return self.forex_cache 