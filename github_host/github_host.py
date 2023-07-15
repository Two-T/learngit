import sys, os
from shutil import copyfile
from urllib.request import urlopen
import time

# download github_hosts
def download_hosts():
    url = 'https://raw.hellogithub.com/hosts'
    resp = urlopen(url)
    if resp.getcode() == 200:
        with open('github_hosts', 'wb') as f:
            f.write(resp.read())
        print('get hosts files successful :D')
    else:
        print('get hosts failed :(')


def check_system():
    sys_info = sys.version

    def check_hosts(path):
        with open(path, 'r', encoding='utf-8') as f:
            hosts = f.readlines()
            for i in hosts:
                if '127.0.0.1' in i:
                    return True
            return False

    if 'GCC' in sys_info:
        try:
            # wsl
            hosts = r'/mnt/c/Windows/system32/drivers/etc/hosts'
            check_hosts(hosts)
        except:
            # ubuntu
            hosts = r'/etc/hosts'
    else:
        hosts = r'C:/Windows/System32/drivers/etc/hosts'
    print('hosts place:', hosts)
    copyfile(hosts, 'hosts')
    time.sleep(0.3)
    return hosts


# backup ori hosts
def backup(hosts_path):
    copyfile(hosts_path, hosts_path + '_bac')
    time.sleep(0.3)
    print('back hosts to hosts_bac')


# if host_file have github_host part, delete them.
def delete_github_part(host_file):
    with open(host_file, 'r',encoding='utf-8') as f, open('temp', 'w',encoding='utf-8') as tempf:
        rows = f.readlines()
        
        not_github = True
        start = True
        end = True
        for line in rows:
            if  start and '# GitHub520 Host Start' in line:
                not_github = False
                start = False
            
            if not_github:
                tempf.write(line)
            
            if end and '# GitHub520 Host End' in line:
                not_github = True
                end = False

    os.remove(host_file)
    time.sleep(0.3)
    os.rename('temp', host_file)
    time.sleep(0.3)


def add_github_part(hosts_file, github_hosts):
    with open(hosts_file,
              'r', encoding='utf-8') as f,open(github_hosts,'r',encoding='utf-8') as gf:
        rows = f.readlines()
        gf_rows = gf.readlines()

    with open('temp', 'w', encoding='utf-8') as f:
        rows.extend(gf_rows)
        f.writelines(rows)
    os.remove(hosts_file)
    time.sleep(0.3)
    os.remove(github_hosts)
    time.sleep(0.3)
    os.rename('temp', 'hosts')
    time.sleep(0.3)


def replace_file(hosts_path):
    os.remove(hosts_path)
    time.sleep(0.3)
    copyfile('hosts', hosts_path)
    os.remove('hosts')
    time.sleep(0.3)
    print('well done!')


def flush_dns(hosts_path):
    sys_ver = ''
    if 'etc' in hosts_path:
        sys_ver = 'ubuntu'
    if 'mnt/c' in hosts_path:
        sys_ver = 'win'
    elif 'System32' in hosts_path:
        sys_ver = 'win'

    if sys_ver == 'win':
        os.system('ipconfig /flushdns')
        os.system("pause")
    else:
        print('please flush dns')

def main():
    download_hosts()
    hosts_path = check_system()
    backup(hosts_path)
    delete_github_part('hosts')
    add_github_part('hosts', 'github_hosts')
    replace_file(hosts_path)
    flush_dns(hosts_path)

if __name__ == "__main__":
    main()