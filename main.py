import json
import time
from pprint import pprint
import boto3
import pandas as pd
from botocore.exceptions import ClientError
import os
import requests
from dotenv import load_dotenv

from streamlit_stats import StreamlitStatistics

load_dotenv()


def github_connector(github_access_token):
    username = "omkarjawaji"
    url_prefix = f'https://api.github.com'
    url = f"{url_prefix}/users/{username}/repos"
    headers = {
        "Authorization": f"token {github_access_token}"
    }

    response = requests.get(url, headers=headers)
    stats_data = list()
    if response.status_code == 200:
        repos = response.json()
        for repo in repos:
            content_url = f"{url_prefix}/repos/{username}/{repo['name']}/contents/"
            contents_response = requests.get(content_url, headers=headers)
            check_list = [True if content_file['name'].find('.ipynb') != -1 else False for content_file in
                          json.loads(contents_response.text)]
            if True in check_list:
                stats_data.append([repo['name'], repo['html_url'], True])
            else:
                stats_data.append([repo['name'], repo['html_url'], False])

    else:
        print("Error:", response.status_code)

    return stats_data


def fetch_github_creds_aws(aws_access_key, aws_secret_key_id, secret_id):
    client = boto3.client('secretsmanager',
                          aws_access_key_id=aws_access_key,
                          aws_secret_access_key=aws_secret_key_id,
                          region_name='ap-south-1')
    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_id
        )
    except ClientError as e:
        raise e

    secret = get_secret_value_response['SecretString']
    return json.loads(secret)['GITHUB_ACCESS_TOKEN']


if __name__ == '__main__':
    access_token = fetch_github_creds_aws(aws_access_key=os.getenv('AWS_ACCESS_KEY'),
                                          aws_secret_key_id=os.getenv('AWS_SECRET_ACCESS_ID'),
                                          secret_id=os.getenv('SECRET_ID'))
    streamlit_stats_data = github_connector(access_token)

    data_df = pd.DataFrame(streamlit_stats_data, columns=['name', 'link', 'file_exists'])
    ss = StreamlitStatistics(data_df)
    ss.display_stats()
