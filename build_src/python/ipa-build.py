# -*- coding: utf-8 -*-

__author__ = 'Wu Xiaocheng'

'''
编译xcode工程并生成ipa文件
'''

import commands
import sys
import os
import datetime
from config import xcodeBuildConfigs
from common import ShellError, Dict, toDict

buildConfig = toDict(xcodeBuildConfigs)

if __name__ == '__main__':
    mode = sys.argv[1]
    teamIdentifier = sys.argv[2]
    provisioningProfile = sys.argv[3]
    p12FileUrl = sys.argv[4]
    p12Pwd = sys.argv[5]
    mobileprovisionUrl = sys.argv[6]
    projectName = sys.argv[7]
    params = None
    cleanCommand = None
    buildCommand = None
    createIPACommand = None
    importCommand = None
    exportCommand = None
    ipaPath = None
    print '----------python 开始-------------'

    print 'teamIdentifier %s' % teamIdentifier
    print 'provisioningProfile %s' % provisioningProfile
    currentPath = os.getcwd()
    if mode == 'debug':
        params = buildConfig.debug
        ipaPath = '%s/appbuild/%s_%s_test_%s' % (
            currentPath,params.project, params.version, datetime.datetime.now().strftime("%m%d%H%M"))
        buildCommand = 'xcodebuild -project %s.xcodeproj -target %s -configuration %s -sdk %s build CODE_SIGN_IDENTITY="%s" PROVISIONING_PROFILE="%s"' % (
            params.project, params.target, params.configuration, params.sdk, params.code_sign_identity, params.provisioning_profile)
        createIPACommand = 'xcrun -sdk %s PackageApplication -v build/%s-iphoneos/%s.app -o %s' % (
            params.sdk, params.configuration, params.project, ipaPath)
    elif mode == 'release':
        params = buildConfig.release
        ipaPath = '%s/appbuild/%s_%s_pro_%s' % (
            currentPath,params.project, params.version, datetime.datetime.now().strftime("%m%d%H%M"))
        importCommand = 'security import %s -P "%s"' % (
            p12FileUrl,p12Pwd)
        importMobileprovisionCommand = 'cp %s ~/Library/MobileDevice/Provisioning\ Profiles/%s.mobileprovision' % (
            mobileprovisionUrl,provisioningProfile)
        importEntitlementsCommand = 'cp %s/build_src/push.entitlements %s/platforms/ios/push.entitlements' % (
            currentPath,currentPath)		
        buildCommand = 'xcodebuild -workspace platforms/ios/%s.xcworkspace -scheme %s  -sdk %s archive -configuration %s -destination generic/platform=iOS -archivePath appBuild/archive.xcarchive DEVELOPMENT_TEAM="%s" PROVISIONING_PROFILE="%s" CODE_SIGN_IDENTITY="iPhone Distribution" CODE_SIGN_ENTITLEMENTS="push.entitlements"' % (
            projectName, projectName, params.sdk, params.configuration,teamIdentifier,provisioningProfile)        
        #buildCommand = 'xcodebuild -project platforms/ios/%s.xcodeproj -scheme %s -sdk %s archive -configuration %s -destination generic/platform=iOS -archivePath appBuild/archive.xcarchive DEVELOPMENT_TEAM="%s" PROVISIONING_PROFILE="%s" CODE_SIGN_IDENTITY="iPhone Distribution" CODE_SIGN_ENTITLEMENTS="push.entitlements"' % (
            #params.xcworkspace, params.scheme, params.sdk, params.configuration,teamIdentifier,provisioningProfile)
        #exportCommand = 'xcodebuild -exportArchive -archivePath appBuild/myapp.xcarchive -exportPath appBuild -exportOptionsPlist p.list PROVISIONING_PROFILE="321" CODE_SIGN_IDENTITY="Phone Distribution: HAND Enterprise Solutions CO., LTD. (63M9FZGR9Q)"'
        exportCommand = 'xcodebuild -exportArchive -archivePath appBuild/archive.xcarchive -exportPath %s -exportOptionsPlist build_src/exportOptionsPlist.plist PROVISIONING_PROFILE="%s"' % (
            ipaPath,provisioningProfile)
		
			

	"""
    projectPath = params.path
    currentPath = os.getcwd()

    os.chdir(projectPath)
    print 'switchToPath %s' % os.getcwd()

    print 'clean project'
	
    cleanCommand = 'xcodebuild -target %s clean' % params.target
    result, message = commands.getstatusoutput(cleanCommand)
	"""
	

	# ----------------------
	print 'importCommand %s' % importCommand

	result, message = commands.getstatusoutput(importCommand)

    if result != 0:
        print message
        raise ShellError('shell error occur command is %s' % importCommand)
    else:
        print ">> importCommand success"
		
	# ----------------------
	print 'importMobileprovisionCommand %s' % importMobileprovisionCommand

	result, message = commands.getstatusoutput(importMobileprovisionCommand)

    if result != 0:
        print message
        raise ShellError('shell error occur command is %s' % importMobileprovisionCommand)
    else:
        print ">>importMobileprovisionCommand success"		

    #-----------------------------

	print 'importEntitlementsCommand %s' % importEntitlementsCommand

	result, message = commands.getstatusoutput(importEntitlementsCommand)

    if result != 0:
        print message
        raise ShellError('shell error occur command is %s' % importEntitlementsCommand)
    else:
        print ">>importEntitlementsCommand success"		
    #-----------------------------
    print 'build project'
    print 'buildCommand %s' % buildCommand

    result, message = commands.getstatusoutput(buildCommand)
    if result != 0:
        print message
        raise ShellError('shell error occur command is %s' % buildCommand)
    else:
        print ">>build success"

		
		
    print 'create ipa'
    print 'buildCommand %s' % exportCommand

    result, message = commands.getstatusoutput(exportCommand)
    if result != 0:
        print message
        raise ShellError('shell error occur command is %s' % exportCommand)
    else:
        print "create success"
        print '>>ipa path : %s' % ipaPath
    
    print '----------python 打包结束-------------'

    """
    print 'clear intermediate files generated during the build'
    clearCommand = 'rm -R ./build'
    result, message = commands.getstatusoutput(clearCommand)
    if result != 0:
        print message
        raise ShellError('shell error occur command is %s' % clearCommand)
    else:
        print "clear success"
	"""

