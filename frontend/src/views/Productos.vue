<template>
  <div>
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-3xl font-bold text-gray-800">Gestión de Productos</h1>
      <button @click="openModal()" class="btn-primary">
        + Nuevo Producto
      </button>
    </div>

    <!-- Tabla de productos -->
    <div class="card overflow-hidden">
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="table-header">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">ID</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Nombre</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Categoría</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Precio</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Stock</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Estado</th>
              <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">Acciones</th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="producto in productos" :key="producto.id" class="table-row">
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{{ producto.id }}</td>
              <td class="px-6 py-4 text-sm font-medium text-gray-900">{{ producto.nombre }}</td>
              <td class="px-6 py-4 text-sm text-gray-500">{{ getCategoriaName(producto.categoria_id) }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">S/ {{ Number(producto.precio_venta_unitario).toFixed(2) }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm">
                <span :class="producto.stock_actual <= 10 ? 'text-red-600 font-bold' : 'text-gray-900'">
                  {{ producto.stock_actual }}
                </span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm">
                <span :class="producto.activo ? 'text-green-600' : 'text-red-600'" class="font-semibold">
                  {{ producto.activo ? 'Activo' : 'Inactivo' }}
                </span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium space-x-2">
                <button @click="openModal(producto)" class="text-blue-600 hover:text-blue-900">Editar</button>
                <button @click="deleteProducto(producto.id)" class="text-red-600 hover:text-red-900">Eliminar</button>
              </td>
            </tr>
            <tr v-if="productos.length === 0">
              <td colspan="7" class="px-6 py-4 text-center text-gray-500">No hay productos registrados</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Modal -->
    <div v-if="showModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 overflow-y-auto">
      <div class="bg-white rounded-lg p-8 max-w-2xl w-full mx-4 my-8">
        <h2 class="text-2xl font-bold mb-6 text-gray-800">
          {{ editMode ? 'Editar Producto' : 'Nuevo Producto' }}
        </h2>
        
        <form @submit.prevent="saveProducto" class="grid grid-cols-2 gap-4">
          <div class="col-span-2">
            <label class="block text-gray-700 text-sm font-bold mb-2">Nombre *</label>
            <input v-model="form.nombre" type="text" required class="input-field">
          </div>

          <div>
            <label class="block text-gray-700 text-sm font-bold mb-2">Categoría *</label>
            <select v-model="form.categoria_id" required class="input-field">
              <option value="">Seleccione...</option>
              <option v-for="cat in categorias" :key="cat.id" :value="cat.id">{{ cat.nombre }}</option>
            </select>
          </div>

          <div>
            <label class="block text-gray-700 text-sm font-bold mb-2">Marca</label>
            <input v-model="form.marca" type="text" class="input-field">
          </div>

          <div>
            <label class="block text-gray-700 text-sm font-bold mb-2">Precio Venta *</label>
            <input v-model.number="form.precio_venta_unitario" type="number" step="0.01" required class="input-field">
          </div>

          <div>
            <label class="block text-gray-700 text-sm font-bold mb-2">Precio Costo *</label>
            <input v-model.number="form.precio_costo_unitario" type="number" step="0.01" required class="input-field">
          </div>

          <div>
            <label class="block text-gray-700 text-sm font-bold mb-2">Stock Actual</label>
            <input v-model.number="form.stock_actual" type="number" class="input-field">
          </div>

          <div>
            <label class="block text-gray-700 text-sm font-bold mb-2">Estado</label>
            <select v-model="form.activo" class="input-field">
              <option :value="true">Activo</option>
              <option :value="false">Inactivo</option>
            </select>
          </div>

          <div class="col-span-2">
            <label class="block text-gray-700 text-sm font-bold mb-2">Descripción</label>
            <textarea v-model="form.descripcion" rows="3" class="input-field"></textarea>
          </div>
          
          <div class="col-span-2 flex justify-end space-x-3 mt-4">
            <button type="button" @click="closeModal()" class="btn-secondary">Cancelar</button>
            <button type="submit" class="btn-primary">{{ editMode ? 'Actualizar' : 'Crear' }}</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import api from '../services/api'

export default {
  name: 'Productos',
  data() {
    return {
      productos: [],
      categorias: [],
      showModal: false,
      editMode: false,
      form: {
        id: null,
        nombre: '',
        categoria_id: '',
        marca: '',
        precio_venta_unitario: 0,
        precio_costo_unitario: 0,
        stock_actual: 0,
        activo: true,
        descripcion: ''
      }
    }
  },
  mounted() {
    this.loadProductos()
    this.loadCategorias()
  },
  methods: {
    async loadProductos() {
      try {
        const response = await api.productos.getAll()
        this.productos = response.data
      } catch (error) {
        alert('Error al cargar productos')
      }
    },
    async loadCategorias() {
      try {
        const response = await api.categorias.getAll()
        this.categorias = response.data
      } catch (error) {
        console.error('Error al cargar categorías')
      }
    },
    getCategoriaName(id) {
      const cat = this.categorias.find(c => c.id === id)
      return cat ? cat.nombre : '-'
    },
    openModal(producto = null) {
      if (producto) {
        this.editMode = true
        this.form = { ...producto }
      } else {
        this.editMode = false
        this.form = {
          id: null,
          nombre: '',
          categoria_id: '',
          marca: '',
          precio_venta_unitario: 0,
          precio_costo_unitario: 0,
          stock_actual: 0,
          activo: true,
          descripcion: ''
        }
      }
      this.showModal = true
    },
    closeModal() {
      this.showModal = false
    },
    async saveProducto() {
      try {
        if (this.editMode) {
          await api.productos.update(this.form.id, this.form)
          alert('Producto actualizado exitosamente')
        } else {
          await api.productos.create(this.form)
          alert('Producto creado exitosamente')
        }
        this.closeModal()
        this.loadProductos()
      } catch (error) {
        alert('Error: ' + (error.response?.data?.error || error.message))
      }
    },
    async deleteProducto(id) {
      if (!confirm('¿Eliminar este producto?')) return
      try {
        await api.productos.delete(id)
        alert('Producto eliminado')
        this.loadProductos()
      } catch (error) {
        alert('Error: ' + (error.response?.data?.error || error.message))
      }
    }
  }
}
</script>