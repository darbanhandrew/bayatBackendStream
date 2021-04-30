import requests
import socket


class ArvanStream:
    session = requests.Session()
    session.headers.update({'Authorization': 'Apikey 7ad7faa2-2376-43ac-afcd-4df0497a79f8'})
    base_url = 'https://napi.arvancloud.com/live/2.0/streams/'
    stream_id = 'fe4e2c83-9fc9-4fcd-beed-cbb5df622e0d'

    @staticmethod
    def get_real_ip_addr(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        remote_addr = request.META.get('REMOTE_ADDR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        elif remote_addr:
            ip = remote_addr
        else:
            ip = request.META.get('AR_REAL_IP')
        return ip

    def get_secure_link(self, ip):
        full_url = self.base_url + self.stream_id+'?secure_ip='+str(ip)
        response = self.session.get(full_url)
        reponse = response.json()
        return reponse['data']['hls_playlist']