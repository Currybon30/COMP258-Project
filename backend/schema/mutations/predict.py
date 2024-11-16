import graphene
from models.model import predict

class PredictInput(graphene.InputObjectType):
    data = graphene.List(graphene.Float)

class Predict(graphene.Mutation):
    class Arguments:
        input = PredictInput(required=True)

    result = graphene.String()

    def mutate(self, info, input):
        result = predict(input.data)
        return Predict(result=str(result))
