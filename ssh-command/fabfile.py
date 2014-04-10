from fabric.api import *
from ilogue.fexpect import expect, expecting, run
from sshsettings import *

'

@roles('hosts')
def yum_sunet():
    put('/var/CentOS-Base.repo','/tmp/CentOS-Base.repo',use_sudo=True)
    sudo('mv -f /tmp/CentOS-Base.repo /etc/yum.repos.d/')
    sudo ('echo tsflags=repackage >> /etc/yum.conf')
    sudo ('echo %_repackage_all_erasures 1 >> /etc/rpm/macros')


@roles('hosts')
def test_heart():
    with settings(warn_only=True):
        local("./heart.py " + env.host_string)

@roles('hosts')
def yum_update():
    sudo('yum update -y')

@roles('hosts')
def yum_update_openssl():
    with settings(warn_only=True):
        sudo('yum install openssl -y')


@roles('hosts')
def reboot():
    sudo('reboot')


@roles('hosts')
def no_root_ssh():
    sudo("sed -i 's/PermitRootLogin yes/PermitRootLogin no/g' /etc/ssh/sshd_config")
    sudo("sed -i 's/#PermitRootLogin yes/PermitRootLogin no/g' /etc/ssh/sshd_config")
    sudo("sed -i 's/#PermitRootLogin no/PermitRootLogin no/g' /etc/ssh/sshd_config")

@roles('hosts')
def ossec_update():
    put("/var/ossec-hids-2.7.1.tar.gz","/var/", use_sudo=True)
    sudo("tar zxf /var/ossec-hids-2.7.1.tar.gz -C /var/")
    run("ls -l")
    put ("/var/ossec-hids-2.7.1/etc/preloaded-vars.conf","/tmp/preloaded-vars.conf")
    sudo("mv -f /tmp/preloaded-vars.conf /var/ossec-hids-2.7.1/etc/preloaded-vars.conf")
    sudo("/var/ossec-hids-2.7.1/install.sh")
    sudo("/var/ossec/bin/ossec-control restart")
    sudo ("rm -rf /var/ossec-hids-2.7.1")
    sudo ("rm -rf /var/ossec-hids-2.7.1.tar.gz")


@roles('hosts')
def update_clamav():
    sudo("sed -i 's+0.98/clamav-0.98.tar.gz+0.98.1/clamav-0.98.1.tar.gz+g' /opt/syco/bin/public/installClam.py")
    sudo("syco install-clam-client -f")

@roles('hosts')
def update_server():
	#yum_sunet()
	#no_root_ssh()
	#ossec_update()
	#update_clamav()
    yum_update()
    reboot()

@roles('hosts')
def sysctl_no_time():
    sudo("cp /etc/sysctl.conf /etc/sysctl.conf.bak")
    sudo("echo 'net.ipv4.tcp_timestamps = 0' >> /etc/sysctl.conf")
    with settings(warn_only=True):
        sudo("sysctl -p")

@roles('hosts')
def noetag_apache():
    with settings(warn_only=True):
        sudo("echo '#Apache secrity update' >> /etc/httpd/conf/httpd.conf")
        sudo("echo 'Header unset ETag' >> /etc/httpd/conf/httpd.conf")
        sudo("echo 'FileETag None' >> /etc/httpd/conf/httpd.conf")


@roles('hosts')
def change_root_passwd2():
    prompts = []
    prompts += expect('^Nytt*','pass')
    prompts += expect('^Ange*:','pass')
    env.user = 'root'
    sudo('passwd root')

