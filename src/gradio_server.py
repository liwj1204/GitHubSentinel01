import gradio as gr  # 导入gradio库用于创建GUI

from config import Config  # 导入配置管理模块
from github_client import GitHubClient  # 导入用于GitHub API操作的客户端
from report_generator import ReportGenerator  # 导入报告生成器模块
from llm import LLM  # 导入可能用于处理语言模型的LLM类
from subscription_manager import SubscriptionManager  # 导入订阅管理器
from logger import LOG  # 导入日志记录器

# 创建各个组件的实例
config = Config()
github_client = GitHubClient(config.github_token)
llm = LLM(config.api_key)
report_generator = ReportGenerator(llm)
subscription_manager = SubscriptionManager(config.subscriptions_file)

def export_progress_by_date_range(repo, days):
    # 定义一个函数，用于导出和生成指定时间范围内项目的进展报告
    raw_file_path = github_client.export_progress_by_date_range(repo, days)  # 导出原始数据文件路径
    report, report_file_path = report_generator.generate_report_by_date_range(raw_file_path, days)  # 生成并获取报告内容及文件路径

    return report, report_file_path  # 返回报告内容和报告文件路径

# 新增订阅函数
def add_subscription(repo):
    subscription_manager.add_subscription(repo)
    return "订阅添加成功", subscription_manager.list_subscriptions()

# 删除订阅函数
def remove_subscription(repo):
    subscription_manager.remove_subscription(repo)
    return "订阅删除成功", subscription_manager.list_subscriptions()

# 更新订阅函数
def update_subscription(old_repo, new_repo):
    subscription_manager.update_subscription(old_repo, new_repo)
    return "订阅更新成功", subscription_manager.list_subscriptions()

# 创建Gradio界面
with gr.Blocks() as demo:
    gr.Markdown("# GitHubSentinel")  # 设置界面标题

    with gr.Tab("报告生成"):  # 第一个Tab用于报告生成
        with gr.Row():
            repo_dropdown = gr.Dropdown(
                subscription_manager.list_subscriptions(), label="订阅列表", info="已订阅GitHub项目"
            )
            report_days_slider = gr.Slider(value=2, minimum=1, maximum=7, step=1, label="报告周期", info="生成项目过去一段时间进展，单位：天")

        report_output = gr.Markdown()
        report_file_output = gr.File(label="下载报告")

        generate_button = gr.Button("生成报告")
        generate_button.click(
            export_progress_by_date_range,
            inputs=[repo_dropdown, report_days_slider],
            outputs=[report_output, report_file_output],
        )

    with gr.Tab("订阅管理"):  # 第二个Tab用于管理订阅
        gr.Markdown("## 管理订阅")  # 添加管理订阅的标题

        with gr.Row():
            new_repo_input = gr.Textbox(label="添加新的订阅仓库")
            add_button = gr.Button("添加订阅")
            add_button.click(
                add_subscription,
                inputs=[new_repo_input],
                outputs=[new_repo_input, repo_dropdown],
            )

        with gr.Row():
            remove_repo_input = gr.Dropdown(
                subscription_manager.list_subscriptions(), label="删除订阅的仓库"
            )
            remove_button = gr.Button("删除订阅")
            remove_button.click(
                remove_subscription,
                inputs=[remove_repo_input],
                outputs=[remove_repo_input, repo_dropdown],
            )

        with gr.Row():
            update_old_repo_input = gr.Dropdown(
                subscription_manager.list_subscriptions(), label="选择要更新的订阅"
            )
            update_new_repo_input = gr.Textbox(label="新的仓库名称")
            update_button = gr.Button("更新订阅")
            update_button.click(
                update_subscription,
                inputs=[update_old_repo_input, update_new_repo_input],
                outputs=[update_old_repo_input, update_new_repo_input, repo_dropdown],
            )

if __name__ == "__main__":
    demo.launch(share=True, server_name="0.0.0.0")  # 启动界面并设置为公共可访问