# -*- coding: utf-8 -*-

__author__ = 'liyanjun'

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
    bundleId = sys.argv[8]
    p12FileUrlName = sys.argv[9]
    
    params = None
    cleanCommand = None
    buildCommand = None
    createIPACommand = None
    importCommand = None
    importPartitionListCommand = None
    exportCommand = None
    ipaPath = None
    result = None
    message = None
    print '----------python 开始-------------'
    print 'buildConfig===',buildConfig
    print 'teamIdentifier %s' % teamIdentifier
    print 'provisioningProfile %s' % provisioningProfile
    print mode
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
        ipaPath = '%s/appbuild/%s_pro' % (
            currentPath,params.project)
        # importCommand = 'security import %s -P "%s" -A -T /usr/bin/codesign' % (
        #     p12FileUrl,p12Pwd)
        importCommand = 'security import %s -k ~/Library/Keychains/login.keychain -P "%s" -T /usr/bin/codesign -T /usr/bin/security -T /usr/bin/productbuild' % (
            p12FileUrl,p12Pwd)

        importPartitionListCommand = 'security set-key-partition-list -S apple-tool:,apple: -s -k handhand ~/Library/Keychains/login.keychain 1> /dev/null'


        importMobileprovisionCommand = 'cp %s ~/Library/MobileDevice/Provisioning\ Profiles/%s.mobileprovision' % (
            mobileprovisionUrl,provisioningProfile)
        # importEntitlementsCommand = 'cp %s/build_src/push.entitlements %s/platforms/ios/push.entitlements' % (
            # currentPath,currentPath)      
        #buildCommand = 'xcodebuild -workspace ../platforms/ios/%s.xcworkspace -scheme %s  -sdk %s archive -configuration %s -destination generic/platform=iOS -archivePath appBuild/archive.xcarchive DEVELOPMENT_TEAM="%s" PROVISIONING_PROFILE="%s" CODE_SIGN_IDENTITY="iPhone Distribution" CODE_SIGN_ENTITLEMENTS="push.entitlements"' % (
            #projectName, projectName, params.sdk, params.configuration,teamIdentifier,provisioningProfile)
        buildCommand = 'xcodebuild -workspace ../%s.xcworkspace -scheme %s  -sdk %s archive -configuration %s -destination generic/platform=iOS -archivePath appBuild/archive.xcarchive DEVELOPMENT_TEAM="%s" PROVISIONING_PROFILE_SPECIFIER="%s"  PRODUCT_BUNDLE_IDENTIFIER="%s"  CODE_SIGN_IDENTITY="iPhone Distribution"' % (
            projectName, projectName, params.sdk, params.configuration,teamIdentifier,provisioningProfile,bundleId)
        print buildCommand      
        #buildCommand = 'xcodebuild -project platforms/ios/%s.xcodeproj -scheme %s -sdk %s archive -configuration %s -destination generic/platform=iOS -archivePath appBuild/archive.xcarchive DEVELOPMENT_TEAM="%s" PROVISIONING_PROFILE="%s" CODE_SIGN_IDENTITY="iPhone Distribution" CODE_SIGN_ENTITLEMENTS="push.entitlements"' % (
            #params.xcworkspace, params.scheme, params.sdk, params.configuration,teamIdentifier,provisioningProfile)
        exportCommand = 'xcodebuild -exportArchive -archivePath appBuild/archive.xcarchive -exportPath %s -exportOptionsPlist build_src/exportOptionsPlist.plist PROVISIONING_PROFILE="%s" -allowProvisioningUpdates' % (
            ipaPath,provisioningProfile)
        
    # ----------------------

    print '----xcode clean----'
    if mode != 'debug':
        xcodebuildclean = 'xcodebuild clean -workspace ../%s.xcworkspace -scheme %s -configuration Release' % (projectName,projectName)
        print 'importCommand %s' % xcodebuildclean
        result, message = commands.getstatusoutput(xcodebuildclean)

        if result != 0:
            print message
        else:
            print "----xcode clean success ------"


    if mode != 'debug':
        unlockChain = 'security unlock-keychain -p handhand ~/Library/Keychains/login.keychain'
        commands.getstatusoutput(unlockChain)
        print 'unlockChain:',unlockChain

        # commands.getstatusoutput(importCommand)
        print 'importCommand %s' % importCommand
        result, message = commands.getstatusoutput(importCommand)

        if result != 0:
            print message
        else:
            print ">> importCommand success"


        print 'importPartitionListCommand %s' % importPartitionListCommand
        result2, message2 = commands.getstatusoutput(importPartitionListCommand)

        if result2 != 0:
            print message2
        else:
            print ">> importPartitionListCommand success"

    # ----------------------

        
    print 'importMobileprovisionCommand %s' % importMobileprovisionCommand
    result, message = commands.getstatusoutput(importMobileprovisionCommand)

    if result != 0:
        print message
        raise ShellError('shell error occur command is %s' % importMobileprovisionCommand)
    else:
        print ">>importMobileprovisionCommand success"      

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

