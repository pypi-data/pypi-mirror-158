# Kafkademia

Este es un paquete sencillo que busca resaltar la capacidad
que se tiene al hacer uso de uno de los clientes para Kafka.

Se pretende que al leer el código, quede en evidencia la 
posibilidad de crear tanto productores o consumidores Kafka.

# Como utilizar Kafkademia?
Este paquete provee de la posibilidad de crear 2 cosas mediante la linea de comandos.

1. Productor: el paquete tiene la posibilidad de crear 
productores que generan mensajes con contenido pseudoaleatorios.
El contenido de estos mensajes dependerán de lo que se le indique.

2. Consumidor: el paquete puede crear un consumidor que escuche un tópico

Los posibles parametros serán los siguientes:

- Servidores bootstrap (bootstrap_servers <lista separada con , de servidores>) 
- Topico ("--topico <topico>")
- Productor ("--productor"): este indica que se estará creando un productor. 
Al indicar la creación de un productor es obligatorio indicar
cual de los ejemplos disponibles en el paquete se quiere producir,
esto se logra mediante:
    - "--atm": productor que genera mensajes simulados de movimientos de ATMs.
    - "--ventas": productor que genera mensajes simulados de ventas.
- Consumidor ("--consumidor"): este producirá un consumidor para el tópico indicado.

# Importante
* Solamente se puede crear un productor o un consumidor por vez. Si se introducen ambos flags en un solo comando se finalizará con un error.
* Al crear un productor, solamente se podrá hacer referencia a uno de los ejemplos, si se introducen ambos flags, el comando finalizará con un error.