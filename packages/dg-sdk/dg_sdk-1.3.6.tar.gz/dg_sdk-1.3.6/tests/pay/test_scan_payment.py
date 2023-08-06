import unittest

import dg_sdk
from tests.conftest import *


class TestScanPayment(unittest.TestCase):

    def setUp(self):
        # dg_sdk.DGClient.mer_config = dg_sdk.MerConfig(private_key, public_key, sys_id, product_id, huifu_id)

        print("setup")

    def tearDown(self):
        print("tearDown")

    def test_payment_create(self):
        result = dg_sdk.ScanPayment.create(trade_type="A_NATIVE",
                                           trans_amt="1.00",
                                           goods_desc="test")
        assert result["resp_code"] == "00000100"

    def test_payment_query(self):
        result = dg_sdk.ScanPayment.create(trade_type="A_NATIVE",
                                           trans_amt="1.00",
                                           goods_desc="test")

        result = dg_sdk.ScanPayment.query(org_req_date=result["req_date"],
                                          org_req_seq_id=result["req_seq_id"])

        assert result["resp_code"] == "00000000"

    def test_payment_close(self):
        result = dg_sdk.ScanPayment.create(trade_type="A_NATIVE",
                                           trans_amt="1.00",
                                           goods_desc="test")

        result = dg_sdk.ScanPayment.close(org_req_date=result["req_date"],
                                          org_req_seq_id=result["req_seq_id"])

        assert result["resp_code"] == "20000001"

    def test_payment_close_query(self):
        result = dg_sdk.ScanPayment.create(trade_type="A_NATIVE",
                                           trans_amt="1.00",
                                           goods_desc="test")
        result = dg_sdk.ScanPayment.close(org_req_date=result["req_date"],
                                          org_req_seq_id=result["req_seq_id"])
        result = dg_sdk.ScanPayment.close_query(org_req_date=result["req_date"],
                                                org_req_seq_id=result["req_seq_id"])

        assert result["resp_code"] == "23000001"

    def test_payment_refund(self):
        result = dg_sdk.ScanPayment.create(trade_type="A_NATIVE",
                                           trans_amt="1.00",
                                           goods_desc="test")

        result = dg_sdk.ScanPayment.refund(ord_amt="0.01",
                                           org_req_date=result["req_date"],
                                           org_req_seq_id=result["req_seq_id"])

        assert result["resp_code"] == "23000000"

    def test_payment_refund_query(self):
        result = dg_sdk.ScanPayment.create(trade_type="A_NATIVE",
                                           trans_amt="1.00",
                                           goods_desc="test")

        result = dg_sdk.ScanPayment.refund(ord_amt="0.01",
                                           org_req_date=result["req_date"],
                                           org_req_seq_id=result["req_seq_id"])
        result = dg_sdk.ScanPayment.refund_query(org_req_date=result["req_date"],
                                                 org_req_seq_id=result["req_seq_id"])

        assert result["resp_code"] == "23000001"

    def test_union_user_id(self):
        result = dg_sdk.ScanPayment.union_user_id("fadsfa/tTBQ==")
        assert result["data"]["resp_code"] == "90000000"

    def test_micro_create(self):
        result = dg_sdk.ScanPayment.micro_create("0.10",
                                                 "test",
                                                 "12212312312312",
                                                 risk_check_data)
        assert result["resp_code"] == "10000000"

    def test_confirm(self):
        result = dg_sdk.ScanPayment.confirm(org_req_date="20220401",
                                            org_req_seq_id="22121212121221")
        assert result["resp_code"] == "23000001"

    def test_confirm_query(self):
        result = dg_sdk.ScanPayment.confirm_query(org_req_date="20220401",
                                                  org_req_seq_id="22121212121221")
        assert result["resp_code"] == "23000001"

    def test_confirm_refund(self):
        result = dg_sdk.ScanPayment.confirm_refund(org_req_date="20220401",
                                                   org_req_seq_id="22121212121221")
        assert result["resp_code"] == "23000001"

    def test_preorder_create1(self):
        hosting_data = {
            "project_title": "project_title",
            "project_id": "project_id",
            "private_info": "private_info",
            "callback_url": "https://paas.huifu.com/partners/api/#/cpjs/api_cpjs_hosting"
        }
        result = dg_sdk.ScanPayment.preorder_create(pre_order_type="1",
                                                    trans_amt="1.01",
                                                    goods_desc="goods_desc",
                                                    hosting_data=json.dumps(hosting_data))
        assert result["resp_code"] == "40000001"

    def test_preorder_create2(self):
        app_data = {
            "app_schema": "app_schema",
        }
        result = dg_sdk.ScanPayment.preorder_create(pre_order_type="2",
                                                    trans_amt="1.01",
                                                    goods_desc="goods_desc",
                                                    app_data=json.dumps(app_data))
        assert result["resp_code"] == "00000000"

    def test_preorder_create3(self):
        miniapp_data = {
            "seq_id": "",
        }
        result = dg_sdk.ScanPayment.preorder_create(pre_order_type="3",
                                                    trans_amt="1.01",
                                                    goods_desc="goods_desc",
                                                    miniapp_data=json.dumps(miniapp_data))
        assert result["resp_code"] == "00000000"
