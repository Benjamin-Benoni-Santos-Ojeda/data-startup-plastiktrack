# E0: Propuesta de Proyecto - Startup "PlastikTrack"

**Proyecto Integrador:** DATA STARTUP  
**Entregas:** E0 (Definición y Factibilidad Estratégica) y E1 (Ingeniería de Datos y Analítica Base)  
**Roles:** Cloud Lead (Benjamin Benoni Santos Ojeda - 25460724) & Data Lead (Juan Carrillo Orozco - 25460331)  
**Fecha:** Octubre / Noviembre 2026  
**Empresa / Caso de Estudio:** Distribuidora Mayorista "PlastikTrack" (Distribuidor Javier Morales)

---

## 1. Resumen Ejecutivo y Misión de la Startup

**PlastikTrack** es una startup SaaS B2B enfocada en modernizar y optimizar la cadena de suministro de distribuidoras mayoristas de bolsas, películas y desechables plásticos que abastecen a la densa red de tiendas de abarrotes, recauderías, pollerías y comercios minoristas en México.

En el comercio mayorista tradicional, más del 85% de las decisiones de reabastecimiento se toman de manera puramente empírica ("al tanteo" o "a ojo de buen cubero"). Esto genera dos fallas operativas críticas que drenan el margen del negocio:
1. **Quiebres de stock recurrentes** en productos de alta rotación (bolsas tipo camiseta y rollos) durante los días pico de reparto y ciclos de quincena, forzando compras de emergencia a precios inflados (~15% más caras) o pérdida irreversible de ventas ante competidores.
2. **Sobreinventario y capital inmovilizado** en líneas voluminosas de baja rotación (contenedores térmicos de unicel, vasos y charolas desechables), saturando el espacio de bodega física y castigando el flujo de caja.

PlastikTrack resuelve esta fricción convirtiendo el historial transaccional de venta en un motor de telemetría analítica y pronósticos de demanda a 7 y 14 días, permitiendo a los distribuidores aprovisionarse con precisión quirúrgica a costo computacional cero gracias a una arquitectura Cloud-Native en Oracle Cloud Infrastructure (OCI).

---

## 2. Lean Canvas de PlastikTrack (9 Bloques)

| Bloque | Componente | Descripción Estratégica en PlastikTrack |
| :--- | :--- | :--- |
| **1** | **Problema** | • Quiebres de stock en bolsas de alta rotación durante quincenas y días de reparto.<br>• Capital inmovilizado y espacio de bodega ocupado por productos desechables de baja rotación.<br>• Falta de visibilidad analítica: compras semanales basadas en intuición.<br>• Pérdida de clientes hacia otros distribuidores por falta de abasto oportuno. |
| **2** | **Segmento de Clientes** | • **Early Adopter:** Distribuidor Javier Morales (propietario de distribuidora de bolsas y desechables, 1 bodega central, 2 rutas de reparto abasteciendo a más de 140 tiendas de abarrotes y negocios de comida).<br>• Distribuidores mayoristas y comercializadoras de plásticos, empaques y desechables en centrales de abasto y zonas suburbanas. |
| **3** | **Propuesta de Valor Única** | *"Elimina los quiebres de inventario en quincena y libera hasta un 30% de tu capital de trabajo con pronósticos inteligentes de demanda diseñados específicamente para distribuidores de plásticos."* |
| **4** | **Solución** | • Tablero de control interactivo en tiempo real con KPIs clave y análisis de estacionalidad.<br>• Motor de recomendación de órdenes de compra con horizonte predictivo a 7 y 14 días.<br>• Descomposición de periodicidad (días pico de reparto: lunes, miércoles, viernes y efectos de quincena).<br>• Alertas automatizadas de reposición por SKU enviadas por WhatsApp / Web. |
| **5** | **Canales** | • Venta consultiva directa y demostración in-situ en bodegas de distribución.<br>• Alianzas comerciales y recomendación referenciada ("boca a boca") en Centrales de Abasto.<br>• Portal web autogestionable y notificaciones vía canal de mensajería (WhatsApp Business API). |
| **6** | **Estructura de Costos** | • **Costo Operativo de Infraestructura: $0.00 USD / mes** gracias a OCI Always Free Tier.<br>• Cómputo: 4 OCPU Ampere A1 ARM + 24 GB RAM en Oracle Cloud.<br>• Almacenamiento: 200 GB Block Storage + 10 GB Object Storage (Free Tier).<br>• Dominio y SSL: Cloudflare Zero Trust / Let's Encrypt ($0 USD adicionales).<br>• Mantenimiento y desarrollo: Salario de equipo fundador / horas de ingeniería. |
| **7** | **Fuentes de Ingresos** | • Modelo de Suscripción SaaS B2B recurrente: **$450.00 MXN / mes** por distribuidor (adaptado a la disposición de pago validada en entrevista de $300 - $600 MXN).<br>• Opción anual prepagada: **$4,500.00 MXN / año** (2 meses de descuento).<br>• Servicios adicionales de integración y onboarding con sistemas de tickets preexistentes ($1,200 MXN pago único opcional). |
| **8** | **Métricas Clave** | • **WAPE / MAPE:** Precisión del pronóstico a 7 y 14 días (> 88%).<br>• **Stockout Rate:** Reducción de incidencias por desabasto en días pico (reducción meta: > 70%).<br>• **Días de Inventario (DSI):** Disminución de permanencia de desechables en bodega de 45 a 20 días.<br>• **MRR / ARR & Churn:** Ingreso mensual recurrente y retención de suscripciones (> 95%). |
| **9** | **Ventaja Injusta** | • Modelos analíticos calibrados para la microeconomía y estacionalidad del comercio informal y minorista mexicano (quincenas salariales, días de tianguis y pedidos de reparto).<br>• Estructura de costo cero de nube (FinOps OCI) que permite ofrecer un precio mensual imbatible frente a ERPs corporativos costosos e inaccesibles para el distribuidor medio. |

---

## 3. Registro de la Entrevista a Profundidad (15 Minutos)

**Entrevistado:** Javier Morales (48 años)  
**Rol:** Dueño y operador de "Distribuidora de Plásticos y Desechables San Juan"  
**Ubicación:** Nezahualcóyotl / Iztapalapa, Zona Metropolitana del Valle de México  
**Entrevistadores:** Cloud Lead & Data Lead  
**Duración:** 15 minutos  

### Transcripción de Preguntas y Respuestas Clave:

* **P1: Javier, ¿cómo decides actualmente qué productos y cuántos bultos pedir cada semana a los fabricantes o importadores de plástico?**
  > **Javier:** *"La verdad todo lo hago a ojo de buen cubero y de memoria. Los lunes en la mañana me doy una vuelta por los pasillos de la bodega, veo qué tarimas se ven bajas y anoto en una libreta: 'pedir 50 bultos de camiseta negra, 30 de rollo poliseda'. El problema es que a veces creo que tengo suficiente y cuando caen los pedidos fuertes de media semana me doy cuenta de que ya no tengo bolsa de kilo o del número 2, y tengo que andar comprándole de emergencia a otros distribuidores que me la venden 15% más cara para no quedarle mal a los tenderos."*

* **P2: ¿Has detectado patrones específicos en qué días de la semana o fechas del mes se dispara la venta?**
  > **Javier:** *"¡Claro que sí! Los días de reparto fuerte son los lunes, miércoles y viernes. Los lunes los abarroteros surten lo que se les acabó el fin de semana, y los viernes se preparan para el sábado y domingo. Pero lo que de verdad manda es la quincena. Los días 14, 15 y 16, y los fines de mes (30 y 31), las tiendas venden mucho más porque la gente cobra y compra su despensa, así que a nosotros se nos dispara el pedido de bolsa de rollo y camiseta como un 25% a 30% arriba de un día normal."*

* **P3: ¿Cuáles de tus productos te causan más dolores de cabeza con el inventario o dinero estancado?**
  > **Javier:** *"Los desechables: las charolas de unicel, los vasos del número 8 y 10, y los contenedores térmicos para comida. Esos productos ocupan muchísimo volumen físico en la bodega, llenan las tarimas altas y se mueven muy lento. Compro cajas completas porque el fabricante no me vende por pieza suelta, y a veces pasan tres o cuatro semanas y apenas he vendido un 30% de la caja. Ahí tengo miles de pesos parados que me harían falta para comprar más bolsa negra o emplaye, que vuelan."*

* **P4: ¿Cuentas con alguna computadora o sistema de punto de venta donde registres lo que sale del negocio?**
  > **Javier:** *"Tengo una computadora básica en el mostrador con un software de punto de venta sencillo donde cobro e imprimo notas de remisión para los choferes repartidores. Todo se registra con fecha, producto y cantidad porque necesito cuadrar caja todos los días, pero ese programa no me dice qué pedir mañana ni analiza nada; solo sirve de calculadora y para que los empleados no se confundan con los precios."*

* **P5: Si contaras con una plataforma digital que leyera tus notas de venta y te dijera con exactitud cuántos bultos pedir cada semana para nunca quedarte sin bolsa en quincena ni estancar dinero en desechables, ¿cuánto estarías dispuesto a pagar al mes?**
  > **Javier:** *"Si de verdad me evita quedarme sin bolsa un viernes de quincena, me ahorraría miles de pesos; nada más en un quiebre de stock pierdo fácil más de 2,000 pesos de ganancia neta. Yo pagaría con gusto entre $300 y $600 pesos al mes sin problema, siempre y cuando no sea un software enredado de los que usan las grandes empresas, sino algo que pueda ver directo en mi teléfono o en la pantalla de la oficina sin complicaciones."*

---

## 4. Cadena de Transformación: Negocio -> Analítica -> Variable a Predecir

Para garantizar impacto económico tangible, el pipeline analítico se estructura bajo la siguiente jerarquía de valor:

```mermaid
flowchart LR
    A["Pregunta de Negocio:<br>¿Cómo evitar quiebres en quincena y optimizar el capital de trabajo?"] --> B["Pregunta Analítica:<br>¿Cuáles son los ciclos periódicos, estacionalidad y tendencia de ventas por SKU?"]
    B --> C["Variable a Predecir:<br><b>unidades</b> vendidas diarias por producto a horizontes de 7 y 14 días"]
```

1. **Pregunta de Negocio:**
   > *"¿Cómo podemos optimizar los pedidos semanales de la distribuidora para maximizar el nivel de servicio en días pico de reparto y ciclos de quincena, minimizando a la vez el capital inmovilizado en productos de baja rotación?"*
2. **Pregunta Analítica:**
   > *"¿Qué componentes de periodicidad semanal (lunes/miércoles/viernes), patrones bimensuales de quincena (efecto 15 y 30/31) y tendencias de consumo caracterizan la demanda histórica de cada uno de los 12 productos del catálogo?"*
3. **Variable Objetivo a Predecir:**
   > `unidades` (variable cuantitativa entera continua por SKU y fecha, proyectada a horizontes operativos de 7 y 14 días para sincronizarse con los tiempos de reposición de los fabricantes).

---

## 5. Inventario de Datos de Ventas

El dataset histórico transaccional que soporta la fase analítica y de modelado cuenta con las siguientes especificaciones técnicas de volumen y esquema:

* **Total de Observaciones Crudas:** **16,498 registros** transaccionales en el archivo fuente `ventas_distribuidora.csv`.
* **Total de Observaciones Limpias:** **16,428 registros** curados y deduplicados por clave de negocio (`fecha` + `producto`).
* **Cobertura Temporal:** **1,369 días continuos** (del **1 de enero de 2023 al 30 de septiembre de 2026** sin interrupciones, equivalente a 3 años y 9 meses de historial operativo).
* **Profundidad de Catálogo:** **12 productos oficiales** distribuidos equilibradamente en 3 familias funcionales (Bolsas Rollo, Bolsas Camiseta, y Desechables y Empaque).
* **Volumen Físico y Monetario Acumulado:** **411,524 unidades** comercializadas representando **$18,672,916.50 MXN** en facturación total acumulada.
* **Estructura Tabular del Registro:**

| Columna | Tipo de Dato | Descripción y Regla de Negocio |
| :--- | :--- | :--- |
| `fecha` | `date` (YYYY-MM-DD) | Marca temporal del día operativo (1,369 fechas únicas continuas). |
| `producto` | `string` (categoría) | Nombre homologado del SKU de acuerdo al catálogo oficial de Javier. |
| `unidades` | `integer` | Volumen físico despachado en el día (bultos, paquetes o millares según SKU). |
| `precio_unitario` | `float` (MXN) | Precio unitario mayorista pactado con la red minorista. |
| `total` | `float` (MXN) | Importe transaccionado del día calculado como: `unidades * precio_unitario`. |

### Catálogo de Productos y Estadísticas Históricas de Demanda:
1. **Bolsa Negra Camiseta:** Precio $38.50 MXN | 57,251 u totales | $2,204,163.50 MXN *(Producto Estrella)*
2. **Bolsa Rollo Baja Densidad:** Precio $29.50 MXN | 49,701 u totales | $1,466,179.50 MXN
3. **Bolsa Camiseta Poliseda:** Precio $41.00 MXN | 48,483 u totales | $1,987,803.00 MXN
4. **Bolsa Basura Todos Tamanios:** Precio $41.00 MXN | 45,146 u totales | $1,850,986.00 MXN
5. **Bolsa Rollo Alta Densidad:** Precio $36.00 MXN | 42,698 u totales | $1,537,128.00 MXN
6. **Bolsa Rollo Poliseda:** Precio $33.00 MXN | 39,325 u totales | $1,297,725.00 MXN
7. **Bolsa Camiseta Color:** Precio $44.25 MXN | 35,548 u totales | $1,572,999.00 MXN
8. **Bolsa Camiseta Plata:** Precio $47.00 MXN | 31,271 u totales | $1,469,737.00 MXN
9. **Pelicula Plastica Emplaye:** Precio $95.50 MXN | 20,310 u totales | $1,939,605.00 MXN
10. **Vasos Desechables:** Precio $57.00 MXN | 16,609 u totales | $946,713.00 MXN *(Baja rotación)*
11. **Charolas Desechables:** Precio $67.50 MXN | 13,390 u totales | $903,825.00 MXN *(Baja rotación)*
12. **Contenedor Termico Unicel:** Precio $75.00 MXN | 11,792 u totales | $884,400.00 MXN *(Baja rotación)*

---

## 6. Sección de Arranque Técnico y Control Financiero (FinOps)

### Arquitectura OCI Always Free Tier
PlastikTrack opera bajo un principio estricto de eficiencia en nube: el costo de infraestructura mensual es de **$0.00 USD**. La plataforma se despliega aprovechando las capacidades del programa *Always Free* de Oracle Cloud Infrastructure (OCI):
* **Compute VM:** 1 instancia Ampere A1 (ARM64) con 4 OCPUs y 24 GB de memoria RAM, suficiente para orquestar microservicios de ingesta, API en FastAPI, almacenamiento PostgreSQL y dashboard en Streamlit.
* **Storage:** 200 GB en Block Volumes NVMe Always Free particionados para la base de datos y logs.
* **Egress Data Transfer:** 10 TB mensuales gratuitos.

### Control Presupuestal y Alerta Activa (FinOps)
Para salvaguardar la viabilidad financiera de la startup y garantizar costo operativo cero ($0.00 USD), se implementó una política de presupuesto preventiva de **$1.00 USD mensual en estado 'Active'** con alcance a la Tenancy completa en Oracle Cloud Infrastructure (OCI). Dicha política está estrictamente monitoreada por una regla de alerta detonada al **100% del gasto real (Actual Spend)** para impedir cualquier cobro fuera del tier Always Free.

* **Monto Límite del Presupuesto:** **$1.00 USD / mes** (Alcance: Tenancy completa / Root Compartment).
* **Estado de la Política:** **Active** (Verificación continua cada 4 horas vía OCI Billing Service).
* **Métrica de Activación (Trigger):** **Actual Spend** (Gasto real acumulado en el período mensual).
* **Umbral de Alerta:** **100% ($1.00 USD)** con disparo automático inmediato.
* **Canal y Destinatario:** Notificación prioritaria vía correo electrónico institucional ante cualquier consumo detectado fuera del tier Always Free.

A continuación se documenta la evidencia fotográfica de la configuración activa en la consola de OCI:

#### Detalle del Presupuesto en Tenancy
![Detalle del Presupuesto OCI](img/alerta_presupuesto_detalle.png)

#### Regla de Alerta al 100% de Gasto Real
![Regla de Alerta de Presupuesto 100%](img/alerta_presupuesto_regla.png)

*Figura 1: Presupuesto mensual preventivo de $1.00 USD en estado activo con alcance de Tenancy completa en OCI.*  
*Figura 2: Regla de notificación inmediata al correo institucional ante el 100% de gasto real detectado fuera del tier Always Free.*
