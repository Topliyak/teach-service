from rest_framework import serializers


class CoursePostRequest_Section(serializers.Serializer):
	name = serializers.CharField()
	parent = serializers.IntegerField(
		min_value=0,
		allow_null=True,
	)


class CoursePostRequest_Page(serializers.Serializer):
	parent = serializers.IntegerField(min_value=0)
	name = serializers.CharField(allow_blank=True)
	content = serializers.CharField()
	answer = serializers.DictField(allow_null=True)


class CoursePostRequest(serializers.Serializer):
	name = serializers.CharField(min_length=3)
	sections = CoursePostRequest_Section(many=True)
	pages = CoursePostRequest_Page(many=True)
