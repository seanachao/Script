from fabric import Connection
import logging
import coloredlogs
coloredlogs.install(level='debug')
#from fabric.colors import red,green
#coloredlogs.install(level = 'DEBUG')
logger = logging.getLogger('your-module')
#hosts = ['192.168.146.134','192.168.146.135','192.168.146.136']
hosts = ['10.10.7.42','10.10.7.43','10.10.7.44','10.10.7.47','10.10.7.48','10.10.7.46']
def check():
    pass

for i in hosts:
    #print (red("hello"))
    #if ("47" in i):
    #    break
    c = Connection("root@%s"%(i),connect_kwargs={"password":"theshimima???"})
    logger.info("{} is cleaned".format(i))
    #cmd = " curl -L https://github.com/docker/compose/releases/download/1.18.0/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose"
    #result = c.run(cmd)
    #cmd = "chmod +x /usr/local/bin/docker-compose"
    #result = c.run(cmd)
    #result = c.run('uname -s',hide=True)
    #result = c.run('docker ps',hide=True)
    #print(result.stdout)
    #c.run('mkdir -p /root/scripts')
    #c.put('clean_1.sh','/root/scripts')
    #c.run('apt-get install lrzsz')
    #c.run('apt-get install sshpass')
    #c.run("mkdir -p /root/temp")
    #c.run("rm -rf /root/temp/*")
    #c.run("rm -rf /root/*.tar.gz")
    #c.run("rm -rf /root/download")
    

    with c.cd('/root/temp'):
        c.run('rm -rf /root/temp/*')
        c.run('rm -rf /root/artifacts/*')
        #c.put('clean_1.sh','/home/') 
        #c.run('chmod +x clean_1.sh')
        #c.run('bash clean_1.sh')
        #c.run("mkdir -p sun")
        #c.run("touch 111.txt")
        
    
        #c.run("docker pull itsthenetwork/nfs-server-alpine:9")

        #c.put('clean_2.sh','/home/')
        #c.run('bash clean_2.sh')
        #c.run('rm clean_2.sh')

        #files = c.run("ls")
