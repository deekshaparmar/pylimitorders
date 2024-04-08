import unittest

from limit.limit_order_agent import LimitOrderAgent
from trading_framework.execution_client import ExecutionClient


class LimitOrderAgentTest(unittest.TestCase):

    def test_limit_order_execution(self):
        class MockExecutionClient(ExecutionClient):
            def __init__(self):
                super().__init__()

            def buy(self, product_id: str, amount: int):
                print(f"Bought {amount} shares of {product_id}")

            def sell(self, product_id: str, amount: int):
                print(f"Sold {amount} shares of {product_id}")

        execution_client = MockExecutionClient()
        agent = LimitOrderAgent(execution_client)

        # Adding buy order for IBM
        agent.add_order(is_buy=True, product_id='IBM', amount=1000, limit=100)

        # Price drops below limit, order should execute
        agent.on_price_tick('IBM', 99.9)

        # Adding sell order for Google
        agent.add_order(is_buy=False, product_id='GOOG', amount=500, limit=1500)

        # Price rises above limit, order should execute
        agent.on_price_tick('GOOG', 1510)

        # Both orders should be executed, so the orders list should be empty
        self.assertEqual(len(agent.orders), 0)


if __name__ == '__main__':
    unittest.main()
