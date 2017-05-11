#!/bin/bash
#path=`dirname $0`
#cd "${path}"

$teamIdentifier
$provisioningProfile
$p12FileUrl
$p12Pwd
$mobileprovisionUrl
$mobileprovisionFileName
$mobileprovisionName
$mobileprovisionPath

$projectUrl
$projectFileName
$projectName
$aNum
$hasPush

echo $0
echo $*
hasPush=false
aNum=2
while getopts ":c:w:l:p:PD" opt
do
	case $opt in
		c )
				echo $OPTARG;  
				p12FileUrl=$OPTARG;
				echo "c index $OPTIND";;
		w )
				echo $OPTARG;  
				p12Pwd=$OPTARG		
				echo "w $OPTIND";;

		l )
				echo $OPTARG;  
				mobileprovisionUrl=$OPTARG			
				echo "l $OPTIND";;
		p )
				echo $OPTARG;     
				projectUrl=$OPTARG;		
				echo "p $OPTIND";;
		P )
				hasPush=true
				echo "P $OPTIND";;
		D )
				aNum=1;
				echo "D $OPTIND";;		

		? )
				echo "error"                    
				exit 1;;
		esac
done


if [ ! -n "$p12FileUrl" -o  ! -n "$p12Pwd" -o  ! -n "$mobileprovisionUrl" -o  ! -n "$projectUrl" ] ;then
  echo "---- 参数校验 失败 参数不全 -----"
else
  echo "---- 参数校验通过 -----"
  echo -e "\nInput a number from below items"
	echo "1. build ipa debug"
	echo "2. build ipa release"


	#read aNum
	
	echo $aNum
	case $aNum in
		1)  . ./ionic.sh
			ruby test.rb
			python ipa-build.py 'debug'
		;;
		2)  ionic platform add ios
	
			if [ $hasPush == true ]
			then
				ruby build_src/ruby/xcproj.rb $projectUrl 1
			else
				ruby build_src/ruby/xcproj.rb $projectUrl 0
			fi

			mobileprovisionFileName=`basename $mobileprovisionUrl`
			mobileprovisionPath=`dirname $mobileprovisionUrl`
			mobileprovisionName=${mobileprovisionFileName%.*}
			echo “filename: ${mobileprovisionFileName%.*}”
			echo “extension: ${mobileprovisionFileName##*.}”
			echo "mobileprovisionName $mobileprovisionUrl >> $mobileprovisionName"
			#security cms -D -i ${mobileprovisionName}".mobileprovision" > ${mobileprovisionName}".plist"
			security cms -D -i ${mobileprovisionUrl} > ${mobileprovisionName}".plist"
			plistName=${mobileprovisionName}".plist"
			teamIdentifier=$(/usr/libexec/PlistBuddy -c 'Print TeamIdentifier:0' $plistName)
			provisioningProfile=$(/usr/libexec/PlistBuddy -c 'Print UUID' $plistName)
			mobileprovisionFullName=${mobileprovisionName}".mobileprovision"
			
			#------------ 获取项目名称  -----------
			projectFileName=`basename $projectUrl`
			projectName=${projectFileName%.*}
			echo “filename: ${projectFileName%.*}”
			
			echo $p12FileUrl 
			echo $p12Pwd
			
			python build_src/python/ipa-build.py 'release' $teamIdentifier $provisioningProfile $p12FileUrl $p12Pwd $mobileprovisionUrl	$projectName	

		;;
		*)  echo 'You input error! stop'
		;;
	esac
fi 
:<<!


echo $OPTIND
echo $*
shift $(($OPTIND - 1))
echo $*
echo $0




#
!