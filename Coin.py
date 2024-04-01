import requests
import pandas as pd

# 네이버 검색 API 사용
def naver_search(api_key, secret_key, query, display=10, start=1, sort="date", search_type="news"):
    """
    네이버 검색 API를 사용하여 뉴스 또는 블로그 검색 결과를 가져옴.

    :param api_key: 클라이언트 ID
    :param secret_key: 클라이언트 시크릿
    :param query: 검색 질의어
    :param display: 검색 결과 출력 건수 (기본값 10, 최대 100)
    :param start: 검색 시작 위치 (기본값 1, 최대 1000)
    :param sort: 정렬 옵션 (date: 날짜순, sim: 유사도순)
    :param search_type: 검색 타입 ("news" 또는 "blog")
    :return: 검색 결과 리스트
    """
    base_url = f"https://openapi.naver.com/v1/search/{search_type}.json"
    headers = {
        "X-Naver-Client-Id": api_key,
        "X-Naver-Client-Secret": secret_key
    }
    params = {
        "query": query,
        "display": display,
        "start": start,
        "sort": sort
    }

    response = requests.get(base_url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()['items']
    else:
        print(f"Error {response.status_code}")
        return []
    
def save_results_to_excel(news_results, blog_results, market_data, filename='search_results.xlsx'):
    # 뉴스, 블로그, 시장 데이터를 엑셀 파일로 저장
    news_df = pd.DataFrame(news_results)
    blog_df = pd.DataFrame(blog_results)
    market_df = pd.DataFrame([market_data])

    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        news_df.to_excel(writer, sheet_name='News')
        blog_df.to_excel(writer, sheet_name='Blogs')
        market_df.to_excel(writer, sheet_name='Market Data')

    print(f'{filename}로 저장 완료.')

def get_crypto_data(api_key, symbol):
    # CoinMarketCap API를 사용하여 암호화폐 시세 정보를 가져오기
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
    parameters = {"symbol": symbol, "convert": "USD"}
    headers = {"Accepts": "application/json", "X-CMC_PRO_API_KEY": api_key}

    response = requests.get(url, headers=headers, params=parameters)
    data = response.json()

    if response.status_code == 200:
        return data['data'][symbol][0]
    else:
        print(f"Error {response.status_code}: {data.get('status', {}).get('error_message', '')}")
        return {}

def main():
    # API 키, 시크릿 및 검색 질의어 설정
    client_id = "내가 발급받은 ID"
    client_secret = "내가 발급받은 SECRET"
    search_query = "암호화폐명 입력 ㄱㄱ"

    # 네이버 검색 API 결과
    news_results = naver_search(client_id, client_secret, search_query, search_type="news")
    blog_results = naver_search(client_id, client_secret, search_query, search_type="blog")

    # CoinMarketCap API 결과
    cmc_api_key = "내 코인마켓캡 API"
    market_data = get_crypto_data(cmc_api_key, search_query)

    # 결과를 엑셀로 저장
    save_results_to_excel(news_results, blog_results, market_data)

if __name__ == "__main__":
    main()
