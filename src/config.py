import json
import os

class Config:
    def __init__(self):
        self.load_config()
    
    def load_config(self):
        # 从环境变量获取GitHub Token
        self.github_token = os.getenv('GITHUB_TOKEN')
        self.api_key = os.getenv('OPENAI_API_KEY')
        
        with open('config.json', 'r') as f:
            config = json.load(f)
            
            # 如果环境变量中没有GitHub Token，则从配置文件中读取
            if not self.github_token:
                self.github_token = config.get('github_token')
            if not self.api_key:
                self.api_key = config.get('api_key')
                
            self.notification_settings = config.get('notification_settings')
            self.subscriptions_file = config.get('subscriptions_file')
            self.update_interval = config.get('update_interval', 24 * 60 * 60)  # 默认24小时
        print(self.api_key)