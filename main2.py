from memory_profiler import profile
import os
import sys
import numpy as np
path = os.path.abspath('./build/lib.linux-x86_64-3.8/animator')
print(path)
sys.path.insert(0, path)
# from animator import skia
import skia
print(skia.__file__)

def print2(i, *args,**kwargs):
    if i>9997:
        # skia.Path.Rect((10,20,30,40)).dump()
        print(*args,**kwargs)
        print('****************')

@profile
def main():
    for i in range(1):
        # print2(i,skia.RuntimeEffect.MakeForShader("""
        # uniform vec4 u_color;
        # vec4 main(vec2 coord) {
        #     return vec4(coord,0,1);
        # }
        # """))
        r=skia.RuntimeEffect.MakeForShader("""
const float maxIterations = 100;
uniform shader image;
vec2 absIm(vec2 c) {
	return vec2(abs(c.x), abs(c.y));
}
vec2 sqIm(vec2 c) {
	return vec2(c.x*c.x-c.y*c.y, 2.0*c.x*c.y);
}
vec2 sqrtIm(vec2 c) {
	return vec2(c.x*c.x-c.y*c.y, 2.0*c.x*c.y);
}
float iterateMandelbrot(vec2 coord) {
	vec2 z = vec2(0,0);
	for(float i=0;i<maxIterations;i++){
		z = sqIm(absIm(z)) + coord;
		if(length(z)>2) return i/maxIterations;
	}
	return maxIterations;
}

vec4 main(vec2 coord) {
    return image.eval(vec2(iterateMandelbrot((coord/512-vec2(1.5,1))*1.1)*256,0));
}
            """.strip())
        if r.effect is None:
            raise Exception(r.errorText)
        b=skia.RuntimeShaderBuilder(r.effect)
        b.child('image').set(skia.Image.open('/home/sherlock/Pictures/pal.png').makeShader())
        b.makeImage(skia.ImageInfo.MakeN32Premul(1024, 1024)).save('/home/sherlock/Pictures/changed2.png')
# a=np.zeros((1000,1000,4),dtype=np.uint8)
# print2(i,skia.Canvas(a).drawRect((100,200,300,400),skia.Paint()))
# if i==9999:
#     import matplotlib.pyplot as plt
#     plt.imshow(a)
#     plt.show()
# print2(i,np.array(ii.colorInfo().colorSpace().serialize(),copy=False))

main()