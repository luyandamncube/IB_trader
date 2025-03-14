from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.common import *
import time

class IBTraderApp(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)
        self.timeout = False  # Timeout flag
        self.is_connected = False  # Connection status flag
        self.balance_received = False  # Track if account balance has been received

    # Override error handling to suppress 2104, 2106, 2158, etc.
    def error(self, reqId, errorCode, errorString):
        if errorCode in [2104, 2106, 2158]:  # Suppress these informational messages
            return
        print(f"Error: {errorCode}, Message: {errorString}")

    # Callback for receiving account summary information (balance details)
    def accountSummary(self, reqId: int, account: str, tag: str, value: str, currency: str):
        print(f"Received Account Summary - {tag}: {value} {currency}")
        if tag == "CashBalance" or tag == "BuyingPower":
            self.balance_received = True  # Mark that we've received the balance info

    # Callback for the next valid order ID (not used in this case, but required for the app to work)
    def nextValidId(self, orderId: int):
        pass

    # Request account summary after connection is established
    def request_account_balance(self):
        print("Requesting account balance information...")
        # Request account summary for "CashBalance" and "BuyingPower"
        self.reqAccountSummary(1, "All", "CashBalance")
        self.reqAccountSummary(1, "All", "BuyingPower")

    # Function to handle timeout directly in the main loop (extended to 120 seconds)
    def check_timeout(self):
        start_time = time.time()
        while not self.balance_received:
            # If no response after 120 seconds, disconnect
            if time.time() - start_time > 120:
                print("Timeout: No response from IBKR in 120 seconds.")
                self.disconnect()
                break
            time.sleep(0.1)  # Check every 100ms

def main():
    app = IBTraderApp()

    try:
        print("Attempting to connect to IBKR...")
        app.connect("127.0.0.1", 7497, 0)  # Connect to IBKR TWS in Paper Trading mode
        app.request_account_balance()  # Request account balance immediately after connection
        app.check_timeout()  # Check for timeout in the main loop
        app.run()  # Start the application, enter the event loop
    except Exception as e:
        print(f"Failed to connect to IBKR: {str(e)}")

if __name__ == "__main__":
    main()
