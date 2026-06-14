import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

Y_LIM_MAX_VISUAL = 25.0
X_LIM_MAX = 20
LIMITE_FISICO_RAM = 16.0
a_init = 6.0
b_init = 0.5
M0_init = 2.0

plt.style.use('default')
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.size'] = 10
fig, ax = plt.subplots(figsize=(12, 7.5))
fig.patch.set_facecolor('#F0F2F5')
ax.set_facecolor('#FAFBFC')
plt.subplots_adjust(left=0.10, right=0.90, bottom=0.32, top=0.85)
t = np.linspace(0, X_LIM_MAX, 800)

COLOR_RAM_ESTABLE = "#12EA36"      
COLOR_RAM_SATURADO = '#E63946'     
COLOR_ASINTOTA = "#F30D0D"         
COLOR_LIMITE = "#000000"           
COLOR_OVERFLOW = '#E63946'         
COLOR_FILL_RAM = "#17E12C"

# 4. CÁLCULO INICIAL

eq_equilibrio_init = a_init / b_init
M_teorica = eq_equilibrio_init + (M0_init - eq_equilibrio_init) * np.exp(-b_init * t)
M_actual_init = np.clip(M_teorica, 0, LIMITE_FISICO_RAM)

# 5. ELEMENTOS GRÁFICOS

# -- Línea de límite físico --
ax.axhline(LIMITE_FISICO_RAM, color=COLOR_LIMITE, linestyle='-', lw=2.5, alpha=0.9,
           label=f'Límite Físico Hardware ({LIMITE_FISICO_RAM:.0f} GB)', zorder=3)
# -- Línea de equilibrio teórico --
linea_asintota, = ax.plot([0, X_LIM_MAX], [eq_equilibrio_init, eq_equilibrio_init],
                          color=COLOR_ASINTOTA, linestyle='--', lw=2.0, alpha=0.9,
                          label=f'Equilibrio Teórico ($a/b = {eq_equilibrio_init:.2f}$ GB)', zorder=3)
# -- Zona de saturación 
overflow_mask = M_teorica > LIMITE_FISICO_RAM
fill_overflow = ax.fill_between(t, LIMITE_FISICO_RAM, M_teorica, where=overflow_mask,
                                color=COLOR_OVERFLOW, alpha=0.20, interpolate=True,
                                label='Zona de Saturación', zorder=1)
# -- Área bajo la curva real --
fill_ram = ax.fill_between(t, 0, M_actual_init, color=COLOR_FILL_RAM, alpha=0.10, zorder=1)
# -- Curva real de RAM --
color_inicial = COLOR_RAM_SATURADO if eq_equilibrio_init > LIMITE_FISICO_RAM else COLOR_RAM_ESTABLE
linea_ram, = ax.plot(t, M_actual_init, lw=3.0, color=color_inicial,
                     label='Uso de RAM $M(t)$ (Real)', zorder=4)

# 6. ANOTACIONES Y TEXTO DINÁMICO

# Ecuación del modelo
ax.text(0.02, 0.98,
        r'Modelo:' + '\n' + r'$\dfrac{dM}{dt} = a - bM$' + '\n' +
        r'$M(t)=\dfrac{a}{b} + \left(M_0 - \dfrac{a}{b}\right)e^{-bt}$',
        transform=ax.transAxes, fontsize=11, verticalalignment='top', color="#FF0000",
        bbox=dict(boxstyle='round,pad=0.5', facecolor='white', edgecolor='#DDDDDD', alpha=0.95))
# Indicador de estado del sistema
saturado_inicial = eq_equilibrio_init > LIMITE_FISICO_RAM
estado_color = COLOR_RAM_SATURADO if saturado_inicial else '#2A9D8F'
estado_texto = '⚠ SATURADO' if saturado_inicial else '✓ ESTABLE'
texto_estado = ax.text(0.98, 0.95, estado_texto, transform=ax.transAxes,
                       fontsize=20, fontweight='bold', color=estado_color,
                       horizontalalignment='right', verticalalignment='top',
                       bbox=dict(boxstyle='round,pad=0.5', facecolor='white',
                                 edgecolor=estado_color, lw=2.5, alpha=0.95))

# 7. CONFIGURACIÓN DE EJES

ax.set_xlim(0, X_LIM_MAX)
ax.set_ylim(0, Y_LIM_MAX_VISUAL)
ax.set_xlabel('Tiempo ($t$ en segundos)', fontsize=12, color='#333333', labelpad=10)
ax.set_ylabel('Memoria RAM ocupada ($M$ en GB)', fontsize=12, color='#333333', labelpad=10)
ax.set_title('Dinámica de Memoria RAM — Modelo de Ecuación Diferencial Ordinaria',
             fontsize=15, fontweight='bold', color='#1D3557', pad=15)
ax.grid(True, linestyle='--', alpha=0.5, color='#BBBBBB')
ax.tick_params(axis='both', which='major', labelsize=10, colors='#555555')
# Bordes suaves
for spine in ax.spines.values():
    spine.set_color("#000000")
    spine.set_linewidth(1.0)

ax.legend(loc='upper left', frameon=True, fancybox=True, shadow=True,
          facecolor='white', edgecolor='#DDDDDD', fontsize=9)

# 8. SLIDERS INTERACTIVOS

ax_a = plt.axes([0.18, 0.20, 0.54, 0.03])
ax_b = plt.axes([0.18, 0.13, 0.54, 0.03])
ax_M0 = plt.axes([0.18, 0.06, 0.54, 0.03])
slider_a = Slider(ax_a, 'Tasa de Entrada ($a$)  ', 0.1, 12.0, valinit=a_init,
                  valfmt=' %1.2f GB/s', color=COLOR_RAM_ESTABLE, track_color='#E0E0E0')
slider_b = Slider(ax_b, 'Tasa de Liberación ($b$) ', 0.1, 2.0, valinit=b_init,
                  valfmt=' %1.2f 1/s', color=COLOR_ASINTOTA, track_color='#E0E0E0')
slider_M0 = Slider(ax_M0, 'Memoria Inicial ($M_0$)    ', 0.0, LIMITE_FISICO_RAM * 1.5, valinit=M0_init,
                   valfmt=' %1.2f GB', color='#2A9D8F', track_color='#E0E0E0')
# Estética de los ejes de sliders
for slider_ax in [ax_a, ax_b, ax_M0]:
    slider_ax.set_facecolor('#F0F2F5')
    for spine in ['top', 'right', 'left']:
        slider_ax.spines[spine].set_visible(False)
    slider_ax.spines['bottom'].set_color('#CCCCCC')
    slider_ax.tick_params(colors='#666666', labelsize=9)

# 9. FUNCIÓN DE ACTUALIZACIÓN

def actualizar(val):
    a = slider_a.val
    b = slider_b.val
    M0 = slider_M0.val
    
    asintota_actual = a / b
    M_nueva_teorica = asintota_actual + (M0 - asintota_actual) * np.exp(-b * t)
    M_nueva_saturada = np.clip(M_nueva_teorica, 0, LIMITE_FISICO_RAM)
    
    # Actualizar líneas principales
    linea_ram.set_ydata(M_nueva_saturada)
    linea_asintota.set_ydata([asintota_actual, asintota_actual])
    
    # Actualizar color de la línea según estado
    saturado = asintota_actual > LIMITE_FISICO_RAM
    nuevo_color = COLOR_RAM_SATURADO if saturado else COLOR_RAM_ESTABLE
    linea_ram.set_color(nuevo_color)
    
    linea_asintota.set_label(f'Equilibrio Teórico ($a/b = {asintota_actual:.2f}$ GB)')
    
    # Actualizar rellenos
    global fill_ram, fill_overflow
    
    fill_ram.remove()
    fill_ram = ax.fill_between(t, 0, M_nueva_saturada, color=COLOR_FILL_RAM, alpha=0.10, zorder=1)
    
    fill_overflow.remove()
    overflow_mask = M_nueva_teorica > LIMITE_FISICO_RAM
    fill_overflow = ax.fill_between(t, LIMITE_FISICO_RAM, M_nueva_teorica, where=overflow_mask,
                                    color=COLOR_OVERFLOW, alpha=0.20, interpolate=True,
                                    label='Zona de Saturación', zorder=1)
    
    # Actualizar indicador de estado
    estado_texto = '⚠ SATURADO' if saturado else '✓ ESTABLE'
    texto_estado.set_text(estado_texto)
    texto_estado.set_color(nuevo_color)
    texto_estado.set_bbox(dict(boxstyle='round,pad=0.5', facecolor='white',
                               edgecolor=nuevo_color, lw=2.5, alpha=0.95))
    
    # Refrescar leyenda
    ax.legend(loc='upper left', frameon=True, fancybox=True, shadow=True,
              facecolor='white', edgecolor='#DDDDDD', fontsize=9)
    
    fig.canvas.draw_idle()
# Vincular eventos
slider_a.on_changed(actualizar)
slider_b.on_changed(actualizar)
slider_M0.on_changed(actualizar)
plt.show()
