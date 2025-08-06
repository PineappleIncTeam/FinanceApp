from drf_yasg.inspectors import SwaggerAutoSchema

class CustomSwaggerAutoSchema(SwaggerAutoSchema):
    def get_security(self):
        return [{'Bearer': []}]

    def get_override_parameters(self):
        parameters = super().get_override_parameters()

        for param in parameters:
            if param.name == 'Authorization' and param.in_ == 'header':
                if param.default and not param.default.lower().startswith('bearer '):
                    param.default = f'Bearer {param.default}'
        return parameters