from perlin_noise import PerlinNoise
from PIL import Image,ImageColor,ImageDraw,ImageEnhance,ImageFilter
import random,subprocess,time,math,os
import numpy as np
print("生成的行星颜值差不关我事QωQ（按Enter键开始生成）")
#print("注:可能会出bug,但是概率低（按Enter键开始生成）")
input()
def rdnum(lt,rt):#方便随机Be convenient to generate randomly
    return random.randint(lt,rt)
Project_image_shadow = Image.new(mode="RGBA",size=(2048,2048),color=(0,0,0,0))#影子
Project_image_Sphere = Image.new(mode="RGBA",size=(2048,2048),color=(0,0,0,0))#大气
Project_image_ring = Image.new(mode="RGBA",size=(2048,2048),color=(0,0,0,0))#环
Project_Background = Image.new(mode="RGBA",size=(2048,2048),color=(0,0,0,0))#背景
size = random.randint(300,900)#星球尺寸The size of planet
ringsize = random.randint(0,int(size * (2 / 3)))#环尺寸（保证环最内层半径大于星球半径）The size of rings(To prove the radius of the innermost ring is more than the radius of planet)
width = rdnum(0,2048)#环的挤压程度The degree of squeeze
hxsizes = []
for q in range(200):
    for q2 in range(5):
        hxsizes.append(q+820)#让取值取到820~1020的概率更大It is more likely that the ring will be sized from 800 to 1020
for q in range(520):
    hxsizes.append(q+300)
hxsize = random.choice(hxsizes)
Project_hx = Image.new(mode="RGBA",size=(2048,2048),color=(0,0,0,0))
hx_color = [(180, 200, 235, 255), (160, 180, 235, 255), (150, 170, 235, 255), (130, 150, 220, 255), (220, 220, 235, 255), (200, 200, 235, 255), (235, 220, 190, 255), (235, 210, 160, 255), (235, 200, 130, 255), (235, 180, 80, 255), (235, 160, 60, 255), (235, 130, 30, 255), (235, 80, 30, 255), (180, 40, 10, 255)]
hx_color_dark = [(105, 125, 160, 255), (85, 105, 160, 255), (75, 95, 160, 255), (35, 75, 145, 255), (145, 145, 160, 255), (125, 125, 160, 255), (160, 145, 115, 255), (160, 135, 85, 255), (160, 125, 55, 255), (160, 105, 5, 255), (180, 105, 25, 255), (160, 55, 0, 255), (160, 5, 0, 255), (105, 0, 0, 255)]
hx_color_bright = [(220,240,255,255), (200,220,255,255),(190,210,255,255), (170,190,240,255),(255,255,255,255), (255,255,255,255),(255,255,230,255), (255,250,200,255),(255,240,170,255), (255,220,120,255),(255,180,100,255), (255,170,70,255),(255,120,70,255), (220,80,50,255)]
colorhx = rdnum(0,13)#恒星颜色选择Choosing the color of fixed star
shadow_direction = rdnum(0,360)#影子朝向The direction of shadow
ishx = random.choice([True,False])#是否有恒星（阴影是否朝向我们）Is fixed star there(Is shadow towards to us)
l = random.randint(0,1024-size)#阴影部分的凹凸程度The degree of convex and concave in the part of shadow
def shadow():#影子部分The part of shadow
    shd = ImageDraw.Draw(Project_image_shadow)
    shd.ellipse((size*0.97,size*0.97,2048-size*0.97,2048-size*0.97),fill=(0,0,0,255))
    shd.rectangle((0,0,1024,2048),fill=(0,0,0,0))
    if ishx:#影子凹凸判断Inferring whether the shadow is convex or concave
        shd.ellipse(((size+l)*0.97,size*0.97,2048-(size+l)*0.97,2048-size*0.97),fill=(0,0,0,255))
    else:
        shd.ellipse(((size+l)*0.97,size*0.97,2048-(size+l)*0.97,2048-size*0.97),fill=(0,0,0,0))
    return Project_image_shadow
def sphere(tp,img,size,canvassize=2048):#1为行星，0为恒星 If tp equals to one,then tp is planet,if tp equals to zero,then tp is fixed star
    sph = ImageDraw.Draw(img)
    if tp == 1:
        color = (rdnum(0,255),rdnum(0,255),rdnum(0,255),255)
    elif tp == 2:
        color = hx_color_bright[colorhx]
    else:
        color = hx_color[colorhx]
    sph.ellipse((size,size,canvassize-size,canvassize-size),fill=color)
    return img
def light_line(img,blur,size=0,canvassize=4096):
    ltle = ImageDraw.Draw(img)
    ltle.ellipse((548+(8*size),2038+(0.01*size),3548-(8*size),2058-(0.01*size)),fill=hx_color_bright[colorhx])
    return img.filter(ImageFilter.BoxBlur(blur))
def geographic_L(a,b,c,size):#地形灰度图生成Generating the grayscale graph
    noise = PerlinNoise(octaves=a, seed=b)
    noise_data = np.zeros((2048-2*size, 2048-2*size), dtype=np.uint8)
    for i in range(2048-2*size):
        for j in range(2048-2*size):
            val = noise([i/size, j/size])
            noise_data[i,j] = np.clip(int((val + 1) * c/2), 0, 255)
        print(f"渲染进行了{i}/{2047-2*size}")
    print("加载中......")
    return Image.fromarray(noise_data, mode='L')
def apply_circular_mask(a):#只保留圆Only save the part of circle
    img = a
    mask = Image.new('L', img.size, 0)
    draw = ImageDraw.Draw(mask)
    width, height = img.size
    center_x, center_y = width // 2, height // 2
    radius = min(width, height) // 2
    draw.ellipse(
        (center_x - radius, center_y - radius, 
         center_x + radius, center_y + radius),
        fill=255
    )
    img.putalpha(mask)
    return img
def colorize_by_gray(a):#分层设色Layered coloring
    img = a.convert('L')
    pixels = np.array(img)
    pixels = np.clip(pixels, 0, 255)
    color_img = Image.new('RGB', img.size)
    color_pixels = color_img.load()
    color_num = {}
    for i in range(18):#随机色彩RGB生成Generating RGB of color randomly
        color_num[f"{i}"] = rdnum(0,255)
    color_stops = {
        0: (color_num["0"],color_num["1"],color_num["2"]),
        64: (color_num["3"],color_num["4"],color_num["5"]),
        128: (color_num["6"],color_num["7"],color_num["8"]),
        192: (color_num["9"],color_num["10"],color_num["11"]),
        224: (color_num["12"],color_num["13"],color_num["14"]),
        255: (color_num["15"],color_num["16"],color_num["17"])
    }
    gradient_map = []
    for gray in range(255):
        lower = max([k for k in color_stops.keys() if k <= gray])
        upper = min([k for k in color_stops.keys() if k >= gray])
        if lower == upper:
            color = color_stops[lower]
        else:
            ratio = (gray - lower) / (upper - lower)
            color = tuple(
                int(color_stops[lower][c] * (1-ratio) + color_stops[upper][c] * ratio)
                for c in range(3)
            )
        gradient_map.append(color)
    for y in range(img.height):
        for x in range(img.width):
            gray = min(255, max(0, pixels[y, x]))
            color_pixels[x, y] = gradient_map[int(gray)]
    return color_img
def ring():#环部The part of ring
    ring = Image.new(mode="RGBA",size=(2048,2048),color=(0,0,0,0))
    sph = ImageDraw.Draw(ring)
    a = []
    x = rdnum(55,255)
    y = rdnum(55,255)
    z = rdnum(55,255)
    for j in range(int(rdnum(30,120))):#单个环宽度和环数量调整Tuning the width of simple ring and the number of a various of rings
        a.append(rdnum(j*5,5+j*5)/10)
    for i in a:#生成环Generating ring
        sph.ellipse((ringsize*(0.9+0.01*i),ringsize*(0.9+0.01*i),2048-ringsize*(0.9+0.01*i),2048-ringsize*(0.9+0.01*i)),fill=(x,y,z,rdnum(0,200)))
    sph.ellipse((ringsize*(0.9+0.01*i),ringsize*(0.9+0.01*i),2048-ringsize*(0.9+0.01*i),2048-ringsize*(0.9+0.01*i)),fill=(0,0,0,0))
    sph.rectangle((0,0,1024,2048),fill=(0,0,0,0))#删除半边环Deleting half of ring
    return ring.resize((width,2048))#挤压环extruding ring
def star():#背景Background
    star = ImageDraw.Draw(Project_Background)
    star.rectangle((0,0,2048,2048),fill=(rdnum(0,15),rdnum(0,15),rdnum(0,15),255))
    for _ in range(2000):#星星数量The number of Stars
        star_sizex = random.randint(0,2048)
        star_sizey = random.randint(0,2048)
        star_size = random.randint(5,30)/10
        star.ellipse((star_sizex,star_sizey,star_sizex+star_size,star_sizey+star_size),fill=(255,255,255,255))
    return Project_Background
def fisheye_effect(img,size):#鱼眼Fisheye
    width = 2048 - 2*size
    height = 2048 - 2*size
    dst = Image.new('RGB', (width, height))
    cx, cy = width/2, height/2
    radius = min(cx, cy)
    for y in range(height):
        for x in range(width):
            dx, dy = x - cx, y - cy
            dist = math.sqrt(dx**2 + dy**2)
            if dist <= radius:
                theta = math.atan2(dy, dx)
                new_dist = (dist / radius)**1.25 * radius#鱼眼强度The strongth of fisheys
                src_x = int(cx + new_dist * math.cos(theta))
                src_y = int(cy + new_dist * math.sin(theta))
                if 0 <= src_x < width and 0 <= src_y < height:
                    dst.putpixel((x,y), img.getpixel((src_x, src_y)))
    return dst
def colorize_by_gray_hx(a):#分层设色（恒星）（参考行星分层设色）Layered coloring(fixed star)(Referring the layered coloring of planet)
    img = a.convert('L')
    pixels = np.array(img)
    color_img = Image.new('RGB', img.size)
    color_pixels = color_img.load()
    color_stops = {
        0: hx_color_dark[colorhx],
        128: hx_color[colorhx],
        255: hx_color_bright[colorhx]
    }
    gradient_map = []
    for gray in range(256):
        lower = max([k for k in color_stops.keys() if k <= gray])
        upper = min([k for k in color_stops.keys() if k >= gray])
        if lower == upper:
            color = color_stops[lower]
        else:
            ratio = (gray - lower) / (upper - lower)
            color = tuple(
                int(color_stops[lower][c] * (1-ratio) + color_stops[upper][c] * ratio)
                for c in range(3)
            )
        gradient_map.append(color)
    for y in range(img.height):
        for x in range(img.width):
            gray = pixels[y, x]
            color_pixels[x, y] = gradient_map[gray]
    return color_img
hxsurf = apply_circular_mask(fisheye_effect(colorize_by_gray_hx(apply_circular_mask(geographic_L(hxsize * 0.3 + rdnum(-3,3)/10,rdnum(-10000,10000),rdnum(50,1020),hxsize))),hxsize))
hxf = sphere(0,Project_hx,hxsize).filter(ImageFilter.GaussianBlur(100))
ImageDraw.Draw(hxf).ellipse((hxsize,hxsize,2048-hxsize,2048-hxsize),fill=hx_color[colorhx])
Project_hximg = Image.new(mode="RGBA",size=(2048,2048),color=(0,0,0,0))
for i in range(21):
    blurred = hxf.filter(ImageFilter.GaussianBlur(1.2*i))
    Project_hximg.paste(blurred, (0,0), blurred)
    print(f"正在点亮恒星{i}/20")
blurred = hxf.filter(ImageFilter.GaussianBlur(2))
Project_hximg.paste(hxsurf, (hxsize,hxsize), hxsurf)
Project_hxend = ImageEnhance.Brightness(Project_hximg).enhance(rdnum(10,30)/10)
light_0 = sphere(2,Image.new(mode="RGBA",size=(4096,4096),color=(0,0,0,0)),1708,canvassize=4096).filter(ImageFilter.BoxBlur(200))
light_1 = light_line(Image.new(mode="RGBA",size=(4096,4096),color=(0,0,0,0)),10,100).rotate(rdnum(30,150))
light_2 = light_line(Image.new(mode="RGBA",size=(4096,4096)),15)
light_1.paste(light_0,(0,0),light_0)
light_2.paste(light_1,(0,0),light_1)
Project_starlight = (ImageEnhance.Brightness(light_2).enhance(3))
Project_starlight = Project_starlight.resize((int(4096 * (1024 - hxsize) / 240), int(4096 * (1024 - hxsize) / 240)))
Project_image_ring.paste(ring(),(int(1024-(width/2)),0),ring())
tring = Project_image_ring.rotate(rdnum(0,360))
if random.choice([True,False]):
    ImageDraw.Draw(tring).rectangle((0,0,2048,2048),fill=(0,0,0,0))
geography = apply_circular_mask(fisheye_effect(colorize_by_gray(apply_circular_mask(geographic_L((1024 - size) * 0.011,rdnum(-10000,10000),rdnum(30,200),size))),size))
shadow_rotate = shadow().rotate(shadow_direction)
shadow_filter = shadow_rotate.filter(ImageFilter.GaussianBlur(radius=25*size/1024))
sphere_filter = sphere(1,Project_image_Sphere,1.05*size).filter(ImageFilter.GaussianBlur(radius=30*size/1024))
Background_filter = star().filter(ImageFilter.GaussianBlur(1))
Project_image = Image.new('RGB',(2048,2048),'black')
if not ishx:
    ImageDraw.Draw(Project_hxend).rectangle((0,0,2048,2048),fill=(0,0,0,0))
    ImageDraw.Draw(Project_starlight).rectangle((0,0,4096,4096),fill=(0,0,0,0))
if hxsize < 750:
    ImageDraw.Draw(Project_starlight).rectangle((0,0,int(4096 * (1024 - hxsize) / 240),int(4096 * (1024 - hxsize) / 240)),fill=(0,0,0,0))#
Project_image.paste(Background_filter,(0,0),Background_filter)
Project_image.paste(Project_hxend.filter(ImageFilter.GaussianBlur(80)),(int(1.28 * ((1024-size)**2)/l * math.cos(math.radians(shadow_direction + 180))),int(-1.28 * ((1024-size)**2)/l * math.sin(math.radians(shadow_direction + 180)))),Project_hxend.filter(ImageFilter.GaussianBlur(80)))#用什么公式才能让恒星相对行星半径和阴影位置合理
Project_image.paste(Project_hxend,(int(1.28 * ((1024-size)**2)/l * math.cos(math.radians(shadow_direction + 180))),int(-1.28 * ((1024-size)**2)/l * math.sin(math.radians(shadow_direction + 180)))),Project_hxend)
Project_image.paste(Project_hxend.filter(ImageFilter.GaussianBlur(250)),(int(1.28 * ((1024-size)**2)/l * math.cos(math.radians(shadow_direction + 180))),int(-1.28 * ((1024-size)**2)/l * math.sin(math.radians(shadow_direction + 180)))),Project_hxend.filter(ImageFilter.GaussianBlur(250)))#用什么公式才能让恒星相对行星半径和阴影位置合理
Project_image.paste(Project_starlight,(int(1024-2048*((1024-hxsize)/240)+(1.28 * ((1024-size)**2)/l * math.cos(math.radians(shadow_direction + 180)))),int(1024-2048*((1024-hxsize)/240)-(1.28 * ((1024-size)**2)/l * math.sin(math.radians(shadow_direction + 180))))),Project_starlight)#问：如果这里粘贴的位置为结果的中心，那输入坐标是什么式子
Project_image.paste(tring,(0,0),tring)
for _ in range(rdnum(0,15)):
    Project_image.paste(sphere_filter,(0,0),sphere_filter)
Project_image.paste(geography,(size,size),geography)
Project_image.paste(ImageEnhance.Brightness(shadow_filter).enhance(0),(0,0),ImageEnhance.Brightness(shadow_filter).enhance(0))
Project_image.paste(tring.rotate(180),(0,0),tring.rotate(180))
Project_image.show()
if not os.path.exists("Star_Photos"):
    os.mkdir("Star_Photos")
os.chdir("Star_Photos")
Num_of_photo = 0
while True:
    if os.path.exists(f"Star_Photo{Num_of_photo}.png"):
        Num_of_photo += 1
    else:
        Project_image.save(f"Star_Photo{Num_of_photo}.png")
        break
print("星图生成完毕！（按Enter键退出程序）")
input()
#程序作者：Maugfy
#代码提供：deepseek