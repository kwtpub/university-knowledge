#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path('.')
VIS = ROOT / 'visuals'
VIS.mkdir(exist_ok=True)


def _style_3d(ax, title: str) -> None:
    ax.set_title(title, fontsize=10)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    ax.grid(True, alpha=0.3)


def _replace_visual_block(md_path: Path, new_block: str) -> None:
    text = md_path.read_text(encoding='utf-8')
    marker = '## Наглядное представление'
    if marker in text:
        text = text.split(marker)[0].rstrip() + '\n\n' + new_block.strip() + '\n'
    else:
        text = text.rstrip() + '\n\n' + new_block.strip() + '\n'
    md_path.write_text(text, encoding='utf-8')


def ticket50() -> None:
    # 1) Real 3D surfaces for cylinders
    fig = plt.figure(figsize=(16, 5), dpi=170)

    # Elliptic cylinder: x^2/a^2 + y^2/b^2 = 1
    a, b = 3.0, 1.8
    t = np.linspace(0, 2 * np.pi, 150)
    z = np.linspace(-3.0, 3.0, 70)
    T, Z = np.meshgrid(t, z)
    X = a * np.cos(T)
    Y = b * np.sin(T)

    ax1 = fig.add_subplot(1, 3, 1, projection='3d')
    ax1.plot_surface(X, Y, Z, cmap='viridis', alpha=0.78, linewidth=0)
    # sample point on surface
    t0, z0 = 0.8, 1.2
    p = (a * np.cos(t0), b * np.sin(t0), z0)
    lhs = p[0] ** 2 / a ** 2 + p[1] ** 2 / b ** 2
    ax1.scatter(*p, color='crimson', s=34)
    _style_3d(ax1, f'Эллипт. цилиндр\nLHS={lhs:.2f} (=1)')
    ax1.view_init(26, 40)

    # Hyperbolic cylinder: x^2/a^2 - y^2/b^2 = 1
    a, b = 1.8, 1.2
    y = np.linspace(-2.4, 2.4, 160)
    z = np.linspace(-2.7, 2.7, 70)
    Y, Z = np.meshgrid(y, z)
    Xp = a * np.sqrt(1.0 + (Y ** 2) / (b ** 2))
    Xn = -Xp

    ax2 = fig.add_subplot(1, 3, 2, projection='3d')
    ax2.plot_surface(Xp, Y, Z, cmap='plasma', alpha=0.73, linewidth=0)
    ax2.plot_surface(Xn, Y, Z, cmap='plasma', alpha=0.73, linewidth=0)
    y0, z0 = 1.0, 0.7
    p = (a * np.sqrt(1.0 + y0 ** 2 / b ** 2), y0, z0)
    lhs = p[0] ** 2 / a ** 2 - p[1] ** 2 / b ** 2
    ax2.scatter(*p, color='crimson', s=34)
    _style_3d(ax2, f'Гипербол. цилиндр\nLHS={lhs:.2f} (=1)')
    ax2.view_init(24, 38)

    # Parabolic cylinder: y^2 = 2 p x  => x = y^2/(2p)
    p_par = 1.0
    y = np.linspace(-3.0, 3.0, 180)
    z = np.linspace(-2.8, 2.8, 70)
    Y, Z = np.meshgrid(y, z)
    X = (Y ** 2) / (2 * p_par)

    ax3 = fig.add_subplot(1, 3, 3, projection='3d')
    ax3.plot_surface(X, Y, Z, cmap='cividis', alpha=0.78, linewidth=0)
    y0, z0 = 1.6, -0.9
    p = (y0 ** 2 / (2 * p_par), y0, z0)
    lhs = p[1] ** 2
    rhs = 2 * p_par * p[0]
    ax3.scatter(*p, color='crimson', s=34)
    _style_3d(ax3, f'Парабол. цилиндр\ny^2={lhs:.2f}, 2px={rhs:.2f}')
    ax3.view_init(25, 42)

    fig.suptitle('Билет 50: цилиндры по каноническим уравнениям', fontsize=13)
    fig.tight_layout()
    fig.savefig(VIS / 'bilet-50-surfaces.png', bbox_inches='tight')
    plt.close(fig)

    # 2) Base curves in Oxy (generator direction = Oz)
    fig, axs = plt.subplots(1, 3, figsize=(16, 4.2), dpi=170)

    a, b = 3.0, 1.8
    t = np.linspace(0, 2 * np.pi, 300)
    axs[0].plot(a * np.cos(t), b * np.sin(t), color='#0f766e', lw=2)
    axs[0].scatter([a * np.cos(0.9)], [b * np.sin(0.9)], color='crimson', s=28)
    axs[0].set_title('x²/a² + y²/b² = 1')

    a, b = 1.8, 1.2
    yy = np.linspace(-2.7, 2.7, 250)
    xx = a * np.sqrt(1 + yy ** 2 / b ** 2)
    axs[1].plot(xx, yy, color='#a21caf', lw=2)
    axs[1].plot(-xx, yy, color='#a21caf', lw=2)
    axs[1].scatter([a * np.sqrt(1 + 0.9 ** 2 / b ** 2)], [0.9], color='crimson', s=28)
    axs[1].set_title('x²/a² - y²/b² = 1')

    p_par = 1.0
    yy = np.linspace(-3.2, 3.2, 280)
    xx = yy ** 2 / (2 * p_par)
    axs[2].plot(xx, yy, color='#1d4ed8', lw=2)
    axs[2].scatter([1.28], [1.6], color='crimson', s=28)
    axs[2].set_title('y² = 2px')

    for ax in axs:
        ax.axhline(0, color='black', lw=0.8)
        ax.axvline(0, color='black', lw=0.8)
        ax.set_aspect('equal', adjustable='box')
        ax.grid(alpha=0.3)
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.text(0.02, 0.95, 'образующие // Oz', transform=ax.transAxes, fontsize=9, va='top')

    fig.suptitle('Билет 50: направляющие кривые в Oxy', fontsize=13)
    fig.tight_layout()
    fig.savefig(VIS / 'bilet-50-generators.png', bbox_inches='tight')
    plt.close(fig)

    block = '''
## Наглядное представление

### 1) Цилиндры как реальные 3D-поверхности (по формулам)
![Билет 50 - цилиндры 3D](visuals/bilet-50-surfaces.png)

### 2) Направляющие кривые в плоскости Oxy + образующие вдоль Oz
![Билет 50 - направляющие](visuals/bilet-50-generators.png)
'''
    _replace_visual_block(ROOT / 'Билет-50.md', block)


def ticket49() -> None:
    # 1) Surfaces
    fig = plt.figure(figsize=(12, 5.6), dpi=170)

    # Elliptic paraboloid: x^2/a^2 + y^2/b^2 = 2z
    a, b = 2.5, 1.8
    x = np.linspace(-3.2, 3.2, 180)
    y = np.linspace(-3.0, 3.0, 180)
    X, Y = np.meshgrid(x, y)
    Z = 0.5 * (X ** 2 / a ** 2 + Y ** 2 / b ** 2)

    ax1 = fig.add_subplot(1, 2, 1, projection='3d')
    ax1.plot_surface(X, Y, Z, cmap='viridis', alpha=0.82, linewidth=0)
    p = (1.5, 1.0, 0.5 * (1.5 ** 2 / a ** 2 + 1.0 ** 2 / b ** 2))
    lhs = p[0] ** 2 / a ** 2 + p[1] ** 2 / b ** 2
    rhs = 2 * p[2]
    ax1.scatter(*p, color='crimson', s=36)
    _style_3d(ax1, f'Эллиптич. параболоид\nLHS={lhs:.2f}, RHS={rhs:.2f}')
    ax1.view_init(27, 40)

    # Hyperbolic paraboloid: x^2/a^2 - y^2/b^2 = 2z
    a, b = 2.3, 1.7
    x = np.linspace(-3.2, 3.2, 220)
    y = np.linspace(-3.2, 3.2, 220)
    X, Y = np.meshgrid(x, y)
    Z = 0.5 * (X ** 2 / a ** 2 - Y ** 2 / b ** 2)

    ax2 = fig.add_subplot(1, 2, 2, projection='3d')
    ax2.plot_surface(X, Y, Z, cmap='coolwarm', alpha=0.82, linewidth=0)
    p = (2.0, 1.0, 0.5 * (2.0 ** 2 / a ** 2 - 1.0 ** 2 / b ** 2))
    lhs = p[0] ** 2 / a ** 2 - p[1] ** 2 / b ** 2
    rhs = 2 * p[2]
    ax2.scatter(*p, color='crimson', s=36)
    _style_3d(ax2, f'Гиперболич. параболоид\nLHS={lhs:.2f}, RHS={rhs:.2f}')
    ax2.view_init(27, 43)

    fig.suptitle('Билет 49: параболоиды по каноническим уравнениям', fontsize=13)
    fig.tight_layout()
    fig.savefig(VIS / 'bilet-49-surfaces.png', bbox_inches='tight')
    plt.close(fig)

    # 2) Cross sections
    fig, axs = plt.subplots(2, 2, figsize=(12, 8), dpi=170)

    # Elliptic paraboloid, z = const => ellipse
    a, b, z0 = 2.5, 1.8, 1.0
    t = np.linspace(0, 2 * np.pi, 300)
    rx = a * np.sqrt(2 * z0)
    ry = b * np.sqrt(2 * z0)
    axs[0, 0].plot(rx * np.cos(t), ry * np.sin(t), color='#0f766e', lw=2)
    axs[0, 0].set_title('x²/a² + y²/b² = 2z0 (z0>0): эллипс')

    # Hyperbolic paraboloid, z = const => hyperbola
    a, b, z0 = 2.3, 1.7, 0.8
    yy = np.linspace(-4, 4, 300)
    xx = a * np.sqrt(2 * z0 + yy ** 2 / b ** 2)
    axs[0, 1].plot(xx, yy, color='#a21caf', lw=2)
    axs[0, 1].plot(-xx, yy, color='#a21caf', lw=2)
    axs[0, 1].set_title('x²/a² - y²/b² = 2z0: гипербола')

    # x=0 section for hyperbolic paraboloid => z = -(y^2)/(2b^2)
    b = 1.7
    y = np.linspace(-3.5, 3.5, 300)
    z = -(y ** 2) / (2 * b ** 2)
    axs[1, 0].plot(y, z, color='#1d4ed8', lw=2)
    axs[1, 0].set_title('x=0 => z = - y²/(2b²): парабола вниз')
    axs[1, 0].set_xlabel('y')
    axs[1, 0].set_ylabel('z')

    # y=0 section for hyperbolic paraboloid => z = x^2/(2a^2)
    a = 2.3
    x = np.linspace(-3.5, 3.5, 300)
    z = (x ** 2) / (2 * a ** 2)
    axs[1, 1].plot(x, z, color='#b45309', lw=2)
    axs[1, 1].set_title('y=0 => z = x²/(2a²): парабола вверх')
    axs[1, 1].set_xlabel('x')
    axs[1, 1].set_ylabel('z')

    for ax in axs.ravel():
        ax.axhline(0, color='black', lw=0.7)
        ax.axvline(0, color='black', lw=0.7)
        ax.grid(alpha=0.3)
        ax.set_aspect('equal', adjustable='box')

    fig.suptitle('Билет 49: характерные сечения', fontsize=13)
    fig.tight_layout()
    fig.savefig(VIS / 'bilet-49-sections.png', bbox_inches='tight')
    plt.close(fig)

    block = '''
## Наглядное представление

### 1) Эллиптический и гиперболический параболоиды (3D)
![Билет 49 - параболоиды](visuals/bilet-49-surfaces.png)

### 2) Сечения (эллипс, гипербола и параболы)
![Билет 49 - сечения](visuals/bilet-49-sections.png)
'''
    _replace_visual_block(ROOT / 'Билет-49.md', block)


def ticket48() -> None:
    # 1) Main quadrics in one 2x2 3D figure
    fig = plt.figure(figsize=(14, 12), dpi=170)

    # Ellipsoid
    a, b, c = 3.0, 2.2, 1.6
    u = np.linspace(0, 2 * np.pi, 160)
    v = np.linspace(-np.pi / 2, np.pi / 2, 120)
    U, V = np.meshgrid(u, v)
    X = a * np.cos(V) * np.cos(U)
    Y = b * np.cos(V) * np.sin(U)
    Z = c * np.sin(V)

    ax1 = fig.add_subplot(2, 2, 1, projection='3d')
    ax1.plot_surface(X, Y, Z, cmap='viridis', alpha=0.8, linewidth=0)
    u0, v0 = 1.0, 0.45
    p = (a * np.cos(v0) * np.cos(u0), b * np.cos(v0) * np.sin(u0), c * np.sin(v0))
    lhs = p[0] ** 2 / a ** 2 + p[1] ** 2 / b ** 2 + p[2] ** 2 / c ** 2
    ax1.scatter(*p, color='crimson', s=34)
    _style_3d(ax1, f'Эллипсоид\nLHS={lhs:.2f} (=1)')
    ax1.view_init(25, 40)

    # One-sheet hyperboloid
    a, b, c = 2.2, 1.6, 1.4
    u = np.linspace(0, 2 * np.pi, 160)
    w = np.linspace(-1.2, 1.2, 120)
    U, W = np.meshgrid(u, w)
    X = a * np.cosh(W) * np.cos(U)
    Y = b * np.cosh(W) * np.sin(U)
    Z = c * np.sinh(W)

    ax2 = fig.add_subplot(2, 2, 2, projection='3d')
    ax2.plot_surface(X, Y, Z, cmap='plasma', alpha=0.78, linewidth=0)
    u0, w0 = 0.8, 0.35
    p = (a * np.cosh(w0) * np.cos(u0), b * np.cosh(w0) * np.sin(u0), c * np.sinh(w0))
    lhs = p[0] ** 2 / a ** 2 + p[1] ** 2 / b ** 2 - p[2] ** 2 / c ** 2
    ax2.scatter(*p, color='crimson', s=34)
    _style_3d(ax2, f'1-полост. гиперболоид\nLHS={lhs:.2f} (=1)')
    ax2.view_init(24, 42)

    # Two-sheet hyperboloid
    a, b, c = 1.8, 1.4, 1.6
    u = np.linspace(0, 2 * np.pi, 160)
    w = np.linspace(0.0, 1.15, 120)
    U, W = np.meshgrid(u, w)
    X = a * np.sinh(W) * np.cos(U)
    Y = b * np.sinh(W) * np.sin(U)
    Zp = c * np.cosh(W)
    Zn = -c * np.cosh(W)

    ax3 = fig.add_subplot(2, 2, 3, projection='3d')
    ax3.plot_surface(X, Y, Zp, cmap='coolwarm', alpha=0.78, linewidth=0)
    ax3.plot_surface(X, Y, Zn, cmap='coolwarm', alpha=0.78, linewidth=0)
    u0, w0 = 1.1, 0.5
    p = (a * np.sinh(w0) * np.cos(u0), b * np.sinh(w0) * np.sin(u0), c * np.cosh(w0))
    lhs = -p[0] ** 2 / a ** 2 - p[1] ** 2 / b ** 2 + p[2] ** 2 / c ** 2
    ax3.scatter(*p, color='crimson', s=34)
    _style_3d(ax3, f'2-полост. гиперболоид\nLHS={lhs:.2f} (=1)')
    ax3.view_init(23, 43)

    # Cone
    a, b, c = 2.0, 1.4, 1.7
    u = np.linspace(0, 2 * np.pi, 160)
    t = np.linspace(0.0, 1.2, 110)
    U, T = np.meshgrid(u, t)
    X = a * T * np.cos(U)
    Y = b * T * np.sin(U)
    Zp = c * T
    Zn = -c * T

    ax4 = fig.add_subplot(2, 2, 4, projection='3d')
    ax4.plot_surface(X, Y, Zp, cmap='cividis', alpha=0.8, linewidth=0)
    ax4.plot_surface(X, Y, Zn, cmap='cividis', alpha=0.8, linewidth=0)
    u0, t0 = 0.6, 0.9
    p = (a * t0 * np.cos(u0), b * t0 * np.sin(u0), c * t0)
    lhs = p[0] ** 2 / a ** 2 + p[1] ** 2 / b ** 2 - p[2] ** 2 / c ** 2
    ax4.scatter(*p, color='crimson', s=34)
    _style_3d(ax4, f'Конус\nLHS={lhs:.2f} (=0)')
    ax4.view_init(24, 41)

    fig.suptitle('Билет 48: эллипсоид, гиперболоиды, конус (точки удовлетворяют формулам)', fontsize=13)
    fig.tight_layout()
    fig.savefig(VIS / 'bilet-48-surfaces.png', bbox_inches='tight')
    plt.close(fig)

    # 2) Typical sections z = const
    fig, axs = plt.subplots(2, 2, figsize=(12, 8), dpi=170)

    # Ellipsoid section z=z0 => ellipse
    a, b, c = 3.0, 2.2, 1.6
    z0 = 0.8
    t = np.linspace(0, 2 * np.pi, 300)
    k = np.sqrt(max(0.0, 1.0 - z0 ** 2 / c ** 2))
    axs[0, 0].plot(a * k * np.cos(t), b * k * np.sin(t), color='#0f766e', lw=2)
    axs[0, 0].set_title('Эллипсоид, z=z0: эллипс')

    # One-sheet hyperboloid z=z0 => ellipse
    a, b, c = 2.2, 1.6, 1.4
    z0 = 1.0
    k = np.sqrt(1.0 + z0 ** 2 / c ** 2)
    axs[0, 1].plot(a * k * np.cos(t), b * k * np.sin(t), color='#a21caf', lw=2)
    axs[0, 1].set_title('1-полост. гиперболоид, z=z0: эллипс')

    # Two-sheet hyperboloid z=z0 => ellipse (|z0|>c)
    a, b, c = 1.8, 1.4, 1.6
    z0 = 2.2
    k = np.sqrt(z0 ** 2 / c ** 2 - 1.0)
    axs[1, 0].plot(a * k * np.cos(t), b * k * np.sin(t), color='#1d4ed8', lw=2)
    axs[1, 0].set_title('2-полост. гиперболоид, |z0|>c: эллипс')

    # Cone z=z0 => ellipse
    a, b, c = 2.0, 1.4, 1.7
    z0 = 1.1
    k = abs(z0) / c
    axs[1, 1].plot(a * k * np.cos(t), b * k * np.sin(t), color='#b45309', lw=2)
    axs[1, 1].set_title('Конус, z=z0: эллипс')

    for ax in axs.ravel():
        ax.axhline(0, color='black', lw=0.7)
        ax.axvline(0, color='black', lw=0.7)
        ax.grid(alpha=0.3)
        ax.set_aspect('equal', adjustable='box')
        ax.set_xlabel('x')
        ax.set_ylabel('y')

    fig.suptitle('Билет 48: сечения плоскостями z = const', fontsize=13)
    fig.tight_layout()
    fig.savefig(VIS / 'bilet-48-sections.png', bbox_inches='tight')
    plt.close(fig)

    block = '''
## Наглядное представление

### 1) 3D-вид поверхностей + отмеченные точки, проверяющие формулы
![Билет 48 - поверхности](visuals/bilet-48-surfaces.png)

### 2) Сечения плоскостями z = const
![Билет 48 - сечения](visuals/bilet-48-sections.png)
'''
    _replace_visual_block(ROOT / 'Билет-48.md', block)


def main() -> None:
    # Strictly from the end as requested: 50 -> 49 -> 48
    ticket50()
    ticket49()
    ticket48()
    print('Generated/updated tickets: 50, 49, 48')


if __name__ == '__main__':
    main()
