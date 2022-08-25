
def getNamesGroupUser(request):
	namesGroup=[group.name for group in request.user.groups.all()]

	return {"names_group": namesGroup}