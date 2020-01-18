from flask import Flask, render_template, flash
from flask_bootstrap import Bootstrap

from module.db import *

app = Flask(__name__)
app.secret_key = "Maliwan"  # 跨域访问
bootstrap = Bootstrap(app)

db = DB()

# 主页
@app.route('/')
def index():
    return render_template('Main.html')


# ONU自动发现
@app.route('/onu', methods=['POST','GET'])
def onu_list():
    today = time.strftime("%Y-%m-%d", time.localtime())
    onus = db.get_onu_autofind()
    #flash(onus[0])
    total_cost = 5
    summary_of_orders = {"aaa": 1, "bbb": 2, "ccc": 3}
    return render_template('onu_list.html', onu_list=onus, total_cost=total_cost,
                           summary_of_orders=summary_of_orders)

    """
    orders = []
    total_cost = 0
    summary_of_orders = {}
    if request.method == 'POST':
        if request.form.get("button") == '今日订单':
            today = time.strftime("%Y-%m-%d", time.localtime())
            orders=db.get_orders_list(today)
            #统计全部订单价格
            for order in orders:
                total_cost += order[4] #下标4为cost的存储位置，也许用字典更好
            #统计订单汇总数据
            summary_of_orders = db.get_summary_of_orders(orders)
    return render_template('order_list.html', orders = orders, total_cost=total_cost,
                           summary_of_orders=summary_of_orders)
                           """

# 刷新ONU自动发现
@app.route("/get_onu_list")
def refresh_onu_list():
    onus = db.get_onu_autofind()
    return render_template('RefreshOnuList.html', onu_list=onus)



def main():
    app.run(host='0.0.0.0', port=8800)


if __name__ == "__main__":
    main()
