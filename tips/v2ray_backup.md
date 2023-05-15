# v2ray

## gen_acme

curl https://get.acme.sh | sh

### standalone模式

~/.acme.sh/acme.sh --issue -d xxxxxxx --standalone --keylength ec-256 --force --server letsencrypt

### 使用现有的nginx模式

acme.sh --issue -d domain.com -w /www/domain.com --keylength ec-256 --server letsencrypt

location /.well-known/acme-challenge/ {
  alias /www/domain.com/.well-known/acme-challenge/;
}

### 为nginx配置证书

acme.sh --install-cert -d domain.you \
--key-file /etc/nginx/certs/domain.you/key \
--fullchain-file /etc/nginx/certs/domain.you/cert \
--reloadcmd "systemctl reload nginx.service"

NOTE: apache和nginx配置证书的方式并不相同。遇到过v2ray证书严重出错的问题。原因就是为nginx使用了apache的配置


## install v2ray

bash <(curl -L https://raw.githubusercontent.com/v2fly/fhs-install-v2ray/master/install-release.sh)

bash <(curl -L https://raw.githubusercontent.com/v2fly/fhs-install-v2ray/master/install-dat-release.sh)


### v2ray conf
```json
{
  "log": {
    "loglevel": "warning",
    "access": "/var/log/v2ray/access.log",
    "error": "/var/log/v2ray/error.log",
  },
  "inbounds": [
    {
      "port": 10000,
      "listen":"127.0.0.1",
      "protocol": "vmess",
      "settings": {
        "clients": [
          {
            "id": "xxxxx",
            "alterId": 0
          }
        ]
      },
      "streamSettings": {
        "network": "ws",
        "wsSettings": {
        "path": "/xxxx"
        }
      }
    }
  ],
  "outbounds": [
    {
      "protocol": "freedom",
      "settings": {}
    }
  ]
}
```

## nginx
```
server {
        listen 80;
        server_name domain.com;
        rewrite ^(.*) https://$server_name$1 permanent;
    }

    server {
      listen 4430 ssl http2;
      server_name domain.com;

      ssl_certificate       /etc/nginx/certs/domain.com/cert;
      ssl_certificate_key   /etc/nginx/certs/domain.com/key;
      ssl_session_tickets off;

      ssl_protocols         TLSv1.2 TLSv1.3;
      ssl_ciphers         HIGH:!aNULL:!MD5;

      location / {
          root /www/domain.com;
          #index /index.html;
          autoindex on;
      }

      error_page 404 /404.html;
      location = /404.html {
      }

      error_page 500 502 503 504 /50x.html;
      location = /50x.html {
      }

      location /v2ray {
          proxy_redirect off;
          proxy_pass http://127.0.0.1:123456;
          proxy_http_version 1.1;
          proxy_set_header Upgrade $http_upgrade;
          proxy_set_header Connection "upgrade";
          proxy_set_header Host $host;
          proxy_set_header X-Real-IP $remote_addr;
          proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
      }
    }
```