from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import (
	contents as contents_serializers,
	page as page_serializers,
	course_posting as course_posting_serializers,
	course_patching as course_patching_serializers,
)

from .services import (
	contents as contents_services,
	page as page_services,
	course as course_services,
)


@api_view(['GET'])
def contents(request):
	request_ser = contents_serializers.ContentsRequest(data=request.GET)

	if request_ser.is_valid() is False:
		return Response('Invalid parameters', status=status.HTTP_400_BAD_REQUEST)

	contents = contents_services.get_contents(*request_ser.data.values())
	resp_ser = contents_serializers.Contents(instance=contents)

	return Response(resp_ser.data)


@api_view(['GET'])
def page(request):
	req_ser = page_serializers.PageRequest(data=request.GET)

	if req_ser.is_valid() is False:
		return Response('Invalid parameters', status=status.HTTP_400_BAD_REQUEST)

	page = page_services.get_page(**req_ser.data)
	resp_ser = page_serializers.PageResponse(instance=page)

	return Response(resp_ser.data)


class Course(APIView):
	def post(self, request):
		if request.user.is_authenticated is False:
			return Response('For post course you must be authenticated', status=status.HTTP_403_FORBIDDEN)

		req_ser = course_posting_serializers.CoursePostRequest(data=request.data)

		req_ser.is_valid(raise_exception=True)

		course_services.try_add_course(
			name=req_ser.data['name'],
			sections_dicts=req_ser.data['sections'],
			pages_dicts=req_ser.data['pages'],
			author=request.user,
		)

		return Response('Success', status=status.HTTP_200_OK)

	def patch(self, request):
		if request.user.is_authenticated is False:
			return Response('For edit course you must be authenticated', status=status.HTTP_403_FORBIDDEN)

		req_ser = course_patching_serializers.PatchRequest(data=request.data)
		req_ser.is_valid(raise_exception=True)

		course_services.edit_course(
			course_id=req_ser.data['course'],
			editor=request.user,
			**req_ser.data
		)

		return Response('Success', status=status.HTTP_200_OK)
