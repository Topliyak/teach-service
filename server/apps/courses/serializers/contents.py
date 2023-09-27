from rest_framework import serializers


class ContentsRequest(serializers.Serializer):
	course = serializers.IntegerField()


class Contents_Section(serializers.Serializer):
	name = serializers.CharField()

	parent = serializers.IntegerField(
		allow_null=True,
	)


class Contents_Page(serializers.Serializer):
	name = serializers.CharField()
	parent = serializers.IntegerField()


class Contents(serializers.Serializer):
	sections = Contents_Section(
		many=True,
	)

	pages = Contents_Page(
		many=True,
	)
