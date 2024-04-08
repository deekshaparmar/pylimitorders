from trading_framework.execution_client import ExecutionClient
from trading_framework.price_listener import PriceListener


class LimitOrderAgent(PriceListener):
    def __init__(self, execution_client: ExecutionClient) -> None:
        super().__init__()
        self.execution_client = execution_client
        self.orders = []  # List to store orders

    def add_order(self, is_buy: bool, product_id: str, amount: int, limit: float):
        """
        This function used for Adding an order to the agent's list of orders
        here is_buy Flag indicating whether to buy or sell, product_id: Product ID,
        amount param indicates Amount to buy/sell, and limit param indicates Limit at which to buy or sell
        """
        self.orders.append({'is_buy': is_buy, 'product_id': product_id, 'amount': amount, 'limit': limit})

    def execute_orders(self, product_id: str, price: float):
        """
        This function Execute orders if market price is at or better than the limit
        here  product_id indicating Product ID and price indicating Current market price
        """
        for order in self.orders:
            if order['product_id'] == product_id:
                if (order['is_buy'] and price <= order['limit']) or (not order['is_buy'] and price >= order['limit']):
                    if order['is_buy']:
                        self.execution_client.buy(order['product_id'], order['amount'])
                    else:
                        self.execution_client.sell(order['product_id'], order['amount'])
                    # Remove executed order from list
                    self.orders.remove(order)

    def on_price_tick(self, product_id: str, price: float):
        """
        this function get invoked on market data change
        here product_id indicated ID of the product that has a price change
        and price indicates The current market price of the product
        """
        self.execute_orders(product_id, price)
