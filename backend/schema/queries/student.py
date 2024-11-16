import graphene

class Query(graphene.ObjectType):
    get_student = graphene.String(id=graphene.Int())

    def resolve_get_student(self, info, id):
        # Mock implementation
        return f"Student with ID: {id}"
