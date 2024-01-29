import csv
import asyncio
import json

import aiohttp


START_URL = 'https://ridsport.se/appresource/4.3cb87ac0181add8e8cf3750/12.bf1aab51875678c7738f16d/search?query=&district=&municipality=&subSport=&svAjaxReqParam=ajax'


HEADERS = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'Connection': 'keep-alive',
    'Cookie': 'JSESSIONID=DC9738FEFD8E704A242A8F4D7B3A580D; SiteVisionLTM=!m2iD7ietQ1ZxeLTenlzEFn0oniVgyofn232SHiQG/t7HxehjLLeRNig1kne197mDuNDgkWMH1jk=; _tpc_persistance_cookie=!QfK5uI5pe7HsQdp6WdSYpbg81J3/XA/xFFbwhdF4+/xXDOzNG+d9o9VTaqraEMkLsljKH0o3wnqchko=; BBN019d87b7=017575bf120fa992aafb7612c15fd7da79a0542d92b9c9a6e22c1ba93c15eb8d954b80b2de045dcb33ac92cda3bac9fff0ec9be6eb; sv-cookie-consent=.c3YtaW50ZXJuYWwtc3Ytd2ViLWFuYWx5dGljcyxzdi1pbnRlcm5hbC1tdG1fY29va2llX2NvbnNlbnQ=; BBNeec01410053=082953afa5ab200032d2ea6d4a61476964d2f45f322e9a6d3a0ff0124c2da779f7402d788072004f0885a63f0a1130009a4bffae85bf49d1085c4ce8effdc48d9fbb5eac5e36625f2f808757ab2b15567dd0f766ceb2f54b90b2c966f1320481; googtrans=/sv/en; googtrans=/sv/en',
    'Host': 'ridsport.se',
    'Referer': 'https://ridsport.se/om-oss/organisation/foreningar',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"'
}


async def get_results():
    async with aiohttp.ClientSession() as session:
        async with session.get(
            START_URL,
            headers=HEADERS
        ) as response:
            try:
                res = json.loads(await response.text())
            except Exception as ex:
                return {}
            if res:
                return res


if __name__ == '__main__':
    await get_results()
