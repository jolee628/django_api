from datetime import datetime

def form_input_param(request_data):
    """
    Check what params were sent, and then create the input_params for using the django object accordingly
    :param request_data:
    :return: input_params
    """

    requested_params_keys = list(request_data.dict().keys())
    input_params = {}

    if 'type' in requested_params_keys:
        input_params['type__iexact'] = request_data['type']

    if 'skus' in requested_params_keys:
        input_params['sku__in'] = request_data['skus'].split(',')

    # Assuming the input time will look something like this: 2020-11-05-00:00:00

    if 'start' in requested_params_keys:
        input_params['date_time__range'] = [datetime.strptime(request_data['start'], "%Y-%m-%d-%H:%M:%S"),
                                            datetime.now()]

    if 'end' in requested_params_keys:
        input_params['date_time__lt'] = datetime.strptime(request_data['end'], "%Y-%m-%d-%H:%M:%S")

    if 'city' in requested_params_keys:
        input_params['order_city__iexact'] = request_data['city']

    if 'state' in requested_params_keys:
        input_params['order_state__iexact'] = request_data['state']

    if 'postal' in requested_params_keys:
        input_params['order_postal__iexact'] = request_data['postal']

    return input_params