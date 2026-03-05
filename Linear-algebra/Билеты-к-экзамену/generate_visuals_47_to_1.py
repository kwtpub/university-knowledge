#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Circle

ROOT = Path('.')
VIS = ROOT / 'visuals'
VIS.mkdir(exist_ok=True)


def set2d(ax, title: str, xlabel: str = 'x', ylabel: str = 'y', equal: bool = True):
    ax.set_title(title, fontsize=11)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.axhline(0, color='black', lw=0.8)
    ax.axvline(0, color='black', lw=0.8)
    ax.grid(alpha=0.3)
    if equal:
        ax.set_aspect('equal', adjustable='box')


def set3d(ax, title: str):
    ax.set_title(title, fontsize=10)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    ax.grid(True, alpha=0.3)


def replace_visual_block(md_path: Path, new_block: str) -> None:
    text = md_path.read_text(encoding='utf-8')
    marker = '## Наглядное представление'
    if marker in text:
        text = text.split(marker)[0].rstrip() + '\n\n' + new_block.strip() + '\n'
    else:
        text = text.rstrip() + '\n\n' + new_block.strip() + '\n'
    md_path.write_text(text, encoding='utf-8')


def save_fig(fig, name: str):
    fig.tight_layout()
    fig.savefig(VIS / name, bbox_inches='tight', dpi=170)
    plt.close(fig)


# ---------- Ticket 47 ----------
def t47():
    fig, axs = plt.subplots(1, 3, figsize=(15, 4.8))
    # ellipse
    a, b = 3, 2
    t = np.linspace(0, 2*np.pi, 300)
    axs[0].plot(a*np.cos(t), b*np.sin(t), lw=2, color='#0f766e')
    set2d(axs[0], 'После приведения: эллипс\n x²/9 + y²/4 = 1')

    # hyperbola
    y = np.linspace(-4, 4, 400)
    x = np.sqrt(1 + y**2/4) * 2
    axs[1].plot(x, y, lw=2, color='#a21caf')
    axs[1].plot(-x, y, lw=2, color='#a21caf')
    set2d(axs[1], 'После приведения: гипербола\n x²/4 - y²/4 = 1')

    # parabola
    x = np.linspace(-1, 5, 300)
    y = np.sqrt(2*np.maximum(0, x))
    axs[2].plot(x, y, lw=2, color='#2563eb')
    axs[2].plot(x, -y, lw=2, color='#2563eb')
    set2d(axs[2], 'После приведения: парабола\n y² = 2x')

    fig.suptitle('Билет 47: общее уравнение кривой 2-го порядка -> канонические формы')
    save_fig(fig, 'bilet-47-canonical.png')

    block = '''
## Наглядное представление

### Приведение общего уравнения к каноническому виду
![Билет 47 - канонические кривые](visuals/bilet-47-canonical.png)
'''
    replace_visual_block(ROOT / 'Билет-47.md', block)


# ---------- Ticket 46 ----------
def t46():
    fig = plt.figure(figsize=(12, 5.5))
    ax1 = fig.add_subplot(1, 2, 1)
    ax1.axis('off')
    steps = [
        '1) Квадр. часть: A',
        '2) Собств. значения/векторы',
        '3) Поворот: убрать Dxy, Exz, Fyz',
        '4) Сдвиг: убрать линейные члены',
        '5) Канонический вид поверхности',
    ]
    y = 0.9
    for s in steps:
        ax1.text(0.05, y, s, fontsize=11, va='top')
        y -= 0.16
    ax1.set_title('Алгоритм приведения (Билет 46)')

    ax2 = fig.add_subplot(1, 2, 2)
    x = np.linspace(-3, 3, 240)
    y = np.linspace(-3, 3, 240)
    X, Y = np.meshgrid(x, y)
    Z1 = 2*X**2 + 1.3*Y**2 + 1.7*X*Y
    cs1 = ax2.contour(X, Y, Z1, levels=8, colors='#9f1239', linewidths=1)
    theta = np.deg2rad(25)
    Xr = X*np.cos(theta) + Y*np.sin(theta)
    Yr = -X*np.sin(theta) + Y*np.cos(theta)
    Z2 = 2.4*Xr**2 + 0.9*Yr**2
    ax2.contour(X, Y, Z2, levels=8, colors='#0369a1', linewidths=1)
    ax2.clabel(cs1, inline=True, fontsize=7)
    set2d(ax2, 'Красный: со смешанным членом\nСиний: после поворота (без XY)')

    fig.suptitle('Билет 46: геометрический смысл диагонализации квадратичной части')
    save_fig(fig, 'bilet-46-reduction.png')

    block = '''
## Наглядное представление

### Приведение поверхности 2-го порядка к каноническому виду
![Билет 46 - приведение](visuals/bilet-46-reduction.png)
'''
    replace_visual_block(ROOT / 'Билет-46.md', block)


# ---------- Ticket 45 ----------
def t45():
    fig, axs = plt.subplots(1, 2, figsize=(12, 5.2))

    x = np.linspace(-3, 3, 240)
    y = np.linspace(-3, 3, 240)
    X, Y = np.meshgrid(x, y)

    Qpos = 2*X**2 + Y**2
    axs[0].contour(X, Y, Qpos, levels=8, cmap='Greens')
    set2d(axs[0], 'Q(x,y)=2x²+y² > 0 (x≠0,y≠0)')
    axs[0].text(-2.8, 2.55, 'Положительно определена\nΔ1>0, Δ2>0', fontsize=9)

    Qind = X**2 - Y**2
    axs[1].contour(X, Y, Qind, levels=[-4,-2,-1,-0.5,0.5,1,2,4], cmap='coolwarm')
    set2d(axs[1], 'Q(x,y)=x²-y² (знакопеременная)')
    axs[1].text(-2.8, 2.55, 'Сильвестр не выполнен', fontsize=9)

    fig.suptitle('Билет 45: квадратичные формы и критерий Сильвестра')
    save_fig(fig, 'bilet-45-sylvester.png')

    block = '''
## Наглядное представление

### Квадратичная форма: тип поверхности уровня и знакоопределённость
![Билет 45 - критерий Сильвестра](visuals/bilet-45-sylvester.png)
'''
    replace_visual_block(ROOT / 'Билет-45.md', block)


# ---------- Ticket 44 ----------
def t44():
    fig, axs = plt.subplots(1, 2, figsize=(12, 4.8))

    A = np.array([[2, 3], [3, 1]])
    K = np.array([[0, 2], [-2, 0]])

    im1 = axs[0].imshow(A, cmap='Blues')
    axs[0].set_title('Симметрическая матрица A=Aᵀ')
    for i in range(2):
        for j in range(2):
            axs[0].text(j, i, f'{A[i,j]}', ha='center', va='center')

    im2 = axs[1].imshow(K, cmap='Reds')
    axs[1].set_title('Кососимметрическая K=-Kᵀ')
    for i in range(2):
        for j in range(2):
            axs[1].text(j, i, f'{K[i,j]}', ha='center', va='center')

    for ax in axs:
        ax.set_xticks([0,1]); ax.set_yticks([0,1])

    fig.suptitle('Билет 44: B = B_сим + B_кос на уровне матриц')
    save_fig(fig, 'bilet-44-symm-skew.png')

    block = '''
## Наглядное представление

### Разложение билинейной формы на симметрическую и кососимметрическую части
![Билет 44 - симм и кососимм формы](visuals/bilet-44-symm-skew.png)
'''
    replace_visual_block(ROOT / 'Билет-44.md', block)


# ---------- Ticket 43 ----------
def t43():
    fig = plt.figure(figsize=(12, 5.2))
    ax1 = fig.add_subplot(1, 2, 1, projection='3d')

    x = np.linspace(-2,2,120)
    y = np.linspace(-2,2,120)
    X, Y = np.meshgrid(x,y)
    # B(x,y)= [x y] A [u v]^T ; for visualization fix second vector = (y, x)
    Z = 2*X*Y + X**2 - 0.5*Y**2
    ax1.plot_surface(X,Y,Z, cmap='viridis', alpha=0.85, linewidth=0)
    set3d(ax1, 'Bilinear example as surface z=B(x,y)')
    ax1.view_init(26, 40)

    ax2 = fig.add_subplot(1, 2, 2)
    A = np.array([[1,2],[3,4]])
    C = np.array([[1,1],[0,1]])
    Ap = C.T @ A @ C
    ax2.axis('off')
    ax2.text(0.05,0.84,'A = [[1,2],[3,4]]', fontsize=11)
    ax2.text(0.05,0.66,'C = [[1,1],[0,1]]', fontsize=11)
    ax2.text(0.05,0.48,f"A' = CᵀAC = {Ap.tolist()}", fontsize=11)
    ax2.text(0.05,0.30,'Смена базиса меняет матрицу\nпо формуле A\' = CᵀAC', fontsize=11)
    ax2.set_title('Координатное представление')

    fig.suptitle('Билет 43: билинейная форма и её матрица')
    save_fig(fig, 'bilet-43-bilinear.png')

    block = '''
## Наглядное представление

### Билинейная форма: поверхность значений и матричная запись
![Билет 43 - билинейная форма](visuals/bilet-43-bilinear.png)
'''
    replace_visual_block(ROOT / 'Билет-43.md', block)


# ---------- Ticket 42 ----------
def t42():
    fig, axs = plt.subplots(1, 2, figsize=(12, 5))

    x = np.linspace(-4,4,400)
    for c in [-3,-1,1,3]:
        y = (c - 2*x)/3
        axs[0].plot(x, y, lw=1.8, label=f'f(x,y)={c}')
    set2d(axs[0], 'Линии уровня линейной формы f=2x+3y')
    axs[0].legend(fontsize=8)

    axs[1].axis('off')
    axs[1].text(0.05,0.80,'f(x)=aᵀx', fontsize=13)
    axs[1].text(0.05,0.63,"a' = Cᵀa", fontsize=13)
    axs[1].text(0.05,0.43,'Геометрически: все линии уровня\nпараллельны и ортогональны a.', fontsize=11)
    axs[1].arrow(0.22,0.2,0.35,0.25, width=0.01, color='crimson', transform=axs[1].transAxes)
    axs[1].text(0.60,0.46,'вектор a', transform=axs[1].transAxes)

    fig.suptitle('Билет 42: линейная форма как семейство параллельных гиперплоскостей')
    save_fig(fig, 'bilet-42-linear-form.png')

    block = '''
## Наглядное представление

### Линейная форма f(x)=aᵀx как геометрический объект
![Билет 42 - линейная форма](visuals/bilet-42-linear-form.png)
'''
    replace_visual_block(ROOT / 'Билет-42.md', block)


# ---------- Ticket 41 ----------
def t41():
    fig, ax = plt.subplots(figsize=(7.8, 6.2))
    p = 2.0
    y = np.linspace(-6,6,400)
    x = y**2/(2*p)
    ax.plot(x,y, lw=2, color='#2563eb')

    F = (p/2, 0)
    directrix_x = -p/2
    ax.scatter([F[0]],[F[1]], color='crimson', s=45)
    ax.axvline(directrix_x, color='#b45309', lw=1.8, ls='--')

    M = (2.0, np.sqrt(2*p*2.0))
    ax.scatter([M[0]], [M[1]], color='black', s=35)
    ax.plot([M[0], F[0]], [M[1], F[1]], color='crimson', lw=1.6)
    ax.plot([M[0], directrix_x], [M[1], M[1]], color='#b45309', lw=1.6)
    ax.text(F[0]+0.1, F[1]+0.3, 'F(p/2,0)', fontsize=10)
    ax.text(directrix_x+0.1, 5.1, 'директриса x=-p/2', fontsize=10)
    ax.text(M[0]+0.1, M[1]+0.2, 'M', fontsize=10)

    set2d(ax, 'Билет 41: парабола y²=2px, |MF| = dist(M, директриса)')
    ax.set_xlim(-3.5, 9)
    ax.set_ylim(-7, 7)

    save_fig(fig, 'bilet-41-parabola.png')

    block = '''
## Наглядное представление

### Парабола через фокус и директрису
![Билет 41 - парабола](visuals/bilet-41-parabola.png)
'''
    replace_visual_block(ROOT / 'Билет-41.md', block)


# ---------- Ticket 40 ----------
def t40():
    fig, ax = plt.subplots(figsize=(8, 6.2))
    a, b = 3.0, 2.0
    t = np.linspace(-2,2,500)
    x = a*np.cosh(t)
    y = b*np.sinh(t)
    ax.plot(x,y, color='#a21caf', lw=2)
    ax.plot(-x,y, color='#a21caf', lw=2)

    c = np.sqrt(a*a + b*b)
    F1, F2 = (-c,0), (c,0)
    ax.scatter([F1[0],F2[0]], [0,0], color='crimson', s=40)

    xx = np.linspace(-8,8,200)
    ax.plot(xx, (b/a)*xx, ls='--', color='#475569')
    ax.plot(xx, -(b/a)*xx, ls='--', color='#475569')

    set2d(ax, 'Билет 40: гипербола x²/a² - y²/b² = 1\nасимптоты y=±(b/a)x')
    ax.set_xlim(-9,9); ax.set_ylim(-7,7)

    save_fig(fig, 'bilet-40-hyperbola.png')
    block = '''
## Наглядное представление

### Гипербола: фокусы, асимптоты и каноническое уравнение
![Билет 40 - гипербола](visuals/bilet-40-hyperbola.png)
'''
    replace_visual_block(ROOT / 'Билет-40.md', block)


# ---------- Ticket 39 ----------
def t39():
    fig, ax = plt.subplots(figsize=(8, 6.2))
    a, b = 4.0, 2.6
    t = np.linspace(0,2*np.pi,400)
    ax.plot(a*np.cos(t), b*np.sin(t), color='#0f766e', lw=2)

    c = np.sqrt(a*a-b*b)
    F1, F2 = (-c,0), (c,0)
    ax.scatter([F1[0],F2[0]], [0,0], color='crimson', s=40)

    e = c/a
    d = a/e
    ax.axvline(d, ls='--', color='#b45309')
    ax.axvline(-d, ls='--', color='#b45309')

    M = (a*np.cos(0.9), b*np.sin(0.9))
    ax.scatter([M[0]],[M[1]], color='black', s=30)
    ax.plot([M[0],F1[0]],[M[1],F1[1]], color='crimson', lw=1.5)
    ax.plot([M[0],F2[0]],[M[1],F2[1]], color='crimson', lw=1.5)

    set2d(ax, 'Билет 39: эллипс x²/a² + y²/b² = 1\n r1+r2 = 2a')
    ax.set_xlim(-8.5,8.5); ax.set_ylim(-5.5,5.5)
    save_fig(fig, 'bilet-39-ellipse.png')

    block = '''
## Наглядное представление

### Эллипс: фокусы, директрисы и фокальное свойство
![Билет 39 - эллипс](visuals/bilet-39-ellipse.png)
'''
    replace_visual_block(ROOT / 'Билет-39.md', block)


# ---------- Ticket 38 ----------
def t38():
    fig, axs = plt.subplots(1,2, figsize=(12,5.2))

    # angle between lines
    v1 = np.array([3,1]); v2 = np.array([1,3])
    axs[0].arrow(0,0,v1[0],v1[1], width=0.04, color='#1d4ed8')
    axs[0].arrow(0,0,v2[0],v2[1], width=0.04, color='#dc2626')
    set2d(axs[0], 'Угол между прямыми\n cosφ=|s1·s2|/(|s1||s2|)')
    axs[0].set_xlim(-1,4.5); axs[0].set_ylim(-1,4.5)

    # line-plane angle via normal
    axs[1].axis('off')
    axs[1].text(0.05,0.78,'sinφ = |n·s| / (|n||s|)', fontsize=13)
    axs[1].text(0.05,0.56,'Если n·s = 0 -> прямая // плоскости', fontsize=11)
    axs[1].text(0.05,0.40,'Если s || n -> прямая ⟂ плоскости', fontsize=11)
    axs[1].arrow(0.2,0.15,0.35,0.20, width=0.01, color='crimson', transform=axs[1].transAxes)
    axs[1].arrow(0.2,0.15,0.05,0.35, width=0.01, color='#2563eb', transform=axs[1].transAxes)
    axs[1].text(0.58,0.37,'s', transform=axs[1].transAxes)
    axs[1].text(0.28,0.52,'n', transform=axs[1].transAxes)

    fig.suptitle('Билет 38: углы между прямыми и между прямой и плоскостью')
    save_fig(fig, 'bilet-38-angles.png')

    block = '''
## Наглядное представление

### Углы с участием прямой: формулы через скалярное произведение
![Билет 38 - углы](visuals/bilet-38-angles.png)
'''
    replace_visual_block(ROOT / 'Билет-38.md', block)


# ---------- Ticket 37 ----------
def t37():
    fig = plt.figure(figsize=(11,5.3))
    ax1 = fig.add_subplot(1,2,1, projection='3d')

    t = np.linspace(-2,2,120)
    x = 1 + 2*t
    y = -1 + t
    z = 0.5 + 1.5*t
    ax1.plot3D(x,y,z, color='#2563eb', lw=2.4)
    ax1.scatter([1],[-1],[0.5], color='crimson', s=30)
    set3d(ax1, 'Параметрически: x=x0+lt, y=y0+mt, z=z0+nt')
    ax1.view_init(24, 36)

    ax2 = fig.add_subplot(1,2,2)
    ax2.axis('off')
    ax2.text(0.05,0.80,'Каноническая форма:', fontsize=12)
    ax2.text(0.05,0.68,'(x-x0)/l = (y-y0)/m = (z-z0)/n', fontsize=12)
    ax2.text(0.05,0.47,'Как пересечение плоскостей:', fontsize=12)
    ax2.text(0.05,0.35,'A1x+B1y+C1z+D1=0', fontsize=12)
    ax2.text(0.05,0.25,'A2x+B2y+C2z+D2=0', fontsize=12)
    ax2.text(0.05,0.08,'Это одна и та же прямая в разных представлениях.', fontsize=10)

    fig.suptitle('Билет 37: прямая в пространстве')
    save_fig(fig, 'bilet-37-line-space.png')

    block = '''
## Наглядное представление

### Прямая в пространстве: параметрическая, каноническая и как пересечение плоскостей
![Билет 37 - прямая в пространстве](visuals/bilet-37-line-space.png)
'''
    replace_visual_block(ROOT / 'Билет-37.md', block)


# ---------- Ticket 36 ----------
def t36():
    fig = plt.figure(figsize=(11.5,5.2))
    ax1 = fig.add_subplot(1,2,1, projection='3d')

    # plane: x+y+z-2=0
    xx, yy = np.meshgrid(np.linspace(-1,3,20), np.linspace(-1,3,20))
    zz = 2 - xx - yy
    ax1.plot_surface(xx,yy,zz, alpha=0.45, color='#38bdf8')
    P = np.array([2.5, 2.0, 1.5])
    n = np.array([1.0,1.0,1.0]); n = n/np.linalg.norm(n)
    # projection on plane
    d = (P[0]+P[1]+P[2]-2)/np.sqrt(3)
    Q = P - d*n
    ax1.scatter(*P, color='crimson', s=35)
    ax1.scatter(*Q, color='black', s=30)
    ax1.plot([P[0],Q[0]],[P[1],Q[1]],[P[2],Q[2]], color='crimson', lw=2)
    set3d(ax1, 'Расстояние от точки до плоскости')
    ax1.view_init(22, 35)

    ax2 = fig.add_subplot(1,2,2)
    ax2.axis('off')
    ax2.text(0.05,0.77,'d = |Ax0+By0+Cz0+D| / √(A²+B²+C²)', fontsize=12)
    ax2.text(0.05,0.54,'cosφ = |n1·n2| / (|n1||n2|)', fontsize=12)
    ax2.text(0.05,0.35,'Параллельность: n1 || n2', fontsize=11)
    ax2.text(0.05,0.24,'Перпендикулярность: n1·n2 = 0', fontsize=11)

    fig.suptitle('Билет 36: расстояние и углы для плоскостей')
    save_fig(fig, 'bilet-36-distance-angle-planes.png')

    block = '''
## Наглядное представление

### Расстояние от точки до плоскости и угол между плоскостями через нормали
![Билет 36 - расстояние и углы](visuals/bilet-36-distance-angle-planes.png)
'''
    replace_visual_block(ROOT / 'Билет-36.md', block)


# ---------- Ticket 35 ----------
def t35():
    fig = plt.figure(figsize=(11.8,5.2))
    ax1 = fig.add_subplot(1,2,1, projection='3d')

    a,b,c = 3,2,4
    # intercept plane x/a + y/b + z/c =1 => z=c*(1-x/a-y/b)
    xx, yy = np.meshgrid(np.linspace(0,3,20), np.linspace(0,2,20))
    zz = c*(1-xx/a-yy/b)
    zz[zz<0] = np.nan
    ax1.plot_surface(xx,yy,zz, alpha=0.55, color='#22c55e')
    ax1.scatter([a,0,0],[0,b,0],[0,0,c], color='crimson', s=30)
    set3d(ax1, 'Плоскость в отрезках: x/a + y/b + z/c = 1')
    ax1.view_init(21, 35)

    ax2 = fig.add_subplot(1,2,2)
    ax2.axis('off')
    ax2.text(0.05,0.82,'Через точку M0 и нормаль n:', fontsize=12)
    ax2.text(0.05,0.70,'A(x-x0)+B(y-y0)+C(z-z0)=0', fontsize=12)
    ax2.text(0.05,0.50,'Через три точки M1,M2,M3:', fontsize=12)
    ax2.text(0.05,0.38,'det[[x-x1,y-y1,z-z1], ... ] = 0', fontsize=12)
    ax2.text(0.05,0.18,'Все формы эквивалентны и задают ту же плоскость.', fontsize=10)

    fig.suptitle('Билет 35: разные формы уравнения плоскости')
    save_fig(fig, 'bilet-35-plane-forms.png')

    block = '''
## Наглядное представление

### Разные формы уравнения плоскости и их геометрический смысл
![Билет 35 - формы плоскости](visuals/bilet-35-plane-forms.png)
'''
    replace_visual_block(ROOT / 'Билет-35.md', block)


# ---------- Ticket 34 ----------
def t34():
    fig = plt.figure(figsize=(11.2,5.3))
    ax1 = fig.add_subplot(1,2,1, projection='3d')
    xx, yy = np.meshgrid(np.linspace(-2,3,22), np.linspace(-2,3,22))
    zz = (3 - xx - 2*yy)/2
    ax1.plot_surface(xx,yy,zz, alpha=0.55, color='#93c5fd')
    p0 = np.array([1.0,0.0,1.0])
    n = np.array([1.0,2.0,2.0])
    ax1.quiver(p0[0],p0[1],p0[2], n[0],n[1],n[2], color='crimson', length=1.4, normalize=True)
    set3d(ax1, 'Плоскость Ax+By+Cz+D=0 и нормаль n=(A,B,C)')
    ax1.view_init(21,33)

    ax2 = fig.add_subplot(1,2,2)
    ax2.axis('off')
    ax2.text(0.05,0.80,'Общее уравнение: Ax+By+Cz+D=0', fontsize=12)
    ax2.text(0.05,0.60,'Нормаль: n=(A,B,C)', fontsize=12)
    ax2.text(0.05,0.42,'D=0 -> плоскость через O', fontsize=11)
    ax2.text(0.05,0.30,'A=0 -> параллельна Ox', fontsize=11)
    ax2.text(0.05,0.18,'A=B=0 -> z=const', fontsize=11)

    fig.suptitle('Билет 34: общее уравнение плоскости')
    save_fig(fig, 'bilet-34-general-plane.png')

    block = '''
## Наглядное представление

### Плоскость и её нормальный вектор
![Билет 34 - общее уравнение плоскости](visuals/bilet-34-general-plane.png)
'''
    replace_visual_block(ROOT / 'Билет-34.md', block)


# ---------- Ticket 33 ----------
def t33():
    fig = plt.figure(figsize=(12,5.3))
    ax1 = fig.add_subplot(1,2,1)
    x = np.linspace(0,2.5,240)
    y = 0.8*x**2
    ax1.plot(x,y, color='#2563eb', lw=2)
    ax1.plot(x,-y, color='#2563eb', lw=2)
    set2d(ax1, 'Порождающая кривая (меридиан)')

    ax2 = fig.add_subplot(1,2,2, projection='3d')
    u = np.linspace(0,2.5,120)
    v = np.linspace(0,2*np.pi,150)
    U,V = np.meshgrid(u,v)
    R = 0.8*U**2
    X = U
    Y = R*np.cos(V)
    Z = R*np.sin(V)
    ax2.plot_surface(X,Y,Z, cmap='viridis', alpha=0.8, linewidth=0)
    set3d(ax2, 'Поверхность вращения (вращение кривой вокруг Ox)')
    ax2.view_init(22,35)

    fig.suptitle('Билет 33: поверхность вращения')
    save_fig(fig, 'bilet-33-rotation-surface.png')

    block = '''
## Наглядное представление

### Как образуется поверхность вращения из кривой
![Билет 33 - поверхность вращения](visuals/bilet-33-rotation-surface.png)
'''
    replace_visual_block(ROOT / 'Билет-33.md', block)


# ---------- Ticket 32 ----------
def t32():
    fig = plt.figure(figsize=(12,5.3))
    ax1 = fig.add_subplot(1,2,1, projection='3d')

    # sphere and plane intersection -> circle
    u = np.linspace(0,2*np.pi,80)
    v = np.linspace(0,np.pi,60)
    U,V = np.meshgrid(u,v)
    R = 2.5
    X = R*np.sin(V)*np.cos(U)
    Y = R*np.sin(V)*np.sin(U)
    Z = R*np.cos(V)
    ax1.plot_surface(X,Y,Z, alpha=0.25, color='#93c5fd', linewidth=0)

    xx, yy = np.meshgrid(np.linspace(-2.8,2.8,20), np.linspace(-2.8,2.8,20))
    z0 = 1.0
    zz = np.full_like(xx, z0)
    ax1.plot_surface(xx,yy,zz, alpha=0.3, color='#fcd34d')

    r = np.sqrt(R*R-z0*z0)
    t = np.linspace(0,2*np.pi,300)
    ax1.plot3D(r*np.cos(t), r*np.sin(t), np.full_like(t,z0), color='crimson', lw=2)

    set3d(ax1, 'Кривая = пересечение двух поверхностей')
    ax1.view_init(25,38)

    ax2 = fig.add_subplot(1,2,2)
    ax2.axis('off')
    ax2.text(0.05,0.82,'Поверхность: F(x,y,z)=0', fontsize=12)
    ax2.text(0.05,0.64,'Кривая в пространстве:', fontsize=12)
    ax2.text(0.05,0.52,'F1(x,y,z)=0, F2(x,y,z)=0', fontsize=12)
    ax2.text(0.05,0.34,'Пример на рисунке:\nсфера ∩ плоскость = окружность', fontsize=11)

    fig.suptitle('Билет 32: поверхности и кривые в пространстве')
    save_fig(fig, 'bilet-32-surfaces-curves.png')

    block = '''
## Наглядное представление

### Кривая как пересечение двух поверхностей
![Билет 32 - поверхности и кривые](visuals/bilet-32-surfaces-curves.png)
'''
    replace_visual_block(ROOT / 'Билет-32.md', block)


# ---------- Ticket 31 ----------
def t31():
    fig = plt.figure(figsize=(12,5.3))
    ax1 = fig.add_subplot(1,2,1, projection='3d')
    a = np.array([2,1,0.5])
    b = np.array([0.5,2,1])
    c = np.array([1,0.4,2])

    O = np.zeros(3)
    for vec, col, lab in [(a,'#2563eb','a'), (b,'#dc2626','b'), (c,'#16a34a','c')]:
        ax1.quiver(*O, *vec, color=col, linewidth=2)
        ax1.text(*(vec+0.1), lab)
    set3d(ax1, 'Векторы a,b,c -> (a,b,c)=det[a b c]')
    ax1.view_init(23,34)

    ax2 = fig.add_subplot(1,2,2)
    ax2.axis('off')
    ax2.text(0.05,0.84,'a×b = det[[i,j,k],[a1,a2,a3],[b1,b2,b3]]', fontsize=11)
    ax2.text(0.05,0.64,'(a,b,c)=det[[a1,a2,a3],[b1,b2,b3],[c1,c2,c3]]', fontsize=11)
    ax2.text(0.05,0.44,'|a×b| = площадь параллелограмма', fontsize=11)
    ax2.text(0.05,0.30,'|(a,b,c)| = объём параллелепипеда', fontsize=11)

    fig.suptitle('Билет 31: векторное и смешанное произведение в координатах')
    save_fig(fig, 'bilet-31-coordinate-products.png')

    block = '''
## Наглядное представление

### Координатные формулы векторного и смешанного произведений
![Билет 31 - произведения в координатах](visuals/bilet-31-coordinate-products.png)
'''
    replace_visual_block(ROOT / 'Билет-31.md', block)


# ---------- Ticket 30 ----------
def t30():
    fig = plt.figure(figsize=(11.5,5.3))
    ax1 = fig.add_subplot(1,2,1, projection='3d')

    a = np.array([2,0.5,0.7])
    b = np.array([0.6,1.8,0.4])
    c = np.array([0.5,0.8,1.7])

    O = np.zeros(3)
    verts = [O, a, b, c, a+b, a+c, b+c, a+b+c]
    edges = [(0,1),(0,2),(0,3),(1,4),(1,5),(2,4),(2,6),(3,5),(3,6),(4,7),(5,7),(6,7)]
    for i,j in edges:
        p,q = verts[i], verts[j]
        ax1.plot([p[0],q[0]],[p[1],q[1]],[p[2],q[2]], color='#475569', lw=1.4)

    for vec,col,lab in [(a,'#2563eb','a'),(b,'#dc2626','b'),(c,'#16a34a','c')]:
        ax1.quiver(0,0,0,*vec,color=col,linewidth=2)
        ax1.text(*(vec+0.08), lab)

    vol = abs(np.dot(a, np.cross(b,c)))
    set3d(ax1, f'Параллелепипед: V=|(a,b,c)|={vol:.2f}')
    ax1.view_init(23,36)

    ax2 = fig.add_subplot(1,2,2)
    ax2.axis('off')
    ax2.text(0.05,0.80,'(a,b,c) = a·(b×c)', fontsize=13)
    ax2.text(0.05,0.60,'Компланарность: (a,b,c)=0', fontsize=12)
    ax2.text(0.05,0.42,'Vпараллелепипеда = |(a,b,c)|', fontsize=12)
    ax2.text(0.05,0.27,'Vпирамиды = |(a,b,c)| / 6', fontsize=12)

    fig.suptitle('Билет 30: смешанное произведение')
    save_fig(fig, 'bilet-30-mixed-product.png')

    block = '''
## Наглядное представление

### Смешанное произведение как ориентированный объём
![Билет 30 - смешанное произведение](visuals/bilet-30-mixed-product.png)
'''
    replace_visual_block(ROOT / 'Билет-30.md', block)


# ---------- Ticket 29 ----------
def t29():
    fig = plt.figure(figsize=(11.5,5.3))
    ax1 = fig.add_subplot(1,2,1, projection='3d')

    a = np.array([2.0,0.6,0.3])
    b = np.array([0.4,1.9,0.7])
    c = np.cross(a,b)

    ax1.quiver(0,0,0,*a,color='#2563eb',linewidth=2)
    ax1.quiver(0,0,0,*b,color='#dc2626',linewidth=2)
    ax1.quiver(0,0,0,*c,color='#16a34a',linewidth=2)
    ax1.text(*(a+0.1),'a'); ax1.text(*(b+0.1),'b'); ax1.text(*(c+0.1),'a×b')
    set3d(ax1, '|a×b|=|a||b|sinφ, направление по правой руке')
    ax1.view_init(24,35)

    ax2 = fig.add_subplot(1,2,2)
    ax2.axis('off')
    ax2.text(0.05,0.80,'Sпараллелограмма = |a×b|', fontsize=12)
    ax2.text(0.05,0.62,'Sтреугольника = |a×b|/2', fontsize=12)
    ax2.text(0.05,0.42,'Коллинеарность: a×b = 0', fontsize=12)
    ax2.text(0.05,0.25,'[a,b]=-[b,a]', fontsize=12)

    fig.suptitle('Билет 29: векторное произведение')
    save_fig(fig, 'bilet-29-cross-product.png')

    block = '''
## Наглядное представление

### Векторное произведение: нормаль, площадь и ориентация
![Билет 29 - векторное произведение](visuals/bilet-29-cross-product.png)
'''
    replace_visual_block(ROOT / 'Билет-29.md', block)


# ---------- Ticket 28 ----------
def t28():
    fig, axs = plt.subplots(1,2, figsize=(12,5.2))

    a = np.array([4,2])
    b = np.array([3,0.8])
    proj = (np.dot(a,b)/np.dot(b,b))*b

    axs[0].arrow(0,0,a[0],a[1], width=0.04, color='#2563eb')
    axs[0].arrow(0,0,b[0],b[1], width=0.04, color='#dc2626')
    axs[0].arrow(0,0,proj[0],proj[1], width=0.03, color='#16a34a')
    axs[0].plot([a[0],proj[0]],[a[1],proj[1]], ls='--', color='#475569')
    set2d(axs[0], 'Скалярное произведение и проекция')
    axs[0].set_xlim(-1,5); axs[0].set_ylim(-1,3.5)

    axs[1].axis('off')
    axs[1].text(0.05,0.80,'(a,b)=|a||b|cosφ', fontsize=12)
    axs[1].text(0.05,0.62,'proj_b(a)=((a,b)/(b,b)) b', fontsize=12)
    axs[1].text(0.05,0.44,'|a|=√(a,a)', fontsize=12)
    axs[1].text(0.05,0.26,'a ⟂ b ⇔ (a,b)=0', fontsize=12)

    fig.suptitle('Билет 28: скалярное произведение, модуль и проекция')
    save_fig(fig, 'bilet-28-dot-projection.png')

    block = '''
## Наглядное представление

### Скалярное произведение и проекция вектора
![Билет 28 - скалярное произведение](visuals/bilet-28-dot-projection.png)
'''
    replace_visual_block(ROOT / 'Билет-28.md', block)


# ---------- Ticket 27 ----------
def t27():
    fig, axs = plt.subplots(1,3, figsize=(15,4.8))

    # polar
    r, phi = 3, np.deg2rad(40)
    x, y = r*np.cos(phi), r*np.sin(phi)
    axs[0].arrow(0,0,x,y, width=0.03, color='#2563eb')
    axs[0].text(x+0.1,y+0.1,'(r,φ)', fontsize=9)
    set2d(axs[0], 'Полярные: x=r cosφ, y=r sinφ')
    axs[0].set_xlim(-1,4.5); axs[0].set_ylim(-1,4)

    # cylindrical idea
    axs[1].axis('off')
    axs[1].text(0.06,0.75,'Цилиндрические (r,φ,z)', fontsize=12)
    axs[1].text(0.06,0.58,'x=r cosφ', fontsize=11)
    axs[1].text(0.06,0.48,'y=r sinφ', fontsize=11)
    axs[1].text(0.06,0.38,'z=z', fontsize=11)
    axs[1].text(0.06,0.20,'Это полярные координаты\nв плоскости + высота z.', fontsize=10)

    # spherical idea
    axs[2].axis('off')
    axs[2].text(0.06,0.75,'Сферические (r,θ,φ)', fontsize=12)
    axs[2].text(0.06,0.58,'x=r sinθ cosφ', fontsize=11)
    axs[2].text(0.06,0.48,'y=r sinθ sinφ', fontsize=11)
    axs[2].text(0.06,0.38,'z=r cosθ', fontsize=11)
    axs[2].text(0.06,0.20,'r — расстояние от O,\nθ — угол с Oz, φ — азимут.', fontsize=10)

    fig.suptitle('Билет 27: полярная, цилиндрическая, сферическая координаты')
    save_fig(fig, 'bilet-27-coordinate-systems.png')

    block = '''
## Наглядное представление

### Переходы между системами координат
![Билет 27 - системы координат](visuals/bilet-27-coordinate-systems.png)
'''
    replace_visual_block(ROOT / 'Билет-27.md', block)


# ---------- Ticket 26 ----------
def t26():
    fig, axs = plt.subplots(1,2, figsize=(12,5.1))

    A = np.array([1,1]); B = np.array([7,4]); m,n = 2,1
    M = (n*A + m*B)/(m+n)

    axs[0].plot([A[0],B[0]],[A[1],B[1]], color='#2563eb', lw=2)
    axs[0].scatter([A[0],B[0],M[0]],[A[1],B[1],M[1]], color=['black','black','crimson'])
    axs[0].text(A[0]-0.2,A[1]-0.3,'A'); axs[0].text(B[0]+0.1,B[1],'B'); axs[0].text(M[0]+0.1,M[1],'M')
    set2d(axs[0], 'Деление отрезка в отношении m:n')
    axs[0].text(0.1,0.92,'M=(nA+mB)/(m+n)', transform=axs[0].transAxes, fontsize=10)
    axs[0].set_xlim(0,8.5); axs[0].set_ylim(0,5.5)

    axs[1].axis('off')
    axs[1].text(0.05,0.82,'В ДПСК: OM = x i + y j + z k', fontsize=12)
    axs[1].text(0.05,0.64,'|a| = √(ax²+ay²+az²)', fontsize=12)
    axs[1].text(0.05,0.46,'dist(A,B)=√((x2-x1)²+...)', fontsize=12)
    axs[1].text(0.05,0.28,'Центр масс: R = (Σmi ri)/(Σmi)', fontsize=12)

    fig.suptitle('Билет 26: координаты вектора и деление отрезка')
    save_fig(fig, 'bilet-26-coordinates-segment.png')

    block = '''
## Наглядное представление

### Координатная геометрия: векторы, расстояния, деление отрезка
![Билет 26 - координаты и деление отрезка](visuals/bilet-26-coordinates-segment.png)
'''
    replace_visual_block(ROOT / 'Билет-26.md', block)


# ---------- Ticket 25 ----------
def t25():
    fig, axs = plt.subplots(1,2, figsize=(12,5.2))
    a = np.array([2.5,1.5]); b=np.array([1.2,2.4])

    axs[0].arrow(0,0,a[0],a[1], width=0.04, color='#2563eb')
    axs[0].arrow(a[0],a[1],b[0],b[1], width=0.04, color='#dc2626')
    axs[0].arrow(0,0,a[0]+b[0],a[1]+b[1], width=0.04, color='#16a34a')
    set2d(axs[0], 'Правило треугольника: a+b')
    axs[0].set_xlim(-0.5,4.5); axs[0].set_ylim(-0.5,4.8)

    O=np.array([0,0]); A=a; B=b; C=a+b
    axs[1].plot([O[0],A[0],C[0],B[0],O[0]],[O[1],A[1],C[1],B[1],O[1]], color='#475569')
    axs[1].arrow(0,0,a[0],a[1], width=0.03, color='#2563eb')
    axs[1].arrow(0,0,b[0],b[1], width=0.03, color='#dc2626')
    axs[1].arrow(0,0,C[0],C[1], width=0.03, color='#16a34a')
    set2d(axs[1], 'Правило параллелограмма')
    axs[1].set_xlim(-0.5,4.5); axs[1].set_ylim(-0.5,4.8)

    fig.suptitle('Билет 25: операции с геометрическими векторами')
    save_fig(fig, 'bilet-25-vector-ops.png')

    block = '''
## Наглядное представление

### Сложение векторов: правило треугольника и параллелограмма
![Билет 25 - операции с векторами](visuals/bilet-25-vector-ops.png)
'''
    replace_visual_block(ROOT / 'Билет-25.md', block)


# ---------- Ticket 24 ----------
def t24():
    fig, axs = plt.subplots(1,2, figsize=(12,5.2))

    A = np.array([[4,1],[2,3]])
    tr = np.trace(A)
    det = np.linalg.det(A)
    disc = tr**2 - 4*det
    l1 = (tr + np.sqrt(disc))/2
    l2 = (tr - np.sqrt(disc))/2

    axs[0].axis('off')
    axs[0].text(0.05,0.84,'Пример: A=[[4,1],[2,3]]', fontsize=12)
    axs[0].text(0.05,0.68,f'tr(A)={tr:.0f}, det(A)={det:.0f}', fontsize=12)
    axs[0].text(0.05,0.52,'λ² - tr(A)λ + det(A)=0', fontsize=12)
    axs[0].text(0.05,0.36,f'λ1={l1:.0f}, λ2={l2:.0f}', fontsize=12)
    axs[0].text(0.05,0.20,'Дальше: (A-λI)x=0 для каждого λ', fontsize=11)

    lam = np.linspace(0,7,300)
    poly = lam**2 - tr*lam + det
    axs[1].plot(lam, poly, color='#2563eb', lw=2)
    axs[1].axhline(0, color='black', lw=0.8)
    axs[1].scatter([l1,l2],[0,0], color='crimson', s=30)
    axs[1].set_title('Характеристический многочлен')
    axs[1].set_xlabel('λ'); axs[1].set_ylabel('p(λ)')
    axs[1].grid(alpha=0.3)

    fig.suptitle('Билет 24: нахождение собственных значений (2x2)')
    save_fig(fig, 'bilet-24-eigen-2x2.png')

    block = '''
## Наглядное представление

### Алгоритм поиска собственных значений через характеристический многочлен
![Билет 24 - собственные значения 2x2](visuals/bilet-24-eigen-2x2.png)
'''
    replace_visual_block(ROOT / 'Билет-24.md', block)


# ---------- Ticket 23 ----------
def t23():
    fig, axs = plt.subplots(1,2, figsize=(12,5.1))
    A = np.array([[4,1],[2,3]])
    vals, vecs = np.linalg.eig(A)
    D = np.diag(vals)

    axs[0].axis('off')
    axs[0].text(0.05,0.82,'Свойства:', fontsize=12)
    axs[0].text(0.05,0.66,f'λ1+λ2 = tr(A) = {np.trace(A):.0f}', fontsize=11)
    axs[0].text(0.05,0.52,f'λ1·λ2 = det(A) = {np.linalg.det(A):.0f}', fontsize=11)
    axs[0].text(0.05,0.36,'Если есть базис из собств. векторов,\nA=PDP⁻¹', fontsize=11)

    axs[1].imshow(D, cmap='Greens')
    axs[1].set_title('Диагональная матрица D\nв собственном базисе')
    for i in range(2):
        for j in range(2):
            axs[1].text(j,i,f'{D[i,j]:.1f}',ha='center',va='center')
    axs[1].set_xticks([0,1]); axs[1].set_yticks([0,1])

    fig.suptitle('Билет 23: свойства собственных значений и диагонализация')
    save_fig(fig, 'bilet-23-eigen-properties.png')

    block = '''
## Наглядное представление

### Связь собственных значений с tr(A), det(A) и диагонализацией
![Билет 23 - свойства собственных значений](visuals/bilet-23-eigen-properties.png)
'''
    replace_visual_block(ROOT / 'Билет-23.md', block)


# ---------- Ticket 22 ----------
def t22():
    fig, axs = plt.subplots(1,2, figsize=(12,5.1))
    A = np.array([[4,1],[2,3]])
    tr, det = np.trace(A), np.linalg.det(A)
    lam = np.linspace(0,7,300)
    p = lam**2 - tr*lam + det

    axs[0].plot(lam,p, color='#2563eb', lw=2)
    axs[0].axhline(0,color='black',lw=0.8)
    axs[0].set_title('p(λ)=det(A-λI)')
    axs[0].set_xlabel('λ'); axs[0].set_ylabel('p(λ)')
    axs[0].grid(alpha=0.3)

    axs[1].axis('off')
    axs[1].text(0.05,0.82,'Инварианты характеристического многочлена:', fontsize=11)
    axs[1].text(0.05,0.64,'коэффициент при λ^(n-1) = -tr(A)', fontsize=11)
    axs[1].text(0.05,0.48,'свободный член = det(A)', fontsize=11)
    axs[1].text(0.05,0.30,'При подобии A\'=C⁻¹AC\nмногочлен не меняется.', fontsize=11)

    fig.suptitle('Билет 22: характеристический многочлен')
    save_fig(fig, 'bilet-22-charpoly.png')

    block = '''
## Наглядное представление

### Характеристический многочлен и его инварианты
![Билет 22 - характеристический многочлен](visuals/bilet-22-charpoly.png)
'''
    replace_visual_block(ROOT / 'Билет-22.md', block)


# ---------- Ticket 21 ----------
def t21():
    fig, axs = plt.subplots(1,2, figsize=(12,5.1))

    A = np.array([[2,0],[0,0.5]])
    v1 = np.array([1,0.2])
    v2 = np.array([0.2,1])
    e1 = np.array([1,0])
    e2 = np.array([0,1])

    for vec,col,lab in [(v1,'#2563eb','v'), (A@v1,'#93c5fd','Av')]:
        axs[0].arrow(0,0,vec[0],vec[1], width=0.03, color=col)
        axs[0].text(vec[0]+0.05,vec[1]+0.05,lab)
    for vec,col,lab in [(e1,'#dc2626','x eigvec'), (A@e1,'#fca5a5','A x eigvec')]:
        axs[0].arrow(0,0,vec[0],vec[1], width=0.02, color=col)
    set2d(axs[0], 'Собственный вектор не меняет направления')
    axs[0].set_xlim(-0.5,2.5); axs[0].set_ylim(-0.5,1.5)

    axs[1].axis('off')
    axs[1].text(0.05,0.82,'Ax = λx', fontsize=14)
    axs[1].text(0.05,0.62,'Собственные значения: корни det(A-λI)=0', fontsize=11)
    axs[1].text(0.05,0.46,'Собственные векторы: Ker(A-λI)', fontsize=11)
    axs[1].text(0.05,0.28,'Собств. подпространство =\nвсе такие x + 0', fontsize=11)

    fig.suptitle('Билет 21: собственные значения и векторы')
    save_fig(fig, 'bilet-21-eigen-geometry.png')

    block = '''
## Наглядное представление

### Геометрический смысл собственного вектора
![Билет 21 - собственные векторы](visuals/bilet-21-eigen-geometry.png)
'''
    replace_visual_block(ROOT / 'Билет-21.md', block)


# ---------- Ticket 20 ----------
def t20():
    fig, axs = plt.subplots(1,2, figsize=(12,5.1))

    # composition on square
    sq = np.array([[0,0],[1,0],[1,1],[0,1],[0,0]], dtype=float)
    F = np.array([[2,0],[0,1]])
    G = np.array([[1,1],[0,1]])
    sf = (F @ sq.T).T
    sgf = (G @ sf.T).T

    axs[0].plot(sq[:,0],sq[:,1], color='black', lw=1.5, label='x')
    axs[0].plot(sf[:,0],sf[:,1], color='#2563eb', lw=1.8, label='f(x)')
    axs[0].plot(sgf[:,0],sgf[:,1], color='#dc2626', lw=1.8, label='g(f(x))')
    set2d(axs[0], 'Суперпозиция: [g∘f]=[g][f]')
    axs[0].legend(fontsize=8)

    axs[1].axis('off')
    axs[1].text(0.05,0.80,'(f+g)(x)=f(x)+g(x)', fontsize=12)
    axs[1].text(0.05,0.62,'(λf)(x)=λf(x)', fontsize=12)
    axs[1].text(0.05,0.44,'(g∘f)(x)=g(f(x))', fontsize=12)
    axs[1].text(0.05,0.26,'f обратимо ⇔ det A ≠ 0', fontsize=12)

    fig.suptitle('Билет 20: действия с линейными отображениями')
    save_fig(fig, 'bilet-20-map-operations.png')

    block = '''
## Наглядное представление

### Сложение, масштабирование, композиция и обратимость отображений
![Билет 20 - действия с отображениями](visuals/bilet-20-map-operations.png)
'''
    replace_visual_block(ROOT / 'Билет-20.md', block)


# ---------- Ticket 19 ----------
def t19():
    fig, axs = plt.subplots(2,2, figsize=(10,8.5))
    sq = np.array([[0,0],[1,0],[1,1],[0,1],[0,0]], float)

    mats = [
        (np.eye(2), 'E'),
        (np.array([[2,0],[0,1]]), 'Растяжение'),
        (np.array([[1,1],[0,1]]), 'Сдвиг'),
        (np.array([[np.cos(np.pi/6), -np.sin(np.pi/6)],[np.sin(np.pi/6), np.cos(np.pi/6)]]), 'Поворот'),
    ]

    for ax, (M, title) in zip(axs.ravel(), mats):
        tr = (M @ sq.T).T
        ax.plot(sq[:,0],sq[:,1], color='black', lw=1.2)
        ax.plot(tr[:,0],tr[:,1], color='#2563eb', lw=2)
        set2d(ax, title)
        ax.set_xlim(-1.5,2.5); ax.set_ylim(-1.5,2.5)

    fig.suptitle('Билет 19: матрица линейного преобразования на плоскости')
    save_fig(fig, 'bilet-19-transform-matrices.png')

    block = '''
## Наглядное представление

### Как разные матрицы действуют на фигуру
![Билет 19 - матрицы преобразований](visuals/bilet-19-transform-matrices.png)
'''
    replace_visual_block(ROOT / 'Билет-19.md', block)


# ---------- Ticket 18 ----------
def t18():
    fig, axs = plt.subplots(1,3, figsize=(15,4.8))

    # injective
    axs[0].axis('off')
    axs[0].set_title('Инъекция')
    left = [(0.2,0.8),(0.2,0.5),(0.2,0.2)]
    right = [(0.8,0.8),(0.8,0.5),(0.8,0.2),(0.8,0.05)]
    for p in left: axs[0].add_patch(Circle(p,0.03,color='#2563eb'))
    for p in right: axs[0].add_patch(Circle(p,0.03,color='#dc2626'))
    for p,q in zip(left,right[:3]): axs[0].add_patch(FancyArrowPatch(p,q,arrowstyle='->',mutation_scale=10))

    # surjective
    axs[1].axis('off')
    axs[1].set_title('Сюръекция')
    left = [(0.2,0.8),(0.2,0.6),(0.2,0.4),(0.2,0.2)]
    right = [(0.8,0.75),(0.8,0.5),(0.8,0.25)]
    for p in left: axs[1].add_patch(Circle(p,0.03,color='#2563eb'))
    for p in right: axs[1].add_patch(Circle(p,0.03,color='#dc2626'))
    arr = [(0,0),(1,1),(2,1),(3,2)]
    for i,j in arr: axs[1].add_patch(FancyArrowPatch(left[i],right[j],arrowstyle='->',mutation_scale=10))

    # bijection
    axs[2].axis('off')
    axs[2].set_title('Биекция (изоморфизм)')
    left = [(0.2,0.75),(0.2,0.5),(0.2,0.25)]
    right = [(0.8,0.75),(0.8,0.5),(0.8,0.25)]
    for p in left: axs[2].add_patch(Circle(p,0.03,color='#2563eb'))
    for p in right: axs[2].add_patch(Circle(p,0.03,color='#dc2626'))
    for p,q in zip(left,right): axs[2].add_patch(FancyArrowPatch(p,q,arrowstyle='->',mutation_scale=10))

    fig.suptitle('Билет 18: инъекция, сюръекция, биекция')
    save_fig(fig, 'bilet-18-inj-surj-bij.png')

    block = '''
## Наглядное представление

### Инъекция, сюръекция, биекция и изоморфизм
![Билет 18 - инъекция сюръекция биекция](visuals/bilet-18-inj-surj-bij.png)
'''
    replace_visual_block(ROOT / 'Билет-18.md', block)


# ---------- Ticket 17 ----------
def t17():
    fig, axs = plt.subplots(1,3, figsize=(15,4.8))
    sq = np.array([[0,0],[1,0],[1,1],[0,1],[0,0]], float)

    Ms = [
        (np.array([[1,0],[0,1]]), 'id'),
        (np.array([[1.8,0],[0,0.8]]), 'растяжение'),
        (np.array([[np.cos(np.pi/4), -np.sin(np.pi/4)],[np.sin(np.pi/4), np.cos(np.pi/4)]]), 'поворот'),
    ]
    for ax,(M,tit) in zip(axs,Ms):
        tr = (M@sq.T).T
        ax.plot(sq[:,0],sq[:,1], color='black', lw=1.2)
        ax.plot(tr[:,0],tr[:,1], color='#2563eb', lw=2)
        set2d(ax, tit)
        ax.set_xlim(-1.5,2.2); ax.set_ylim(-1.5,2.2)

    fig.suptitle('Билет 17: линейные преобразования на примерах')
    save_fig(fig, 'bilet-17-linear-maps.png')

    block = '''
## Наглядное представление

### Примеры линейных преобразований (id, растяжение, поворот)
![Билет 17 - линейные преобразования](visuals/bilet-17-linear-maps.png)
'''
    replace_visual_block(ROOT / 'Билет-17.md', block)


# ---------- Ticket 16 ----------
def t16():
    fig, axs = plt.subplots(1,2, figsize=(12,5.0))

    e1 = np.array([1,0]); e2 = np.array([0,1])
    b1 = np.array([1,1]); b2=np.array([2,0.5])
    x_new = np.array([1.2, 0.8])
    x_old = x_new[0]*b1 + x_new[1]*b2

    axs[0].arrow(0,0,e1[0],e1[1], color='black', width=0.02)
    axs[0].arrow(0,0,e2[0],e2[1], color='black', width=0.02)
    axs[0].arrow(0,0,b1[0],b1[1], color='#2563eb', width=0.02)
    axs[0].arrow(0,0,b2[0],b2[1], color='#dc2626', width=0.02)
    axs[0].arrow(0,0,x_old[0],x_old[1], color='#16a34a', width=0.02)
    set2d(axs[0], 'Старый и новый базисы')
    axs[0].set_xlim(-0.5,3.5); axs[0].set_ylim(-0.5,2.5)

    axs[1].axis('off')
    C = np.column_stack([b1,b2])
    axs[1].text(0.05,0.80,f'C = [{b1.tolist()} {b2.tolist()}]', fontsize=11)
    axs[1].text(0.05,0.62,'x = C x\'', fontsize=12)
    axs[1].text(0.05,0.44,f'x\'={x_new.round(2).tolist()} -> x={x_old.round(2).tolist()}', fontsize=11)
    axs[1].text(0.05,0.26,'A\' = C⁻¹AC', fontsize=12)

    fig.suptitle('Билет 16: преобразование базиса')
    save_fig(fig, 'bilet-16-change-basis.png')

    block = '''
## Наглядное представление

### Матрица перехода и преобразование координат
![Билет 16 - преобразование базиса](visuals/bilet-16-change-basis.png)
'''
    replace_visual_block(ROOT / 'Билет-16.md', block)


# ---------- Ticket 15 ----------
def t15():
    fig, axs = plt.subplots(1,2, figsize=(12,5.1))

    v1 = np.array([3,1])
    v2 = np.array([2,2.5])
    u1 = v1
    proj = np.dot(v2,u1)/np.dot(u1,u1)*u1
    u2 = v2 - proj

    for vec,col,lab in [(v1,'#2563eb','v1=u1'),(v2,'#dc2626','v2'),(proj,'#f59e0b','proj_u1(v2)'),(u2,'#16a34a','u2')]:
        axs[0].arrow(0,0,vec[0],vec[1], width=0.03, color=col)
        axs[0].text(vec[0]+0.08,vec[1]+0.08,lab, fontsize=9)
    set2d(axs[0], 'Шаг Грама-Шмидта')
    axs[0].set_xlim(-0.5,3.8); axs[0].set_ylim(-0.5,3.5)

    axs[1].axis('off')
    axs[1].text(0.05,0.80,'u1=v1', fontsize=12)
    axs[1].text(0.05,0.62,'u2=v2 - proj_u1(v2)', fontsize=12)
    axs[1].text(0.05,0.44,'proj_u(v)=((v,u)/(u,u))u', fontsize=12)
    axs[1].text(0.05,0.26,'dim V + dim V⊥ = dim пространства', fontsize=11)

    fig.suptitle('Билет 15: ортогонализация Грама-Шмидта')
    save_fig(fig, 'bilet-15-gram-schmidt.png')

    block = '''
## Наглядное представление

### Ортогонализация: вычитание проекции
![Билет 15 - Грам-Шмидт](visuals/bilet-15-gram-schmidt.png)
'''
    replace_visual_block(ROOT / 'Билет-15.md', block)


# ---------- Ticket 14 ----------
def t14():
    fig, axs = plt.subplots(1,2, figsize=(12,5.0))

    e1=np.array([1,0]); e2=np.array([0,1]); x=np.array([2.5,1.5])
    axs[0].arrow(0,0,e1[0],e1[1], width=0.02, color='black')
    axs[0].arrow(0,0,e2[0],e2[1], width=0.02, color='black')
    axs[0].arrow(0,0,x[0],x[1], width=0.03, color='#2563eb')
    axs[0].plot([x[0],x[0]],[0,x[1]], ls='--', color='#475569')
    axs[0].text(x[0]+0.05,0.05,'x1'); axs[0].text(0.05,x[1]+0.05,'x2')
    set2d(axs[0], 'Ортонормированный базис, x=(x1,x2)')
    axs[0].set_xlim(-0.5,3.5); axs[0].set_ylim(-0.5,2.5)

    axs[1].axis('off')
    axs[1].text(0.05,0.80,'x_i = (x,e_i)', fontsize=12)
    axs[1].text(0.05,0.62,'|x|² = Σ x_i² (Парсеваль)', fontsize=12)
    axs[1].text(0.05,0.44,'В ортонорм. базисе\nкоординаты = проекции', fontsize=11)

    fig.suptitle('Билет 14: ортогональный базис и равенство Парсеваля')
    save_fig(fig, 'bilet-14-orthonormal-parseval.png')

    block = '''
## Наглядное представление

### Ортонормированный базис: координаты как скалярные произведения
![Билет 14 - Парсеваль](visuals/bilet-14-orthonormal-parseval.png)
'''
    replace_visual_block(ROOT / 'Билет-14.md', block)


# ---------- Ticket 13 ----------
def t13():
    fig, axs = plt.subplots(1,2, figsize=(12,5.0))

    x=np.array([3,1]); y=np.array([1.3,2.4]); s=x+y
    axs[0].arrow(0,0,x[0],x[1], width=0.03, color='#2563eb')
    axs[0].arrow(0,0,y[0],y[1], width=0.03, color='#dc2626')
    axs[0].arrow(0,0,s[0],s[1], width=0.03, color='#16a34a')
    set2d(axs[0], '|x+y| ≤ |x|+|y| (треугольник)')
    axs[0].set_xlim(-0.5,5.0); axs[0].set_ylim(-0.5,4.0)

    t=np.linspace(-3,3,200)
    axs[1].plot(t, t*0+np.linalg.norm(x)*np.linalg.norm(y), color='#16a34a', lw=2)
    axs[1].plot(t, t*0-np.linalg.norm(x)*np.linalg.norm(y), color='#16a34a', lw=2)
    axs[1].scatter([0],[np.dot(x,y)], color='crimson', s=35)
    axs[1].set_xlim(-1,1)
    axs[1].set_title('|(x,y)| ≤ |x||y| (КБШ)')
    axs[1].set_xticks([]); axs[1].grid(alpha=0.3)

    fig.suptitle('Билет 13: неравенства КБШ и треугольника')
    save_fig(fig, 'bilet-13-inequalities.png')

    block = '''
## Наглядное представление

### Геометрический смысл неравенств КБШ и треугольника
![Билет 13 - неравенства](visuals/bilet-13-inequalities.png)
'''
    replace_visual_block(ROOT / 'Билет-13.md', block)


# ---------- Ticket 12 ----------
def t12():
    fig, axs = plt.subplots(1,2, figsize=(12,5.0))

    v1=np.array([1,2]); v2=np.array([2,1])
    axs[0].arrow(0,0,v1[0],v1[1], width=0.03, color='#2563eb')
    axs[0].arrow(0,0,v2[0],v2[1], width=0.03, color='#dc2626')
    set2d(axs[0], 'Евклидово пространство: скалярное произведение')
    axs[0].set_xlim(-0.5,2.8); axs[0].set_ylim(-0.5,2.8)

    G=np.array([[np.dot(v1,v1),np.dot(v1,v2)],[np.dot(v2,v1),np.dot(v2,v2)]])
    axs[1].imshow(G, cmap='Blues')
    axs[1].set_title(f'Матрица Грама G, det G = {np.linalg.det(G):.2f} > 0')
    for i in range(2):
        for j in range(2):
            axs[1].text(j,i,f'{G[i,j]:.0f}',ha='center',va='center')
    axs[1].set_xticks([0,1]); axs[1].set_yticks([0,1])

    fig.suptitle('Билет 12: евклидово пространство и матрица Грама')
    save_fig(fig, 'bilet-12-gram-matrix.png')

    block = '''
## Наглядное представление

### Матрица Грама как таблица всех скалярных произведений
![Билет 12 - матрица Грама](visuals/bilet-12-gram-matrix.png)
'''
    replace_visual_block(ROOT / 'Билет-12.md', block)


# ---------- Ticket 11 ----------
def t11():
    fig = plt.figure(figsize=(11.5,5.2))
    ax1 = fig.add_subplot(1,2,1, projection='3d')

    # subspace plane z = x + y through origin
    xx, yy = np.meshgrid(np.linspace(-2,2,20), np.linspace(-2,2,20))
    zz = xx + yy
    ax1.plot_surface(xx,yy,zz, alpha=0.45, color='#93c5fd')
    ax1.quiver(0,0,0,1,0,1,color='#2563eb',linewidth=2)
    ax1.quiver(0,0,0,0,1,1,color='#dc2626',linewidth=2)
    set3d(ax1, 'Подпространство как плоскость через O')
    ax1.view_init(23,35)

    ax2 = fig.add_subplot(1,2,2)
    ax2.axis('off')
    ax2.text(0.05,0.80,'Lin{v1,...,vk} = все линейные комбинации', fontsize=11)
    ax2.text(0.05,0.62,'Базис: ЛНЗ + порождение всего V', fontsize=11)
    ax2.text(0.05,0.44,'dim V = число векторов в базисе', fontsize=11)
    ax2.text(0.05,0.26,'Любую ЛНЗ систему можно\nдополнить до базиса', fontsize=11)

    fig.suptitle('Билет 11: линейные пространства и подпространства')
    save_fig(fig, 'bilet-11-vector-spaces.png')

    block = '''
## Наглядное представление

### Подпространство, линейная оболочка, базис и размерность
![Билет 11 - линейные пространства](visuals/bilet-11-vector-spaces.png)
'''
    replace_visual_block(ROOT / 'Билет-11.md', block)


# ---------- Ticket 10 ----------
def t10():
    fig, axs = plt.subplots(1,2, figsize=(12,5.1))

    axs[0].axis('off')
    axs[0].text(0.05,0.82,'Однородная система Ax=0', fontsize=12)
    axs[0].text(0.05,0.64,'dim ФСР = n - rank(A)', fontsize=12)
    axs[0].text(0.05,0.46,'Общее решение: x = Σ ci x(i)', fontsize=12)
    axs[0].text(0.05,0.28,'Неоднородная: x = x_частн + x_одн', fontsize=12)

    # nullspace line in R2 example
    t = np.linspace(-3,3,200)
    axs[1].plot(t, -2*t, color='#2563eb', lw=2)
    set2d(axs[1], 'Пример ФСР в R²: x2 = -2x1')

    fig.suptitle('Билет 10: фундаментальная система решений')
    save_fig(fig, 'bilet-10-fsr.png')

    block = '''
## Наглядное представление

### ФСР как базис пространства решений Ax=0
![Билет 10 - ФСР](visuals/bilet-10-fsr.png)
'''
    replace_visual_block(ROOT / 'Билет-10.md', block)


# ---------- Ticket 9 ----------
def t9():
    fig, axs = plt.subplots(1,2, figsize=(12,5.0))

    axs[0].axis('off')
    axs[0].text(0.05,0.80,'Ax=0 всегда совместна', fontsize=12)
    axs[0].text(0.05,0.62,'rank(A)=n -> только x=0', fontsize=12)
    axs[0].text(0.05,0.44,'rank(A)<n -> бесконечно много', fontsize=12)
    axs[0].text(0.05,0.26,'Все линейные комбинации решений\nтоже решения', fontsize=11)

    t=np.linspace(-3,3,200)
    axs[1].plot(t,-t,color='#2563eb',lw=2,label='решения')
    axs[1].scatter([0],[0],color='crimson',s=35,label='тривиальное')
    set2d(axs[1], 'Геометрия множества решений (пример в R²)')
    axs[1].legend(fontsize=8)

    fig.suptitle('Билет 9: однородные системы')
    save_fig(fig, 'bilet-09-homogeneous.png')

    block = '''
## Наглядное представление

### Однородная система: от тривиального к пространству решений
![Билет 9 - однородные системы](visuals/bilet-09-homogeneous.png)
'''
    replace_visual_block(ROOT / 'Билет-09.md', block)


# ---------- Ticket 8 ----------
def t8():
    fig, axs = plt.subplots(1,2, figsize=(12,5.1))

    axs[0].axis('off')
    axs[0].text(0.05,0.82,'Гаусс: (A|b) -> ступенчатая форма', fontsize=12)
    axs[0].text(0.05,0.64,'rank A = rank(A|b) -> совместна', fontsize=12)
    axs[0].text(0.05,0.46,'= n -> единственное решение', fontsize=11)
    axs[0].text(0.05,0.34,'< n -> бесконечно много', fontsize=11)
    axs[0].text(0.05,0.22,'rank A < rank(A|b) -> нет решений', fontsize=11)

    axs[1].axis('off')
    axs[1].text(0.05,0.78,'[1 0 | 2]\n[0 1 | 1]', fontsize=13)
    axs[1].text(0.50,0.78,'единств.', fontsize=11)
    axs[1].text(0.05,0.50,'[1 0 1 | 2]\n[0 1 1 | 1]', fontsize=13)
    axs[1].text(0.50,0.50,'беск. мн-во', fontsize=11)
    axs[1].text(0.05,0.22,'[1 0 | 1]\n[0 0 | 1]', fontsize=13)
    axs[1].text(0.50,0.22,'несовместна', fontsize=11)

    fig.suptitle('Билет 8: метод Гаусса и теорема Кронекера-Капелли')
    save_fig(fig, 'bilet-08-gauss-kk.png')

    block = '''
## Наглядное представление

### Классификация СЛАУ через ранги после метода Гаусса
![Билет 8 - Гаусс и Кронекер-Капелли](visuals/bilet-08-gauss-kk.png)
'''
    replace_visual_block(ROOT / 'Билет-08.md', block)


# ---------- Ticket 7 ----------
def t7():
    fig, axs = plt.subplots(1,2, figsize=(12,5.0))

    A=np.array([[2,1],[1,3]],float); b=np.array([5,7],float)
    x=np.linalg.solve(A,b)
    D=np.linalg.det(A)
    D1=np.linalg.det(np.column_stack([b,A[:,1]]))
    D2=np.linalg.det(np.column_stack([A[:,0],b]))

    axs[0].axis('off')
    axs[0].text(0.05,0.82,'Матричный метод: x=A⁻¹b', fontsize=12)
    axs[0].text(0.05,0.64,f'A={A.tolist()}, b={b.tolist()}', fontsize=10)
    axs[0].text(0.05,0.50,f'x={x.round(3).tolist()}', fontsize=11)

    axs[1].axis('off')
    axs[1].text(0.05,0.82,'Крамер: xi = Di / D', fontsize=12)
    axs[1].text(0.05,0.64,f'D={D:.1f}, D1={D1:.1f}, D2={D2:.1f}', fontsize=11)
    axs[1].text(0.05,0.46,f'x1={D1/D:.3f}, x2={D2/D:.3f}', fontsize=11)
    axs[1].text(0.05,0.28,'Условие: det(A) ≠ 0', fontsize=11)

    fig.suptitle('Билет 7: матричный метод и метод Крамера')
    save_fig(fig, 'bilet-07-cramer-matrix.png')

    block = '''
## Наглядное представление

### Сравнение матричного метода и метода Крамера на одном примере
![Билет 7 - Крамер и матричный метод](visuals/bilet-07-cramer-matrix.png)
'''
    replace_visual_block(ROOT / 'Билет-07.md', block)


# ---------- Ticket 6 ----------
def t6():
    fig, axs = plt.subplots(1,2, figsize=(12,5.0))
    A=np.array([[2,1],[1,1]],float)
    inv=np.linalg.inv(A)

    axs[0].axis('off')
    axs[0].text(0.05,0.82,'A⁻¹ существует ⇔ det(A)≠0', fontsize=12)
    axs[0].text(0.05,0.64,f'A={A.tolist()}, det={np.linalg.det(A):.1f}', fontsize=11)
    axs[0].text(0.05,0.46,f'A⁻¹={inv.round(3).tolist()}', fontsize=11)
    axs[0].text(0.05,0.28,'A⁻¹ = (1/detA) adj(A)', fontsize=12)

    axs[1].axis('off')
    axs[1].text(0.05,0.82,'Метод Гаусса-Жордана:', fontsize=12)
    axs[1].text(0.05,0.64,'(A|E) -> (E|A⁻¹)', fontsize=12)
    axs[1].text(0.05,0.46,'[2 1 | 1 0] -> [1 0 | 1 -1]', fontsize=11)
    axs[1].text(0.05,0.34,'[1 1 | 0 1] -> [0 1 | -1 2]', fontsize=11)

    fig.suptitle('Билет 6: обратная матрица')
    save_fig(fig, 'bilet-06-inverse.png')

    block = '''
## Наглядное представление

### Обратная матрица: критерий существования и метод Гаусса
![Билет 6 - обратная матрица](visuals/bilet-06-inverse.png)
'''
    replace_visual_block(ROOT / 'Билет-06.md', block)


# ---------- Ticket 5 ----------
def t5():
    fig, axs = plt.subplots(1,2, figsize=(12,5.0))
    A=np.array([[1,2,3],[2,4,6],[1,1,1]],float)
    # echelon
    E=A.copy()
    E[1]=E[1]-2*E[0]
    E[2]=E[2]-E[0]

    axs[0].axis('off')
    axs[0].text(0.05,0.80,'A=', fontsize=12)
    axs[0].text(0.14,0.80,str(A.astype(int).tolist()), fontsize=10)
    axs[0].text(0.05,0.56,'Ступенчатая форма:', fontsize=12)
    axs[0].text(0.05,0.44,str(E.astype(int).tolist()), fontsize=10)
    axs[0].text(0.05,0.28,'rank(A)=число ненулевых строк = 2', fontsize=11)

    axs[1].axis('off')
    axs[1].text(0.05,0.80,'Ранг = max порядок ненулевого минора', fontsize=11)
    axs[1].text(0.05,0.62,'Базисный минор задаёт ЛНЗ строки/столбцы', fontsize=11)
    axs[1].text(0.05,0.44,'ЭП сохраняют ранг', fontsize=11)

    fig.suptitle('Билет 5: ранг матрицы')
    save_fig(fig, 'bilet-05-rank.png')

    block = '''
## Наглядное представление

### Ранг матрицы через ступенчатый вид и базисный минор
![Билет 5 - ранг матрицы](visuals/bilet-05-rank.png)
'''
    replace_visual_block(ROOT / 'Билет-05.md', block)


# ---------- Ticket 4 ----------
def t4():
    fig, axs = plt.subplots(1,2, figsize=(12,5.0))

    # area scaling by determinant
    square=np.array([[0,0],[1,0],[1,1],[0,1],[0,0]], float)
    A=np.array([[2,1],[0,1]])
    tr=(A@square.T).T
    axs[0].fill(square[:,0],square[:,1], alpha=0.25, color='gray', label='E, area=1')
    axs[0].fill(tr[:,0],tr[:,1], alpha=0.35, color='#2563eb', label=f'A, area=|detA|={abs(np.linalg.det(A)):.0f}')
    set2d(axs[0], 'det как коэффициент площади')
    axs[0].legend(fontsize=8)

    axs[1].axis('off')
    axs[1].text(0.05,0.82,'det(Aᵀ)=det(A)', fontsize=12)
    axs[1].text(0.05,0.64,'Перестановка строк -> смена знака', fontsize=11)
    axs[1].text(0.05,0.46,'Умножение строки на λ -> det*λ', fontsize=11)
    axs[1].text(0.05,0.28,'det(AB)=det(A)det(B)', fontsize=12)

    fig.suptitle('Билет 4: свойства определителей')
    save_fig(fig, 'bilet-04-det-properties.png')

    block = '''
## Наглядное представление

### Геометрический смысл свойств определителя
![Билет 4 - свойства определителей](visuals/bilet-04-det-properties.png)
'''
    replace_visual_block(ROOT / 'Билет-04.md', block)


# ---------- Ticket 3 ----------
def t3():
    fig, axs = plt.subplots(1,2, figsize=(12,5.0))

    A=np.array([[2,1,3],[0,1,2],[4,1,0]])
    det=np.linalg.det(A)
    axs[0].axis('off')
    axs[0].text(0.05,0.84,f'A={A.tolist()}', fontsize=10)
    axs[0].text(0.05,0.66,'Разложение по 1-й строке:', fontsize=11)
    axs[0].text(0.05,0.52,'detA = a11*A11 + a12*A12 + a13*A13', fontsize=11)
    axs[0].text(0.05,0.34,f'detA = {det:.0f}', fontsize=12)

    axs[1].axis('off')
    axs[1].text(0.05,0.80,'Минор Mij: вычеркнуть i-ю строку, j-й столбец', fontsize=11)
    axs[1].text(0.05,0.60,'Алгебр. дополнение Aij = (-1)^(i+j) Mij', fontsize=11)
    axs[1].text(0.05,0.40,'Разложение по любой строке/столбцу\nдаёт тот же det.', fontsize=11)

    fig.suptitle('Билет 3: вычисление определителя')
    save_fig(fig, 'bilet-03-determinant-expansion.png')

    block = '''
## Наглядное представление

### Разложение определителя по строке/столбцу через миноры
![Билет 3 - вычисление определителя](visuals/bilet-03-determinant-expansion.png)
'''
    replace_visual_block(ROOT / 'Билет-03.md', block)


# ---------- Ticket 2 ----------
def t2():
    fig, axs = plt.subplots(1,2, figsize=(12,5.0))
    A=np.array([[1,2,3],[4,5,6],[7,8,9]], dtype=float)
    B=A.copy(); B[[0,1]]=B[[1,0]]
    C=A.copy(); C[1]=2*C[1]
    D=A.copy(); D[2]=D[2]-3*D[0]

    axs[0].axis('off')
    axs[0].text(0.05,0.82,'1) Перестановка строк R1 <-> R2', fontsize=11)
    axs[0].text(0.05,0.66,str(B.astype(int).tolist()), fontsize=10)
    axs[0].text(0.05,0.46,'2) Умножение строки R2 <- 2R2', fontsize=11)
    axs[0].text(0.05,0.30,str(C.astype(int).tolist()), fontsize=10)

    axs[1].axis('off')
    axs[1].text(0.05,0.82,'3) R3 <- R3 - 3R1', fontsize=11)
    axs[1].text(0.05,0.66,str(D.astype(int).tolist()), fontsize=10)
    axs[1].text(0.05,0.44,'Элементарные преобразования\nсохраняют ранг', fontsize=11)
    axs[1].text(0.05,0.26,'Используются в методе Гаусса', fontsize=11)

    fig.suptitle('Билет 2: элементарные преобразования матриц')
    save_fig(fig, 'bilet-02-row-operations.png')

    block = '''
## Наглядное представление

### Три типа элементарных преобразований строк
![Билет 2 - элементарные преобразования](visuals/bilet-02-row-operations.png)
'''
    replace_visual_block(ROOT / 'Билет-02.md', block)


# ---------- Ticket 1 ----------
def t1():
    fig, axs = plt.subplots(2,3, figsize=(12,8.0))
    mats = [
        (np.array([[1,2],[3,4]]), 'Прямоугольная'),
        (np.eye(3), 'Единичная'),
        (np.zeros((3,3)), 'Нулевая'),
        (np.diag([2,5,1]), 'Диагональная'),
        (np.array([[1,2,3],[0,4,5],[0,0,6]]), 'Верхнетреугольная'),
        (np.array([[2,1,3],[1,4,0],[3,0,5]]), 'Симметрическая'),
    ]

    for ax, (M,title) in zip(axs.ravel(), mats):
        ax.imshow(M, cmap='Blues')
        ax.set_title(title, fontsize=10)
        ax.set_xticks([]); ax.set_yticks([])
        for i in range(M.shape[0]):
            for j in range(M.shape[1]):
                ax.text(j,i,f'{M[i,j]:.0f}',ha='center',va='center',fontsize=8)

    fig.suptitle('Билет 1: основные типы матриц')
    save_fig(fig, 'bilet-01-matrix-types.png')

    block = '''
## Наглядное представление

### Основные типы матриц из билета
![Билет 1 - типы матриц](visuals/bilet-01-matrix-types.png)
'''
    replace_visual_block(ROOT / 'Билет-01.md', block)


def main():
    # Continue strictly from the end after 50-48: 47 -> 1
    gens = [
        t47, t46, t45, t44, t43, t42, t41, t40, t39, t38, t37, t36, t35, t34,
        t33, t32, t31, t30, t29, t28, t27, t26, t25, t24, t23, t22, t21, t20,
        t19, t18, t17, t16, t15, t14, t13, t12, t11, t10, t9, t8, t7, t6, t5,
        t4, t3, t2, t1,
    ]
    for fn in gens:
        fn()
    print('Generated visuals for tickets 47..1 and updated markdown blocks.')


if __name__ == '__main__':
    main()
