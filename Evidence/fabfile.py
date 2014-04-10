from __future__ import with_statement
from fabric.api import local, settings, abort
from fabric.contrib.console import confirm
from fabric.api import *
from write import *
from EvidenceSettings import *
import time


def get_version():
    out = sudo('cat /etc/issue')
    write_to_file('666_' + env.host_string + '_issue', out, 'Logs',env.host_string)


def access_list():
    out = 'Local user accounts ans uid \n'
    out += sudo('getent passwd  | awk -F":" \'{ print "username: " $1 "\t\tuid:" $3 }\'')
    write_to_file('8.1_' + env.host_string + '_access_list', out, '8.1',env.host_string)


def anti_spoof():
    with settings(warn_only=True):
        out = 'If nf_conntrack mod is enable antisppofing is on Only relevant om fw\n'
        out += sudo('lsmod | grep nf_conntrack')
        write_to_file('1.3.4_' + env.host_string + '_anti_spoof', out, '1.3.4',env.host_string)


def stateful():
    with settings(warn_only=True):
        out = 'List stateful ip tables only relevant on fw\n'
        out += sudo('cat /proc/sys/net/ipv4/conf/br0/rp_filter')
        write_to_file('1.3.6_' + env.host_string + '_stateful', out, '1.3.6',env.host_string)


def fim_logs():
    with settings(warn_only=True):
        out = 'Alerts from OSSEC server logs \n'
        out += sudo(' tail -n50 /var/ossec/logs/alerts/alerts.log')
        write_to_file('10.2.7_' + env.host_string + '_fim_logs', out, 'Logs',env.host_string)


def antivirus():
    out = 'Crontab dail config \n'
    out += sudo('ls -l /etc/cron.daily/ | grep virus')
    out += 'Commands that run the scan daily on server Update virus def and scan \n'
    out += sudo('cat /etc/cron.daily/viruscan.sh')
    write_to_file('5.2_' + env.host_string + '_antivirus', out, '5.2', env.host_string)


def antivirus_logs():
    out = 'Last scan result\n'
    out += sudo('cat /var/log/clamav/scan-latest.log')
    write_to_file('5.2_' + env.host_string + '_antivirus', out, 'Logs', env.host_string)


def service():
    out = 'Showing all services run on server\n'
    out += sudo('service --status-all | grep running')
    write_to_file('2.2.2a_' + env.host_string + '_service', out, '2.2.2a', env.host_string)


def release():
    out = 'Redhat centos Version\n'
    out += sudo('cat /etc/redhat-release')
    write_to_file('6.1_' + env.host_string + '_release', out, '6.1', env.host_string)


def fimsettings():
    out = sudo('cat /var/ossec/etc/ossec.conf')
    write_to_file('11.5_' + env.host_string + '_fimsettings', out, '11.5',env.host_string)


def iptables():
    out = sudo('iptables-save')
    write_to_file('1.x' + env.host_string + '_iptables', out, '1.x', env.host_string)


def netstat():
    out = 'Showing all services lissen on ports\n'
    out += sudo('netstat -anp | grep LISTEN')
    write_to_file('2.2.2a_' + env.host_string + '_netstat', out, '2.2.2a', env.host_string)


def session():
    out = 'Time out set for console user \n'
    out += sudo('grep TMOUT /etc/profile')
    out += '\n Show timeout in ssh config \n'
    out += sudo('grep ClientAliveInterval /etc/ssh/sshd_config')
    write_to_file('8.5.15_' + env.host_string + '_session', out, '8.5.15', env.host_string)


def shadow_file():
    out = 'Show acces to the shadow file\n'
    out += sudo('ls -l /etc/shadow')
    write_to_file('8.4_' + env.host_string + '_shadow_file', out, '8.4', env.host_string)


def shadow():
    out = 'Local password settings compleity override by ldap\n'
    out += sudo('cat /etc/pam.d/system-auth | grep cracklib')
    out += '\n Password status in shadow file\n'
    out += sudo('awk -F":" \'{ print "username: " $1 "\tlastchange:" $3 "\tMinimum:" $4 "\tMaximum:" $5 "\tWarn:" $6 "\tInactive:" $7 "\tExpire:" $8 }\' /etc/shadow')
    write_to_file('8.5.3_8.5.9-8.5.14_' + env.host_string + '_shadow', out, '8.5.3_8.5.9-8.5.14', env.host_string)


def time():
    out = 'NTP servers that local ntp server uses\n'
    out += sudo('grep "^server"  /etc/ntp.conf')
    write_to_file('10.4a_' + env.host_string + '_time', out, '10.4', env.host_string)


def twofac():
    with settings(warn_only=True):
        out = 'Openvpnd settings showing ca certs and at bottom connection to ldap server (uses sign cert and login = 2 auth) \n'
        out += sudo('cat /etc/openvpn/server.conf')
        write_to_file('8.1_' + env.host_string + '_2_auth', out, '8.1', env.host_string)


def switchlogs():
    import time
    with settings(warn_only=True):
        out = 'Showing logs from switch logged to syslog server, Will only show logs on syslog server.\n'
        out += sudo('tail -n 50 /var/log/rsyslog/' + time.strftime('%Y/%m/%d') + '/10.100.*')
        write_to_file('10.2_' + env.host_string + '_switch_log', out, 'Logs', env.host_string)


def ldap_settings():
    with settings(warn_only=True):
        out = 'Ldap dump showing password complexity and server users\n'
        out += sudo('slapcat')
        write_to_file('8.5.3_8.5.9-8.5.14_' + env.host_string + '_ldap', out, '8.5.3_8.5.9-8.5.14', env.host_string)


def ssh_logs():
    with settings(warn_only=True):
        out = 'Logsample showing ssh user access on local server\n'
        out += sudo("tail -n 50 /var/log/secure | grep 'sshd:auth'")
        write_to_file('10.2.2_' + env.host_string + '_Login', out, 'Logs', env.host_string)


def sudo_logs():
    with settings(warn_only=True):
        out = 'Logsample showing allows sudo commands run\n'
        out += sudo("tail -n 50 /var/log/secure | grep 'sudo'")
        write_to_file('10.2.2_' + env.host_string + '_admin_actions', out, 'Logs', env.host_string)


def patch_status():
    with settings(warn_only=True):
        out = 'Local Patch level on server\n'
        out += sudo('yum update -n') + '\n'
        out += sudo('rpm -q ntp') + '\n'
        out += sudo('rpm -q openssh-server') + '\n'
        out += sudo('rpm -q rsyslog') + '\n'
        out += sudo('/var/ossec/bin/ossec-control restart') + '\n'
        out += sudo('rpm -q postfix') + '\n'
        out += sudo('rpm -q sssd') + '\n'
        out += sudo('rpm -q openldap') + '\n'
        out += sudo('rpm -q freeradius') + '\n'
        out += sudo('rpm -q bind') + '\n'
        out += sudo('rpm -q iptables') + '\n'
        out += sudo('rpm -q openvpn') + '\n'
        out += sudo('rpm -q icinga') + '\n'
        out += sudo('rpm -q openvpn') + '\n'
        out += sudo('rpm -q openvas') + '\n'
        out += sudo('rpm -q openvas-scanner') + '\n'
        out += sudo('rpm -q openvas-libraries') + '\n'
        out += sudo('rpm -q mysql-server') + '\n'
        out += sudo('rpm -q httpd') + '\n'
        out += sudo("cat /var/log/modsec_audit.log | grep 'ModSecurity for Apache' | uniq")
        out += sudo('rpm -q libvirt') + '\n'
        out += sudo('java -version') + '\n'
        out += sudo("su glassfish -c '/usr/local/glassfish4/bin/asadmin version'") + '\n'
        out += sudo('/usr/local/bin/snort --version') + '\n'
        out += sudo("su glassfish -c '/usr/local/glassfish4/bin/asadmin --port 4848 list-applications'")
        write_to_file('6.1a_' + env.host_string + '_patch', out, '6.1', env.host_string)


@roles('switch')
def switch_conf():
    local('scp ' + env.user + '@SWITCH-IP:/cfg/startup-config 1-switch.conf')
    local('scp ' + env.user + '@SWITCH-IP:/cfg/startup-config 1-switch.conf')
    with open('tc-switch.conf', 'r') as content_file:
        out_tc = content_file.read()
    write_to_file('6.1a_switc-1_config', out_tc, '6.1', env.host_string)
    with open('av-switch.conf', 'r') as content_file:
        out_av = content_file.read()
    write_to_file('6.1a_switc-2_config', out_av, '6.1', env.host_string)


def nmap_scan():
    local('nmap -PNAO --open '+env.host_string+' -oN '+env.host_string+".nmap")
    with open(env.host_string+'.nmap', 'r') as content_file:
        out = content_file.read()
    write_to_file('2.2.2a_' + env.host_string + '_nmap', out, '2.2.2a', env.host_string)


@roles('hosts')
def all():
    get_version()
    access_list()
    anti_spoof()
    stateful()
    fim_logs()
    antivirus()
    service()
    release()
    fimsettings()
    iptables()
    netstat()
    session()
    shadow_file()
    shadow()
    time()
    twofac()
    ldap_settings()
    patch_status()
    switchlogs()
    ssh_logs()
    sudo_logs()
    antivirus_logs()
    nmap_scan()
