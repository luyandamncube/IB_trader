from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
import time

class TestApp(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)

    # Callback function for next valid ID
    def nextValidId(self, orderId: int):
        print(f"Connected successfully! Next valid order ID: {orderId}")
        # Disconnect after receiving valid ID (test purpose)
        self.disconnect()

    # Override error handling to suppress 2104, 2106, 2158, etc.
    def error(self, reqId, errorCode, errorString):
        if errorCode in [2104, 2106, 2158]:  # Suppress these informational messages
            return
        print(f"Error: {errorCode}, Message: {errorString}")

    # Callback for market data updates
    def tickPrice(self, reqId: int, tickType: int, price: float, attrib: int):
        print(f"Price update received for request ID {reqId}: {tickType} - {price}")

    # Callback for when the connection is closed
    def connectionClosed(self):
        print("Connection closed.")

def main():
    app = TestApp()
    try:
        print("Attempting to connect to IBKR...")
        app.connect("127.0.0.1", 7497, 0)  # Connect to the TWS API on local machine and paper account port
        print("Connection request sent.")
        app.run()  # Start the application, enter the event loop
    except Exception as e:
        print(f"Failed to connect to IBKR: {str(e)}")

if __name__ == "__main__":
    main()
