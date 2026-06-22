# Atlas Nacional de Datos Meteorológicos y Vulnerabilidad Energética

**Autor:** Johan Antonio Vásquez Aquino  
---

## Objetivo

Obtener una webapp capaz de:
- Leer archivos de datos para extracción de información
- Aplicar transformaciones de unidades, zonas horarias y desacumulación
- Armar por separado distintas partes de la web app para evitar confusión de errores
- Mostrar los datos en un mapa interactivo a distintos niveles (municipal, estatal)
- Ser escalable y modular para incorporar nuevas variables, regiones y años

---

## Plan de Desarrollo — 5 Fases

### Fase 1 — Extracción y procesamiento de datos

Base de todo el proyecto. Se aplican transformaciones clave antes de que los datos toquen la app.

- [✅] Cargar archivos ERA5 .nc con Xarray y verificar que tipo de archivos se consideran para la ingesta
- [ ] Establecer unidades de medida y aspectos a unificar de los datos
- [ ] Función de conversión a UTC para establecer una sola zona horaria 
- [ ] Conversión de unidades a los correspondientes
- [ ] Verificación de formato de los datos (como el ssrd)
- [ ] Decidir que proceso aplicar para zonas con falta de datos
- [ ] Script independiente para ingesta de datos (que la app lo consuma sin cambios)
- [ ] Exportar resultados procesados a formato intermedio (CSV / Parquet)
- [ ] Extracción de shapefiles INEGI

---

### Fase 2 — Mapa estático

Antes de agregar reactividad, verificar que el mapa funciona y los datos tienen sentido físico.

- [ ] Cargar shapefile municipal de Oaxaca con (geopandas)
- [ ] Verificar y explorar la graficación de shapefiles
- [ ] Hardcodear datos de prueba (temperatura / radiación) para una fecha fija
- [ ] Renderizar mapa estático con plotly para verificación de gráfica
- [ ] Verificar que los valores se asignan correctamente y  tienen sentido físico
- [ ] Identificar municipios con datos faltantes y documentarlos con el proceso designado para estos
- [ ] Ajustar escala de color y proyección del mapa

---

### Fase 3 — Controles sin lógica completa

Construir el dashboard con controles funcionales pero salida simplificada.

- [ ] Crear layout base para la selección de información
- [ ] Definir que datos se usarán de prueba
- [ ] Agregar los selectores de parámetros
- [ ] Conectar callbacks, recibir inputs y mostrar en pantalla los valores seleccionados
- [ ] Verificar que los callbacks reciben los datos correctamente antes de conectar el mapa

---

### Fase 4 — Reactividad completa

Unir extracción de datos y mapa para visualización dinámica real.

- [ ] Conectar callbacks al pipeline de extracción
- [ ] Actualizar mapa según variable y fecha seleccionada
- [ ] Manejo de datos con valores faltantes
- [ ] Agregar información para hover, titulos, variables y colores dinámicos
- [ ] (opción)Implementar un loader para indicar carga mientras se procesan datos
- [ ] Pruebas de coherencia física: validar que los valores tienen sentido geográfico

---

### Fase 5 — Modularidad completa

Refactorización final para que el proyecto sea mantenible y escalable.

- [ ] Separar pipeline de ingesta de datos en módulo independiente 
- [ ] Crear funciones reutilizables para cada tipo de visualización segun sea conveniente
- [ ] Separar layout y callbacks de Dash en módulos 
- [ ] Documentar cada función
- [ ] Asegurarse de que agregar una nueva variable solo requiere modificar el script de ingesta
- [ ] Asegurarse de que agregar una nueva región (estado / república) no requiere cambios en la app

---

### Implementación

- [ ] Integrar las 5 fases en la app final de Dash
- [ ] Pruebas de usuario con datos reales de Oaxaca 2023
- [ ] Deploy de versión beta


---

## Notas técnicas

- Considerar años donde existía cambio de horario
- En todo momento documentar el proceso para reproducibilidad