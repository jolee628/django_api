from django.http import HttpRequest, HttpResponse
from django.core import serializers
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import FBATransaction
import csv
import io
from datetime import datetime
import statistics
from .helpers import form_input_param

from pprint import pprint

# *** This will be highly relevant ***
# https://docs.djangoproject.com/en/3.1/topics/db/queries/

class TransactionsListView(GenericAPIView):
    """
    Handles retrieving and creating transactions
    """

    permission_classes = (AllowAny,)

    def get(self, request: HttpRequest):
        """
        Returns a list of transactions by the given filters

        params:
        type (str): Returns transactions of this type
        skus (list): Returns transactions with this SKU, should be sent/parsed as a comma separated string if multiple SKU's
        start (str): Returns transactions occurring after this date/time
        end (str): Returns transactions occurring before this date/time
        city (str): Returns transactions in this city
        state (str): Returns transactions in this state
        postal (str): Returns transactions in this postal address
        """
        # Dictionary containing all parameters sent in the query string
        request_data = request.GET
        input_params = form_input_param((request_data))

        print(input_params)
        transactions = FBATransaction.objects.filter(**input_params)
        tran_values = list(transactions.values())
        json_response = JsonResponse(tran_values, safe=False)
        return json_response


    @csrf_exempt
    def post(self, request: HttpRequest):
        """
        Imports a CSV file of transactions
        """

        # https://docs.djangoproject.com/en/3.1/ref/request-response/#django.http.HttpRequest.FILES
        for _, file in request.FILES.items():
            csv_file = file.read().decode('utf-8')
            io_string = io.StringIO(csv_file)
            next(io_string)

            for col in csv.reader(io_string, delimiter=','):

                # When putting time into the database, convert it to datetime.
                # In this example, it was confirmed that only PDT and PST were in the dataset
                # simply remove them for simplicity

                date_time = col[0].strip(" PDT") if "PDT" in col[0] else col[0].strip(" PST")
                date_time = datetime.strptime(date_time, "%b %d, %Y %I:%M:%S %p")

                FBATransaction.objects.get_or_create(
                    date_time = date_time,
                    type = col[1],
                    order_id = col[2],
                    sku = col[3],
                    description = col[4],
                    quantity = None if col[5] == '' else col[5],
                    order_city = col[6],
                    order_state = col[7],
                    order_postal = col[8],
                    total_price = col[9]
                )

        return Response("ok", status=status.HTTP_200_OK)


class TransactionsStatsView(GenericAPIView):
    """
    Returns aggregated stats of transactions by the given filters
    """

    permission_classes = (AllowAny,)

    def get(self, request: HttpRequest):
        """
        Returns a response containing the summed, average, and median totals for transactions using any given filters.

        params:
        type (str): Returns transactions of this type
        skus (list): Returns transactions with this SKU, should be sent/parsed as a comma separated string if multiple SKU's
        start (str): Returns transactions occurring after this date/time
        end (str): Returns transactions occurring before this date/time
        city (str): Returns transactions in this city
        state (str): Returns transactions in this state
        postal (str): Returns transactions in this postal address
        """
        # Contains all parameters sent in the query string
        request_data = request.GET
        input_params = form_input_param((request_data))

        transactions = FBATransaction.objects.filter(**input_params)
        tran_values = list(transactions.values())

        # put all the prices into a list, and then use python built in method to find sum, average and median

        total_prices = [each['total_price'] for each in tran_values]
        total_prices.sort()
        sum_total_prices = sum(total_prices)
        median = statistics.median(total_prices)
        avg = sum_total_prices / len(total_prices)

        return Response({"sum": sum_total_prices, "median": median, "average": avg}, status=status.HTTP_200_OK)
