# -*- coding: utf-8 -*-

__author__ = 'Arms'

'''
Xcode打包相关参数设定
'''

xcodeBuildConfigs = {
    'debug': {
        'path': '/Users/ucsmy/Desktop/Ewallet_3.0',
        'version': '3.0',
        'project': 'Ewallet',
        'target': 'Ewallet',
        'configuration': 'Debug',
        'sdk': 'iphoneos9.2',
        'code_sign_identity': '',
        'provisioning_profile': ''
    },
    'release': {
        'path': '/Users/wuxiaocheng/Documents/mobile/IOS_HAND/meike/huilianyi-v2/platforms/ios',
        'version': '1.0',
        'project': '',
		"xcworkspace": "",
		"scheme": "",
        'target': '',
        'configuration': 'Release',
        'sdk': 'iphoneos',
        'code_sign_identity': '',
        'provisioning_profile': ''
    }
}

qdSvnConfigs = {
    'test_svn_path': '',
    'test_local_path': '/Users/ucsmy/Desktop/3.0',
    'pro_svn_path': '',
    'pro_local_path': ''
}
