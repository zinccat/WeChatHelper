# 设置环境变量

export WECHATY_LOG="verbose"
export WECHATY_PUPPET="wechaty-puppet-padlocal"
export WECHATY_PUPPET_PADLOCAL_TOKEN="puppet_padlocal_your_token"

export WECHATY_PUPPET_SERVER_PORT="9001"
# 可使用代码随机生成UUID：import uuid;print(uuid.uuid4());
export WECHATY_TOKEN="your_uuid"

docker run -ti \
	  --name wechaty_puppet_service_token_gateway \
	    --rm \
	      -e WECHATY_LOG \
	        -e WECHATY_PUPPET \
		  -e WECHATY_PUPPET_PADLOCAL_TOKEN \
		    -e WECHATY_PUPPET_SERVER_PORT \
		      -e WECHATY_TOKEN \
		        -p "$WECHATY_PUPPET_SERVER_PORT:$WECHATY_PUPPET_SERVER_PORT" \
			  wechaty/wechaty:0.65

