"""
Schemas de validación para usuarios.
"""

from marshmallow import Schema, fields, validate, validates, ValidationError as MarshmallowValidationError


class UsuarioRegistroSchema(Schema):
    """Schema para validar el registro de usuarios."""

    email = fields.Email(
        required=True,
        error_messages={
            'required': 'El email es requerido',
            'invalid': 'El formato del email no es válido'
        }
    )
    password = fields.Str(
        required=True,
        validate=validate.Length(min=6, max=255),
        error_messages={
            'required': 'La contraseña es requerida',
            'invalid': 'La contraseña debe tener al menos 6 caracteres'
        }
    )
    nombre = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=100),
        error_messages={
            'required': 'El nombre es requerido',
            'invalid': 'El nombre debe tener entre 1 y 100 caracteres'
        }
    )
    apellido = fields.Str(
        required=False,
        validate=validate.Length(max=100),
        allow_none=True
    )
    rol = fields.Str(
        required=False,
        validate=validate.OneOf(['empleado', 'jefe', 'administrador']),
        missing='empleado',
        error_messages={
            'invalid': 'El rol debe ser uno de: empleado, jefe, administrador'
        }
    )

    @validates('password')
    def validate_password(self, value):
        """Validación adicional de contraseña."""
        if len(value) < 6:
            raise MarshmallowValidationError('La contraseña debe tener al menos 6 caracteres')
        if len(value) > 255:
            raise MarshmallowValidationError('La contraseña es demasiado larga')


class UsuarioLoginSchema(Schema):
    """Schema para validar el login de usuarios."""

    email = fields.Email(
        required=True,
        error_messages={
            'required': 'El email es requerido',
            'invalid': 'El formato del email no es válido'
        }
    )
    password = fields.Str(
        required=True,
        error_messages={
            'required': 'La contraseña es requerida'
        }
    )


class UsuarioUpdateSchema(Schema):
    """Schema para validar la actualización de usuarios."""

    nombre = fields.Str(
        required=False,
        validate=validate.Length(min=1, max=100)
    )
    apellido = fields.Str(
        required=False,
        validate=validate.Length(max=100),
        allow_none=True
    )
    email = fields.Email(
        required=False,
        error_messages={
            'invalid': 'El formato del email no es válido'
        }
    )
    rol = fields.Str(
        required=False,
        validate=validate.OneOf(['empleado', 'jefe', 'administrador']),
        error_messages={
            'invalid': 'El rol debe ser uno de: empleado, jefe, administrador'
        }
    )
    activo = fields.Bool(
        required=False
    )


class CambiarPasswordSchema(Schema):
    """Schema para validar el cambio de contraseña."""

    password_actual = fields.Str(
        required=True,
        error_messages={
            'required': 'La contraseña actual es requerida'
        }
    )
    password_nueva = fields.Str(
        required=True,
        validate=validate.Length(min=6, max=255),
        error_messages={
            'required': 'La contraseña nueva es requerida',
            'invalid': 'La contraseña nueva debe tener al menos 6 caracteres'
        }
    )

    @validates('password_nueva')
    def validate_password_nueva(self, value):
        """Validación adicional de contraseña nueva."""
        if len(value) < 6:
            raise MarshmallowValidationError('La contraseña nueva debe tener al menos 6 caracteres')
        if len(value) > 255:
            raise MarshmallowValidationError('La contraseña nueva es demasiado larga')
