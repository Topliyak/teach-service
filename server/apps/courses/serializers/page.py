# params
# 			- "course" int <course id>,
# 			- "num" int <page number>
#
# 		response {
# 			"name": <page name>,
# 			"content": <page content>,
# 			"answer": <answer structure or null>
# 		}

from rest_framework import serializers


class PageRequest(serializers.Serializer):
	course = serializers.IntegerField()
	num = serializers.IntegerField()


class PageResponse(serializers.Serializer):
	name = serializers.CharField()
	content = serializers.CharField()
	answer = serializers.DictField(
		allow_null=True,
	)
