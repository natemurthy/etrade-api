"""Print orders"""
import configparser
import pickle
import sys
from tabulate import tabulate

config = configparser.ConfigParser()
config.read('config.ini')

BASE_URL = "https://api.etrade.com"
ACCT = {
    "accountId": config["DEFAULT"]["account_id"],
    "accountIdKey": config["DEFAULT"]["account_id_key"]
}


# this should be of the form key1=value,key2=value2
query_filter = None
if len(sys.argv) > 1:
    query_filter = sys.argv[1]

def parse_args(s):
    result = {}
    if s is not None:
        terms = [kwargs.split("=") for kwargs in s.split(",")]
        for kv in terms:
            result[kv[0]] = kv[1]
    return result


def load_oauth_session():
    """Load oauth session from pickle file"""
    with open('session.pickle', 'rb') as f:
        return pickle.load(f)


def get_orders(session, order_status):
    orders_url = "{}/v1/accounts/{}/orders.json".format(BASE_URL, ACCT["accountIdKey"])
    headers = {"consumerkey": config["DEFAULT"]["CONSUMER_KEY"]}
    params_open = {"status": order_status}
    print('GET', orders_url, '\n')
    resp = session.get(orders_url, header_auth=True, params=params_open, headers=headers)
    return resp.status_code, resp.json()


def print_orders(response, status):
    """
    Formats and displays a list of orders

    :param response: response object of a list of orders
    :param status: order status related to the response object
    """
    table_header = [
        'Order #', 
        'Security Type', 
        'Symbol', 
        'Status', 
        'Price', 
        'Quantity', 
        'Desc',
        'Term',
        'Price Type', 
    ]
    orders_arr = []
    filter_kws = parse_args(query_filter)

    if response is not None and "OrdersResponse" in response and "Order" in response["OrdersResponse"]:
        for order in response["OrdersResponse"]["Order"]:
            if order is not None and "OrderDetail" in order:
                order_row = []
                if order is not None and 'orderId' in order:
                    # col 0
                    order_row.append(str(order["orderId"]))

    
                details = order["OrderDetail"]

                if len(details) == 1:
                    detail = details[0]
 
                    instrument = detail["Instrument"][0]
                
                    if 'Product' in instrument and 'securityType' in instrument["Product"]:
                        # col 1
                        order_row.append(instrument["Product"]["securityType"])

                    if 'Product' in instrument and 'symbol' in instrument["Product"]:
                        # col 2 
                        order_row.append(instrument["Product"]["symbol"])

                    if status != "expired" and status != "rejected" and 'status' in detail:
                        # col 3
                        order_row.append(detail["status"])

                    if 'limitPrice' in detail:
                        # col 4
                        order_row.append(str('${:,.2f}'.format(detail["limitPrice"])))

                    if 'orderedQuantity' in instrument:
                        # col 5
                        order_row.append(str("{:,}".format(instrument["orderedQuantity"])))

                    if 'symbolDescription' in instrument and 'orderAction' in instrument:
                        # col 6
                        # this will have len=1 for single positions, and len=2 for option spreads
                        instruments = detail["Instrument"]
                        if len(instruments) == 2:
                            leg_0 = "{} {}".format(instruments[0]['orderAction'], instruments[0]['symbolDescription'])
                            leg_1 = "{} {}".format(instruments[1]['orderAction'], instruments[1]['symbolDescription'])
                            order_row.append("{} / {}".format(leg_0, leg_1))
                        else:
                            order_row.append("{} {}".format(instrument['orderAction'], instrument['symbolDescription']))

                    if 'orderTerm' in detail:
                        # col 7
                        order_row.append(detail["orderTerm"])

                    if 'priceType' in detail:
                        # col 8
                        order_row.append(detail["priceType"])

                orders_arr.append(order_row)

    filtered_orders = orders_arr
    if 'security_type' in filter_kws:
        filtered_orders = list(
            filter(lambda r: r[1] == filter_kws['security_type'], filtered_orders))
    if 'symbol' in filter_kws:
        filtered_orders = list(
            filter(lambda r: filter_kws['symbol'] in r[2], filtered_orders))

    filtered_orders = [table_header] + filtered_orders
    print(tabulate(filtered_orders, headers='firstrow'))


if __name__ == "__main__":
    s = load_oauth_session()

    order_status = 'OPEN'
    http_code, resp_json = get_orders(s, order_status)
    if http_code != 200:
        print("unable to fetch orders", http_code, resp_json)
    
    print_orders(resp_json, order_status)
