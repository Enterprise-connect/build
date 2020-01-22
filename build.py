__author__ = 'Apolo Yasuda <apolo.yasuda@ge.com>'

'''
   EC SDK build script
'''

import  os, json, base64, sys, threading, subprocess
from time import sleep

#import ec_common
from common import Common

c=Common(__name__)

PLUGINS=os.environ["PLUGINS"]
BINARY="{}/{}".format(os.environ["DIST"],os.environ["ARTIFACT"])
APIBIN="{}/{}".format(os.environ["API"],os.environ["API"])
APISRC="{}/src/{}".format(os.environ["GOPATH"],os.environ["APIPKG"])
TLSSRC="{}/src/{}".format(os.environ["GOPATH"],os.environ["TLSPLUGINPKG"])
VLNSRC="{}/src/{}".format(os.environ["GOPATH"],os.environ["VLNPLUGINPKG"])
KEPSRC="{}/src/{}".format(os.environ["GOPATH"],os.environ["KEPPLUGINPKG"])
DHOME="{}/src/{}".format(os.environ["GOPATH"],os.environ["DHOME"])
TLSPLUGINBIN="{}/{}/{}".format(PLUGINS,os.environ["TLSPLUGIN"],os.environ["TLSPLUGIN"])
VLNPLUGINBIN="{}/{}/{}".format(PLUGINS,os.environ["VLNPLUGIN"],os.environ["VLNPLUGIN"])
KEPPLUGINBIN="{}/{}/{}".format(PLUGINS,os.environ["KEPPLUGIN"],os.environ["KEPPLUGIN"])
EC_TAG=""

def main():

    print "generate linux_amd64 artifacts"
    os.system("CGO_ENABLED=0 GOOS=linux GODEBUG=netdns=cgo GOARCH=amd64 go build -tags netgo -a -v -o /{}_linux_sys {}/*.go".format(BINARY,DHOME))
    
    os.system("CGO_ENABLED=0 GOOS=linux GODEBUG=netdns=go GOARCH=amd64 go build -tags netgo -a -v -o /{}_linux_var {}/*.go".format(BINARY,DHOME))

    #print "generate linux_adm64 secuity api binary"
    #os.system("CGO_ENABLED=0 GOOS=linux GODEBUG=netdns=cgo GOARCH=amd64 go build -tags netgo -a -v -o /{}_linux {}/*.go".format(APIBIN, APISRC))

    os.system("/{}_linux_sys -inf".format(BINARY))
    #get the current rev
    op = subprocess.check_output(["/{}_linux_sys".format(BINARY), "-ver"])
    EC_TAG =  op[op.rfind(" [")+2:op.rfind("]")]
    TLSLDFLAGS="-X main.REV={}.tls".format(EC_TAG)
    VLNLDFLAGS="-X main.REV={}.vln".format(EC_TAG)
    KEPLDFLAGS="-X main.REV={}.kep".format(EC_TAG)
    print "EC_TAG: {}".format(EC_TAG)
    
    print "generate linux_amd64 plugins bin dns resolved by system"
    os.system('CGO_ENABLED=0 GOOS=linux GODEBUG=netdns=cgo GOARCH=amd64 go build -ldflags "{}" -tags netgo -a -v -o /{}_linux_sys {}/*.go'.format(TLSLDFLAGS,TLSPLUGINBIN,TLSSRC))
    os.system('CGO_ENABLED=0 GOOS=linux GODEBUG=netdns=cgo GOARCH=amd64 go build -ldflags "{}" -tags netgo -a -v -o /{}_linux_sys {}/*.go'.format(VLNLDFLAGS,VLNPLUGINBIN,VLNSRC))
    os.system('CGO_ENABLED=0 GOOS=linux GODEBUG=netdns=cgo GOARCH=amd64 go build -ldflags "{}" -tags netgo -a -v -o /{}_linux_sys {}/*.go'.format(KEPLDFLAGS,KEPPLUGINBIN,KEPSRC))

    print "generate linux_amd64 plugins dns resolved by go."
    os.system('CGO_ENABLED=0 GOOS=linux GODEBUG=netdns=go GOARCH=amd64 go build -ldflags "{}" -tags netgo -a -v -o /{}_linux_var {}/*.go'.format(TLSLDFLAGS,TLSPLUGINBIN,TLSSRC))
    os.system('CGO_ENABLED=0 GOOS=linux GODEBUG=netdns=go GOARCH=amd64 go build -ldflags "{}" -tags netgo -a -v -o /{}_linux_var {}/*.go'.format(VLNLDFLAGS,VLNPLUGINBIN,VLNSRC))
    os.system('CGO_ENABLED=0 GOOS=linux GODEBUG=netdns=go GOARCH=amd64 go build -ldflags "{}" -tags netgo -a -v -o /{}_linux_var {}/*.go'.format(KEPLDFLAGS,KEPPLUGINBIN,KEPSRC))


    print "generate darwin_amd64 artifacts"
    os.system("CGO_ENABLED=0 GOOS=darwin GODEBUG=netdns=cgo GOARCH=amd64 go build -tags netgo -a -v -o /{}_darwin_sys {}/*.go".format(BINARY,DHOME))
    os.system("CGO_ENABLED=0 GOOS=darwin GODEBUG=netdns=go GOARCH=amd64 go build -tags netgo -a -v -o /{}_darwin_var {}/*.go".format(BINARY,DHOME))

    print "generate darwin_amd64 plugins bin dns resolved by system"
    os.system('CGO_ENABLED=0 GOOS=darwin GODEBUG=netdns=cgo GOARCH=amd64 go build -ldflags "{}" -tags netgo -a -v -o /{}_darwin_sys {}/*.go'.format(TLSLDFLAGS,TLSPLUGINBIN,TLSSRC))
    os.system('CGO_ENABLED=0 GOOS=darwin GODEBUG=netdns=cgo GOARCH=amd64 go build -ldflags "{}" -tags netgo -a -v -o /{}_darwin_sys {}/*.go'.format(KEPLDFLAGS,KEPPLUGINBIN,KEPSRC))

    print "generate darwin_amd64 plugins dns resolved by go."
    os.system('CGO_ENABLED=0 GOOS=darwin GODEBUG=netdns=go GOARCH=amd64 go build -ldflags "{}" -tags netgo -a -v -o /{}_darwin_var {}/*.go'.format(TLSLDFLAGS,TLSPLUGINBIN,TLSSRC))
    os.system('CGO_ENABLED=0 GOOS=darwin GODEBUG=netdns=go GOARCH=amd64 go build -ldflags "{}" -tags netgo -a -v -o /{}_darwin_var {}/*.go'.format(KEPLDFLAGS,KEPPLUGINBIN,KEPSRC))


    print "generate windows_amd64 artifacts"
    os.system("CGO_ENABLED=0 GOOS=windows GODEBUG=netdns=cgo GOARCH=amd64 go build -tags netgo -a -v -o /{}_windows_sys.exe {}/*.go".format(BINARY,DHOME))
    os.system("CGO_ENABLED=0 GOOS=windows GODEBUG=netdns=go GOARCH=amd64 go build -tags netgo -a -v -o /{}_windows_var.exe {}/*.go".format(BINARY,DHOME))

    print "generate windows_amd64 plugins bin dns resolved by system"
    os.system('CGO_ENABLED=0 GOOS=windows GODEBUG=netdns=cgo GOARCH=amd64 go build -ldflags "{}" -tags netgo -a -v -o /{}_windows_sys.exe {}/*.go'.format(TLSLDFLAGS,TLSPLUGINBIN,TLSSRC))
    os.system('CGO_ENABLED=0 GOOS=windows GODEBUG=netdns=cgo GOARCH=amd64 go build -ldflags "{}" -tags netgo -a -v -o /{}_windows_sys.exe {}/*.go'.format(KEPLDFLAGS,KEPPLUGINBIN,KEPSRC))

    print "generate windows_amd64 plugins dns resolved by go."
    os.system('CGO_ENABLED=0 GOOS=windows GODEBUG=netdns=go GOARCH=amd64 go build -ldflags "{}" -tags netgo -a -v -o /{}_windows_var.exe {}/*.go'.format(TLSLDFLAGS,TLSPLUGINBIN,TLSSRC))
    os.system('CGO_ENABLED=0 GOOS=windows GODEBUG=netdns=go GOARCH=amd64 go build -ldflags "{}" -tags netgo -a -v -o /{}_windows_var.exe {}/*.go'.format(KEPLDFLAGS,KEPPLUGINBIN,KEPSRC))

    
    print "generate linux_arm artifacts"
    os.system("CGO_ENABLED=0 GOOS=linux GODEBUG=netdns=cgo GOARCH=arm go build -tags netgo -a -v -o /{}_arm_sys {}/*.go".format(BINARY,DHOME))
    os.system("CGO_ENABLED=0 GOOS=linux GODEBUG=netdns=go GOARCH=arm go build -tags netgo -a -v -o /{}_arm_var {}/*.go".format(BINARY,DHOME))

    print "generate linux_arm plugins bin dns resolved by system"
    os.system('CGO_ENABLED=0 GOOS=linux GODEBUG=netdns=cgo GOARCH=arm go build -ldflags "{}" -tags netgo -a -v -o /{}_arm_sys {}/*.go'.format(TLSLDFLAGS,TLSPLUGINBIN,TLSSRC))
    os.system('CGO_ENABLED=0 GOOS=linux GODEBUG=netdns=cgo GOARCH=arm go build -ldflags "{}" -tags netgo -a -v -o /{}_arm_sys {}/*.go'.format(VLNLDFLAGS,VLNPLUGINBIN,VLNSRC))
    os.system('CGO_ENABLED=0 GOOS=linux GODEBUG=netdns=cgo GOARCH=arm go build -ldflags "{}" -tags netgo -a -v -o /{}_arm_sys {}/*.go'.format(KEPLDFLAGS,KEPPLUGINBIN,KEPSRC))

    print "generate linux_arm plugins dns resolved by go."
    os.system('CGO_ENABLED=0 GOOS=linux GODEBUG=netdns=go GOARCH=arm go build -ldflags "{}" -tags netgo -a -v -o /{}_arm_var {}/*.go'.format(TLSLDFLAGS,TLSPLUGINBIN,TLSSRC))
    os.system('CGO_ENABLED=0 GOOS=linux GODEBUG=netdns=go GOARCH=arm go build -ldflags "{}" -tags netgo -a -v -o /{}_arm_var {}/*.go'.format(VLNLDFLAGS,VLNPLUGINBIN,VLNSRC))
    os.system('CGO_ENABLED=0 GOOS=linux GODEBUG=netdns=go GOARCH=arm go build -ldflags "{}" -tags netgo -a -v -o /{}_arm_var {}/*.go'.format(KEPLDFLAGS,KEPPLUGINBIN,KEPSRC))


    print "copying plugins.yml examples.."
    os.system("cp {}/plugins.yml /{}/{}".format(TLSSRC,PLUGINS,os.environ["TLSPLUGIN"]))
    os.system("cp {}/plugins.yml /{}/{}".format(VLNSRC,PLUGINS,os.environ["VLNPLUGIN"]))
    os.system("cp {}/plugins.yml /{}/{}".format(KEPSRC,PLUGINS,os.environ["KEPPLUGIN"]))

    
    CKF = 'checksum.txt'
    DIST=os.environ['DIST']

    
    #temp remove lib
    #LIB=os.environ['LIB']

    c.chksumgen('/{}'.format(DIST),CKF)

    #temp remove lib
    #c.chksumgen('/{}'.format(LIB),CKF)

    op = subprocess.check_output(["ls", "-al", "/{}".format(os.environ["DIST"])])
    print op

    op = subprocess.check_output(["/{}_linux_sys".format(BINARY), "-ver"])
    print op
    
    fl = os.listdir('/{}'.format(DIST))
    for filename in fl:
        if filename==CKF:
            continue
        
        os.system('cd /{}; tar -czvf {}.tar.gz ./{}'.format(DIST,filename,filename))
        os.system('rm /{}/{}'.format(DIST,filename))
    
    return
        
if __name__=='__main__':
    main()
