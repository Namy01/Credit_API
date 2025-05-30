
from rest_framework.response import Response
from rest_framework import status


def helper_function(data, message, status_code):
   return Response(
      {
         "status_code": status_code,
         "message": message,
         "data": data
         
      }, status=status_code
   )


def helper_function2(dataset, request):
    method = request.method.upper()

    if method == "GET":
        if dataset:
            return helper_function(
                data=dataset,
                message="Success",
                status_code=status.HTTP_200_OK
            )
        else:
            return helper_function(
                data=None,
                message="No data found",
                status_code=status.HTTP_404_NOT_FOUND
            )

    elif method == "POST":
        if hasattr(dataset, "is_valid") and dataset.is_valid():
            dataset.save()
            return helper_function(
                data=dataset.data,
                message="Successfully created",
                status_code=status.HTTP_201_CREATED
            )
        else:
            return helper_function(
                data=dataset.errors if hasattr(dataset, "errors") else None,
                message="Validation failed",
                status_code=status.HTTP_400_BAD_REQUEST
            )