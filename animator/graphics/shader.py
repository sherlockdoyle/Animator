"""Shaders can be used in place of colors."""
from __future__ import annotations

from pathlib import Path
from typing import Sequence

from animator import skia
from animator._common_types import ColorLike
from animator.graphics.color import color as parse_color
from animator.graphics.Context2d import CompositeOperation, _composite_operation


class Shader:
    def __init__(self, sksl: str) -> None:
        """Create a shader from the given sksl code. If the sksl code is invalid, a :class:`ValueError` will be raised.

        :param sksl: The sksl code for the shader.
        """
        result = skia.RuntimeEffect.MakeForShader(sksl)
        if result.effect is None:
            raise ValueError(result.errorText)
        self.__effect: skia.RuntimeEffect = result.effect
        self.__uniform_names: set[str] = {u.name for u in self.__effect.uniforms()}
        self.__children_names: set[str] = {c.name for c in self.__effect.children()}
        self.__builder: skia.RuntimeShaderBuilder = skia.RuntimeShaderBuilder(self.__effect)

    @classmethod
    def from_file(cls, path: str) -> Shader:
        """Create a shader from the given file *path*."""
        return cls(Path(path).read_text())

    @property
    def uniform_names(self) -> set[str]:
        """Names of the shader's uniforms."""
        return self.__uniform_names

    @property
    def children_names(self) -> set[str]:
        """Names of the shader's children."""
        return self.__children_names

    @property
    def builder(self) -> skia.RuntimeShaderBuilder:
        """The shader's builder, useful for building runtime shader image filters."""
        return self.__builder

    def build(self) -> skia.Shader:
        """Build the shader."""
        return self.__builder.makeShader()

    def get_uniform(self, name: str) -> skia.RuntimeEffectBuilder.BuilderUniform:
        """
        Get the uniform with the given *name*. Call :meth:`skia.RuntimeEffectBuilder.BuilderUniform.set` on the returned
        object to set the uniform's value.
        """
        return self.__builder.uniform(name)

    def get_child(self, name: str) -> skia.RuntimeEffectBuilder.BuilderChild:
        """
        Get the child with the given *name*. Call :meth:`skia.RuntimeEffectBuilder.BuilderChild.set` on the returned
        object to set the child's value.
        """
        return self.__builder.child(name)

    def __getitem__(
        self, name: str
    ) -> skia.RuntimeEffectBuilder.BuilderUniform | skia.RuntimeEffectBuilder.BuilderChild:
        """Get the uniform or child with the given *name*."""
        if name in self.__uniform_names:
            return self.__builder.uniform(name)
        elif name in self.__children_names:
            return self.__builder.child(name)
        raise KeyError(f'No uniform or child with name {name!r}')

    def __setitem__(
        self,
        name: str,
        value: int
        | float
        | Sequence[int]
        | Sequence[float]
        | skia.Matrix
        | skia.Color4f
        | skia.Shader
        | skia.ColorFilter
        | skia.Blender
        | None,
    ) -> None:
        """Set the uniform or child with the given *name* to the given *value*."""
        if name in self.__uniform_names:
            if not isinstance(value, (int, float, Sequence, skia.Matrix, skia.Color4f)):
                raise TypeError(f'Uniform {name!r} must be int, float, list, skia.Matrix, or skia.Color4f')
            if isinstance(value, skia.Color4f):
                value = value.vec()
            self.__builder.uniform(name).set(value)
        elif name in self.__children_names:
            if not (value is None or isinstance(value, (skia.Shader, skia.ColorFilter, skia.Blender))):
                raise TypeError(f'Child {name!r} must be skia.Shader, skia.ColorFilter, skia.Blender, or None')
            self.__builder.child(name).set(value)
        else:
            raise KeyError(f'No uniform or child named {name!r}')


_BlenderLike = skia.BlendMode | skia.Blender | CompositeOperation
_ColorLikeOrShader = ColorLike | skia.Color4f | skia.Shader


def _to_blender(blend_mode: _BlenderLike) -> skia.Blender:
    if isinstance(blend_mode, skia.Blender):
        return blend_mode
    return skia.Blender.Mode(_composite_operation[blend_mode] if isinstance(blend_mode, str) else blend_mode)


def _to_shader(color: _ColorLikeOrShader) -> skia.Shader:
    if isinstance(color, skia.Shader):
        return color
    if isinstance(color, skia.Color4f):
        return skia.Shader.Color(color)
    return skia.Shader.Color(parse_color(color))


class ShaderBlender:
    """
    Blends multiple shaders together using a blend mode.

    >>> ShaderBlender('color')[
    ...     shader1,
    ...     shader2,
    ...     ...
    ... ]
    """

    def __init__(self, mode: _BlenderLike) -> None:
        """Create a blender to blend shaders using the given blend *mode*."""
        self.__blender = _to_blender(mode)

    @classmethod
    def Arithmetic(
        cls, k1: float, k2: float, k3: float | None = None, k4: float | None = None, /, enforce_premul: bool = False
    ) -> ShaderBlender:
        """Create a blender that uses the given arithmetic coefficients."""
        if k3 is None:
            k3 = k1
            k1 = k4 = 0
        return cls(skia.Blenders.Arithmetic(k1, k2, k3, k4, enforce_premul))  # type: ignore k4 is not None

    def blend(self, dst: skia.Shader, src: skia.Shader) -> skia.Shader:
        """Blend the given *src* shader into the given *dst* shader."""
        return skia.Shader.Blend(self.__blender, dst, src)

    def __getitem__(self, shaders: _ColorLikeOrShader | tuple[_ColorLikeOrShader, ...]) -> skia.Shader:
        """
        Blend the one or more *shaders* (or colors) together. Each shader will be blended into the result of the
        previous shaders.
        """
        if not isinstance(shaders, tuple):
            shaders = (shaders,)
        result = _to_shader(shaders[0])
        for shader in shaders[1:]:
            result = skia.Shader.Blend(self.__blender, result, _to_shader(shader))
        return result
