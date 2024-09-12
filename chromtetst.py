import pychrome

# Create a browser instance
browser = pychrome.Browser(url="http://127.0.0.1:5000")

# Create a tab
tab = browser.new_tab()

# Define request event handler
def request_will_be_sent(request):
    print("Request URL: ", request["request"]["url"])

# Define response event handler
def response_received(response):
    print("Response URL: ", response["response"]["url"])

# Start the tab
tab.start()

# Enable the network domain
tab.Network.enable()

# Set event handlers
tab.Network.requestWillBeSent = request_will_be_sent
tab.Network.responseReceived = response_received

# Navigate to a URL
tab.Page.navigate(url="https://open.spotify.com/lyrics")

# Wait for events
tab.wait(10)

# Stop the tab
tab.stop()

# Close the tab
browser.close_tab(tab)
