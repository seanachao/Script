#-*-coding:utf-8 -*-
import pymongo
import pdb
from kubernetes import client,config
#from host_operations import get_config_from_params 
#from get_service_url import get_services_urls
#mongodb = pymongo.MongoClient("mongodb://localhost:27017")
#host="10.10.7.30"
host="127.0.0.1"
#host="localhost"
mongodb = pymongo.MongoClient("mongodb://{}:27017".format(host))
dev_db = mongodb['dev']
host_db = dev_db['host']
K8S_CRED_TYPE = {
"account":'0',
'cert':'1',
'config':'2'
}
def get_node_ip(v1,node_name):
    ret = v1.list_node()
    ip = ""
    for i in ret.items:
        for addr in i.status.addresses:
            if addr.type == "ExternalIP":
                ip = addr.address
            elif addr.type == "InternalIP":
                ip = addr.address
            else:
                continue
    return ip

def get_node_ip_of_service(v1, service_name):
    ret = v1.list_pod_for_all_namespaces(watch=False)

    for i in ret.items:
        if i.metadata.name.startswith(service_name):
            return get_node_ip(v1,i.spec.node_name)

def get_service_external_port(v1, namespace, ip):
    ret = v1.list_service_for_all_namespaces(watch=False)
    #print(ret)
    results = {}
    # result template
    r_template = ip + ":" + "{}"
    for i in ret.items:
        if i.metadata.namespace == namespace:
            tmp_name = i.metadata.name.replace("-", "_")
            print(tmp_name)
            if i.metadata.name.startswith("peer"):
                for port in i.spec.ports:
                    # transfer port name which can be recognized.
                    if port.name == "externale-listen-endpoint":
                        external_port = port.node_port
                        name = tmp_name + "_grpc"
                        value = r_template.format(external_port)

                    elif port.name == "listen":
                        event_port = port.node_port
                        name = tmp_name + "_event"
                        value = r_template.format(event_port)

                    else:
                        print(i.metadata.name)
                        continue

                    results[name] = value

            elif i.metadata.name.startswith("ca"):
                name = tmp_name + "_ecap"
                for port in i.spec.ports:
                    _port = port.node_port
                    value = r_template.format(_port)
                    results[name] = value

            elif i.metadata.name.startswith("orderer0"):
                name = "orderer0"
                for port in i.spec.ports:
                    _port = port.node_port
                    value = r_template.format(_port)
                    results[name] = value

            elif i.metadata.name.startswith("orderer1"):
                name = "orderer1"
                for port in i.spec.ports:
                    _port = port.node_port
                    value = r_template.format(_port)
                    results[name] = value

            elif i.metadata.name.startswith("orderer"):
                # 如果都不是order0和orderer1，则为orderer，也就是solo模式
                name = "orderer"
                for port in i.spec.ports:
                    _port = port.node_port
                    value = r_template.format(_port)
                    results[name] = value
            else:
                continue

    return results

def get_services_urls(v1, cluster_name):
    ret = v1.list_service_for_all_namespaces(watch=False)
    service = ""
    for i in ret.items:
        if i.metadata.namespace == cluster_name:
            service = i.metadata.name
            break

    service_ip = get_node_ip_of_service(v1,service)
    service_urls = get_service_external_port(v1,cluster_name,
                                                   service_ip)
    print('services_urls is \t',service_urls)
    return service_urls



def get_config_from_params(k8s_params):
    """ get the configuration from params
    :params: k8s_params to connect to Kubernetes Master node
    :return: python kubernetes config
    """
    k8s_config = client.Configuration()
    k8s_config.host = k8s_params.get('K8SAddress')
    if not k8s_config.host.startswith("http://"):
        k8s_config.host = "http://" + k8s_config.host

    if k8s_params.get('K8SCredType') == K8S_CRED_TYPE['account']:
        k8s_config.username = k8s_params.get('K8SUsername')
        k8s_config.password = k8s_params.get('K8SPassword')

    elif k8s_params.get('K8SCredType') == K8S_CRED_TYPE['cert']:
        cert_content = k8s_params.get('K8SCert')
        key_content = k8s_params.get('K8SKey')
        k8s_config.cert_file = \
            config.kube_config._create_temp_file_with_content(cert_content)
        k8s_config.key_file = \
            config.kube_config._create_temp_file_with_content(key_content)

    # Use config file content to set k8s_config if it exist.
    elif k8s_params.get('K8SCredType') == K8S_CRED_TYPE['config']:
        config_content = k8s_params.get('K8SConfig')

        if config_content.strip():
            config_file = \
                config.kube_config. \
                _create_temp_file_with_content(config_content)

            loader = \
                config.kube_config. \
                _get_kube_config_loader_for_yaml_file(config_file)

            loader.load_and_set(k8s_config)

    if k8s_params.get('K8SUseSsl') == "false":
        k8s_config.verify_ssl = False
    else:
        k8s_config.verify_ssl = True
        k8s_config.ssl_ca_cert = \
            config.kube_config. \
            _create_temp_file_with_content(k8s_params.get('K8SSslCert'))

    client.Configuration.set_default(k8s_config)

    return k8s_config

def get_name(name='k8s_test'):
    return name 

def get_params():
    k8s_name = get_name()
    query_name = {"name":k8s_name}
    params = host_db.find_one(query_name) 
    return params

def get_k8s_params(params):
    return params.get('k8s_param')

def get_kube_config_from_params1(k8s_params):
    k8s_config = client.Configuration()
    k8s_config.host = k8s_params.get('K8SAddress')
    print(k8s_config.host)
    if not k8s_config.host.startswith('https://'):
        k8s_config.host = "https://" + k8s_config.host

    cert_content = k8s_params.get('K8SCert')
    key_content = k8s_params.get('K8SKey')
    #print("key content is",key_content)

    k8s_config.cert_file = \
            config.kube_config._create_temp_file_with_content(cert_content)
    k8s_config.key_file = \
            config.kube_config._create_temp_file_with_content(key_content)
    k8s_config.ssl_ca_cert = \
            config.kube_config._create_temp_file_with_content(k8s_params.get('K8SSslCert'))
    return k8s_config


    return True
#cluster_name = "baas-dcw7c1ef88-1565349005000"
#cluster_name = "baas-74qbrum2d0d-1565059267000"
#cluster_name = "baas-30jjirrt8if-1565764486000"
cluster_name = "baas-9i7tco9e5gt-1565766088000"

def list_all_namespace(k8s_config):
    client.Configuration.set_default(k8s_config)
    v1 = client.CoreV1Api()
    try:
        result = v1.list_pod_for_all_namespaces()
        #print(type(result))
        pods = v1.list_pod_for_all_namespaces()
        pod_list = []
        for i in pods.items:
            pod_list.append(i.metadata.name)
        print(pod_list) 
        for i in pod_list:
           print(i)
        result = v1.list_service_for_all_namespaces(watch=False)
        #print ("res is ",result)

        #print(result)
        service = ""
        for i in result.items:
            print(i.metadata.namespace)
            if i.metadata.namespace == cluster_name:
                 print(i.metadata.namespace)
                 service = i.metadata.name
                 break
        print(service)
        return result
    except Exception as e:
        print(e)
    
def check_host(k8s_config):
    client.Configuration.set_default(k8s_config)
    v1 = client.CoreV1Api()
    #client.Configuration.set_default(k8s_config)
    #v1 = client.CoreV1Api()
    #v1 = client.CoreV1Api()
    try:
        result = v1.list_node()
    except Exception as e:
        print(e)
        error_msg = (
               "Can't create kubernetes host due"
               "to an incorrect parameters"
                )
        raise Exception(error_msg)
    #return True

def get_services(cluster_name,k8s_config):
    print("Get the service url")
    # make sure connect the k8s api 
    client.Configuration.set_default(k8s_config)
    v1 = client.CoreV1Api()
    # make 
    res = get_services_urls(v1,cluster_name)
    print("Getted the service url")
    return res
logo = '*' * 10
def main():
    pdb.set_trace()
    print("get the k8s_params")
    k8s_params = get_k8s_params(get_params())
    print(logo + "Getted" + logo)
    #print(k8s_params)
    #get_kube_config_from_params1
    k8s_config  = get_config_from_params(k8s_params)#get_kube_config_from_params(k8s_params)
    print("set the k8s_config")
    #k8s_config  = get_kube_config_from_params1(k8s_params)#get_kube_config_from_params(k8s_params)
    print(logo + "Setted" + logo)
    #check_host(k8s_config)
    print("get the k8s namespace")
    #res = list_all_namespace(k8s_config)
    #print(logo +"Getted" + logo)

    res = get_services(cluster_name,k8s_config)
    #print(res)

mongodb.close()
if __name__ == '__main__':
    main()
