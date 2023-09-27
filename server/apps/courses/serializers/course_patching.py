from rest_framework import serializers


class PatchRequest_EditSection(serializers.Serializer):
	index = serializers.IntegerField()

	new_index = serializers.IntegerField(
		required=False,
	)

	parent = serializers.IntegerField(
		required=False,
	)

	name = serializers.CharField(
		max_length=200,
		required=False,
	)


class PatchRequest_NewSection(serializers.Serializer):
	index = serializers.IntegerField()
	parent = serializers.IntegerField(
		allow_null=True,
	)
	name = serializers.CharField(
		max_length=200,
	)


class PatchRequest_EditPage(serializers.Serializer):
	index = serializers.IntegerField()

	section = serializers.IntegerField(
		required=False,
	)

	name = serializers.CharField(
		max_length=200,
		required=False,
	)

	content = serializers.CharField(
		required=False,
	)

	answer = serializers.DictField(
		allow_null=True,
		required=False,
	)

	new_index = serializers.IntegerField(
		required=False,
	)


class PatchRequest_NewPage(serializers.Serializer):
	index = serializers.IntegerField()

	section = serializers.IntegerField(
		# required=False,
	)

	name = serializers.CharField(
		max_length=200,
		# required=False,
	)

	content = serializers.CharField(
		# required=False,
	)

	answer = serializers.DictField(
		allow_null=True,
		# required=False,
	)


class PatchRequest(serializers.Serializer):
	course = serializers.IntegerField()

	name = serializers.CharField(
		max_length=200,
		required=False,
	)

	edit_sections = PatchRequest_EditSection(
		many=True,
		required=False,
	)

	new_sections = PatchRequest_NewSection(
		many=True,
		required=False,
	)

	delete_sections = serializers.ListField(
		child=serializers.IntegerField(),
		required=False,
	)

	edit_pages = PatchRequest_EditPage(
		many=True,
		required=False,
	)

	new_pages = PatchRequest_NewPage(
		many=True,
		required=False,
	)

	delete_pages = serializers.ListField(
		child=serializers.IntegerField(),
		required=False,
	)
