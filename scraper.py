import csv
import asyncio
import json
import logging

import aiohttp

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


HEADERS = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'Connection': 'keep-alive',
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
    results_url = 'https://ridsport.se/appresource/4.3cb87ac0181add8e8cf3750/12.bf1aab51875678c7738f16d/search?query' \
                  '=&district=&municipality=&subSport=&svAjaxReqParam=ajax '
    async with aiohttp.ClientSession() as session:
        async with session.get(
            results_url,
            headers=HEADERS
        ) as response:
            res = json.loads(await response.text())
            return res['organisations']


async def get_organization_details(res, session):
    url = f'https://ridsport.se/appresource/4.3cb87ac0181add8e8cf3750/12.bf1aab51875678c7738f16d/organisation' \
          f'?organisationId={res["id"]}&svAjaxReqParam=ajax'
    async with session.get(
        url,
        headers=HEADERS
    ) as response:
        res_text = await response.text()
        try:
            json_res = json.loads(res_text)
        except Exception as ex:
            logger.exception(ex)
        if json_res:
            return json_res['organisation']


async def main():
    all_organisations = await get_results()

    connector = aiohttp.TCPConnector(limit=10)
    async with aiohttp.ClientSession(connector=connector) as session:
        get_detail_tasks = [get_organization_details(org, session) for org in all_organisations if org]
        detailed_organizations = await asyncio.gather(*get_detail_tasks)

    logger.info(f"Extracted {len(detailed_organizations)} organizations. Writing to csv..")
    with open("swedish_equastrian_associations.csv", "w+") as organizations_csv:
        fieldnames = ['Name', 'Associate Code', 'Phone', 'Email', 'Website', 'Address', 'Postal Code', 'County']
        writer = csv.writer(organizations_csv)
        writer.writerow(fieldnames)

        for row in detailed_organizations:
            row_data = [
                row['Organisation_name']['full_name'],
                row.get('code'),
                row.get('Telephone_number', {}).get('phone_1'),
                row.get('Electronic_address', {}).get('email'),
                row.get('Electronic_address', {}).get('homepage'),
                row.get('Postal_address', {}).get('street_address').replace(';', ' '),
                row.get('Postal_address', {}).get('postal_code'),
                row.get('Postal_address', {}).get('postal_place')
            ]
            writer.writerow(row_data)

if __name__ == '__main__':
    asyncio.run(main())
