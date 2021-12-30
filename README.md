# auto_ipa_build
A shell use CLI to build a ionic project to a enterprise ipa file

E-mail: sky1and2sea@hotmail.com

使用命令行从一个ionic项目导出为一个企业证书的ipa包的shell脚本

## Usage

Before use the shell，you need install Xcodeproj, ruby and python on the macOS. ruby and python installed on the macOS，

    $ [sudo] gem install xcodeproj

see more from [Xcodeproj][xcodeproj]

Example:

<pre>
./auto_ipa_build.sh  -P -p xcodeprojFilePath/name.xcodeproj -c p12FilePath/name.p12 -w p12Password -l mobileprovisionFilePath/name.mobileprovision
</pre>

## SYNOPSIS

auto_ipa_build.sh [-P] -p name.xcodeproj -c name.p12 -w p12Password -l name.mobileprovision

## DESCRIPTION

### -P
add it if your project need to use Push Notification

### -p
The Absolute path of xcodeproj file 

### -c 
The Absolute path or Absolute path of p12 file 

### -w 
password of p12 file

### -l
The Absolute path or Absolute path of mobileprovision file

[xcodeproj]: https://github.com/cocoapods/xcodeproj


