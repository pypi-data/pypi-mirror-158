"""
pykist 패키지의 public api 모음
"""

# Copyright 2022 Jueon Park
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from datetime import datetime, timedelta
from collections import namedtuple
from typing import NamedTuple, Optional, Dict, Iterable, Any, List, Tuple, Callable
import json
import time
import requests
import pandas as pd

Json = Dict[str, Any]


# request 관련 유틸리티------------------


class APIRequestParameter(NamedTuple):
    """
    API request용 파라미터를 나타내는 클래스
    """
    url_path: str
    tr_id: Optional[str]
    params: Json
    requires_authentication: bool = True
    requires_hash: bool = False
    extra_header: Optional[Json] = None


class APIResponse:
    """
    API에서 반환된 응답을 나타내는 클래스
    """

    def __init__(self, resp: requests.Response) -> None:
        self.http_code: int = resp.status_code
        self.header: Json = self._header(resp)
        self.body: Json = resp.json()
        self.message: str = self._message()
        self.return_code: Optional[str] = self._return_code()
        self.outputs: List[Json] = self._outputs()

    def is_ok(self) -> bool:
        """
        아무런 오류가 없는 경우 True, 오류가 있는 경우 False를 반환한다.
        """
        return self.http_code == 200 and (self.return_code == "0" or self.return_code is None)

    def raise_if_error(self, check_http_error=True, check_return_code=True) -> None:
        """
        오류가 난 경우 예외를 던진다.
        """
        error_message = f"http response: {self.http_code}, " + \
                        f"return code: {self.return_code}. msg: {self.message}"

        if check_http_error and self.http_code != 200:
            raise RuntimeError(error_message)

        if check_return_code and self.return_code != "0" and self.return_code is not None:
            raise RuntimeError(error_message)

    def _message(self) -> str:
        """
        API의 response에서 응답 메시지를 찾아서 반환한다. 없는 경우 빈 문자열을 반환.
        """
        if "msg" in self.body:
            return self.body["msg"]

        if "msg1" in self.body:
            return self.body["msg1"]

        return ""

    def _return_code(self) -> Optional[str]:
        """
        API에서 성공/실패를 나타내는 return code를 찾아서 반환한다. 없는 경우 None을 반환
        """
        return self.body.get("rt_cd", None)

    def _outputs(self) -> List[Json]:
        """
        API의 output 값(ex> output, output1, output2)들을 list로 가져온다.
        뒤에 붙은 번호 순서대로(output이 있는 경우 제일 앞) 배치한다.
        """
        target_keys = ["output", "output1", "output2"]
        ret = [self.body[target]
               for target in target_keys if target in self.body]

        return ret

    def _header(self, resp: requests.Response) -> Json:
        """
        API의 response에서 header 정보를 찾아서 반환한다.
        """
        header = {}
        for key in resp.headers.keys():
            if key.islower():
                header[key] = resp.headers.get(key)
        return header


def merge_json(datas: Iterable[Json]) -> Json:
    """
    여러개의 json 형식 데이터를 하나로 통합하여 반환한다.
    동일한 key가 있는 경우 뒤에 있는 원소로 덮어쓴다.
    """
    ret = {}
    for data in datas:
        for key, value in data.items():
            ret[key] = value
    return ret


def to_namedtuple(name: str, json_data: Json) -> NamedTuple:
    """
    json 형식의 데이터를 NamedTuple 타입으로 반환한다.
    """
    _x = namedtuple(name, json_data.keys())
    return _x(**json_data)


def get_base_headers() -> Json:
    """
    api에 사용할 header의 기본 base를 반환한다.
    """
    base = {
        "Content-Type": "application/json",
        "Accept": "text/plain",
        "charset": "UTF-8",
    }

    return base


def send_get_request(url: str, headers: Json, params: Json, raise_flag: bool = True) -> APIResponse:
    """
    HTTP GET method로 request를 보내고 APIResponse 객체를 반환한다.
    """
    resp = requests.get(url, headers=headers, params=params)
    api_resp = APIResponse(resp)

    if raise_flag:
        api_resp.raise_if_error()

    return api_resp


def send_post_request(url: str, headers: Json, params: Json,
                      raise_flag: bool = True) -> APIResponse:
    """
    HTTP POST method로 request를 보내고 APIResponse 객체를 반환한다.
    """
    resp = requests.post(url, headers=headers, data=json.dumps(params))
    api_resp = APIResponse(resp)

    if raise_flag:
        api_resp.raise_if_error()

    return api_resp


def none_to_empty_dict(data: Optional[Json]) -> Json:
    """
    입력 값이 None인 경우에 빈 dictionary를 반환한다.
    """
    return data if data is not None else {}

# request 관련 유틸리티------------------


class DomainInfo:
    """
    도메인 정보를 나타내는 클래스. (실제 투자, 모의 투자, etc)
    """

    def __init__(self, kind: Optional[str] = None, url: Optional[str] = None) -> None:
        self.kind = kind
        self.base_url = self._base_url(url)

    def get_url(self, url_path: str):
        """
        url_path를 입력받아서 전체 url을 반환한다.
        """
        separator = "" if url_path.startswith("/") else "/"
        return f"{self.base_url}{separator}{url_path}"

    def _base_url(self, input_url: Optional[str]) -> str:
        """
        domain 정보를 나타내는 base url 반환한다. 잘못된 입력의 경우 예외를 던진다.
        """
        if self.kind == "real":
            return "https://openapi.koreainvestment.com:9443"

        if self.kind == "virtual":
            return "https://openapivts.koreainvestment.com:29443"

        if self.kind is None and input_url is not None:
            return input_url

        raise RuntimeError("invalid domain info")

    def is_real(self) -> bool:
        """
        실제 투자용 도메인 정보인지 여부를 반환한다.
        """
        return self.kind == "real"

    def is_virtual(self) -> bool:
        """
        모의 투자용 도메인 정보인지 여부를 반환한다.
        """
        return self.kind == "virtual"

    def adjust_tr_id(self, tr_id: Optional[str]) -> str:
        """
        모의 투자인 경우, tr_id를 필요에 따라 변경한다.
        """
        if tr_id is not None and self.is_virtual():
            if len(tr_id) >= 1 and tr_id[0] in ["T", "J", "C"]:
                return "V" + tr_id[1:]
        return tr_id


class AccessToken:
    """
    인증용 토큰 정보를 담을 클래스
    """

    def __init__(self) -> None:
        self.value: Optional[str] = None
        self.valid_until: Optional[datetime] = None

    def create(self, resp: NamedTuple) -> None:
        """
        Token을 생성한다.
        """
        self.value: str = f"Bearer {str(resp.access_token)}"
        self.valid_until: datetime = self._valid_until(resp)

    def _valid_until(self, resp: NamedTuple) -> datetime:
        """
        현재 시각 기준으로 Token의 유효기한을 반환한다.
        """
        time_margin = 60
        duration = int(resp.expires_in) - time_margin
        return datetime.now() + timedelta(seconds=duration)

    def is_valid(self) -> bool:
        """
        Token이 유효한지 검사한다.
        """
        return self.value is not None and \
            self.valid_until is not None and \
            datetime.now() < self.valid_until


class Api:
    """
    pykis의 public api를 나타내는 클래스
    """

    def __init__(self, key_info: Json, domain_info: DomainInfo = DomainInfo(kind="real"),
                 account_info: Optional[Json] = None) -> None:
        """
        key_info: API 사용을 위한 인증키 정보. appkey, appsecret
        domain_info: domain 정보 (실전/모의/etc)
        account_info: 사용할 계좌 정보.
                    { "account_code" : "[계좌번호 앞 8자리 숫자]", "product_code" : "[계좌번호 뒤 2자리 숫자]" }
        """
        self.key: Json = key_info
        self.domain: DomainInfo = domain_info
        self.token: AccessToken = AccessToken()
        self.account: Optional[NamedTuple] = None

        self.set_account(account_info)

    def set_account(self, account_info: Optional[Json]) -> None:
        """
        사용할 계좌 정보를 설정한다.
        account_info: 사용할 계좌 정보.
                    { "account_code" : "[계좌번호 앞 8자리 숫자]", "product_code" : "[계좌번호 뒤 2자리 숫자]" }
        """
        if account_info is not None:
            self.account = to_namedtuple("account", account_info)

    # 인증-----------------

    def create_token(self) -> None:
        """
        access token을 발급한다.
        """
        url_path = "/oauth2/tokenP"

        params = merge_json([
            self.get_api_key_data(),
            {
                "grant_type": "client_credentials"
            }
        ])

        req = APIRequestParameter(url_path, tr_id=None,
                                  params=params, requires_authentication=False, requires_hash=False)
        response = self._send_post_request(req)
        body = to_namedtuple("body", response.body)

        self.token.create(body)

    def need_authentication(self) -> bool:
        """
        authentication이 필요한지 여부를 반환한다.
        """
        return not self.token.is_valid()

    def set_hash_key(self, header: Json, param: Json) -> None:
        """
        header에 hash key 설정한다.
        """
        hash_key = self.get_hash_key(param)
        header["hashkey"] = hash_key

    def get_hash_key(self, params: Json) -> str:
        """
        hash key 값을 가져온다.
        """
        url_path = "/uapi/hashkey"
        req = APIRequestParameter(url_path, tr_id=None,
                                  params=params, requires_authentication=False, requires_hash=False)
        response = self._send_post_request(req)

        return response.body["HASH"]

    def get_api_key_data(self) -> Json:
        """
        사용자의 api key 데이터를 반환한다.
        """
        return self.key

    # 인증-----------------

    # 시세 조회------------
    def get_kr_current_price(self, ticker: str) -> int:
        """
        국내 주식 현재가를 반환한다.
        ticker: 종목코드
        return: 해당 종목 현재가 (단위: 원)
        """
        info = self._get_kr_stock_current_price_info(ticker)
        price = info["stck_prpr"]

        return int(price)

    def get_kr_max_price(self, ticker: str) -> int:
        """
        국내 주식의 상한가를 반환한다.
        ticker: 종목코드
        return: 해당 종목의 상한가 (단위: 원)
        """
        info = self._get_kr_stock_current_price_info(ticker)
        price = info["stck_mxpr"]

        return int(price)

    def get_kr_min_price(self, ticker: str) -> int:
        """
        국내 주식의 하한가를 반환한다.
        ticker: 종목코드
        return: 해당 종목의 하한가 (단위: 원)
        """
        info = self._get_kr_stock_current_price_info(ticker)
        price = info["stck_llam"]

        return int(price)

    def _get_kr_stock_current_price_info(self, ticker: str) -> Json:
        """
        국내 주식 현재가 시세 정보를 반환한다.
        ticker: 종목코드
        return: 해당 종목 현재 시세 정보
        """
        url_path = "/uapi/domestic-stock/v1/quotations/inquire-price"

        tr_id = "FHKST01010100"

        params = {
            "FID_COND_MRKT_DIV_CODE": "J",
            "FID_INPUT_ISCD": ticker
        }

        req = APIRequestParameter(url_path, tr_id, params)
        res = self._send_get_request(req)
        return res.outputs[0]

    def _get_kr_history(self, ticker: str, time_unit: str = "D") -> APIResponse:
        """
        해당 종목코드의 과거 가격 조회한다.
        ticker: 종목 코드
        time_unit: 기간 분류 코드 (d/day-일, w/week-주, m/month-월)
        """
        time_unit = time_unit.upper()

        if time_unit in ["DAYS", "DAY"]:
            time_unit = "D"
        elif time_unit in ["WEEKS", "WEEK"]:
            time_unit = "W"
        elif time_unit in ["MONTHS", "MONTH"]:
            time_unit = "M"

        url_path = "/uapi/domestic-stock/v1/quotations/inquire-daily-price"
        tr_id = "FHKST01010400"

        params = {
            "FID_COND_MRKT_DIV_CODE": "J",
            "FID_INPUT_ISCD": ticker,
            "FID_PERIOD_DIV_CODE": time_unit,
            "FID_ORG_ADJ_PRC": "0000000001"
        }

        req = APIRequestParameter(url_path, tr_id, params)

        return self._send_get_request(req, raise_flag=False)

    def get_kr_ohlcv(self, ticker: str, time_unit: str = "D") -> pd.DataFrame:
        """
        해당 종목코드의 과거 가격 정보를 DataFrame으로 반환한다.
        ticker: 종목 코드
        time_unit: 기간 분류 코드 (D/day-일, W/week-주, M/month-월)
        데이터는 최근 30 일/주/월 데이터로 제한됨
        """
        res = self._get_kr_history(ticker, time_unit)
        if not res.is_ok() or len(res.outputs) == 0 or len(res.outputs[0]) == 0:
            return pd.DataFrame()

        date_column = ["Date"]
        other_colums = ["Open", "High", "Low", "Close", "Volume"]

        keys = ["stck_bsop_date", "stck_oprc",
                "stck_hgpr", "stck_lwpr", "stck_clpr", "acml_vol"]
        values = date_column + other_colums

        data = pd.DataFrame(res.outputs[0])

        data = data[keys]
        rename_map = dict(zip(keys, values))

        data.rename(columns=rename_map, inplace=True)

        data[date_column] = data[date_column].apply(pd.to_datetime)
        data[other_colums] = data[other_colums].apply(pd.to_numeric)
        data.set_index("Date", inplace=True)

        return data

    # 시세 조회------------

    # 잔고 조회------------
    def get_kr_buyable_cash(self) -> int:
        """
        구매 가능 현금(원화) 조회
        return: 해당 계좌의 구매 가능한 현금(원화)
        """
        url_path = "/uapi/domestic-stock/v1/trading/inquire-daily-ccld"
        tr_id = "TTTC8908R"

        if self.account is None:
            msg = "계좌가 설정되지 않았습니다. set_account를 통해 계좌 정보를 설정해주세요."
            raise RuntimeError(msg)

        stock_code = ""
        qry_price = 0

        params = {
            "CANO": self.account.account_code,
            "ACNT_PRDT_CD": self.account.product_code,
            "PDNO": stock_code,
            "ORD_UNPR": str(qry_price),
            "ORD_DVSN": "02",
            "CMA_EVLU_AMT_ICLD_YN": "Y",
            "OVRS_ICLD_YN": "N"
        }

        req = APIRequestParameter(url_path, tr_id, params)
        res = self._send_get_request(req)
        output = res.outputs[0]
        return int(output["ord_psbl_cash"])

    def _send_continuous_query(self, request_function: Callable[[Json, Json], APIResponse],
                               to_dataframe:
                               Callable[[APIResponse], pd.DataFrame]) -> pd.DataFrame:
        """
        조회 결과가 100건 이상 존재하는 경우 연속하여 query 후 전체 결과를 DataFrame으로 통합하여 반환한다.
        """
        max_count = 100
        outputs = []

        # 초기값
        extra_header = {}
        extra_param = {}

        for i in range(max_count):
            if i > 0:
                extra_header = {"tr_cont": "N"}    # 공백 : 초기 조회, N : 다음 데이터 조회

            res = request_function(
                extra_header=extra_header,
                extra_param=extra_param
            )
            output = to_dataframe(res)
            outputs.append(output)

            response_tr_cont = res.header["tr_cont"]
            no_more_data = response_tr_cont not in ["F", "M"]

            if no_more_data:
                break

            extra_param["CTX_AREA_FK100"] = res.body["ctx_area_fk100"]
            extra_param["CTX_AREA_NK100"] = res.body["ctx_area_nk100"]

        return pd.concat(outputs)

    def _get_kr_total_balance(self, extra_header: Json = None,
                              extra_param: Json = None) -> APIResponse:
        """
        국내 주식 잔고의 조회 전체 결과를 반환한다.
        """
        url_path = "/uapi/domestic-stock/v1/trading/inquire-balance"
        tr_id = "TTTC8434R"

        extra_header = none_to_empty_dict(extra_header)
        extra_param = none_to_empty_dict(extra_param)

        extra_header = merge_json([{"tr_cont": ""}, extra_header])

        params = {
            "CANO": self.account.account_code,
            "ACNT_PRDT_CD": self.account.product_code,
            "AFHR_FLPR_YN": "N",
            "FNCG_AMT_AUTO_RDPT_YN": "N",
            "FUND_STTL_ICLD_YN": "N",
            "INQR_DVSN": "01",
            "OFL_YN": "N",
            "PRCS_DVSN": "01",
            "UNPR_DVSN": "01",
            "CTX_AREA_FK100": "",
            "CTX_AREA_NK100": ""
        }

        params = merge_json([params, extra_param])
        req = APIRequestParameter(url_path, tr_id, params,
                                  extra_header=extra_header)
        return self._send_get_request(req)

    def get_kr_stock_balance(self) -> pd.DataFrame:
        """
        국내 주식 잔고 조회
        return: 국내 주식 잔고 정보를 DataFrame으로 반환
        """

        def to_dataframe(res: APIResponse) -> pd.DataFrame:
            tdf = pd.DataFrame(res.outputs[0])
            if tdf.empty:
                return tdf

            tdf.set_index("pdno", inplace=True)
            cf1 = ["prdt_name", "hldg_qty", "ord_psbl_qty", "pchs_avg_pric",
                   "evlu_pfls_rt", "prpr", "bfdy_cprs_icdc", "fltt_rt"]
            cf2 = ["종목명", "보유수량", "매도가능수량", "매입단가", "수익율", "현재가", "전일대비", "등락"]
            tdf = tdf[cf1]
            tdf[cf1[1:]] = tdf[cf1[1:]].apply(pd.to_numeric)
            ren_dict = dict(zip(cf1, cf2))
            return tdf.rename(columns=ren_dict)

        return self._send_continuous_query(self._get_kr_total_balance, to_dataframe)

    def get_kr_deposit(self) -> int:
        """
        국내 주식 잔고의 총 예수금을 반환한다.
        """
        res = self._get_kr_total_balance()

        output2 = res.outputs[1]
        return int(output2[0]["dnca_tot_amt"])
    # 잔고 조회------------

    # 주문 조회------------
    def _get_kr_orders_once(self, extra_header: Json = None,
                            extra_param: Json = None) -> APIResponse:
        """
        취소/정정 가능한 국내 주식 주문 목록을 반환한다.
        한번만 실행.
        """
        url_path = "/uapi/domestic-stock/v1/trading/inquire-psbl-rvsecncl"
        tr_id = "TTTC8036R"

        extra_header = none_to_empty_dict(extra_header)
        extra_param = none_to_empty_dict(extra_param)

        extra_header = merge_json([{"tr_cont": ""}, extra_header])

        params = {
            "CANO": self.account.account_code,
            "ACNT_PRDT_CD": self.account.product_code,
            "CTX_AREA_FK100": "",
            "CTX_AREA_NK100": "",
            "INQR_DVSN_1": "0",
            "INQR_DVSN_2": "0"
        }

        params = merge_json([params, extra_param])
        req = APIRequestParameter(url_path, tr_id, params,
                                  extra_header=extra_header)
        res = self._send_get_request(req)

        return res

    def get_kr_orders(self) -> pd.DataFrame:
        """
        취소/정정 가능한 국내 주식 주문 목록을 DataFrame으로 반환한다.
        """
        def sell_or_buy(value):  # 01: 매도, 02: 매수
            return "매도" if value == "01" else "매수"

        def to_dataframe(res: APIResponse) -> pd.DataFrame:
            data = pd.DataFrame(res.outputs[0])
            if data.empty:
                return data

            data.set_index("odno", inplace=True)
            keys = ["pdno", "ord_qty", "psbl_qty", "ord_unpr", "sll_buy_dvsn_cd",
                    "ord_tmd", "ord_gno_brno", "orgn_odno"]
            values = ["종목코드", "주문수량", "정정취소가능수량",
                      "주문가격", "매수매도구분", "시간", "주문점", "원번호"]
            data = data[keys]
            sell_or_buy_column = "sll_buy_dvsn_cd"

            data[sell_or_buy_column] = data[sell_or_buy_column].apply(
                sell_or_buy)

            rename_map = dict(zip(keys, values))
            data = data.rename(columns=rename_map)

            return data

        return self._send_continuous_query(self._get_kr_orders_once, to_dataframe)

    # 주문 조회------------

    # 매매-----------------

    def _send_kr_stock_order(self, ticker: str, order_amount: int, price: int, buy: bool) -> Json:
        """
        국내 주식 매매(현금)
        """
        order_type = "00"  # 00: 지정가, 01: 시장가, ...
        if price <= 0:
            price = 0
            order_type = "01"   # 시장가

        url_path = "/uapi/domestic-stock/v1/trading/order-cash"

        if buy:
            tr_id = "TTTC0802U"  # buy
        else:
            tr_id = "TTTC0801U"  # sell

        params = {
            "CANO": self.account.account_code,
            "ACNT_PRDT_CD": self.account.product_code,
            "PDNO": ticker,
            "ORD_DVSN": order_type,
            "ORD_QTY": str(order_amount),
            "ORD_UNPR": str(price),
            "CTAC_TLNO": "",
            # "SLL_TYPE": "01",
            "ALGO_NO": ""
        }

        req = APIRequestParameter(url_path, tr_id=tr_id,
                                  params=params, requires_authentication=True, requires_hash=True)

        response = self._send_post_request(req)
        return response.outputs[0]

    def buy_kr_stock(self, ticker: str, order_amount: int, price: int) -> Json:
        """
        국내 주식 매수(현금)
        ticker: 종목코드
        order_amount: 주문 수량
        price: 주문 가격
        """
        return self._send_kr_stock_order(ticker, order_amount, price, True)

    def sell_kr_stock(self, ticker: str, order_amount: int, price: int) -> Json:
        """
        국내 주식 매매(현금)
        ticker: 종목코드
        order_amount: 주문 수량
        price: 주문 가격
        """
        return self._send_kr_stock_order(ticker, order_amount, price, False)

    # 매매-----------------

    # 정정/취소-------------
    def _revise_cancel_kr_orders(self,  # pylint: disable=too-many-arguments
                                 order_number: str,
                                 is_cancel: bool,
                                 price: int,
                                 amount: Optional[int] = None,
                                 order_branch: str = "06010"
                                 ) -> Json:
        """
        국내 주식 주문을 정정 또는 취소한다
        order_number: 주문 번호
        order_branch: 주문점(통상 06010)
        amount: 정정/취소 적용할 주문의 수량
        price: 정정할 주문의 가격
        is_cancel: 정정구분(취소-True, 정정-False)
        return: 서버 response
        """
        url_path = "/uapi/domestic-stock/v1/trading/order-rvsecncl"
        tr_id = "TTTC0803U"

        order_dv: str = "00"  # order_dv: 주문유형(00-지정가)
        cancel_dv: str = "02" if is_cancel else "01"

        apply_all = "N"  # apply_all: 잔량전부주문여부(Y-잔량전부, N-잔량일부)

        if amount is None or amount <= 0:
            apply_all = "Y"
            amount = 1

        params = {
            "CANO": self.account.account_code,
            "ACNT_PRDT_CD": self.account.product_code,
            "KRX_FWDG_ORD_ORGNO": order_branch,
            "ORGN_ODNO": order_number,
            "ORD_DVSN": order_dv,
            "RVSE_CNCL_DVSN_CD": cancel_dv,
            "ORD_QTY": str(amount),
            "ORD_UNPR": str(price),
            "QTY_ALL_ORD_YN": apply_all
        }

        req = APIRequestParameter(url_path, tr_id=tr_id,
                                  params=params, requires_authentication=True, requires_hash=True)

        res = self._send_post_request(req)
        return res.body

    def cancel_kr_order(self, order_number: str, amount: Optional[int] = None,
                        order_branch: str = "06010") -> Json:
        """
        국내 주식 주문을 취소한다.
        order_number: 주문 번호.
        amount: 취소할 수량. 지정하지 않은 경우 잔량 전부 취소.
        return: 서버 response.
        """

        return self._revise_cancel_kr_orders(order_number=order_number,
                                             is_cancel=True,
                                             amount=amount,
                                             price=1,
                                             order_branch=order_branch)

    def cancel_all_kr_orders(self) -> None:
        """
        미체결된 모든 국내 주식 주문들을 취소한다.
        """
        data = self.get_kr_orders()
        orders = data.index.to_list()
        branchs = data["주문점"].to_list()
        delay = 0.2  # sec

        for order, branch in zip(orders, branchs):
            self.cancel_kr_order(order, order_branch=branch)
            time.sleep(delay)

    def revise_kr_order(self, order_number: str,
                        price: int,
                        amount: Optional[int] = None,
                        order_branch: str = "06010") -> Json:
        """
        국내 주식 주문의 가격을 정정한다.
        order_number: 주문 번호.
        price: 정정할 1주당 가격.
        amount: 정정할 수량. 지정하지 않은 경우 잔량 전부 정정.
        return: 서버 response.
        """

        return self._revise_cancel_kr_orders(order_number=order_number,
                                             is_cancel=False,
                                             amount=amount,
                                             price=price,
                                             order_branch=order_branch)
    # 정정/취소-------------

    # HTTTP----------------

    def _send_get_request(self, req: APIRequestParameter, raise_flag: bool = True) -> APIResponse:
        """
        HTTP GET method로 request를 보내고 response를 반환한다.
        """
        url = self.domain.get_url(req.url_path)
        headers = self._parse_headers(req)
        return send_get_request(url, headers, req.params, raise_flag=raise_flag)

    def _send_post_request(self, req: APIRequestParameter, raise_flag: bool = True) -> APIResponse:
        """
        HTTP GET method로 request를 보내고 response를 반환한다.
        """
        url = self.domain.get_url(req.url_path)
        headers = self._parse_headers(req)

        if req.requires_hash:
            self.set_hash_key(headers, req.params)
        return send_post_request(url, headers, req.params, raise_flag=raise_flag)

    def _parse_headers(self, req: APIRequestParameter) -> Tuple[str, Json]:
        """
        API에 request에 필요한 header를 구해서 튜플로 반환한다.
        """

        headers = [
            get_base_headers(),
            self.get_api_key_data(),
        ]

        tr_id = self.domain.adjust_tr_id(req.tr_id)

        if tr_id is not None:
            headers.append({"tr_id": tr_id})

        if req.requires_authentication:
            if self.need_authentication():
                self.create_token()

            headers.append({
                "authorization": self.token.value,
            })

        extra_header = none_to_empty_dict(req.extra_header)
        headers.append(extra_header)

        headers = merge_json(headers)

        return headers

    # HTTTP----------------
