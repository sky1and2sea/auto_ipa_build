#!/usr/bin/ruby
# -*- coding: utf-8 -*-


require 'xcodeproj'
#project_path = '/Users/username/Documents/mobile/meike/project_path/platforms/ios/xxxx.xcodeproj'
project_path = ARGV[0]
hasPush = ARGV[1]

puts '-------------------------------------'
puts '-----ruby 取消自动签名操作 开始 ------'
puts project_path
puts hasPush
project = Xcodeproj::Project.open(project_path)

project.targets.each do |target|
  puts target.name
end


# 修改配置
project.root_object.attributes['TargetAttributes'] = {}
targetAttributes = project.root_object.attributes['TargetAttributes']
targetAttributes['1D6058900D05DD3D006BFB54'] = {}
bluePrintID = targetAttributes['1D6058900D05DD3D006BFB54']
bluePrintID['ProvisioningStyle'] = "Manual"

if hasPush == '0'
   puts "关闭推送"
   bluePrintID['SystemCapabilities'] = {'com.apple.Push' => {"enabled" => 0}}
else
   puts "打开推送"
   bluePrintID['SystemCapabilities'] = {'com.apple.Push' => {"enabled" => 1}}

end


project.save()
puts project.root_object.attributes
puts '-----ruby 取消自动签名操作完成 ------'




