#from mongoengine import *

import pymongo
import logging
logger = logging.getLogger('your-module')
logging.basicConfig(level = logging.INFO,format = '%(asctime)s - %(name)s - %(message)s')

operator = pymongo.MongoClient("mongodb://localhost:27017/")
#operator = pymongo.MongoClient("mongodb://10.10.7.45:27017/")
db = operator["dev"]

hosts = db["host"]
hosts.delete_many({})
logger.info("delete hosts")
logger.warn("waring !!!")
#logging.info("deling host")
#logging.warning("failed")
server = "192.168.146.145"
#server = "10.10.7.45"
#server = "39.96.16.32"
#server = "10.10.28.133"


#user = pymongo.MongoClient("mongodb://localhost:27017/")
#user = pymongo.MongoClient("mongodb://10.10.7.45:27020/")
def clear_userdashboard():
    #user = pymongo.MongoClient("mongodb://10.10.7.45:27020/")
    #user = pymongo.MongoClient("mongodb://localhost:27020/")
    user = pymongo.MongoClient("mongodb://%s:27020/"%(server))
    #user = pymongo.MongoClient("mongodb://39.96.16.32:27020/")
    user_db = user["user_dashboard"]
    
    peerconfigs = user_db["peerconfigs"]
    peerconfigs.delete_many({})
    
    ordererconfigs = user_db["ordererconfigs"]
    ordererconfigs.delete_many({})
    
    caconfigs = user_db["caconfigs"]
    caconfigs.delete_many({})
    
    chains = user_db["chains"]
    chains.delete_many({})
    
    chainmems = user_db["chainmems"]
    chainmems.delete_many({})
    
    admincacerts = user_db["admincacerts"]
    admincacerts.delete_many({})
    logicchains = user_db["logicchains"]
    logicchains.delete_many({})
    
    networkconfigs = user_db["networkconfigs"]
    networkconfigs.delete_many({})
    
    notifications = user_db["notifications"]
    notifications.delete_many({})
    
    operations = user_db["operations"]
    operations.delete_many({})
    
    orgconfigs = user_db["orgconfigs"]
    orgconfigs.delete_many({})
    
    peercacerts = user_db["peercacerts"]
    peercacerts.delete_many({})
    
    
    rootcacerts = user_db["rootcacerts"]
    rootcacerts.delete_many({})
    
    signatures = user_db["signatures"]
    signatures.delete_many({})
    
    smartconftractcodes = user_db["smartconftractcodes"]
    smartconftractcodes.delete_many({})
    
    smartcontractdeploys = user_db["smartcontractdeploys"]
    smartcontractdeploys.delete_many({})
    
    smartcontractoperatehistories = user_db["smartcontractoperatehistories"]
    smartcontractoperatehistories.delete_many({})
    
    smartcontracts = user_db["smartcontracts"]
    smartcontracts.delete_many({})
    
    entryqueues = user_db["entryqueues"]
    entryqueues.delete_many({})
    
    taskqueues = user_db["taskqueues"]
    taskqueues.delete_many({})
    
    blacklistchains = user_db["blacklistchains"]
    blacklistchains.delete_many({})

    policies = user_db["policies"]
    policies.delete_many({})

    dies = user_db["dies"]
    dies.delete_many({})
    user.close()

def clear_dev():
    #user = pymongo.MongoClient(host="39.96.16.32",port=27017)
    user = pymongo.MongoClient(host=server,port=27017)
    user_db = user['dev']

    cluster = user_db['cluster']
    cluster.delete_many({})

    container = user_db['container']
    container.delete_many({})

    login_history = user_db['login_history']
    login_history.delete_many({})

    service_port = user_db['service_port']
    service_port.delete_many({})
    #hosts = user_db['host']
    #hosts.delete_many({})
    #user.close()
if __name__ == "__main__":
    #clear_dev()
    clear_userdashboard()



