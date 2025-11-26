<template>
  <div>
    <h1 class="text-3xl font-bold text-gray-800 mb-6">Registro de Ventas</h1>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- Formulario de nueva venta -->
      <div class="lg:col-span-2 card">
        <h2 class="text-xl font-bold mb-4 text-gray-800">Nueva Venta</h2>
        
        <form @submit.prevent="crearVenta">
          <!-- Cliente y Vendedor -->
          <div class="grid grid-cols-2 gap-4 mb-4">
            <div>
              <label class="block text-gray-700 text-sm font-bold mb-2">Cliente</label>
              <select v-model="venta.cliente_id" class="input-field">
                <option value="">Seleccione cliente...</option>
                <option v-for="cliente in clientes" :key="cliente.id" :value="cliente.id">
                  {{ cliente.nombres }} {{ cliente.apellidos }}
                </option>
              </select>
            </div>

            <div>
              <label class="block text-gray-700 text-sm font-bold mb-2">Vendedor *</label>
              <select v-model="venta.vendedor_id" required class="input-field">
                <option value="">Seleccione vendedor...</option>
                <option v-for="empleado in empleados" :key="empleado.id" :value="empleado.id">
                  {{ empleado.primer_nombre }} {{ empleado.apellido_paterno }}
                </option>
              </select>
            </div>
          </div>

          <!-- Agregar productos -->
          <div class="mb-4">
            <label class="block text-gray-700 text-sm font-bold mb-2">Agregar Producto</label>
            <div class="flex space-x-2">
              <select v-model="productoSeleccionado" class="input-field flex-1">
                <option value="">Seleccione producto...</option>
                <option v-for="prod in productos" :key="prod.id" :value="prod.id">
                  {{ prod.nombre }} - S/ {{ Number(prod.precio_venta_unitario).toFixed(2) }} (Stock: {{ prod.stock_actual }})
                </option>
              </select>
              <input v-model.number="cantidadProducto" type="number" min="1" placeholder="Cant" 
                     class="input-field w-24">
              <button type="button" @click="agregarProducto" class="btn-success">
                + Agregar
              </button>
            </div>
          </div>

          <!-- Lista de items de la venta -->
          <div class="mb-4">
            <h3 class="font-bold text-gray-700 mb-2">Items de la venta</h3>
            <div class="border rounded-lg overflow-hidden">
              <table class="min-w-full divide-y divide-gray-200">
                <thead class="bg-gray-50">
                  <tr>
                    <th class="px-4 py-2 text-left text-xs font-medium text-gray-500">Producto</th>
                    <th class="px-4 py-2 text-right text-xs font-medium text-gray-500">Cantidad</th>
                    <th class="px-4 py-2 text-right text-xs font-medium text-gray-500">P. Unitario</th>
                    <th class="px-4 py-2 text-right text-xs font-medium text-gray-500">Subtotal</th>
                    <th class="px-4 py-2 text-right text-xs font-medium text-gray-500">Acción</th>
                  </tr>
                </thead>
                <tbody class="bg-white divide-y divide-gray-200">
                  <tr v-for="(item, index) in venta.items" :key="index">
                    <td class="px-4 py-2 text-sm">{{ getProductoNombre(item.producto_id) }}</td>
                    <td class="px-4 py-2 text-sm text-right">{{ item.cantidad }}</td>
                    <td class="px-4 py-2 text-sm text-right">S/ {{ Number(item.precio).toFixed(2) }}</td>
                    <td class="px-4 py-2 text-sm text-right font-semibold">
                      S/ {{ (item.cantidad * item.precio).toFixed(2) }}
                    </td>
                    <td class="px-4 py-2 text-sm text-right">
                      <button type="button" @click="eliminarItem(index)" 
                              class="text-red-600 hover:text-red-800">
                        Eliminar
                      </button>
                    </td>
                  </tr>
                  <tr v-if="venta.items.length === 0">
                    <td colspan="5" class="px-4 py-4 text-center text-gray-500 text-sm">
                      No hay productos agregados
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <!-- Botones -->
          <div class="flex justify-end space-x-3">
            <button type="button" @click="limpiarVenta" class="btn-secondary">
              Limpiar
            </button>
            <button type="submit" class="btn-primary" :disabled="venta.items.length === 0">
              Registrar Venta
            </button>
          </div>
        </form>
      </div>

      <!-- Resumen de la venta -->
      <div class="lg:col-span-1">
        <div class="card sticky top-6">
          <h3 class="text-xl font-bold mb-4 text-gray-800">Resumen</h3>
          
          <div class="space-y-3">
            <div class="flex justify-between text-gray-700">
              <span>Items:</span>
              <span class="font-semibold">{{ venta.items.length }}</span>
            </div>
            
            <div class="flex justify-between text-gray-700">
              <span>Productos:</span>
              <span class="font-semibold">{{ totalProductos }}</span>
            </div>
            
            <div class="border-t pt-3 mt-3">
              <div class="flex justify-between text-lg font-bold text-gray-900">
                <span>TOTAL:</span>
                <span class="text-primary">S/ {{ totalVenta.toFixed(2) }}</span>
              </div>
            </div>

            <div v-if="clienteSeleccionadoInfo && clienteSeleccionadoInfo.es_consumidor" 
                 class="bg-green-50 border border-green-200 rounded p-3 text-sm text-green-800">
              <p class="font-semibold">🎉 Cliente consumidor final</p>
              <p>Se aplicará descuento automático</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Historial de ventas -->
    <div class="mt-8 card">
      <h2 class="text-xl font-bold mb-4 text-gray-800">Historial de Ventas</h2>
      
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="table-header">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">ID</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Fecha</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Cliente</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Vendedor</th>
              <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">Total</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Estado</th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="venta in ventas" :key="venta.id" class="table-row">
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{{ venta.id }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {{ formatDate(venta.fecha) }}
              </td>
              <td class="px-6 py-4 text-sm text-gray-900">Cliente #{{ venta.cliente_id || 'N/A' }}</td>
              <td class="px-6 py-4 text-sm text-gray-900">Vendedor #{{ venta.vendedor_id }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-right font-semibold text-primary">
                S/ {{ Number(venta.total).toFixed(2) }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm">
                <span class="px-2 py-1 rounded-full text-xs font-semibold bg-green-100 text-green-800">
                  {{ venta.estado }}
                </span>
              </td>
            </tr>
            <tr v-if="ventas.length === 0">
              <td colspan="6" class="px-6 py-4 text-center text-gray-500">No hay ventas registradas</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import api from '../services/api'

export default {
  name: 'Ventas',
  data() {
    return {
      ventas: [],
      clientes: [],
      empleados: [],
      productos: [],
      venta: {
        cliente_id: '',
        vendedor_id: '',
        items: []
      },
      productoSeleccionado: '',
      cantidadProducto: 1
    }
  },
  computed: {
    totalVenta() {
      return this.venta.items.reduce((sum, item) => sum + (item.cantidad * item.precio), 0)
    },
    totalProductos() {
      return this.venta.items.reduce((sum, item) => sum + item.cantidad, 0)
    },
    clienteSeleccionadoInfo() {
      return this.clientes.find(c => c.id === this.venta.cliente_id)
    }
  },
  mounted() {
    this.loadData()
  },
  methods: {
    async loadData() {
      try {
        const [ventasRes, clientesRes, empleadosRes, productosRes] = await Promise.all([
          api.ventas.getAll(),
          api.clientes.getAll(),
          api.empleados.getAll(),
          api.productos.getAll()
        ])
        
        this.ventas = ventasRes.data
        this.clientes = clientesRes.data
        this.empleados = empleadosRes.data
        this.productos = productosRes.data.filter(p => p.activo && p.stock_actual > 0)
      } catch (error) {
        alert('Error al cargar datos')
      }
    },
    agregarProducto() {
      if (!this.productoSeleccionado || this.cantidadProducto < 1) {
        alert('Seleccione un producto y cantidad válida')
        return
      }

      const producto = this.productos.find(p => p.id === this.productoSeleccionado)
      
      if (!producto) return

      if (this.cantidadProducto > producto.stock_actual) {
        alert(`Stock insuficiente. Disponible: ${producto.stock_actual}`)
        return
      }

      // Verificar si ya está en la lista
      const existente = this.venta.items.find(i => i.producto_id === producto.id)
      if (existente) {
        existente.cantidad += this.cantidadProducto
      } else {
        this.venta.items.push({
          producto_id: producto.id,
          cantidad: this.cantidadProducto,
          precio: Number(producto.precio_venta_unitario)
        })
      }

      this.productoSeleccionado = ''
      this.cantidadProducto = 1
    },
    eliminarItem(index) {
      this.venta.items.splice(index, 1)
    },
    getProductoNombre(id) {
      const prod = this.productos.find(p => p.id === id)
      return prod ? prod.nombre : 'Producto #' + id
    },
    async crearVenta() {
      if (!this.venta.vendedor_id) {
        alert('Seleccione un vendedor')
        return
      }

      if (this.venta.items.length === 0) {
        alert('Agregue al menos un producto')
        return
      }

      try {
        const data = {
          vendedor_id: this.venta.vendedor_id,
          cliente_id: this.venta.cliente_id || null,
          items: this.venta.items
        }

        await api.ventas.create(data)
        alert('✅ Venta registrada exitosamente')
        this.limpiarVenta()
        this.loadData()
      } catch (error) {
        alert('Error: ' + (error.response?.data?.error || error.message))
      }
    },
    limpiarVenta() {
      this.venta = {
        cliente_id: '',
        vendedor_id: '',
        items: []
      }
      this.productoSeleccionado = ''
      this.cantidadProducto = 1
    },
    formatDate(date) {
      if (!date) return '-'
      return new Date(date).toLocaleDateString('es-PE', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    }
  }
}
</script>