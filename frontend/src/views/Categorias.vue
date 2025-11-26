<template>
  <div>
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-3xl font-bold text-gray-800">Gestión de Categorías</h1>
      <button @click="openModal()" class="btn-primary">
        + Nueva Categoría
      </button>
    </div>

    <!-- Tabla de categorías -->
    <div class="card overflow-hidden">
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="table-header">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">ID</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Nombre</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Descripción</th>
              <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Acciones</th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="categoria in categorias" :key="categoria.id" class="table-row">
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{{ categoria.id }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{{ categoria.nombre }}</td>
              <td class="px-6 py-4 text-sm text-gray-500">{{ categoria.descripcion || '-' }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium space-x-2">
                <button @click="openModal(categoria)" class="text-blue-600 hover:text-blue-900">Editar</button>
                <button @click="deleteCategoria(categoria.id)" class="text-red-600 hover:text-red-900">Eliminar</button>
              </td>
            </tr>
            <tr v-if="categorias.length === 0">
              <td colspan="4" class="px-6 py-4 text-center text-gray-500">No hay categorías registradas</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Modal -->
    <div v-if="showModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg p-8 max-w-md w-full mx-4">
        <h2 class="text-2xl font-bold mb-6 text-gray-800">
          {{ editMode ? 'Editar Categoría' : 'Nueva Categoría' }}
        </h2>
        
        <form @submit.prevent="saveCategoria">
          <div class="mb-4">
            <label class="block text-gray-700 text-sm font-bold mb-2">Nombre *</label>
            <input v-model="form.nombre" type="text" required class="input-field" placeholder="Ej: Libros">
          </div>
          
          <div class="mb-6">
            <label class="block text-gray-700 text-sm font-bold mb-2">Descripción</label>
            <textarea v-model="form.descripcion" rows="3" class="input-field" placeholder="Descripción opcional"></textarea>
          </div>
          
          <div class="flex justify-end space-x-3">
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
  name: 'Categorias',
  data() {
    return {
      categorias: [],
      showModal: false,
      editMode: false,
      form: {
        id: null,
        nombre: '',
        descripcion: ''
      }
    }
  },
  mounted() {
    this.loadCategorias()
  },
  methods: {
    async loadCategorias() {
      try {
        const response = await api.categorias.getAll()
        this.categorias = response.data
      } catch (error) {
        alert('Error al cargar categorías: ' + error.message)
      }
    },
    openModal(categoria = null) {
      if (categoria) {
        this.editMode = true
        this.form = { ...categoria }
      } else {
        this.editMode = false
        this.form = { id: null, nombre: '', descripcion: '' }
      }
      this.showModal = true
    },
    closeModal() {
      this.showModal = false
      this.form = { id: null, nombre: '', descripcion: '' }
    },
    async saveCategoria() {
      try {
        if (this.editMode) {
          await api.categorias.update(this.form.id, this.form)
          alert('Categoría actualizada exitosamente')
        } else {
          await api.categorias.create(this.form)
          alert('Categoría creada exitosamente')
        }
        this.closeModal()
        this.loadCategorias()
      } catch (error) {
        alert('Error al guardar: ' + (error.response?.data?.error || error.message))
      }
    },
    async deleteCategoria(id) {
      if (!confirm('¿Está seguro de eliminar esta categoría?')) return
      
      try {
        await api.categorias.delete(id)
        alert('Categoría eliminada exitosamente')
        this.loadCategorias()
      } catch (error) {
        alert('Error al eliminar: ' + (error.response?.data?.error || error.message))
      }
    }
  }
}
</script>