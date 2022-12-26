from hashlib import md5


def is_valid_prepare_sign(query_params: dict):
    sign_string = f'{query_params["click_trans_id"]}{query_params["service_id"]}cK2fYQ9WtyiWjF{query_params["merchant_trans_id"]}{query_params["amount"]}{query_params["action"]}{query_params["sign_time"]}'
    return query_params["sign_string"] == md5(sign_string.encode()).hexdigest()


def is_valid_complete_sign(query_params: dict):
    sign_string = f'{query_params["click_trans_id"]}{query_params["service_id"]}cK2fYQ9WtyiWjF{query_params["merchant_trans_id"]}{query_params["merchant_prepare_id"]}{query_params["amount"]}{query_params["action"]}{query_params["sign_time"]}'
    return query_params["sign_string"] == md5(sign_string.encode()).hexdigest()