# CMPT 353 PROJECT
# Zachariah Delft, 301386141
#
#

# Gather Data

# Text file where key is saved
KEY_FILE = 'transit_api_key.txt'

# Function to get transit API key from text file
def getAPIKey():
    file = open(KEY_FILE, 'r')
    key = file.read().rstrip()
    file.close()
    return key

def main():
    API_KEY = getAPIKey()
    

if __name__ == '__main__':
    main()