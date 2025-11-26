<template>
  <div>
    <h1 class="text-4xl font-bold text-gray-800 mb-8">Bienvenido al Sistema Pandora</h1>
    
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      <!-- Card Categorías -->
      <router-link to="/categorias" class="card hover:shadow-xl transition transform hover:-translate-y-1">
        <div class="flex items-center space-x-4">
          <div class="bg-blue-100 p-4 rounded-full">
            <svg class="w-8 h-8 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z"></path>
            </svg>
          </div>
          <div>
            <h3 class="text-xl font-semibold text-gray-700">Categorías</h3>
            <p class="text-gray-500 text-sm">Gestionar categorías</p>
          </div>
        </div>
      </router-link>

      <!-- Card Productos -->
      <router-link to="/productos" class="card hover:shadow-xl transition transform hover:-translate-y-1">
        <div class="flex items-center space-x-4">
          <div class="bg-green-100 p-4 rounded-full">
            <svg class="w-8 h-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"></path>
            </svg>
          </div>
          <div>
            <h3 class="text-xl font-semibold text-gray-700">Productos</h3>
            <p class="text-gray-500 text-sm">Gestionar productos</p>
          </div>
        </div>
      </router-link>

      <!-- Card Clientes -->
      <router-link to="/clientes" class="card hover:shadow-xl transition transform hover:-translate-y-1">
        <div class="flex items-center space-x-4">
          <div class="bg-purple-100 p-4 rounded-full">
            <svg class="w-8 h-8 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"></path>
            </svg>
          </div>
          <div>
            <h3 class="text-xl font-semibold text-gray-700">Clientes</h3>
            <p class="text-gray-500 text-sm">Gestionar clientes</p>
          </div>
        </div>
      </router-link>

      <!-- Card Ventas -->
      <router-link to="/ventas" class="card hover:shadow-xl transition transform hover:-translate-y-1">
        <div class="flex items-center space-x-4">
          <div class="bg-yellow-100 p-4 rounded-full">
            <svg class="w-8 h-8 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z"></path>
            </svg>
          </div>
          <div>
            <h3 class="text-xl font-semibold text-gray-700">Ventas</h3>
            <p class="text-gray-500 text-sm">Registrar ventas</p>
          </div>
        </div>
      </router-link>
    </div>

    <!-- Información adicional -->
    <div class="mt-12 card">
      <h2 class="text-2xl font-bold text-gray-800 mb-4">Sistema de Gestión</h2>
      <p class="text-gray-600 leading-relaxed">
        Bienvenido al sistema de gestión de la Librería Pandora. Desde aquí puedes administrar 
        categorías, productos, clientes y realizar ventas de manera eficiente.
      </p>
      <div class="mt-6 grid grid-cols-1 md:grid-cols-3 gap-4">
        <div class="bg-blue-50 p-4 rounded-lg">
          <h3 class="font-semibold text-blue-900 mb-2">✨ Fácil de usar</h3>
          <p class="text-sm text-blue-700">Interfaz intuitiva y moderna</p>
        </div>
        <div class="bg-green-50 p-4 rounded-lg">
          <h3 class="font-semibold text-green-900 mb-2">⚡ Rápido</h3>
          <p class="text-sm text-green-700">Respuesta instantánea</p>
        </div>
        <div class="bg-purple-50 p-4 rounded-lg">
          <h3 class="font-semibold text-purple-900 mb-2">🔒 Seguro</h3>
          <p class="text-sm text-purple-700">Datos protegidos</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Home'
}
</script>